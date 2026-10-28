# EDA Style

EDA notebooks are discovery logic, not presentation logic. They record how knowledge was earned. Keep them analysis-first; do not turn them into interactive products.

Live-session mechanics belong to marimo-pair, and file-format questions to marimo-notebook. This file covers shape and restraint. For a stakeholder-facing document, use [report-style](report-style.md) instead.

## Story Order

For each exploration loop, preserve this order in both the rendered notebook and the dependency graph:

`raw evidence -> low-assumption visualization -> pattern or stated prior question -> hypothesis / candidate interpretation -> validation -> explicit decision -> derived result`

1. Define the observation set and label any a priori constraints.
1. Show raw rows or a compact overview (schema, missingness) before deriving anything.
1. Add low-assumption diagnostics: scatterplots for relationships, histograms for distributions, box plots for group spread and outliers.
1. Name the visible pattern or anomaly before interpreting it.
1. Turn it into a question, hypothesis, or candidate interpretation.
1. Render the focused validation view for that question, not conditioned on the eventual decision.
1. Record the adopted decision as an explicit static input.
1. Derive and display the selected result after the decision.

A priori scientific or data-quality constraints may define the evidence universe up front only when they are clearly labeled and were not tuned from the same displayed outcome.

Computation may happen earlier for technical reasons, but the rendered notebook and reactive dependencies must not leak a later decision into its own evidence.

## Guardrails

### 1. Keep Evidence Upstream of Decisions

- A chart used to justify a decision must not depend on that decision.
- Do not remove selected-out observations from the chart used to justify removing them.
- Plot all eligible candidates before keep/drop/rank choices, then record the exclusions.
- Store human-reviewed choices in a plain static variable after the diagnostics. Export it under a unique name only when downstream cells need it.
- Do not rewrite an EDA notebook into presentation order where the final decision silently selects which evidence is shown.
- Check this on the **graph**, not on file order. A decision variable, widget `.value`, selected subset, or filtered result must not be an ancestor of the diagnostic that justifies it. Lint: `control-upstream-impact`.

### 2. Keep Reversible Exploration Out of the Reactive Graph

- If a human is only changing the viewing lens (a subgroup, a zoom), keep the control local to the diagnostic. Chart-native selection (for example Altair) often fits, but the principle is low state, not a specific library.
- Do not export `.value` into downstream cells unless later computation genuinely depends on it. Treat reversible filtering as a lens, not a recorded decision.
- High human participation is fine when it stays in reversible diagnostics.

### 3. Controls Are an Escalation

Plain code, plots, and batch steps with visible progress are usually enough. Add `mo.ui` only when it clearly reduces analysis friction, and then:

- keep the control, its derived result, and its output adjacent; display the widget where it is defined and read `.value` in the adjacent downstream cell. Lint: `ui-far-consumer`
- do not split one exploration action across several cells that only define widgets. Lint: `ui-split-cells` (a control whose options depend on another control's `.value` is exempt, because marimo forces that chain into consecutive cells)
- always render a control that exists; never hide it behind `if` or `mo.stop` (this also matches marimo-notebook)

### 4. Do Not Let the Notebook Become UI Development

Warning signs:

- widgets added to look interactive, not to reduce analysis friction
- `mo.vstack` / `mo.hstack` dashboard panels, staged reveal, or long explanatory copy before the raw rows
- a widget defined at the top and consumed far below
- several `mo.state` or dynamic-UI pieces coordinating together

Prefer a boring, inspectable notebook over a polished demo. If the notebook is turning into a report, switch to [report-style](report-style.md). If it is turning into an app, extract modules or write an app.

### 5. Name Exports for What They Are

- Give each cell's primary result a unique semantic name (`score_distribution_chart`, not `chart`), even before anything reads it. EDA often needs to look back at intermediate values, and `_`-prefixed names disappear from the variable panel and from a live session.
- Use `_` only for throwaway values (`_fig`, `_ax`, loop variables).
- If a cell exports many names, rename them or split the cell. Do not add underscores to shrink the surface. Lint: `export-surface`.
- Do not define the same public name in two cells.

### 6. Extract When a Signal Is Real

Mark logic as an extraction candidate when the same filter, aggregation, or chart skeleton repeats, or when a clear input/output boundary has formed. Extract only after the pattern is visible. Terminal scripts or persisted stage files are justified only by compute scale or provenance, not by default.

## Decision Table

| Situation | Prefer | Avoid |
| --- | --- | --- |
| EDA story flow | Evidence, pattern, hypothesis, validation, decision, result | Conclusion, cherry-picked chart, justification |
| First-pass data understanding | Raw rows, histogram, scatter, box plot | Jumping to a selected feature set |
| Feature or outlier review | Plot all eligible candidates, then record exclusions | Plotting only the already-kept result |
| Reversible subgroup inspection | Small local control, often chart-native | `mo.ui.dropdown(...).value` feeding distant cells |
| One-off analysis, fixed parameters | Plain variables and direct computation | Sliders and dropdowns first |
| Long-running step | Batch computation with visible progress | Cross-cell UI orchestration around the run |
| Trying several parameters | Minimal control next to the analysis cell | Controls defined far from their consumer |
| Related diagnostics | Adjacent cells | App-like panels |
| Filter or plot logic repeats | Extract a helper | Copying similar cells |
| Cell exports `chart` / `result` | Semantic name | An underscore prefix to hide it |

## Good and Bad Examples

Good: the decision follows the diagnostic and feeds only the derived result.

```python
# After reviewing the score distribution above.
selected_score_rule = "score >= 50"
selected_rows = df.filter(pl.col("score") >= 50)
```

Bad: a selector filters the evidence it is supposed to be judged by.

```python
source_selector = mo.ui.dropdown(["all", "vendor_a", "vendor_b"], value="vendor_a")
source_selector
```

```python
# This chart justifies the choice of source, but is already filtered by it.
_filtered = df[df["source"] == source_selector.value]
source_diagnostic_chart = draw_chart(_filtered)
source_diagnostic_chart
```

## Writing Rhythm

1. Imports and simple configuration
1. Data loading
1. Cleaning and transformation
1. EDA cells, in story order
1. Optional interaction, only with an analytic reason
1. Summary and next steps

This is a rhythm, not a template. The analysis thread matters more than the order of sections.

## Checking

```bash
uvx marimo check notebook.py
python scripts/marimo_lint.py notebook.py --style eda
```

The linter is heuristic. `--style eda` runs the shared rules (`ui-split-cells`, `export-surface`, `oversized-cell`, `repeated-pattern`, `control-upstream-impact`) plus `ui-far-consumer`.

## Checklist

- Is the notebook's primary job still analysis?
- Can every decision be traced to an earlier unconditioned diagnostic?
- Does the notebook build data intuition before testing hypotheses?
- Is any chart filtered by the decision it is meant to justify (check the graph)?
- Are reversible controls kept inside diagnostic views rather than exported as decisions?
- Would removing half the controls make things clearer?
- Is each exploration action concentrated in one cell or a few adjacent cells?
- Does each cell have one intended visible output, with semantic names for what it exports?
- Is there logic better off in a module?
- Did `uvx marimo check notebook.py` pass (or marimo-pair report no structural error)?
