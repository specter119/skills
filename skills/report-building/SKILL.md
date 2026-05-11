---
name: report-building
description: >
  Structures and organizes reports, papers, theses, and documentation.
  Use when asked to create report/paper/thesis/documentation.
  Supports Markdown and Typst output.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Report Building

Handles **long-form structured writing**; does not handle presentation structure design or pure Typst implementation.

## Routing Boundaries

### Route Here

- Long-form writing: reports, papers, technical documentation, business proposals, case studies
- Tasks that require establishing a logical framework first, then developing the argument

### Do Not Route Here

- Short messages or summary-level copy
- Slide or presentation structure design
- Pure Typst implementation issues

## Execution Skeleton

1. Clarify the writing goal, audience, and purpose; select a matching framework from `references/framework-selection.md`.
2. Design the outline per `references/workflow.md`; mark core arguments, key evidence, and action items.
3. Write content section by section, continuously self-checking with MECE, So What, and data-backed principles.
4. When needed, delegate to `@oracle` to review the outline and draft from a reader's perspective.
5. Hand off to the Typst implementation skill for formal typesetting or export.

## Reference Map

- `references/framework-selection.md`
- `references/workflow.md`
- `references/oracle-delegation.md`
- `evals/trigger-cases.md`
- `evals/execution-cases.md`
- `reports/optimization-notes.md`

## Output Contract

- Default output is a clear report skeleton, argument chain, and body text suited to the target medium
- If entering the typesetting phase, hand off to the implementation skill

## Collaboration and Handoff

- When facts or data are needed, call a research skill first
- When also building presentation content, hand off to a presentation structure design skill
