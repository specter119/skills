# Setup and CLI

## Environment Setup

```bash
cp skills/msgraph-explore/.env.example /path/to/project/.env
```

Required environment variables:

| Variable | Description |
| --- | --- |
| `MICROSOFT_CLIENT_ID` | Azure AD app registration client ID |
| `MICROSOFT_AUTHORITY` | `https://login.microsoftonline.com/<tenant-id>` |
| `MICROSOFT_REFRESH_TOKEN` | Can be left empty on first run; will be written back automatically after login |

## Permissions

Recommended to configure all at once on a single delegated app registration:

- `Sites.Read.All`
- `Notes.Read.All`
- `Files.Read.All`

Scripts request the minimum scope per command:

- OneNote: `Sites.Read.All` + `Notes.Read.All`
- Drive: `Sites.Read.All` + `Files.Read.All`

## Common Commands

### Search Content

```bash
uv run skills/msgraph-explore/scripts/msgraph_search.py "Fin skill design"
```

Optional:

```bash
uv run skills/msgraph-explore/scripts/msgraph_search.py "Fin skill design" \
  --entity-types driveItem,listItem \
  --site-path "sites/IACB" \
  --max-results 10 \
  --json
```

### Fetch SharePoint File

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-file \
  --url "<sharepoint-url>"
```

### Sync Drive Folder

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py sync-folder \
  --remote-path "ByProject/IACB/smart-invoice" \
  --output-dir "./data/smart-invoice"
```

### Discover Sites / Notebooks / Sections

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-sites "DevSecOps"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-notebooks --site-id "<site-id>"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-sections \
  --site-id "<site-id>" \
  --notebook-id "<notebook-id>"
uv run skills/msgraph-explore/scripts/msgraph_fetch.py list-pages --site-id "<site-id>"
```

### Fetch Single OneNote Page

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-onenote-page \
  --site-id "<site-id>" \
  --page-id "<page-id>"
```

### Fetch OneNote

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-onenote \
  --site-id "<site-id>" \
  --output-dir "./wiki_cache"
```

## Cache Layout

```plain
~/.cache/msgraph-explore/
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
- `meta` stores eTag, cache timestamps, and other metadata
