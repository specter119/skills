# Execution Cases

## Scenario 1: Create an Exploration Notebook from Scratch

- Input: dataset, analysis goal, minimal constraints
- Expected: start with raw rows / overview, low-assumption plots, and any needed progress-visible batch steps; add UI only if it clearly reduces analysis friction

## Scenario 2: Clean Up an Out-of-Control Notebook

- Input: existing marimo notebook with scattered UI and complex cell dependencies
- Expected: consolidate cell cohesion, reduce exposed names, propose module extraction recommendations

## Scenario 3: Decide Whether to Extract a Module

- Input: a repeated piece of UI / chart / helper logic
- Expected: give a clear verdict of "keep in the notebook" or "extract to a module"

## Scenario 4: Remove Result-First EDA Flow

- Input: a notebook where keep/drop decisions filter the visualization used to justify them
- Expected: show all eligible observations first, store the human decision as a static input after the visualization, and derive the final result downstream

## Scenario 5: Add Human Exploration Without Cross-Cell App State

- Input: an EDA notebook where the user needs to inspect subgroups interactively inside one diagnostic chart
- Expected: keep the interaction local and reversible; prefer chart-native inspection when it fits, and do not export `.value` state unless downstream computation truly needs it

## Scenario 6: Add First-Pass Data Understanding

- Input: a notebook that jumps directly from data loading to a selected model, interpretation, exclusion, or feature subset
- Expected: add raw rows / overview plus scatterplots, histograms, distributions, or box plots first; name visible patterns, turn them into hypotheses, then add focused validation cells

## Scenario 7: Fix Basic Marimo Graph Hygiene

- Input: an exploratory marimo notebook with repeated global names such as `df`, `chart`, or `result`, downstream reads of `_tmp`, or cyclic dependencies
- Expected: give stable cross-cell names only to values that must be reused, localize temporaries with `_` inside their defining cells, avoid duplicate exports, and preserve the EDA evidence chain

## Scenario 8: Fix Output Visibility Without Presentation Polish

- Input: one cell assigns markdown, table, and chart objects but only the last expression is visible
- Expected: choose one primary visible output, split unrelated diagnostics into adjacent cells, or compose one local diagnostic bundle only when the objects must be inspected together

## Scenario 9: Break Decision-Fed Diagnostics

- Input: a selected subset, widget `.value`, or static keep/drop decision feeds the chart used to justify that same decision
- Expected: move the broad diagnostic upstream of the decision, record the human decision after validation, and keep downstream results separate from the evidence chart

## Scenario 10: Resist Demo / Presentation Drift

- Input: an exploratory notebook has dashboard-like `mo.vstack` / `mo.hstack` panels, multiple widget sections, staged reveal, and explanatory copy before raw diagnostics
- Expected: restore EDA order with raw rows, distributions, scatterplots, and validation cells first; remove app-like polish; keep only minimal local reversible controls that improve inspection

## Scenario 11: Repair Tiny Marimo Semantics Regressions

- Input:

```python
# Cell A
chart = build_chart(df)
chart

# Cell B
chart = build_other_chart(df)
chart
```

- Expected: give each export a unique semantic name (for example `revenue_by_region_chart`), avoiding duplicate global `chart`; do not respond by prefixing the cells' domain data with `_`

- Input:

```python
# Cell A
slider = mo.ui.slider(0, 10)
mo.md(f"Selected: {slider.value}")
```

- Expected: display `slider` in Cell A and consume `slider.value` in an adjacent downstream cell

- Input:

```python
# Cell A
diagnostic_chart = build_chart(df)
```

- Expected: make `diagnostic_chart` the final expression so it renders; keep its semantic name

## Scenario 12: Choose Style Before Writing

- Input: "Write a marimo notebook for this sales dataset." No audience stated.
- Expected: state the style choice (EDA by default when exploring) in one sentence, or ask which style is wanted if the audience is unclear; do not blend discovery and communication

## Scenario 13: Write a Report Notebook from a Finished Analysis

- Input: recorded decisions, a derived result file, and a conclusion for a non-technical stakeholder
- Expected: conclusion-first summary on the first screen, one claim with one supporting chart per section, numbers in prose computed from the same cells as the charts, caveats near the claims, any controls placed inside the section they affect, code hidden, appendix linking to the EDA notebook

## Scenario 14: Convert an EDA Notebook into a Report

- Input: a long EDA notebook with raw-first ordering, many diagnostics, and a final decision
- Expected: produce a separate report notebook that loads decisions and the derived result, rebuilds only the charts the story needs with clear titles, and links back to EDA; do not paste diagnostic cells or add a toggle to the EDA notebook

## Scenario 15: Fix Exploration Drift in a Report

- Input: a report notebook that opens with `df.head()`, histograms of every column, and hypotheses before the conclusion
- Expected: move the conclusion and key numbers to the top, keep only evidence that supports a claim, move the rest to the appendix or the EDA notebook

## Scenario 16: Hand Live-Session Mechanics to marimo-pair

- Input: a request to add or edit cells in a running marimo session while following EDA story order
- Expected: use marimo-pair for discovery, `cm` edits, widget values, and packages; apply this skill only for story order, restraint, and cell purpose; do not edit the `.py` file directly during the live session

## Scenario 17: Keep Report Conclusions Stable

- Input: a report whose summary cell reads `threshold.value` and whose headline sentence changes as the slider moves
- Expected: compute the summary from fixed defaults (or label it "At the default threshold ..."), move every cell that reads the control below the control's display position, and let lint `control-upstream-impact` confirm it

## Scenario 18: Place a Control Inside Its Impact Zone

- Input: a report where a dropdown near the top filters a chart four sections later, with unrelated charts in between
- Expected: move the dropdown into the section of the chart it affects (or show it in the same `mo.hstack` as that chart), keep any narrative that interpolates its value inside the zone, and let lint `control-zone-gap` confirm it

## Scenario 19: Allow a Document-Wide Filter

- Input: a report with a date-range filter that every chart should respect
- Expected: put the filter near the top, label it as applying to the whole report, make sure every chart below depends on it, and do not report it as a zone violation

## Scenario 20: Coupled Controls in a Report

- Input: a report with a region dropdown whose options feed a second dropdown for stores, plus a chart that uses both
- Expected: place the dependent controls in adjacent cells, then the chart directly after, with narrative inside the zone; this is allowed in report style and is not an `ui-split-cells` hit
- Contrast: the same pattern in an EDA notebook should be checked for whether a simpler local lens would do

## Scenario 21: Deliver a Report with Controls as WASM

- Input: "Share this report as a self-contained HTML file; readers should still be able to change the filter."
- Expected: use `marimo export html-wasm --mode run --no-show-code` (served over HTTP, or `--single-file`), read data with `mo.notebook_location()` and `public/` (not bundled with `--single-file`), confirm packages exist in Pyodide, and run `marimo check --select MW`; use static `marimo export html` only when there are no controls

## Scenario 22: Do Not Hide Controls Behind Conditions

- Input: a notebook that wraps its widgets in `if not is_script_mode` or `mo.stop(...)`
- Expected: render every control unconditionally and only change the data source in script mode (marimo-notebook); this skill only decides whether the control should exist at all
