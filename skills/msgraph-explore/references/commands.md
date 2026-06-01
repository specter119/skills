# Commands

All commands use `uv run` with PEP 723 inline script metadata.

## Search Content

```bash
uv run skills/msgraph-explore/scripts/msgraph_search.py "Fin skill design"
```

Optional parameters:

```bash
uv run skills/msgraph-explore/scripts/msgraph_search.py "Fin skill design" \
  --entity-types driveItem,listItem \
  --site-path "sites/IACB" \
  --max-results 10 \
  --json
```

| Parameter | Description |
| --- | --- |
| `query` | Search keyword, supports KQL syntax |
| `--entity-types` | Entity types to search (default `driveItem,listItem`; `site` also available) |
| `--site-path` | KQL path scope (e.g., `"sites/IACB"`) |
| `--max-results` | Maximum results (default 25) |
| `--json` | Output JSON with raw identifiers for chaining |

> **Note:** OneNote page search coverage depends on the Graph Search index state and is best-effort / discovery-only. For full OneNote content search, first run `fetch-onenote` to sync locally, then use grep.

## Fetch SharePoint File

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-file \
  --url "<sharepoint-url>"
```

Optional: `--output-dir "./downloads"` (default: `~/.cache/msgraph-explore/materialized/files/`). On success, the last line of stdout is the local absolute path.

## Sync Drive Folder

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py sync-folder \
  --remote-path "ByProject/IACB/smart-invoice" \
  --output-dir "./data/smart-invoice"
```

Optional: `--site-id`, `--site-search`, `--force`. Default drive: `me/drive`.

## Discover Sites / Notebooks / Sections

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-sites "DevSecOps"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-notebooks --site-id "<site-id>"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-sections \
  --site-id "<site-id>" --notebook-id "<notebook-id>"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-pages --site-id "<site-id>"
```

For `list-pages`, optional: `--section-id "<section-id>"`.

## Fetch Single OneNote Page

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-onenote-page \
  --site-id "<site-id>" --page-id "<page-id>"
```

Outputs Markdown to stdout.

## Fetch OneNote

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-onenote \
  --site-id "<site-id>" --output-dir "./wiki_cache"
```

Optional: `--site-search`, `--notebook-id`, `--section-id`.

- Without extra params: fetches all OneNote content under the site
- With `--notebook-id`: fetches a single notebook
- With `--section-id`: fetches a single section
- For single-page fetch, use `fetch-onenote-page` instead

`fetch-onenote` is a one-way fetch from Graph to local Markdown.
