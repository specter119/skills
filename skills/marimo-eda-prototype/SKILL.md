---
name: marimo-eda-prototype
description: >
  Guides Codex to write marimo notebooks for EDA and prototype-first work with restrained UI,
  cohesive cells, clear variable scoping, and deliberate extraction into modules. Use when
  creating or editing exploratory marimo notebooks where analysis comes first and UI stays light.
allowed-tools: Read, Write, Edit, Bash
---

# Marimo EDA Prototype

## Boundary Snapshot
- Focus on prototype-focused EDA: static analysis cells first, UI only when it accelerates insight, and helper extraction once patterns stabilize.
- Avoid turning notebooks into scattered UI development or exposing temporary names beyond their local cells.
- See `references/boundary.md` for the guardrails, decision table, knowledge activation model, and self-check checklist.

## Execution Skeleton
1. Clarify the analysis job, signals worth surfacing, and hypotheses in the first few cells.
2. Load data and perform cleaning/transformation cells that can be read end-to-end.
3. Build the core EDA cells, keeping control, computation, and output close together.
4. Introduce interactive widgets only when they reduce iteration time; keep widget cells thin and co-located with their logic.
5. Once a pattern stabilizes or cross-notebook reuse appears, wire to helper modules instead of growing notebook-local UI.
6. Run optional checkers (`uvx marimo check`, `python scripts/marimo_lint.py ...`) if the notebook grows beyond a first pass, and review the self-check list in the boundary reference.

## Reference Map
- `references/boundary.md` – full boundary discussion, guardrails, decision table, sample rewrites, and optional checker guidance.
- `references/design-patterns.md` – curated design patterns and GitHub notebook examples that embody the target behavior.
- `references/eval-fixtures.md` – sample prompts for evaluating routing and execution quality.
