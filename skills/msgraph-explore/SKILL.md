---
name: msgraph-explore
description: >
  Unified Microsoft Graph skill for SharePoint, OneDrive, and OneNote.
  Supports content search via Graph Search API, SharePoint file fetch,
  drive folder sync, site discovery, notebook discovery, and OneNote
  sync to Markdown.
---

# Microsoft Graph Explore

Unified entry point for Microsoft Graph data retrieval and search capabilities, covering:

- **Content search** via Graph Search API (SharePoint, OneDrive)
- SharePoint file fetch
- OneDrive / SharePoint drive folder sync
- SharePoint site discovery
- OneNote notebook / section discovery
- OneNote sync to Markdown

Use this skill when users need to "search SharePoint content", "search the internal wiki", "pull a SharePoint file", "sync an OneDrive directory", "list sites / notebooks / sections", or "sync the OneNote wiki".

## Architecture

```text
scripts/
  msgraph_auth.py    # Shared module: GraphClient, MSAL auth, constants
  msgraph_search.py  # PEP 723 script: Graph Search API search
  msgraph_fetch.py   # PEP 723 script: OneNote + Drive fetch/sync
```

## Prerequisites

### `.env`

Copy `.env.example` to your project directory or the skill directory:

```bash
cp skills/msgraph-explore/.env.example /path/to/project/.env
```

Required environment variables:

| Variable | Description |
| --- | --- |
| `MICROSOFT_CLIENT_ID` | Azure AD app registration client ID |
| `MICROSOFT_AUTHORITY` | `https://login.microsoftonline.com/<tenant-id>` |
| `MICROSOFT_REFRESH_TOKEN` | Can be left empty on first run; will be written back automatically after login |

### Permissions

Recommended to configure all at once on a single delegated app registration:

- `Sites.Read.All`
- `Notes.Read.All`
- `Files.Read.All`

Scripts request the minimum scope per command:

- Search commands: `Sites.Read.All` + `Files.Read.All`
- OneNote commands: `Sites.Read.All` + `Notes.Read.All`
- Drive commands: `Sites.Read.All` + `Files.Read.All`

## CLI

### Search Content (NEW)

Search for content in SharePoint and OneDrive:

```bash
uv run skills/msgraph-explore/scripts/msgraph_search.py "Fin skill design"
```

Optional parameters:

```bash
uv run skills/msgraph-explore/scripts/msgraph_search.py "Fin skill design" \
  --entity-types driveItem,listItem \
  --site-path "sites/IACB" \
  --max-results 10
```

Output JSON (with full resource objects for chaining):

```bash
uv run skills/msgraph-explore/scripts/msgraph_search.py "Fin skill design" --json
```

Parameter reference:

- `query`: search keyword, supports KQL syntax
- `--entity-types`: entity types to search (default `driveItem,listItem`; `site` also available)
- `--site-path`: KQL path scope (e.g., `"sites/IACB"`)
- `--max-results`: maximum number of results (default 25)
- `--json`: output JSON containing raw identifiers

**Note**: OneNote page search coverage depends on the Graph Search index state and is best-effort / discovery-only. For full OneNote content search, it is recommended to first run `fetch-onenote` to sync locally, then use grep.

### Fetch SharePoint File

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-file \
  --url "<sharepoint-url>"
```

Optional:

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-file \
  --url "<sharepoint-url>" \
  --output-dir "./downloads"
```

When `--output-dir` is not provided, the default write location is:

```plain
~/.cache/msgraph-explore/materialized/files/
```

On success, the last line of `stdout` outputs only the final local absolute path.

### Sync Drive Folder

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py sync-folder \
  --remote-path "ByProject/IACB/smart-invoice" \
  --output-dir "./data/smart-invoice"
```

Optional locating parameters:

- Default: `me/drive`
- `--site-id`
- `--site-search`
- `--force`

### Discover Sites / Notebooks / Sections

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-sites "DevSecOps"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-notebooks --site-id "<site-id>"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-sections \
  --site-id "<site-id>" \
  --notebook-id "<notebook-id>"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-pages \
  --site-id "<site-id>"
```

Optional:

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-pages \
  --site-id "<site-id>" \
  --section-id "<section-id>"
```

### Fetch Single OneNote Page

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-onenote-page \
  --site-id "<site-id>" \
  --page-id "<page-id>"
```

The command outputs the page's Markdown content to `stdout`.

### Fetch OneNote

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-onenote \
  --site-id "<site-id>" \
  --output-dir "./wiki_cache"
```

Optional parameters:

- `--site-search`
- `--notebook-id`
- `--section-id`

Semantics:

- Without extra parameters: fetches all OneNote content under the site
- With `--notebook-id`: fetches a single notebook
- With `--section-id`: fetches a single section
- Single-page fetch does not use this command; use `fetch-onenote-page --page-id` above

Notes:

- `fetch-onenote` is a one-way fetch from Graph to local Markdown

### CLI Entry Point

Use `scripts/msgraph_fetch.py` as the unified data retrieval entry point:

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-file --url "..."
```

## Cache Layout

Unified cache location:

```plain
~/.cache/msgraph-explore/
```

Cache layered by resource type:

```plain
sources/
  drive/
  onenote/
derived/
  onenote/
meta/
  drive/
  onenote/
```

Notes:

- `sources` stores raw remote content
- `derived/onenote` stores Markdown derived output
- `meta` stores eTag, `lastModifiedDateTime`, cache timestamps, and other metadata

OneNote caches not only Markdown but also the original HTML, enabling re-rendering later.
