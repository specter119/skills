# Marimo Notebook Design Patterns

This document captures design patterns from the current sample pool that are worth absorbing into the skill.

Role: this is evidence and rationale for the **EDA style**, not the primary execution checklist. Use `eda-style.md` for action order, guardrails, and graph rules, and `report-style.md` for report notebooks, which have different rules about controls and layout. Live-session mechanics belong to marimo-pair; file format and API belong to marimo-notebook.

The goal is not to enumerate APIs, but to answer:

- What notebook structure fits the EDA style better
- Which patterns indicate the notebook is still within "exploration space"
- Which patterns indicate it is time to extract a helper or module

## 1. Build Data Intuition Before Testing Hypotheses

### Pattern

Start EDA with low-assumption views before narrow analysis:

1. Show raw rows or a compact schema / missingness overview
1. Plot distributions with histograms, density-like summaries, or box plots
1. Plot relationships with scatterplots or small multiples
1. Name the visible pattern, anomaly, cluster, gap, skew, or outlier
1. Turn that observation into a question, hypothesis, or candidate interpretation
1. Add focused validation analysis only after the hypothesis is explicit

### Why it works

- Early charts teach the analyst what the data can plausibly support
- Hypotheses are either generated from observed structure or explicitly labeled as prior questions
- Later validation cells have a clear reason to exist

### Example

Source:

- `fsw_unified_desp/00_data_eval.py`

It starts from loaded rows, then shows a target distribution and process-window scatter before adding a richer chart-native view. The interaction helps inspect patterns in the raw process space; it does not begin with a fixed feature decision.

### Skill implication

When creating an EDA notebook, do not jump straight from `load_data()` to a selected model, exclusion, interpretation, or subset. First add enough low-assumption plots for the analyst to form initial data intuition.

## 2. Keep EDA Story Logic Discovery-First

### Pattern

EDA notebooks should preserve the order in which knowledge is earned:

1. Raw rows or compact overview
1. Unconditioned distribution / scatter / diagnostic
1. Visible pattern noticed by the analyst
1. Explicit question, hypothesis, or candidate interpretation
1. Focused validation
1. Explicit decision
1. Derived result or downstream selection

### Why it works

- The reader can see what was knowable before the decision
- Human judgment is anchored in visible patterns, not hidden assumptions
- The notebook remains an exploration record instead of a retrospective slide deck

### Contrast

Presentation logic can start with a conclusion and select charts to explain it. That is legitimate
for reporting, but it is the wrong default for EDA because it hides the discovery path and makes
the decision look inevitable.

### Skill implication

When refactoring a notebook, preserve the cells that show raw evidence and unconditioned patterns
before any keep/drop/filter/ranking decision. Do not move the chosen result above the diagnostic
just because it reads more cleanly as a report.

## 3. Separate Observation From Decision

### Pattern

Close each EDA loop in this order:

1. Build the complete relevant observation set
1. Render the diagnostic visualization
1. Record the human decision explicitly
1. Derive and display the selected result

### Why it works

- The visualization can reveal unexpected patterns instead of confirming a preset result
- Readers can audit what evidence was available when the decision was made
- Changing a static decision does not rewrite its own supporting evidence

### Counterexample

A feature-selection decision removes highly correlated variables before the correlation heatmap is
built. The heatmap then cannot show the pattern used to justify those removals.

### Skill implication

Inspect both source order and reactive dependencies. A later chart must not consume the keep/drop
result when that chart is the evidence for the same keep/drop decision.

## 4. Prefer Low-State Controls for Reversible Exploration

### Pattern

When human participation is about changing the view, keep the control local and reversible instead of exporting widget state:

1. Show a raw sample or baseline chart first
1. Build the interactive diagnostic in one local cell
1. Prefer chart-native selection for in-chart subgroup inspection when it fits
1. Avoid feeding that selection into downstream cells unless it becomes an explicit decision

### Why it works

- Humans can inspect the evidence deeply without turning the notebook into a stateful app
- The selection remains reversible and auditable as a viewing lens
- The marimo dependency graph stays focused on data and primary results

### Example

Source:

- `fsw_unified_desp/00_data_eval.py`

This notebook first shows loaded rows and unconditional charts, then embeds an alloy selector directly in a chart diagnostic. The selected alloy changes the view but is not exported as notebook state or used as a downstream decision.

### Skill implication

Do not equate "human participates a lot" with "add marimo UI". If the interaction is only a visual lens, prefer chart-local interaction. Use `mo.ui` only when it clearly lowers analysis friction; display the widget near the analysis and consume `.value` in the adjacent downstream cell.

The same applies to display composition: `mo.vstack` / `mo.hstack` can keep a local diagnostic bundle together, but using them as default layout polish pushes EDA toward an app-like presentation.

## 5. Name Stable Seams When They Emerge

### Pattern

Once an exploratory pattern has stabilized, give it a stable helper name and compose it in subsequent cells:

- `load_*`
- `build_*`
- `show_*`
- `annotate_*`

### Why it works

- The notebook's main thread stays clear after the exploratory shape is known
- Users know where to make changes to adapt to their own data
- Subsequent interaction and display do not swallow the analysis logic

### Example

Source:

- `explore_high_dimensional_data.py`

This notebook first defines:

- `load_data`
- `embed_data`
- `scatter_data`
- `show_selection`

Only then does it wire together embedding, chart, and selection drill-down.

### Skill implication

Do not start EDA by inventing helpers for guesses that have not survived first-pass inspection. Once the data source, chart skeleton, embedding algorithm, or display style is repeated or clearly stable, name that seam and keep orchestration cells thin.

## 6. Keep UI Cells Thin

### Pattern

A UI cell is primarily responsible for:

- Generating widgets
- Displaying widgets or a single local bundle
- Keeping widget `.value` consumption in an adjacent downstream analysis cell

Do not pack large amounts of data cleaning, filtering, or state synchronization into the same UI cell.

### Why it works

- The boundary between control and analysis is clear
- UI updates are easier to trace
- The notebook is less likely to grow into a notebook-local component
- Marimo's rule that widgets are defined in one cell and `.value` is consumed downstream stays visible

### Example

Source:

- `explore_high_dimensional_data.py`

`mo.ui.altair_chart(...)` and `mo.ui.table(...)` each play only a thin adapter role.

### Counterexample

Source:

- `laurium-prompt_engineering.py`

Multiple cells simultaneously handle:

- Configuring UI
- Staged reveal
- Explanatory copy
- Parameter wiring

This is closer to an app flow than a lightweight prototype.

## 7. Close One Exploration Loop Locally

### Pattern

For a single exploration action, keep the:

- control
- derived result
- output

as close together as possible — ideally closed locally.

### Why it works

- Reduces `ui-far-consumer` and `ui-split-cells` hints
- Readers do not need to cross many cells to understand what a widget affects
- The feedback loop for parameter experimentation is shorter

### Example

Source:

- `explore_high_dimensional_data.py`
- `interactive-matrices.py`

Both place "small interaction + corresponding output" close together.

### Counterexample

Source:

- `nlp_span_comparison.py`

This notebook is good overall, but the `index` UI is placed far from where it is actually used, so `ui-far-consumer` will still fire.

### Skill implication

Do not place "parameter definitions" far up in the notebook and then let multiple downstream cells consume them in scattered fashion.

## 8. Extraction Signals

### Pattern

Mark logic as an extraction candidate when any of these signals are real:

- Repeated filtering, aggregation, chart skeletons, or rendering panels
- A clear input/output boundary has formed
- Multiple groups of `mo.state` or dynamic UI collections coordinate together
- Parameter synchronization or add/remove controls are maintained across cells
- A reusable domain capability is clearer than another notebook-local cell

### Examples

- `bennet-meyers-notebook.py`: module boundaries and multi-state coordination
- `goodreads-eda.py` / `polars_intro.py`: repeated chart and presentation skeletons

### Skill implication

Do not extract before the exploratory pattern is visible. Once reuse, state coordination, or maintenance cost is clear, move stable capability to a helper module and keep the notebook as analysis orchestration.

## 9. Presentation And App Drift Signals

### Pattern

Watch for notebook structure that serves staged display more than exploration:

- `mo.stop(...)`, staged reveal, or phased prompts in ordinary EDA
- Dashboard-like `mo.vstack` / `mo.hstack` panels
- Long explanatory copy before raw rows or low-assumption plots
- UI sections that demonstrate controls rather than reduce analysis friction
- Long cells carrying component responsibilities instead of local narrative or teaching

### Examples

- `laurium-prompt_engineering.py`: a staged workflow suited to prompt engineering, not default EDA
- `monitoring-ghg-emissions.py`: app-like / pseudo-component structure
- `polars_intro.py`, `akatsuki-tutorial.py`, `xdsl.py`: long narrative / teaching cells that should not be mechanically split

### Skill implication

Progressive disclosure and layout composition are valid when the task is genuinely a workflow, teaching artifact, or report. For EDA, restore raw evidence, low-assumption diagnostics, and focused validation before polish. If the notebook is really meant for readers, move it to the report style (`report-style.md`), where composition and coupled controls are allowed as long as each control's impact zone stays contiguous.

## Summary

Only these short rules are worth hardening into the main skill document:

- keep evidence upstream of decisions
- build data intuition before testing hypotheses
- keep EDA story logic discovery-first, not presentation-first
- prefer low-state controls for reversible exploration
- name stable seams when they emerge
- keep UI cells thin
- close one exploration loop locally
- treat extraction as a signal, not a starting point
- resist presentation and app drift

Remaining details and examples are kept here as supporting material for writing and review.
