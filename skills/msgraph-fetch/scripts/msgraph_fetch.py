# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "httpx",
#     "markdownify",
#     "msal",
#     "orjson",
#     "python-dotenv",
# ]
# ///
"""
Unified Microsoft Graph fetcher for SharePoint, OneDrive, and OneNote.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
from functools import cache
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urlsplit

import httpx
import orjson
from dotenv import dotenv_values
from markdownify import markdownify
from msal import PublicClientApplication

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
NOTES_SCOPES = ("Notes.Read.All", "Sites.Read.All")
DRIVE_SCOPES = ("Files.Read.All", "Sites.Read.All")
CACHE_ROOT = Path.home() / ".cache" / "msgraph-fetch"
DEFAULT_FETCH_OUTPUT_DIR = CACHE_ROOT / "materialized" / "files"
DEFAULT_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def _slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return value.strip("-") or "item"


def _sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:200] if name else "untitled"


def _site_cache_key(site_id: str) -> str:
    return hashlib.md5(site_id.encode(), usedforsecurity=False).hexdigest()[:12]


def _item_cache_key(item_id: str) -> str:
    return hashlib.md5(item_id.encode(), usedforsecurity=False).hexdigest()[:16]


def _read_meta(meta_path: Path) -> dict[str, Any]:
    if meta_path.exists():
        return orjson.loads(meta_path.read_bytes())
    return {}


def _write_meta(meta_path: Path, meta: dict[str, Any]) -> None:
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_bytes(orjson.dumps(meta, option=orjson.OPT_INDENT_2))


def _copy_if_needed(source: Path, target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    source_bytes = source.read_bytes()
    if not target.exists() or target.read_bytes() != source_bytes:
        target.write_bytes(source_bytes)
    return target.resolve()


def _persist_text_if_needed(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.read_text(encoding="utf-8") != content:
        target.write_text(content, encoding="utf-8")


def _encode_graph_path(path: str) -> str:
    stripped = path.strip("/")
    if not stripped:
        return ""
    return quote(stripped, safe="/!$&'()*+,;=:@")


def _update_env_refresh_token(env_path: Path, new_token: str) -> None:
    if not env_path.exists():
        return

    lines = env_path.read_text(encoding="utf-8").splitlines(keepends=True)
    found = False
    with env_path.open("w", encoding="utf-8") as handle:
        for line in lines:
            if line.startswith("MICROSOFT_REFRESH_TOKEN="):
                handle.write(f"MICROSOFT_REFRESH_TOKEN={new_token}\n")
                found = True
            else:
                handle.write(line)
        if not found:
            if lines and not lines[-1].endswith("\n"):
                handle.write("\n")
            handle.write(f"MICROSOFT_REFRESH_TOKEN={new_token}\n")


@cache
def _get_msal_app(
    client_id: str, authority: str, scope_key: tuple[str, ...]
) -> PublicClientApplication:
    del scope_key
    return PublicClientApplication(client_id, authority=authority)


def _get_access_token(env_path: Path, scopes: tuple[str, ...]) -> str:
    config = dotenv_values(env_path)
    client_id = config.get("MICROSOFT_CLIENT_ID", "")
    authority = config.get("MICROSOFT_AUTHORITY", "")
    if not client_id or not authority:
        raise ValueError(
            f"Missing MICROSOFT_CLIENT_ID or MICROSOFT_AUTHORITY in {env_path}"
        )

    app = _get_msal_app(client_id, authority, scopes)
    refresh_token = config.get("MICROSOFT_REFRESH_TOKEN")
    if refresh_token:
        result = app.acquire_token_by_refresh_token(refresh_token, scopes=list(scopes))
        if "access_token" in result:
            if "refresh_token" in result:
                _update_env_refresh_token(env_path, result["refresh_token"])
            return result["access_token"]

    result = app.acquire_token_interactive(scopes=list(scopes))
    if "access_token" not in result:
        raise ValueError(f"Authentication failed: {result.get('error_description')}")
    if "refresh_token" in result:
        _update_env_refresh_token(env_path, result["refresh_token"])
    return result["access_token"]


class GraphClient:
    def __init__(self, env_path: str | Path | None, scopes: tuple[str, ...]):
        self.env_path = Path(env_path) if env_path else DEFAULT_ENV_PATH
        self.scopes = scopes
        self._headers: dict[str, str] | None = None

    @property
    def headers(self) -> dict[str, str]:
        if self._headers is None:
            token = _get_access_token(self.env_path, self.scopes)
            self._headers = {"Authorization": f"Bearer {token}"}
        return self._headers

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        timeout: int = 30,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        url = f"{GRAPH_BASE}{path}" if path.startswith("/") else path
        response = httpx.request(
            method,
            url,
            headers=self.headers,
            params=params,
            timeout=timeout,
            follow_redirects=follow_redirects,
        )
        response.raise_for_status()
        return response

    def get_json(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return self._request("GET", path, params=params).json()

    def get_all(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        next_url: str | None = f"{GRAPH_BASE}{path}" if path.startswith("/") else path
        next_params = params
        while next_url:
            response = self._request("GET", next_url, params=next_params)
            payload = response.json()
            results.extend(payload.get("value", []))
            next_url = payload.get("@odata.nextLink")
            next_params = None
        return results

    def get_text(self, path: str, *, timeout: int = 60) -> str:
        return self._request("GET", path, timeout=timeout).text

    def get_bytes(self, path: str, *, timeout: int = 60) -> bytes:
        return self._request(
            "GET", path, timeout=timeout, follow_redirects=True
        ).content


def _preprocess_onenote_html(html: str) -> str:
    from bs4 import BeautifulSoup, NavigableString

    soup = BeautifulSoup(html, "html.parser")

    for table in soup.find_all("table"):
        if table.find("thead") or table.find("th"):
            continue
        first_tr = table.find("tr")
        if not first_tr:
            continue
        for td in first_tr.find_all("td"):
            td.name = "th"
        thead = soup.new_tag("thead")
        first_tr.wrap(thead)
        remaining_trs = table.find_all("tr")
        if remaining_trs:
            tbody = soup.new_tag("tbody")
            for tr in remaining_trs:
                tbody.append(tr.extract())
            table.append(tbody)

    for cell in soup.find_all(["td", "th"]):
        for ul in cell.find_all(["ul", "ol"]):
            items = [li.get_text(strip=True) for li in ul.find_all("li")]
            ul.replace_with(NavigableString("; ".join(items)))

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if not href.startswith("onenote:"):
            continue
        match = re.match(r"onenote:#(.+?)&", href)
        if match:
            title = unquote(match.group(1))
            link["href"] = f"{_sanitize_filename(title)}.md"

    return str(soup)


def html_to_markdown(html: str) -> str:
    html = re.sub(
        r'<p[^>]*data-tag="to-do"[^>]*>(.*?)</p>',
        r"<li>[ ] \1</li>",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<p[^>]*data-tag="to-do:completed"[^>]*>(.*?)</p>',
        r"<li>[x] \1</li>",
        html,
        flags=re.DOTALL,
    )
    html = _preprocess_onenote_html(html)
    markdown = markdownify(html, heading_style="ATX", strip=["style", "script"])
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


class OneNoteClient:
    def __init__(self, env_path: str | Path | None = None):
        self.graph = GraphClient(env_path, NOTES_SCOPES)

    def _source_root(self, site_id: str) -> Path:
        return CACHE_ROOT / "sources" / "onenote" / _site_cache_key(site_id)

    def _derived_root(self, site_id: str) -> Path:
        return CACHE_ROOT / "derived" / "onenote" / _site_cache_key(site_id)

    def _meta_root(self, site_id: str) -> Path:
        return CACHE_ROOT / "meta" / "onenote" / _site_cache_key(site_id)

    def list_sites(self, search: str) -> list[dict[str, Any]]:
        return self.graph.get_all(f"/sites?search={search}")

    def list_notebooks(self, site_id: str) -> list[dict[str, Any]]:
        return self.graph.get_all(f"/sites/{site_id}/onenote/notebooks")

    def list_sections(
        self, site_id: str, notebook_id: str
    ) -> list[dict[str, Any]]:
        return self.graph.get_all(
            f"/sites/{site_id}/onenote/notebooks/{notebook_id}/sections"
        )

    def list_pages(
        self, site_id: str, *, section_id: str | None = None
    ) -> list[dict[str, Any]]:
        if section_id:
            return self.graph.get_all(f"/sites/{site_id}/onenote/sections/{section_id}/pages")
        return self.graph.get_all(f"/sites/{site_id}/onenote/pages")

    def _page_meta_path(self, site_id: str, page_id: str) -> Path:
        return self._meta_root(site_id) / "pages" / f"{page_id}.json"

    def _page_html_path(self, site_id: str, page_id: str) -> Path:
        return self._source_root(site_id) / "pages" / f"{page_id}.html"

    def _page_markdown_path(self, site_id: str, page_id: str) -> Path:
        return self._derived_root(site_id) / "pages" / f"{page_id}.md"

    def fetch_page_html(self, site_id: str, page_id: str) -> str:
        return self.graph.get_text(
            f"/sites/{site_id}/onenote/pages/{page_id}/content", timeout=60
        )

    def fetch_page_markdown(
        self, site_id: str, page_id: str, *, use_cache: bool = True
    ) -> str:
        meta_path = self._page_meta_path(site_id, page_id)
        html_path = self._page_html_path(site_id, page_id)
        markdown_path = self._page_markdown_path(site_id, page_id)
        page_info = self.graph.get_json(f"/sites/{site_id}/onenote/pages/{page_id}")
        last_modified = page_info.get("lastModifiedDateTime")

        if use_cache and html_path.exists():
            meta = _read_meta(meta_path)
            if meta.get("lastModifiedDateTime") == last_modified:
                if markdown_path.exists():
                    return markdown_path.read_text(encoding="utf-8")
                markdown = html_to_markdown(html_path.read_text(encoding="utf-8"))
                _persist_text_if_needed(markdown_path, markdown)
                return markdown

        html = self.fetch_page_html(site_id, page_id)
        _persist_text_if_needed(html_path, html)

        markdown = html_to_markdown(html)
        _persist_text_if_needed(markdown_path, markdown)
        _write_meta(
            meta_path,
            {
                "page_id": page_id,
                "title": page_info.get("title", ""),
                "lastModifiedDateTime": last_modified,
                "cached_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
        )
        return markdown

    def _sync_pages(
        self,
        site_id: str,
        pages: list[dict[str, Any]],
        output_dir: Path,
        *,
        verbose: bool = True,
    ) -> list[Path]:
        written: list[Path] = []
        total = len(pages)
        for index, page in enumerate(pages, start=1):
            title = page.get("title", page["id"][:12])
            filename = _sanitize_filename(title) + ".md"
            if verbose:
                print(f"  [{index}/{total}] {title}")
            markdown = self.fetch_page_markdown(site_id, page["id"])
            file_path = output_dir / filename
            _persist_text_if_needed(file_path, f"# {title}\n\n{markdown}")
            written.append(file_path.resolve())
        return written

    def sync_section(
        self,
        site_id: str,
        section_id: str,
        output_dir: str | Path,
        *,
        verbose: bool = True,
    ) -> list[Path]:
        output = Path(output_dir)
        pages = self.list_pages(site_id, section_id=section_id)
        if verbose:
            print(f"{len(pages)} page(s) in section")
        written = self._sync_pages(site_id, pages, output, verbose=verbose)
        if verbose:
            print(f"Synced {len(written)} page(s) to {output}")
        return written

    def sync_notebook(
        self,
        site_id: str,
        notebook_id: str,
        output_dir: str | Path,
        *,
        verbose: bool = True,
    ) -> list[Path]:
        output = Path(output_dir)
        written: list[Path] = []
        notebook = self.graph.get_json(f"/sites/{site_id}/onenote/notebooks/{notebook_id}")
        notebook_name = _sanitize_filename(notebook.get("displayName", "notebook"))
        if verbose:
            print(f"Notebook: {notebook_name}")
        for section in self.list_sections(site_id, notebook_id):
            section_name = _sanitize_filename(section.get("displayName", "section"))
            if verbose:
                print(f"Section: {section_name}")
            pages = self.list_pages(site_id, section_id=section["id"])
            written.extend(
                self._sync_pages(
                    site_id,
                    pages,
                    output / notebook_name / section_name,
                    verbose=verbose,
                )
            )
        if verbose:
            print(f"Synced {len(written)} page(s) to {output}")
        return written

    def sync_site(
        self, site_id: str, output_dir: str | Path, *, verbose: bool = True
    ) -> list[Path]:
        output = Path(output_dir)
        written: list[Path] = []
        for notebook in self.list_notebooks(site_id):
            written.extend(self.sync_notebook(site_id, notebook["id"], output, verbose=verbose))
        if verbose:
            print(f"Synced {len(written)} page(s) to {output}")
        return written


class DriveClient:
    def __init__(self, env_path: str | Path | None = None):
        self.graph = GraphClient(env_path, DRIVE_SCOPES)

    def list_sites(self, search: str) -> list[dict[str, Any]]:
        return self.graph.get_all(f"/sites?search={search}")

    def _resolve_site_id(self, site_id: str | None, site_search: str | None) -> str | None:
        if site_id:
            return site_id
        if site_search:
            sites = self.list_sites(site_search)
            if not sites:
                raise ValueError(f"No sites found for '{site_search}'")
            return sites[0]["id"]
        return None

    def _resolve_drive(self, site_id: str | None = None, site_search: str | None = None) -> dict[str, Any]:
        resolved_site_id = self._resolve_site_id(site_id, site_search)
        if resolved_site_id:
            drive = self.graph.get_json(f"/sites/{resolved_site_id}/drive")
            drive["resolved_site_id"] = resolved_site_id
            return drive
        drive = self.graph.get_json("/me/drive")
        drive["resolved_site_id"] = None
        return drive

    def _drive_source_path(self, drive_id: str, item_id: str, filename: str) -> Path:
        return (
            CACHE_ROOT
            / "sources"
            / "drive"
            / _slugify(drive_id)
            / _item_cache_key(item_id)
            / filename
        )

    def _drive_meta_path(self, drive_id: str, item_id: str) -> Path:
        return (
            CACHE_ROOT
            / "meta"
            / "drive"
            / _slugify(drive_id)
            / f"{_item_cache_key(item_id)}.json"
        )

    def _download_item_if_needed(
        self,
        drive_id: str,
        item: dict[str, Any],
        output_path: Path,
        *,
        force: bool = False,
    ) -> tuple[Path, bool]:
        item_id = item["id"]
        filename = item.get("name", item_id)
        source_path = self._drive_source_path(drive_id, item_id, filename)
        meta_path = self._drive_meta_path(drive_id, item_id)
        remote_etag = item.get("eTag") or item.get("cTag") or ""
        cached_meta = _read_meta(meta_path)
        cache_hit = (
            not force
            and source_path.exists()
            and cached_meta.get("etag") == remote_etag
        )

        if not cache_hit:
            content = self.graph.get_bytes(
                f"/drives/{drive_id}/items/{item_id}/content", timeout=120
            )
            source_path.parent.mkdir(parents=True, exist_ok=True)
            source_path.write_bytes(content)
            _write_meta(
                meta_path,
                {
                    "item_id": item_id,
                    "name": filename,
                    "etag": remote_etag,
                    "size": item.get("size"),
                    "webUrl": item.get("webUrl"),
                    "cached_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                },
            )

        local_path = _copy_if_needed(source_path, output_path)
        return local_path, cache_hit

    def _parse_sharepoint_file_url(self, url: str) -> tuple[str, str]:
        decoded_url = unquote(url)
        site_match = re.search(r"sharepoint\.com(?:/:\w:/\w)?/sites/([^/]+)", decoded_url)
        file_match = re.search(r"/Shared Documents/(.+?)(?:\?|$)", decoded_url)
        if not site_match or not file_match:
            raise ValueError(f"Cannot parse SharePoint file URL: {url}")
        site_name = site_match.group(1)
        file_path = file_match.group(1)
        return site_name, file_path

    def fetch_file(self, url: str, output_dir: str | Path | None = None) -> Path:
        site_search, file_path = self._parse_sharepoint_file_url(url)
        drive = self._resolve_drive(site_search=site_search)
        drive_id = drive["id"]
        encoded_path = _encode_graph_path(file_path)
        item = self.graph.get_json(f"/drives/{drive_id}/root:/{encoded_path}")
        filename = item.get("name", Path(urlsplit(url).path).name or "download")
        materialized_dir = Path(output_dir) if output_dir is not None else DEFAULT_FETCH_OUTPUT_DIR
        output_path = materialized_dir / filename
        local_path, _ = self._download_item_if_needed(drive_id, item, output_path)
        return local_path

    def _list_folder_items(
        self, drive_id: str, remote_path: str
    ) -> list[dict[str, Any]]:
        encoded = _encode_graph_path(remote_path)
        if encoded:
            path = f"/drives/{drive_id}/root:/{encoded}:/children"
        else:
            path = f"/drives/{drive_id}/root/children"
        return self.graph.get_all(
            path,
            params={"$select": "name,size,id,file,folder,eTag,cTag,webUrl", "$top": "200"},
        )

    def sync_folder(
        self,
        remote_path: str,
        output_dir: str | Path,
        *,
        site_id: str | None = None,
        site_search: str | None = None,
        force: bool = False,
    ) -> list[Path]:
        drive = self._resolve_drive(site_id=site_id, site_search=site_search)
        drive_id = drive["id"]
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        items = self._list_folder_items(drive_id, remote_path)
        written: list[Path] = []

        print(f"Drive: {drive.get('name', drive_id)}")
        print(f"Remote folder: {remote_path}")
        print(f"Output directory: {output.resolve()}")

        for item in items:
            if "file" not in item:
                print(f"skip  {item.get('name', item['id'])} (not a file)")
                continue

            output_path = output / item["name"]
            local_path, cache_hit = self._download_item_if_needed(
                drive_id, item, output_path, force=force
            )
            action = "skip" if cache_hit and not force else "sync"
            size_kb = (item.get("size", 0) or 0) / 1024
            print(f"{action:<5} {item['name']} ({size_kb:.1f} KB) -> {local_path}")
            written.append(local_path)

        print(f"Done. {len(written)} file(s) materialized.")
        return written


def _require_site_identifier(site_id: str | None, site_search: str | None) -> str:
    if not site_id and not site_search:
        raise ValueError("Provide either --site-id or --site-search")
    return site_id or site_search or ""


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch Microsoft Graph content from SharePoint, OneDrive, and OneNote"
    )
    parser.add_argument(
        "--env",
        default=None,
        help="Path to .env file (default: skill dir .env)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_file = subparsers.add_parser("fetch-file", help="Fetch a SharePoint file")
    fetch_file.add_argument("--url", required=True, help="SharePoint file URL")
    fetch_file.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Local output directory "
            f"(default: {DEFAULT_FETCH_OUTPUT_DIR})"
        ),
    )

    sync_folder = subparsers.add_parser("sync-folder", help="Sync a drive folder")
    sync_folder.add_argument("--remote-path", required=True, help="Remote folder path")
    sync_folder.add_argument("--output-dir", required=True, help="Local output directory")
    sync_folder.add_argument("--site-id", default=None)
    sync_folder.add_argument("--site-search", default=None)
    sync_folder.add_argument("--force", action="store_true")

    list_sites = subparsers.add_parser("list-sites", help="Search SharePoint sites")
    list_sites.add_argument("search", help="Search keyword")

    list_notebooks = subparsers.add_parser("list-notebooks", help="List notebooks")
    list_notebooks.add_argument("--site-id", required=True)

    list_sections = subparsers.add_parser("list-sections", help="List sections")
    list_sections.add_argument("--site-id", required=True)
    list_sections.add_argument("--notebook-id", required=True)

    list_pages = subparsers.add_parser("list-pages", help="List pages")
    list_pages.add_argument("--site-id", required=True)
    list_pages.add_argument("--section-id", default=None)

    fetch_page = subparsers.add_parser(
        "fetch-onenote-page",
        help="Fetch a single OneNote page as Markdown",
    )
    fetch_page.add_argument("--site-id", required=True)
    fetch_page.add_argument("--page-id", required=True)

    fetch_onenote = subparsers.add_parser(
        "fetch-onenote",
        help="Fetch OneNote content to local Markdown files",
    )
    fetch_onenote.add_argument("--site-id", default=None)
    fetch_onenote.add_argument("--site-search", default=None)
    fetch_onenote.add_argument("--output-dir", required=True)
    fetch_onenote.add_argument("--notebook-id", default=None)
    fetch_onenote.add_argument("--section-id", default=None)

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        if args.command == "fetch-file":
            client = DriveClient(env_path=args.env)
            local_path = client.fetch_file(args.url, args.output_dir)
            print(local_path)
            return 0

        if args.command == "sync-folder":
            client = DriveClient(env_path=args.env)
            client.sync_folder(
                args.remote_path,
                args.output_dir,
                site_id=args.site_id,
                site_search=args.site_search,
                force=args.force,
            )
            return 0

        if args.command == "list-sites":
            client = OneNoteClient(env_path=args.env)
            sites = client.list_sites(args.search)
            for site in sites:
                print(f"{site.get('displayName', '?'):<30} {site['id']}")
            return 0

        if args.command == "list-notebooks":
            client = OneNoteClient(env_path=args.env)
            notebooks = client.list_notebooks(args.site_id)
            for notebook in notebooks:
                print(f"{notebook.get('displayName', '?'):<30} {notebook['id']}")
            return 0

        if args.command == "list-sections":
            client = OneNoteClient(env_path=args.env)
            sections = client.list_sections(args.site_id, args.notebook_id)
            for section in sections:
                print(f"{section.get('displayName', '?'):<30} {section['id']}")
            return 0

        if args.command == "list-pages":
            client = OneNoteClient(env_path=args.env)
            pages = client.list_pages(args.site_id, section_id=args.section_id)
            for page in pages:
                print(f"{page.get('title', '?'):<40} {page['id']}")
            return 0

        if args.command == "fetch-onenote-page":
            client = OneNoteClient(env_path=args.env)
            markdown = client.fetch_page_markdown(args.site_id, args.page_id)
            print(markdown)
            return 0

        if args.command == "fetch-onenote":
            _require_site_identifier(args.site_id, args.site_search)
            client = OneNoteClient(env_path=args.env)
            site_id = args.site_id
            if args.site_search:
                sites = client.list_sites(args.site_search)
                if not sites:
                    raise ValueError(f"No sites found for '{args.site_search}'")
                site_id = sites[0]["id"]
                print(f"Using site: {sites[0].get('displayName', site_id)} ({site_id})")

            assert site_id is not None
            if args.section_id:
                client.sync_section(site_id, args.section_id, args.output_dir)
            elif args.notebook_id:
                client.sync_notebook(site_id, args.notebook_id, args.output_dir)
            else:
                client.sync_site(site_id, args.output_dir)
            return 0

    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
