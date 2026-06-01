---
name: typst-authoring
description: >
  Provide Typst technical guidance for writing, compiling, and debugging Typst documents,
  including package selection and diagram solution choice. USE FOR: Typst syntax, compilation,
  debugging, Touying slide implementation, report typesetting, diagram rendering in Typst.
  DO NOT USE FOR: slide narrative/visual design, report content structure, illustration generation.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Typst Authoring

Responsible for **Typst's technical implementation layer**; does not handle content structure or narrative design.

## USE FOR

- Typst syntax, compilation, and debugging
- Technical implementation of Touying slides
- Report templates, typesetting, and export
- Selecting and implementing diagram solutions in Typst

## DO NOT USE FOR

- Narrative arc and visual direction of slides
- Argument structure and content framework of reports
- Illustration generation

## Execution Skeleton

1. Follow [workflow](references/workflow.md) through the diagnostics → compile → output check loop.
2. Then branch by document type: slides → [touying](references/touying.md), reports → [report](references/report.md), diagrams → [diagraph](references/diagraph.md).
3. When package versions are uncertain, consult the latest documentation; do not rely on hard-coded old version numbers.

## Reference Map

- [workflow](references/workflow.md)
- [touying](references/touying.md)
- [report](references/report.md)
- [diagraph](references/diagraph.md)
- [trigger-cases](evals/trigger-cases.md)
- [execution-cases](evals/execution-cases.md)
- [optimization-notes](reports/optimization-notes.md)

## Output Contract

- Default output: compilable Typst implementation or clear fix recommendations
- Attach relevant diagnostic/compile commands when necessary

## Collaboration and Handoff

- If the issue is actually narrative, structure, or visual direction, hand off to the appropriate content-design skill
