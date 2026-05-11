---
name: deep-research
description: >
  Investigate a topic through web search and multi-agent synthesis, archive the raw sources,
  and deliver a structured research report. Use when a user asks for "research", "investigate",
  "deep dive", "deep research", or similar requests that require multi-phase digging and
  documentation rather than a quick answer.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Deep Research

Responsible for **external information research, source archiving, and synthesis reporting**. Does not handle bulk digestion of local materials.

## Routing Boundaries

### Should Route Here

- User explicitly requests "research / investigate / deep dive"
- Requires multi-round search, source archiving, and structured synthesis
- Results need to form a traceable research directory and report

### Should Not Route Here

- Only needs a brief factual answer
- Summarizing a single document
- Primary task is processing locally available materials, not expanding external sources

## Execution Skeleton

1. First decompose the research question into dimensions and define the research directory and subtopics.
2. Multi-round search, fetch, and archive raw sources; then write subtopic findings.
3. Synthesize into a final `report.md`, explicitly marking sources and gaps.
4. Directory logic, error handling, and supervisor heuristics are in `references/execution.md`.

## Reference Map

- `references/decomposition.md`: Topic decomposition templates and dimension checklist
- `references/formats.md`: Sub-agent prompt, findings structure, and archival format
- `references/tools.md`: Tool selection for each research phase
- `references/examples.md`: End-to-end examples
- `references/execution.md`: Workflow, directory logic, error handling, and best practices
- `evals/trigger-cases.md`: Minimal trigger examples
- `evals/execution-cases.md`: Key execution scenarios
- `assets/report-en.md` / `assets/report-zh.md`: Final report templates

## Output Contract

- Default output includes the research directory, archived sources, per-subtopic findings, and a final report
- Key conclusions must be traceable to specific sources

## Collaboration and Handoff

- If long-form writing or presentation design is needed after external research is complete, hand off to the appropriate writing or presentation skill
