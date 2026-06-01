# Architecture and Cache

## Script Layout

```text
scripts/
  msgraph_auth.py    # Shared module: GraphClient, MSAL auth, constants
  msgraph_search.py   # PEP 723 script: Graph Search API search
  msgraph_fetch.py    # PEP 723 script: OneNote + Drive fetch/sync
```

Use `scripts/msgraph_fetch.py` as the unified data retrieval entry point:

```bash
uv run skills/msgraph-explore/scripts/msgraph_fetch.py fetch-file --url "..."
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

- `sources/` — raw remote content
- `derived/onenote/` — Markdown derived output
- `meta/` — eTag, `lastModifiedDateTime`, cache timestamps, and other metadata

OneNote caches both Markdown and original HTML, enabling re-rendering later.
