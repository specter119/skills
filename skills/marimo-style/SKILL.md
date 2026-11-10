---
name: marimo-style
description: >-
  Shape marimo notebooks for their purpose: a discovery-first EDA notebook or a conclusion-first
  report notebook (dynamic HTML for stakeholders). Decides story order, how many controls and
  where, layout, and code visibility. Pairs with marimo-pair (live kernel) and the official
  marimo-notebook (file format and API).
  USE FOR: choosing EDA vs report, structuring cell order, separating evidence from decisions,
  keeping a report's conclusions stable while controls change, placing controls next to what they
  affect, converting EDA into a report, fixing presentation drift in EDA.
  DO NOT USE FOR: code formatting (ruff, PEP 8), driving a running marimo session (marimo-pair),
  marimo file format or API questions (marimo-notebook), full frontend apps.
---

# Marimo Style

This skill decides **what a notebook should look like for its purpose**. It does not decide how to operate marimo or how to write valid marimo code.

## Division of Labor

| Skill                                                                                     | Owns                                                                                                                    |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [marimo-pair](https://github.com/marimo-team/marimo-pair)                                 | A live kernel: running code, editing cells through `cm`, setting widget values, packages, cell boundaries by rerun cost |
| [marimo-notebook](https://github.com/marimo-team/skills/tree/main/skills/marimo-notebook) | The `.py` format, `@app.cell`, API usage, script mode, exports, tests, `marimo check`                                   |
| **marimo-style** (this)                                                                   | Story order, control placement, layout, code visibility, EDA vs report guardrails                                       |

Do not repeat or contradict the other two. Where this skill and an official skill touch the same rule, the split is:

- This skill decides **whether a control should exist and where it goes**. Once a control exists, render it unconditionally; never hide it behind `if` or `mo.stop`. That matches marimo-notebook's "show all UI elements always".
- Never edit the `.py` file during a live session (marimo-pair). Use `cm`.

If the other skills are not installed, this skill still works on its own: write the file and run `uvx marimo check notebook.py`.

## Choose a Style First

Decide before writing any cell. If the request is ambiguous, ask which one is wanted.

| Question     | EDA notebook                                                    | Report notebook                                                                         |
| ------------ | --------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Reader       | The analyst, and future analysts auditing the path              | A stakeholder who did not do the analysis                                               |
| Job          | Find out what the data says                                     | Communicate what is already known                                                       |
| Story order  | Evidence, pattern, hypothesis, validation, decision, result     | Conclusion, supporting evidence, caveats, appendix                                      |
| Conclusion   | Last, recorded as an explicit decision                          | First, and stable (does not change when a control moves)                                |
| Interaction  | Low state: reversible local lenses, plain code and charts first | Coupled controls allowed, but each control's effect is a contiguous zone right after it |
| Layout       | Adjacent cells, little composition                              | Composition allowed: callouts, tabs, accordions, side by side                           |
| Code         | Visible; it is part of the record                               | Hidden; narrative leads                                                                 |
| Delivery     | `marimo edit`                                                   | Dynamic HTML: `marimo run`, `marimo export html-wasm --mode run`, or molab              |
| Failure mode | Presentation drift: charts picked to fit a conclusion           | Exploration drift, or a control that changes something far away                         |

Defaults when unstated: exploring data means EDA; "share", "present", "stakeholder", "summary for others" means report.

A finished EDA usually feeds a report. Keep them as **two notebooks**, not one notebook with a toggle. See [report-style](references/report-style.md#handoff-from-eda).

## Shared Principles

1. **One notebook, one job.** Do not blend discovery and communication.
1. **Every control must earn its place.** Plain code and charts first; add a control only when it clearly helps the reader or analyst. How far controls may reach differs by style.
1. **Conclusions do not depend on the evidence they are judged by.** EDA: a decision is never an ancestor of the chart that justifies it. Report: the summary and claim headings never change when a control moves.
1. **One primary visible output per cell.** Only the final expression renders; assignment alone shows nothing. Split unrelated outputs into adjacent cells.
1. **Name exports for what they are.** Prefer unique semantic names (`churn_by_tenure`, not `result`), even when nothing reads them yet, so they stay inspectable in a live session. Use an `_` prefix only for throwaway values such as `_fig`, `_ax`, loop variables. Do not prefix whole cells or domain data to shrink the export surface.
1. **Extract late.** Repeated or reused logic becomes a helper or module once the pattern is stable.
1. **Say when the notebook has outgrown its role.** If it is turning into an app, recommend extracting modules or writing a real app.

## Graph Rules Worth Checking

marimo-pair and marimo-notebook own the contract. These are the ones that decide whether the *story* survives:

- Read dependencies in the graph, not file order. Order on screen can hide an ancestor.
- Break a cycle by merging tightly coupled work, renaming exports, or extracting a helper.
- Display a widget where it is defined (or in a layout next to its output) and read `.value` in a different cell.
- Run `uvx marimo check notebook.py` before finishing. Details: [marimo docs](https://docs.marimo.io/faq).

## Workflow

1. Pick the style (table above) and say which one and why in one sentence.
1. Read the matching reference:
   - EDA: [eda-style](references/eda-style.md)
   - Report: [report-style](references/report-style.md)
1. Write or review the notebook. In a live session, hand mechanics to marimo-pair.
1. Optionally run the structure linter: `python scripts/marimo_lint.py notebook.py --style eda|report`. It is a heuristic "worth a second look" check, not a gate. Without `--style` it runs only the shared rules.
1. Run the style's checklist and `uvx marimo check`.

## Reference Map

Normal execution:

- [eda-style](references/eda-style.md): EDA story order, guardrails, graph rules, checklist
- [report-style](references/report-style.md): report structure, conclusion stability, control zones, delivery, EDA handoff, checklist

Rationale and maintenance (not normal execution context):

- [design-patterns](references/design-patterns.md): patterns from real notebooks
- [eval-fixtures](references/eval-fixtures.md): lint regression samples and expected hits
- [trigger-cases](evals/trigger-cases.md), [execution-cases](evals/execution-cases.md): evaluation cases
- [optimization-notes](reports/optimization-notes.md): change history

## Output Contract

- State the chosen style.
- EDA: an evidence-before-decision, interaction-restrained notebook; raw evidence and patterns before conclusions.
- Report: a conclusion-first notebook with stable conclusions, each claim next to its evidence, code hidden, every control directly above the zone it affects, delivered as dynamic HTML.
- Delegate live-session mechanics to marimo-pair and file-format questions to marimo-notebook.
