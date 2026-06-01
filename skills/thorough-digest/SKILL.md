---
name: thorough-digest
description: >
  Exhaustively review local materials with parallel sub-agents so no item is skipped. USE FOR:
  batch process local files, digest a folder, synthesize narrative from existing materials. DO NOT USE FOR:
  web research, single-document summaries, slide or report writing.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep
---

# Thorough Digest

Responsible for **exhaustive processing and parallel synthesis of local materials**; does not handle external web research.

## USE FOR

- Batch processing of local files, directories, sections, or material collections
- Item-by-item extraction of key points with no items allowed to be skipped
- Building a unified narrative or comprehensive report from existing materials

## DO NOT USE FOR

- Requires fetching new information from the web
- Only processing one or two documents
- The primary goal is writing slides or a formal report rather than first digesting materials

## Execution Skeleton

1. First inventory all input items to ensure the scope is clear.
2. Follow [workflow](references/workflow.md) to determine grouping and parallelization strategy.
3. Give each sub-agent an explicit item list, output path, and the constraint that no items may be skipped.
4. Aggregate findings from each group; if needed, chain an external research skill to fill gaps.

## Reference Map

- [workflow](references/workflow.md): phased workflow, grouping strategy, output structure
- [guidelines](references/guidelines.md): parallelization granularity, error handling, best practices
- [templates](references/templates.md): inventory / classify / sub-agent / synthesis templates
- [trigger-cases](evals/trigger-cases.md): minimal trigger examples
- [execution-cases](evals/execution-cases.md): key execution scenarios
- [optimization-notes](reports/optimization-notes.md): current refactor rationale

## Output Contract

- Default deliverables: inventory, grouping results, per-group findings, and final synthesis
- Must be able to report total input count, processed count, and coverage status

## Collaboration and Handoff

- If the synthesis phase reveals critical fact gaps, hand off to an external research skill
- If materials are fully digested and the next step is writing a formal deliverable, hand off to a writing or presentation-structure skill
