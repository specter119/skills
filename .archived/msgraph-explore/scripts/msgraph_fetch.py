# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "httpxyz",
#     "markdownify",
#     "markitdown[docx,pptx,xlsx,pdf]",
#     "msal",
#     "orjson",
#     "python-dotenv",
# ]
# ///
"""
Fetch and sync content from SharePoint, OneDrive, and OneNote via Microsoft Graph.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urlsplit

import orjson
from markdownify import markdownify

from msgraph_auth import (
    CACHE_ROOT,
    DEFAULT_ENV_PATH,
    DRIVE_SCOPES,
    NOTES_SCOPES,
    AuthError,
    GraphApiError,
    GraphClient,
)

DEFAULT_FETCH_OUTPUT_DIR = CACHE_ROOT / "materialized" / "files"

_CONVERTIBLE_EXTS = frozenset(
    {".docx", ".pptx", ".xlsx", ".xls", ".pdf", ".html", ".htm"}
)


def _convert_to_markdown(source_path: Path) -> Path | None:
    if source_path.suffix.lower() not in _CONVERTIBLE_EXTS:
        return None
    try:
        from markitdown import MarkItDown

        md = MarkItDown()
        result = md.convert(str(source_path))
        md_path = source_path.with_suffix(source_path.suffix + ".md")
        md_path.write_text(result.text_content, encoding="utf-8")
        return md_path
    except Exception as exc:  # noqa: BLE001
        print(f"warning: markdown conversion failed for {source_path.name}: {exc}")
        return None


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
        parsed = urlsplit(unquote(url))
        parts = parsed.path.strip("/").split("/")
        try:
            idx = parts.index("sites")
            site_name = parts[idx + 1]
        except (ValueError, IndexError):
            raise ValueError(f"Cannot find site name in URL: {url}")
        marker = "Shared Documents/"
        pos = parsed.path.find(marker)
        if pos < 0:
            raise ValueError(f"Cannot find 'Shared Documents' path in URL: {url}")
        file_path = parsed.path[pos + len(marker):]
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

    def fetch_by_ids(
        self, drive_id: str, item_id: str, output_dir: str | Path | None = None
    ) -> Path:
        item = self.graph.get_json(f"/drives/{drive_id}/items/{item_id}")
        if "file" not in item:
            raise ValueError(
                f"Item {item_id} is not a file (name={item.get('name', '?')})"
            )
        filename = item.get("name", "download")
        materialized_dir = (
            Path(output_dir) if output_dir is not None else DEFAULT_FETCH_OUTPUT_DIR
        )
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


class WikiPageClient:
    """Fetch SharePoint wiki/publishing pages via Graph API."""

    _CONTENT_FIELDS = ("PublishingPageContent", "WikiField", "CanvasContent1")

    def __init__(self, env_path: str | Path | None = None):
        self.graph = GraphClient(env_path, DRIVE_SCOPES)

    def find_pages_drive(self, site_id: str) -> str:
        """Find the Pages library drive ID for a site."""
        lists = self.graph.get_all(
            f"/sites/{site_id}/lists",
            params={"$select": "id,displayName,list,drive"},
        )
        for lst in lists:
            template = lst.get("list", {}).get("template", "")
            name = lst.get("displayName", "")
            if template == "850" or name.lower() in ("pages", "site pages"):
                drives = self.graph.get_all(f"/sites/{site_id}/drives")
                for d in drives:
                    if d.get("name", "").lower() == name.lower():
                        return d["id"]
                raise ValueError(
                    f"Found Pages list '{name}' but no matching drive on site {site_id}"
                )
        raise ValueError(f"No Pages library found on site {site_id}")

    def search_pages(
        self,
        drive_id: str,
        query: str,
        *,
        max_results: int = 10,
    ) -> list[dict[str, Any]]:
        """Search the Pages drive for wiki pages matching a query."""
        items = self.graph.get_json(
            f"/drives/{drive_id}/root/search(q='{query}')",
            params={"$top": str(max_results)},
        )
        results = []
        for item in items.get("value", []):
            name = item.get("name", "")
            if not name.lower().endswith(".aspx"):
                continue
            results.append(
                {
                    "name": name,
                    "id": item["id"],
                    "size": item.get("size", 0),
                    "webUrl": item.get("webUrl", ""),
                }
            )
        return results

    def _extract_content_from_fields(
        self, fields: dict[str, Any]
    ) -> tuple[str, str] | None:
        """Extract wiki content from list item fields. Returns (field_name, html)."""
        import html as html_mod

        for field_name in self._CONTENT_FIELDS:
            raw = fields.get(field_name, "")
            if raw:
                content = html_mod.unescape(html_mod.unescape(raw))
                return field_name, content
        return None

    def _extract_content_from_aspx(self, aspx_text: str) -> tuple[str, str] | None:
        """Fallback: extract content from raw .aspx file XML metadata."""
        import html as html_mod
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(aspx_text, "html.parser")
        for field_name in self._CONTENT_FIELDS:
            # html.parser lowercases tags: <mso:PublishingPageContent> → mso:publishingpagecontent
            tag = soup.find(f"mso:{field_name.lower()}")
            if tag:
                raw = tag.decode_contents()
                if raw.strip():
                    content = html_mod.unescape(html_mod.unescape(raw))
                    return field_name, content
        return None

    def fetch_page_content(
        self, drive_id: str, item_id: str
    ) -> tuple[str, str, str]:
        """Fetch a single wiki page content. Returns (title, markdown, source_field)."""
        item = self.graph.get_json(
            f"/drives/{drive_id}/items/{item_id}",
            params={"$expand": "listItem($expand=fields)"},
        )
        filename = item.get("name", "page.aspx")
        title = filename.replace(".aspx", "").replace("_", " ")

        list_item = item.get("listItem", {})
        fields = list_item.get("fields", {})

        if fields.get("Title"):
            title = fields["Title"]

        result = self._extract_content_from_fields(fields)

        if not result:
            aspx_text = self.graph.get_text(
                f"/drives/{drive_id}/items/{item_id}/content", timeout=120
            )
            result = self._extract_content_from_aspx(aspx_text)

        if not result:
            raise ValueError(
                f"No wiki content found in {filename}. "
                f"Available fields: {list(fields.keys())[:15]}"
            )

        field_name, html_content = result
        md = markdownify(html_content, heading_style="ATX", strip=["script", "style"])
        md = re.sub(r"\n{4,}", "\n\n\n", md)
        md = re.sub(r"[ \t]+\n", "\n", md)
        full_md = f"# {title}\n\n*Source: SharePoint Wiki*\n\n{md.strip()}"
        return title, full_md, field_name

    def search_and_fetch(
        self,
        site_id: str,
        query: str,
        output_dir: str | Path,
        *,
        max_results: int = 10,
    ) -> list[Path]:
        """Search for wiki pages and fetch all matches."""
        drive_id = self.find_pages_drive(site_id)
        pages = self.search_pages(drive_id, query, max_results=max_results)
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        results: list[Path] = []

        for page in pages:
            safe_name = _sanitize_filename(page["name"])
            target = out / f"{safe_name}.md"
            try:
                title, md_content, field = self.fetch_page_content(
                    drive_id, page["id"]
                )
                target.write_text(md_content, encoding="utf-8")
                print(f"✅ {safe_name} ({len(md_content)} chars, via {field})")
                results.append(target)
            except Exception as exc:  # noqa: BLE001
                print(f"⚠️  {safe_name}: {exc}")

        return results


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
    fetch_file.add_argument("--url", default=None, help="SharePoint file URL")
    fetch_file.add_argument("--drive-id", default=None, help="Graph drive ID (use with --item-id)")
    fetch_file.add_argument("--item-id", default=None, help="Graph item ID (use with --drive-id)")
    fetch_file.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Local output directory "
            f"(default: {DEFAULT_FETCH_OUTPUT_DIR})"
        ),
    )
    fetch_file.add_argument(
        "--convert",
        action="store_true",
        help="Convert binary files (docx/pptx/xlsx/pdf) to Markdown",
    )
    fetch_file.set_defaults(handler=_handle_fetch_file)

    sync_folder = subparsers.add_parser("sync-folder", help="Sync a drive folder")
    sync_folder.add_argument("--remote-path", required=True, help="Remote folder path")
    sync_folder.add_argument("--output-dir", required=True, help="Local output directory")
    sync_folder.add_argument("--site-id", default=None)
    sync_folder.add_argument("--site-search", default=None)
    sync_folder.add_argument("--force", action="store_true")
    sync_folder.add_argument(
        "--convert",
        action="store_true",
        help="Convert binary files to Markdown after download",
    )
    sync_folder.set_defaults(handler=_handle_sync_folder)

    list_sites = subparsers.add_parser("list-sites", help="Search SharePoint sites")
    list_sites.add_argument("search", help="Search keyword")
    list_sites.set_defaults(handler=_handle_list_sites)

    list_notebooks = subparsers.add_parser("list-notebooks", help="List notebooks")
    list_notebooks.add_argument("--site-id", required=True)
    list_notebooks.set_defaults(handler=_handle_list_notebooks)

    list_sections = subparsers.add_parser("list-sections", help="List sections")
    list_sections.add_argument("--site-id", required=True)
    list_sections.add_argument("--notebook-id", required=True)
    list_sections.set_defaults(handler=_handle_list_sections)

    list_pages = subparsers.add_parser("list-pages", help="List pages")
    list_pages.add_argument("--site-id", required=True)
    list_pages.add_argument("--section-id", default=None)
    list_pages.set_defaults(handler=_handle_list_pages)

    fetch_page = subparsers.add_parser(
        "fetch-onenote-page",
        help="Fetch a single OneNote page as Markdown",
    )
    fetch_page.add_argument("--site-id", required=True)
    fetch_page.add_argument("--page-id", required=True)
    fetch_page.set_defaults(handler=_handle_fetch_onenote_page)

    search_pages = subparsers.add_parser(
        "search-pages", help="Search SharePoint wiki pages"
    )
    search_pages.add_argument("--site-id", required=True, help="SharePoint site ID")
    search_pages.add_argument("--query", required=True, help="Search query")
    search_pages.add_argument("--max-results", type=int, default=10)
    search_pages.set_defaults(handler=_handle_search_pages)

    fetch_wiki_page = subparsers.add_parser(
        "fetch-page", help="Fetch SharePoint wiki page as Markdown"
    )
    fetch_wiki_page.add_argument(
        "--site-id", default=None, help="SharePoint site ID (with --query)"
    )
    fetch_wiki_page.add_argument(
        "--query", default=None, help="Search query (with --site-id)"
    )
    fetch_wiki_page.add_argument(
        "--drive-id", default=None, help="Pages drive ID (with --item-id)"
    )
    fetch_wiki_page.add_argument(
        "--item-id", default=None, help="Drive item ID (with --drive-id)"
    )
    fetch_wiki_page.add_argument(
        "--output-dir", required=True, help="Output directory for markdown files"
    )
    fetch_wiki_page.add_argument("--max-results", type=int, default=10)
    fetch_wiki_page.set_defaults(handler=_handle_fetch_page)

    fetch_onenote = subparsers.add_parser(
        "fetch-onenote",
        help="Fetch OneNote content to local Markdown files",
    )
    fetch_onenote.add_argument("--site-id", default=None)
    fetch_onenote.add_argument("--site-search", default=None)
    fetch_onenote.add_argument("--output-dir", required=True)
    fetch_onenote.add_argument("--notebook-id", default=None)
    fetch_onenote.add_argument("--section-id", default=None)
    fetch_onenote.set_defaults(handler=_handle_fetch_onenote)

    return parser


def _handle_fetch_file(args: argparse.Namespace) -> int:
    client = DriveClient(env_path=args.env)
    if args.drive_id and args.item_id:
        local_path = client.fetch_by_ids(args.drive_id, args.item_id, args.output_dir)
    elif args.url:
        local_path = client.fetch_file(args.url, args.output_dir)
    else:
        raise ValueError("Provide either --url or both --drive-id and --item-id")
    print(local_path)
    if args.convert:
        md_path = _convert_to_markdown(local_path)
        if md_path:
            print(md_path)
    return 0


def _handle_sync_folder(args: argparse.Namespace) -> int:
    client = DriveClient(env_path=args.env)
    written = client.sync_folder(
        args.remote_path,
        args.output_dir,
        site_id=args.site_id,
        site_search=args.site_search,
        force=args.force,
    )
    if args.convert:
        for path in written:
            md_path = _convert_to_markdown(path)
            if md_path:
                print(f"convert {path.name} -> {md_path.name}")
    return 0


def _handle_list_sites(args: argparse.Namespace) -> int:
    client = OneNoteClient(env_path=args.env)
    sites = client.list_sites(args.search)
    for site in sites:
        print(f"{site.get('displayName', '?'):<30} {site['id']}")
    return 0


def _handle_list_notebooks(args: argparse.Namespace) -> int:
    client = OneNoteClient(env_path=args.env)
    notebooks = client.list_notebooks(args.site_id)
    for notebook in notebooks:
        print(f"{notebook.get('displayName', '?'):<30} {notebook['id']}")
    return 0


def _handle_list_sections(args: argparse.Namespace) -> int:
    client = OneNoteClient(env_path=args.env)
    sections = client.list_sections(args.site_id, args.notebook_id)
    for section in sections:
        print(f"{section.get('displayName', '?'):<30} {section['id']}")
    return 0


def _handle_list_pages(args: argparse.Namespace) -> int:
    client = OneNoteClient(env_path=args.env)
    pages = client.list_pages(args.site_id, section_id=args.section_id)
    for page in pages:
        print(f"{page.get('title', '?'):<40} {page['id']}")
    return 0


def _handle_search_pages(args: argparse.Namespace) -> int:
    client = WikiPageClient(env_path=args.env)
    drive_id = client.find_pages_drive(args.site_id)
    print(f"Pages drive: {drive_id}")
    pages = client.search_pages(drive_id, args.query, max_results=args.max_results)
    for page in pages:
        size_kb = page.get("size", 0) / 1024
        print(f"  {page['name']:<60} {size_kb:>8.1f} KB  id={page['id']}")
    print(f"\n{len(pages)} page(s) found.")
    return 0


def _handle_fetch_page(args: argparse.Namespace) -> int:
    client = WikiPageClient(env_path=args.env)
    if args.site_id and args.query:
        paths = client.search_and_fetch(
            args.site_id,
            args.query,
            args.output_dir,
            max_results=args.max_results,
        )
        print(f"\n{len(paths)} page(s) fetched.")
    elif args.drive_id and args.item_id:
        title, md_content, field = client.fetch_page_content(args.drive_id, args.item_id)
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        safe_name = _sanitize_filename(f"{title}.aspx.md")
        target = out / safe_name
        target.write_text(md_content, encoding="utf-8")
        print(f"✅ {target} ({len(md_content)} chars, via {field})")
    else:
        raise ValueError("Provide --site-id --query or --drive-id --item-id")
    return 0


def _handle_fetch_onenote_page(args: argparse.Namespace) -> int:
    client = OneNoteClient(env_path=args.env)
    markdown = client.fetch_page_markdown(args.site_id, args.page_id)
    print(markdown)
    return 0


def _handle_fetch_onenote(args: argparse.Namespace) -> int:
    _require_site_identifier(args.site_id, args.site_search)
    client = OneNoteClient(env_path=args.env)
    site_id = args.site_id
    if args.site_search:
        sites = client.list_sites(args.site_search)
        if not sites:
            raise ValueError(f"No sites found for '{args.site_search}'")
        site_id = sites[0]["id"]
        print(f"Using site: {sites[0].get('displayName', site_id)} ({site_id})")
    if site_id is None:
        raise ValueError("Provide either --site-id or --site-search")
    if args.section_id:
        client.sync_section(site_id, args.section_id, args.output_dir)
    elif args.notebook_id:
        client.sync_notebook(site_id, args.notebook_id, args.output_dir)
    else:
        client.sync_site(site_id, args.output_dir)
    return 0


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1
    try:
        return handler(args)
    except (AuthError, GraphApiError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
