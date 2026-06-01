---
name: marimo-eda-prototype
description: >
  Guides Codex to write marimo notebooks for EDA and prototype-first work with restrained UI,
  cohesive cells, and deliberate extraction into modules. USE FOR: creating/editing exploratory
  marimo notebooks, optimizing cell cohesion, extracting logic to modules. DO NOT USE FOR:
  full frontend apps, general Python scripts, pure API queries without notebook structure decisions.
allowed-tools: Read, Write, Edit, Bash
---

# Marimo EDA Prototype

Responsible for **prototype-first marimo notebooks**, not turning notebooks into interactive products.

## USE FOR

- Create or modify marimo notebooks for EDA / prototype analysis
- Optimize notebook cell cohesion, interaction density, and module boundaries
- Determine whether a piece of notebook logic should be extracted to a helper / module

## DO NOT USE FOR

- Full frontend applications or long-term UI products
- General Python script development
- Pure API queries without notebook structure decisions

## Execution Skeleton

1. First confirm the notebook's primary task is still analysis, not UI orchestration.
2. Follow [workflow](references/workflow.md): write the static analysis version first, then decide whether to add minimal interaction.
3. Use [boundary](references/boundary.md) and [design-patterns](references/design-patterns.md) to assess cell cohesion, graph hygiene, and extraction signals.
4. For technical checks, prefer running `uvx marimo check`; [eval-fixtures](references/eval-fixtures.md) serves as sample notebooks for evaluation.

## Reference Map

- [boundary](references/boundary.md): boundaries, guardrails, decision table, examples
- [workflow](references/workflow.md): default workflow, guardrails, pre-completion checklist
- [design-patterns](references/design-patterns.md): high-value patterns and anti-patterns
- [eval-fixtures](references/eval-fixtures.md): sample notebooks and evaluation materials
- [trigger-cases](evals/trigger-cases.md): minimal trigger examples
- [execution-cases](evals/execution-cases.md): key execution scenarios
- [optimization-notes](reports/optimization-notes.md): current round refactoring decisions

## Output Contract

- Default output is an analysis-first, interaction-restrained, clearly structured marimo notebook
- If the notebook is evolving into an app, explicitly recommend extracting modules or transitioning to product code
