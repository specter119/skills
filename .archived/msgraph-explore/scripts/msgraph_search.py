# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpxyz",
#     "msal",
#     "orjson",
#     "python-dotenv",
# ]
# ///
"""
Search SharePoint and OneDrive content via Microsoft Graph Search API.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from typing import Any

from msgraph_auth import (
    CACHE_ROOT,
    DEFAULT_ENV_PATH,
    SEARCH_SCOPES,
    AuthError,
    GraphApiError,
    GraphClient,
)


@dataclass
class SearchHit:
    """Normalized search result with raw identifiers for chaining."""

    rank: int
    title: str
    summary: str
    web_url: str
    entity_type: str
    hit_id: str
    last_modified: str = ""
    site_id: str = ""
    drive_id: str = ""
    item_id: str = ""
    list_id: str = ""
    list_item_id: str = ""
    resource: dict[str, Any] = field(default_factory=dict)


class SearchClient:
    def __init__(self, env_path: str | None = None):
        self.graph = GraphClient(env_path, SEARCH_SCOPES)

    def search(
        self,
        query: str,
        *,
        entity_types: list[str] | None = None,
        site_path: str | None = None,
        max_results: int = 25,
    ) -> list[SearchHit]:
        """Search content via POST /search/query with optional KQL site scoping."""
        if entity_types is None:
            entity_types = ["driveItem", "listItem"]

        query_string = query
        if site_path:
            query_string = f"{query} path:\"{site_path}\""

        all_hits: list[SearchHit] = []
        offset = 0
        page_size = min(max_results, 25)

        while len(all_hits) < max_results:
            request_body: dict[str, Any] = {
                "requests": [
                    {
                        "entityTypes": entity_types,
                        "query": {"queryString": query_string},
                        "from": offset,
                        "size": page_size,
                    }
                ]
            }

            response = self.graph.post_json(
                "/search/query", request_body, timeout=60
            )

            page_hits = self._parse_response(response)
            if not page_hits:
                break

            all_hits.extend(page_hits)

            more_available = False
            for container in response.get("value", []):
                for hits_container in container.get("hitsContainers", []):
                    if hits_container.get("moreResultsAvailable", False):
                        more_available = True
            if not more_available:
                break

            offset += page_size

        return all_hits[:max_results]

    def _parse_response(self, response: dict[str, Any]) -> list[SearchHit]:
        hits: list[SearchHit] = []
        for result in response.get("value", []):
            for container in result.get("hitsContainers", []):
                for hit in container.get("hits", []):
                    hits.append(self._normalize_hit(hit))
        return hits

    def _normalize_hit(self, hit: dict[str, Any]) -> SearchHit:
        resource = hit.get("resource", {})
        entity_type = resource.get("@odata.type", "").replace("#microsoft.graph.", "")

        parent_ref = resource.get("parentReference", {})
        sp_ids = parent_ref.get("sharepointIds", {})

        # Extract listItem fields if nested
        list_item = resource.get("listItem", {})
        list_item_fields = list_item.get("fields", {}) if list_item else {}

        title = (
            resource.get("name")
            or list_item_fields.get("title")
            or resource.get("displayName")
            or hit.get("hitId", "?")
        )

        return SearchHit(
            rank=hit.get("rank", 0),
            title=title,
            summary=hit.get("summary", ""),
            web_url=resource.get("webUrl", ""),
            entity_type=entity_type,
            hit_id=hit.get("hitId", ""),
            last_modified=resource.get("lastModifiedDateTime", ""),
            site_id=parent_ref.get("siteId", ""),
            drive_id=parent_ref.get("driveId", ""),
            item_id=resource.get("id", ""),
            list_id=sp_ids.get("listId", ""),
            list_item_id=sp_ids.get("listItemId", ""),
            resource=resource,
        )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search SharePoint and OneDrive content via Microsoft Graph Search API"
    )
    parser.add_argument(
        "--env",
        default=None,
        help="Path to .env file (default: skill dir .env)",
    )
    parser.add_argument(
        "query",
        help="Search query string (supports KQL syntax)",
    )
    parser.add_argument(
        "--entity-types",
        default="driveItem,listItem",
        help="Comma-separated entity types to search (default: driveItem,listItem)",
    )
    parser.add_argument(
        "--site-path",
        default=None,
        help='KQL path scope, e.g. "sites/IACB" (optional)',
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=25,
        help="Maximum number of results (default: 25)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output raw JSON results (includes full resource objects)",
    )
    return parser


def _print_human(hits: list[SearchHit]) -> None:
    if not hits:
        print("No results found.")
        return
    print(f"{len(hits)} result(s):\n")
    for hit in hits:
        print(f"  [{hit.rank}] {hit.title}")
        print(f"      type: {hit.entity_type}  modified: {hit.last_modified}")
        if hit.web_url:
            print(f"      url: {hit.web_url}")
        if hit.summary:
            clean = hit.summary.replace("<c0>", "**").replace("</c0>", "**")
            clean = clean.replace("<ddd/>", "...")
            print(f"      {clean}")
        print()


def _print_json(hits: list[SearchHit]) -> None:
    output = [asdict(h) for h in hits]
    print(json.dumps(output, indent=2, ensure_ascii=False, default=str))


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        client = SearchClient(env_path=args.env)
        entity_types = [t.strip() for t in args.entity_types.split(",")]
        hits = client.search(
            args.query,
            entity_types=entity_types,
            site_path=args.site_path,
            max_results=args.max_results,
        )
        if args.json_output:
            _print_json(hits)
        else:
            _print_human(hits)
        return 0
    except (AuthError, GraphApiError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
