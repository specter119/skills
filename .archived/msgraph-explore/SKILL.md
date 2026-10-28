---
name: msgraph-explore
description: >
  Unified Microsoft Graph skill for SharePoint, OneDrive, and OneNote.
  USE FOR: search SharePoint or OneDrive content, fetch SharePoint files, sync drive folders,
  discover sites/notebooks/sections, sync OneNote pages to Markdown.
  DO NOT USE FOR: sending emails, managing calendars, modifying resources, Outlook operations,
  or any write/mutation operations on Microsoft Graph.
---

# Microsoft Graph Explore

**UTILITY SKILL** — retrieves data from Microsoft Graph (SharePoint, OneDrive, OneNote). Read-only; no write/mutation operations.

## Routing Boundaries

### Should Route Here

- Search SharePoint / OneDrive content via Graph Search API
- Fetch or sync SharePoint files, drive folders
- Discover sites, notebooks, sections, pages
- Sync OneNote wiki pages to local Markdown

### Should Not Route Here

- Sending emails or managing calendars
- Modifying / deleting any Microsoft Graph resources
- Outlook-specific operations

## Execution Skeleton

1. Ensure prerequisites are configured (see [setup](references/setup.md)).
2. Choose the right command by task type (see [commands](references/commands.md)).
3. Retrieve data; results are cached locally (see [architecture](references/architecture.md)).

## Reference Map

- [setup](references/setup.md) — Environment variables and permissions
- [commands](references/commands.md) — All CLI commands with examples
- [architecture](references/architecture.md) — Script layout and cache structure
