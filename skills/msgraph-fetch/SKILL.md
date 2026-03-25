---
name: Microsoft Graph Fetch
description: >
  Unified Microsoft Graph fetch skill for SharePoint, OneDrive, and OneNote.
  Supports SharePoint file fetch, drive folder sync, site discovery, notebook
  discovery, and OneNote sync to Markdown.
---

# Microsoft Graph Fetch

统一承接 Microsoft Graph 相关取数能力，覆盖：

- SharePoint file fetch
- OneDrive / SharePoint drive folder sync
- SharePoint site discovery
- OneNote notebook / section discovery
- OneNote sync to Markdown

当用户需要“拉 SharePoint 文件”、“同步 OneDrive 目录”、“列出 site/notebook/section”、“同步 OneNote wiki”时使用这个 skill。

## Prerequisites

### `.env`

将 `.env.example` 复制到你的项目目录或 skill 目录：

```bash
cp skills/msgraph-fetch/.env.example /path/to/project/.env
```

需要的环境变量：

| Variable | Description |
| --- | --- |
| `MICROSOFT_CLIENT_ID` | Azure AD app registration client ID |
| `MICROSOFT_AUTHORITY` | `https://login.microsoftonline.com/<tenant-id>` |
| `MICROSOFT_REFRESH_TOKEN` | 首次可留空，登录后会自动回写 |

### Permissions

建议同一个 delegated app registration 一次性配置：

- `Sites.Read.All`
- `Notes.Read.All`
- `Files.Read.All`

脚本会按命令申请最小 scope：

- OneNote 命令：`Sites.Read.All` + `Notes.Read.All`
- Drive 命令：`Sites.Read.All` + `Files.Read.All`

## CLI

完整实现见 `scripts/msgraph_fetch.py`。

### Fetch SharePoint File

```bash
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py fetch-file \
  --url "<sharepoint-url>"
```

可选：

```bash
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py fetch-file \
  --url "<sharepoint-url>" \
  --output-dir "./downloads"
```

不传 `--output-dir` 时，默认写到：

```plain
~/.cache/msgraph-fetch/materialized/files/
```

成功时 `stdout` 最后一行只输出最终本地绝对路径。

### Sync Drive Folder

```bash
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py sync-folder \
  --remote-path "ByProject/IACB/smart-invoice" \
  --output-dir "./data/smart-invoice"
```

可选定位参数：

- 默认 `me/drive`
- `--site-id`
- `--site-search`
- `--force`

### Discover Sites / Notebooks / Sections

```bash
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py list-sites "DevSecOps"
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py list-notebooks --site-id "<site-id>"
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py list-sections \
  --site-id "<site-id>" \
  --notebook-id "<notebook-id>"
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py list-pages \
  --site-id "<site-id>"
```

可选：

```bash
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py list-pages \
  --site-id "<site-id>" \
  --section-id "<section-id>"
```

### Fetch Single OneNote Page

```bash
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py fetch-onenote-page \
  --site-id "<site-id>" \
  --page-id "<page-id>"
```

命令会输出该页面的 Markdown 内容到 `stdout`。

### Fetch OneNote

```bash
uv run skills/msgraph-fetch/scripts/msgraph_fetch.py fetch-onenote \
  --site-id "<site-id>" \
  --output-dir "./wiki_cache"
```

可选参数：

- `--site-search`
- `--notebook-id`
- `--section-id`

语义：

- 不带额外参数时，抓取整个 site 下的 OneNote 内容
- 带 `--notebook-id` 时，抓取单个 notebook
- 带 `--section-id` 时，抓取单个 section
- 单页抓取不走这个命令，使用上面的 `fetch-onenote-page --page-id`

说明：

- `fetch-onenote` 是从 Graph 单向抓取到本地 Markdown

## Cache Layout

统一使用：

```plain
~/.cache/msgraph-fetch/
```

缓存按资源分层：

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

说明：

- `sources` 存远端原始内容
- `derived/onenote` 存 Markdown 派生结果
- `meta` 存 eTag、`lastModifiedDateTime`、缓存时间等元数据

OneNote 不只缓存 Markdown，也保留原始 HTML，便于后续重新渲染。
