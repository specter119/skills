# Execution Notes

## Phase 1 · Scope
- Clarify only when multiple critical readings exist; keep the user interaction light and fact-based.
- Decompose the topic internally using the templates in `references/decomposition.md` (technology/comparison/concept/problem/trend).
- Brief: generate a short, focused plan listing the topic slug, subtopics, expected report location, and estimated duration.
- Structure: determine the output path and subdirectories before the autonomous research begins. Write a confirmation line such as:

```
Starting research on {topic}
Output directory: {output path}
Research directions:
1. [subtopic-1]
2. [subtopic-2]
...
Estimated [N] minutes, starting now...
```

### Directory logic
- **Scenario 1**: user does not specify a directory → default to `{cwd}/research/{topic-slug}/` with `_sources/`, per-subtopic `findings.md`, and `report.md`.
- **Scenario 2**: user provides an explicit directory string → insert `research/{topic-slug}` under it unless the user has a stronger preference.
- **Scenario 3**: when the user ties research to an existing docs project (e.g., "store in ./docs") → place results in `{project}/research/{topic-slug}/` and keep archival folder `sources/` (without underscore) to match project conventions.
- **Scenario 4**: research for slide/report projects located under `slides/` or `reports/` should land under `{project}/research/` with `sources/`, `notes/`, and `synthesis.md` to align with those projects.
- Always inform the user of the decided path; the internal subtopic structure and filenames are not surfaced for confirmation.

## Phase 2 · Research
- Supervisor picks the parallelization strategy:
  | Topic type | Strategy |
  |------------|----------|
  | Single focus | sequential search with iteration |
  | Multiple comparisons | one sub-agent per item |
  | Multi-faceted topic | parallel per dimension/subtopic |
  | Deep single topic | sequential with follow-up loops |
- Sub-agent pipeline:
  1. WebSearch / WebFetch to gather 2-4 queries.
  2. Fetch URLs, archive full text under `_sources/` (or `sources/` for slide/report projects).
  3. Attach metadata (URL, timestamp, source type) to each archive file.
  4. Write `findings.md` for each subtopic with bullet summaries and citations.
- Supervisor reviews coverage, spots gaps, and spawns follow-up tasks when a dimension lacks sources.
- All agents clean their findings (no raw scraped fragments) before returning, to keep the write pass focused on synthesis.

## Phase 3 · Write
- Copy `assets/report-en.md` or `assets/report-zh.md` into the chosen output path as `report.md`; fill the placeholders in a single pass.
- Summarize each dimension, flag gaps, and link to the archived sources. Use Markdown headings and bullet lists as shown in the templates.
- After writing, report completion to the user with the report path, number/location of sources, and 3 key findings.

## Error handling
| Error | Action |
|-------|--------|
| Sub-agent timeout | document partial results, highlight gaps in the brief/report, continue with fastest remaining sources |
| Search failure | attempt alternative queries or switch between WebSearch/WebFetch; note failed queries in `findings.md` |
| Fetch failure | fall back to Exa crawl when possible; log the failure and reason in the report |
| No sources | escalate to supervisor for clarification before proceeding |

## Best practices
- **Brief first**: the research brief guides decomposition and keeps the autonomous phase aligned with the user ask.
- **Archive everything**: store both summaries and original materials for traceability (raw + summary are not mutually exclusive).
- **Clean returns**: sub-agents should distill conclusions, not dump raw HTML.
- **Note gaps**: when claims are unsupported, mark them explicitly in `findings.md` and the final report.
- **State uncertainty**: flag any low-confidence section or missing evidence within the report.
- **Cycle through quality**: if coverage falls below ~70% for a dimension, add a follow-up search before writing.
