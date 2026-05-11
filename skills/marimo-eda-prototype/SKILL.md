---
name: marimo-eda-prototype
description: >
  Guides Codex to write marimo notebooks for EDA and prototype-first work with restrained UI,
  cohesive cells, clear variable scoping, and deliberate extraction into modules. Use when
  creating or editing exploratory marimo notebooks where analysis comes first and UI stays light.
allowed-tools: Read, Write, Edit, Bash
---

# Marimo EDA Prototype

Responsible for **prototype-first marimo notebooks**, not for turning notebooks into heavily interactive products.

## Routing Boundaries

### Should Route Here

- Create or modify marimo notebooks for EDA / prototype analysis
- Optimize notebook cell cohesion, interaction density, and module boundaries
- Determine whether a piece of notebook logic should be extracted to a helper / module

### Should Not Route Here

- Full frontend applications or long-term UI products
- General Python script development
- Pure API queries without notebook structure decisions

## Execution Skeleton

1. First confirm the notebook's primary task is still analysis, not UI orchestration.
2. Follow `references/workflow.md`: write the static analysis version first, then decide whether to add minimal interaction.
3. Use `references/boundary.md` and `references/design-patterns.md` to assess cell cohesion, graph hygiene, and extraction signals.
4. For technical checks, prefer running `uvx marimo check`; `scripts/marimo_lint.py` serves only as a weak-signal supplement.

## Reference Map

- `references/boundary.md`: boundaries, guardrails, decision table, examples
- `references/workflow.md`: default workflow, guardrails, pre-completion checklist
- `references/design-patterns.md`: high-value patterns and anti-patterns
- `references/eval-fixtures.md`: sample notebooks and evaluation materials
- `evals/trigger-cases.md`: minimal trigger examples
- `evals/execution-cases.md`: key execution scenarios
- `reports/optimization-notes.md`: current round refactoring decisions

## Output Contract

- Default output is an analysis-first, interaction-restrained, clearly structured marimo notebook
- If the notebook is evolving into an app, explicitly recommend extracting modules or transitioning to product code
