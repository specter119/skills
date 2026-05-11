---
name: typst-authoring
description: >
  Provide Typst technical guidance for writing, compiling, and debugging Typst documents,
  including package selection and diagram solution choice. Use when the task is Typst syntax,
  toolchain usage, Touying/report implementation, or diagram rendering inside Typst.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Typst Authoring

Responsible for **Typst's technical implementation layer**; does not handle content structure or narrative design.

## Routing Boundaries

### Should Route Here

- Typst syntax, compilation, and debugging
- Technical implementation of Touying slides
- Report templates, typesetting, and export
- Selecting and implementing diagram solutions in Typst

### Should Not Route Here

- Narrative arc and visual direction of slides
- Argument structure and content framework of reports
- Illustration generation

## Execution Skeleton

1. Follow `references/workflow.md` through the diagnostics → compile → output check loop.
2. Then branch by document type: slides → `references/touying.md`, reports → `references/report.md`, diagrams → `references/diagraph.md`.
3. When package versions are uncertain, consult the latest documentation; do not rely on hard-coded old version numbers.

## Reference Map

- `references/workflow.md`
- `references/touying.md`
- `references/report.md`
- `references/diagraph.md`
- `evals/trigger-cases.md`
- `evals/execution-cases.md`
- `reports/optimization-notes.md`

## Output Contract

- Default output: compilable Typst implementation or clear fix recommendations
- Attach relevant diagnostic/compile commands when necessary

## Collaboration and Handoff

- If the issue is actually narrative, structure, or visual direction, hand off to the appropriate content-design skill
