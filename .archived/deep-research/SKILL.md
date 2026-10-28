---
name: deep-research
description: >
  Investigate a topic through web search and multi-agent synthesis, archive raw sources, and
  deliver a structured research report. USE FOR: "research", "investigate", "deep dive", DO NOT USE FOR: brief factual answers, single-document
  summaries, processing local materials.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Deep Research

Responsible for **external information research, source archiving, and synthesis reporting**. Does not handle bulk digestion of local materials.

## USE FOR

- User explicitly requests "research / investigate / deep dive"
- Requires multi-round search, source archiving, and structured synthesis
- Results need to form a traceable research directory and report

## DO NOT USE FOR

- Only needs a brief factual answer
- Summarizing a single document
- Primary task is processing locally available materials, not expanding external sources

## Execution Skeleton

1. Decompose the research question into dimensions; define the research directory and subtopics.
2. Multi-round search, fetch, and archive raw sources; then write subtopic findings.
3. Synthesize into a final `report.md`, marking sources and gaps.
4. Directory logic, error handling, and supervisor heuristics are in [execution](references/execution.md).

## Reference Map

- [decomposition](references/decomposition.md): Topic decomposition templates and dimension checklist
- [formats](references/formats.md): Sub-agent prompt, findings structure, and archival format
- [tools](references/tools.md): Tool selection for each research phase
- [examples](references/examples.md): End-to-end examples
- [execution](references/execution.md): Workflow, directory logic, error handling, and best practices
- [trigger-cases](evals/trigger-cases.md): Minimal trigger examples
- [execution-cases](evals/execution-cases.md): Key execution scenarios
- [report-en](references/report-en.md) / [report-zh](references/report-zh.md): Final report templates

## Output Contract

- Default output includes research directory, archived sources, per-subtopic findings, and a final report
- Key conclusions must be traceable to specific sources

## Collaboration and Handoff

- If long-form writing or presentation design is needed after research, hand off to the appropriate skill
