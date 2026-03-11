---
name: onenote-wiki
description: >
  Fetches OneNote wiki pages from SharePoint sites via Microsoft Graph API,
  caches locally with eTag invalidation, and converts HTML to Markdown.
  Use when asked to "fetch onenote", "read wiki", "download onenote pages",
  "sync onenote", "拉取 onenote", "同步 wiki".
---

# Fetching OneNote Wiki Pages

Fetches OneNote notebook pages from SharePoint sites via Microsoft Graph API,
converts HTML content to Markdown, and caches locally for offline use.

## When to Activate

- User asks to fetch/read/sync OneNote or wiki content from SharePoint
- User needs to convert OneNote pages to Markdown
- Chinese: "拉取 onenote", "同步 wiki", "读取笔记本"

## Prerequisites

### .env Configuration

Copy `.env.example` from this skill directory to your project root:

```bash
cp .env.example /path/to/project/.env
```

Required variables (see `.env.example` for defaults and comments):

| Variable                  | Description                                                     |
| ------------------------- | --------------------------------------------------------------- |
| `MICROSOFT_CLIENT_ID`     | Azure AD app registration client ID                             |
| `MICROSOFT_AUTHORITY`     | `https://login.microsoftonline.com/<tenant-id>`                 |
| `MICROSOFT_REFRESH_TOKEN` | Leave empty for first run; auto-updated after interactive login |

### App Registration

Required Microsoft Entra (Azure AD) app registration with **delegated** permissions:

- `Notes.Read.All` — read all OneNote notebooks the user can access
- `Sites.Read.All` — resolve SharePoint site IDs

> **Note**: OneNote Graph API dropped app-only auth support (March 2025).
> Must use delegated (user) auth via `PublicClientApplication`.

### Dependencies

```plain
httpx, msal, markdownify, orjson, python-dotenv, polars (optional)
```

## Architecture

```plain
SharePoint Site
  └── OneNote Notebooks
        └── Section Groups (optional nesting)
              └── Sections
                    └── Pages (HTML content)

Graph API hierarchy:
  /sites/{site-id}/onenote/notebooks
  /sites/{site-id}/onenote/notebooks/{id}/sectionGroups
  /sites/{site-id}/onenote/notebooks/{id}/sections
  /sites/{site-id}/onenote/sections/{id}/pages
  /sites/{site-id}/onenote/pages/{id}/content  → HTML
```

## Workflow

### 1. Discover Site

```python
from onenote_wiki import OneNoteClient

client = OneNoteClient()                       # reads .env
client = OneNoteClient(env_path="path/.env")   # explicit path

# Search SharePoint sites by keyword
sites = client.list_sites("DevSecOps")
# Returns: [{"id": "...", "displayName": "...", "description": "..."}, ...]
```

### 2. List Structure

```python
# List all notebooks on a site
notebooks = client.list_notebooks(site_id)

# List sections in a notebook
sections = client.list_sections(site_id, notebook_id)

# List pages in a section
pages = client.list_pages(site_id, section_id=section_id)

# Or list ALL pages across the entire site
all_pages = client.list_pages(site_id)
```

### 3. Fetch & Convert Single Page

```python
# Fetch page content as Markdown (auto-cached)
md = client.fetch_page_markdown(site_id, page_id)

# Fetch raw HTML
html = client.fetch_page_html(site_id, page_id)
```

### 4. Bulk Sync to Local Directory

```python
# Sync all pages from a site to local Markdown files
# Directory structure: {output_dir}/{notebook}/{section}/{page_title}.md
client.sync_site(site_id, output_dir="./wiki_cache")

# Sync specific notebook only
client.sync_notebook(site_id, notebook_id, output_dir="./wiki_cache")
```

### 5. Use in Marimo Notebook

```python
from onenote_wiki import OneNoteClient
import marimo as mo

client = OneNoteClient()
sites = client.list_sites("MyTeam")
site_id = sites[0]["id"]

pages = client.list_pages(site_id)
md_content = client.fetch_page_markdown(site_id, pages[0]["id"])
mo.md(md_content)
```

## Script Reference

Run `scripts/onenote_wiki.py` for the full implementation.

Key design decisions from existing codebase patterns (see `IACB/utils.py`):

| Pattern                         | Source                               | Applied                                   |
| ------------------------------- | ------------------------------------ | ----------------------------------------- |
| MSAL refresh token rotation     | `utils.py` `_get_access_token()`     | Auto-persist new refresh tokens to `.env` |
| eTag-based cache invalidation   | `utils.py` `fetch_sharepoint_file()` | Skip re-download if content unchanged     |
| `@cache` for MSAL app singleton | `utils.py` `_get_msal_app()`         | Avoid re-creating MSAL app per call       |
| httpx for HTTP calls            | Both files                           | Consistent HTTP client                    |
| Graph API site search           | `onenote_eda.py`                     | `sites?search=` for discovery             |

## Graph API Reference

### Key Endpoints

| Action                  | Method | URL                                                          |
| ----------------------- | ------ | ------------------------------------------------------------ |
| Search sites            | GET    | `/v1.0/sites?search={keyword}`                               |
| List notebooks          | GET    | `/v1.0/sites/{site-id}/onenote/notebooks`                    |
| List section groups     | GET    | `/v1.0/sites/{site-id}/onenote/notebooks/{id}/sectionGroups` |
| List sections           | GET    | `/v1.0/sites/{site-id}/onenote/notebooks/{id}/sections`      |
| List pages (site-wide)  | GET    | `/v1.0/sites/{site-id}/onenote/pages`                        |
| List pages (by section) | GET    | `/v1.0/sites/{site-id}/onenote/sections/{id}/pages`          |
| Get page content        | GET    | `/v1.0/sites/{site-id}/onenote/pages/{id}/content`           |
| Personal notebooks      | GET    | `/v1.0/me/onenote/notebooks`                                 |
| Personal pages          | GET    | `/v1.0/me/onenote/pages`                                     |

### Pagination

OneNote API uses `@odata.nextLink` for pagination. Default page size is 20.
Always follow `@odata.nextLink` to get all results:

```python
results = []
url = initial_url
while url:
    resp = httpx.get(url, headers=headers)
    data = resp.json()
    results.extend(data.get("value", []))
    url = data.get("@odata.nextLink")
```

### Page Content (HTML)

The `/content` endpoint returns HTML (not JSON). Key characteristics:

- Content-Type: `text/html`
- Contains OneNote-specific HTML elements (`data-id`, `data-tag` attributes)
- Embedded images use `src` pointing to Graph API resource URLs
- Tables, lists, headings are standard HTML

### HTML → Markdown Conversion

Recommended: `markdownify` (lightweight, already used in the EDA notebook).

Alternative for higher performance: `html-to-markdown` (Rust-powered, pip install html-to-markdown).

OneNote HTML quirks to handle:

- `<br>` tags within paragraphs (preserve as line breaks)
- `<table>` with merged cells (simplify to flat tables)
- `<img>` src pointing to Graph API (optionally download and embed)
- `data-tag="to-do"` for checkboxes (convert to `- [ ]` / `- [x]`)

## Caching Strategy

```plain
~/.cache/onenote-wiki/
  └── {site_id_hash}/
        └── {page_id}.html          # raw HTML cache
        └── {page_id}.md            # converted Markdown
        └── {page_id}.meta.json     # lastModifiedDateTime, eTag
```

Cache invalidation: compare `lastModifiedDateTime` from page metadata.
Only re-fetch content if page was modified since last cache.

## Error Handling

| Error                 | Cause                   | Resolution                                                                       |
| --------------------- | ----------------------- | -------------------------------------------------------------------------------- |
| 401 Unauthorized      | Token expired           | Auto-refresh via MSAL; if refresh token also expired, triggers interactive login |
| 404 Not Found         | Wrong site/page ID      | Verify IDs via list endpoints                                                    |
| 429 Too Many Requests | Rate limiting           | Respect `Retry-After` header, add delays between batch requests                  |
| Scope consent needed  | Missing API permissions | Re-run interactive auth to consent to `Notes.Read.All`                           |
