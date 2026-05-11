# Marimo EDA Prototype Boundaries & Execution Notes

## Goals and Outputs
- Target job: rapidly write marimo notebooks centered on EDA / prototype-first work; analysis and validation come first, UI is added only when it clearly improves exploration efficiency.
- Core output: a notebook with a clear analysis thread, controlled interaction, and explicit module extraction; accompanied by a helper module or brief summary cell when needed.
- Out of scope for this skill: comprehensive marimo API instruction, bulk GitHub fixture scanning, and treating `scripts/marimo_lint.py` as a required gate.

## Key Capability Preferences
1. Use static analysis first to validate the problem / output form and confirm the main thread.
2. Introduce UI only when interaction will significantly accelerate exploration, and keep UI cells lean.
3. Do not treat the notebook as a complex UI container for end users; keep it to wiring data, state, and display.
4. As soon as a piece of logic or widget combination repeats, state coordination becomes complex, or reuse is clear, extract it to a module promptly (e.g., `utils.py`, `charts.py`, `widgets.py`).

## Hard Guardrails

### 1. Do Not Let the Notebook Become Cluttered UI Development
- Avoid: multiple consecutive cells all defining UI, analysis logic scattered across cells, widgets added just to "look interactive".
- Signal: cells sinking into state wiring early on, heavy mixing of UI definitions and logic within a single cell. This indicates it is time to extract to a module.

### 2. Keep UI Close to the Analysis It Controls
- Place controls, derived results, and outputs in the same cell or adjacent cells; avoid leaving readers uncertain about which downstream cells a widget affects.
- Avoid defining UI early in the notebook while the logic that consumes it is scattered far below.

### 3. Only Export Names That Genuinely Need Cross-Cell Reuse
- Only stable helpers, necessary data, or primary results belong in the dependency graph; use the `_` prefix for intermediate / temp values to avoid polluting the graph.

### 4. Extract to a Module When a Reuse Signal Appears
- When interaction / logic is reused across multiple notebooks, state coordination grows increasingly complex, or maintenance cost rises, move the relevant UI / chart / helper to a module.

## Knowledge Activation Model
- Prototype vs product: is this a one-off exploration or has it entered long-term maintenance?
- Notebook vs module: is the current logic a temporary artifact of this analysis or something worth solidifying?
- Reactive graph hygiene: which names must enter the dependency graph, and which should remain cell-local?
- Cell cohesion: can a reader understand one exploration action in isolation?
- Delayed extraction: stay lightweight until a pattern solidifies, then abstract.

## Decision Reference Table
| Situation | Preferred Action | Avoid |
| --- | --- | --- |
| One-off analysis, fixed parameters | Plain variables + direct computation | Adding sliders / dropdowns first |
| Quickly trying multiple parameters | Add minimal UI, close to the analysis cell | Splitting into multiple independent UI cells |
| Filter / plot logic starts repeating | Extract a helper function | Continuing to copy similar cells |
| Interaction block already looks like a component | Extract to a module | Continuing to use the notebook as a UI container |
| Intermediate value serves only the current cell | `_tmp`, `_filtered`, `_chart` | Exposing as a global name |

## Good / Bad Examples
### Good: UI Tightly Coupled to Exploration
```python
threshold = mo.ui.slider(0, 100, value=50, label="Threshold")
_filtered = df[df["score"] >= threshold.value]
mo.vstack([
    threshold,
    mo.md(f"{len(_filtered)} rows match"),
    _filtered.head(),
])
```

### Bad: UI State Scattered
```python
# Cell 1
threshold = mo.ui.slider(0, 100, value=50)
threshold

# Cell 7
_filtered = df[df["score"] >= threshold.value]

# Cell 12
chart = draw_chart(_filtered)
```

### Good: Extract Helper for Stable Pattern
```python
# charts.py
def build_sales_chart(df: pd.DataFrame, metric: str) -> alt.Chart:
    ...

# notebook
metric = mo.ui.dropdown(["revenue", "margin"], value="revenue")
chart = build_sales_chart(df, metric.value)
mo.vstack([metric, chart])
```

### Bad: Pseudo-Component Keeps Growing in the Notebook
```python
metric = mo.ui.dropdown(["revenue", "margin"], value="revenue")
theme = mo.ui.dropdown(["light", "dark"], value="light")
show_labels = mo.ui.checkbox(value=True)
_base = alt.Chart(df) ...
_styled = _apply_theme(_base, theme.value)
_final = _toggle_labels(_styled, show_labels.value)
_final
```

## Writing Rhythm
1. Imports / simple configuration
2. Data loading
3. Cleaning / transformation
4. EDA cells
5. Optional prototype interactions (UI must have an analytic rationale)
6. Summary / next-step outputs

This is not a rigid template; the key is keeping the analysis thread clear and ensuring interaction serves exploration only.

## Final Self-Check Checklist
- Is the notebook's primary task still analysis?
- Does the UI genuinely improve exploration efficiency?
- Is the code for a single exploration action sufficiently concentrated?
- Are only names worth cross-cell reuse exposed?
- Is there any logic that would be better off in a module?
- Would removing half the UI make things clearer?

## Optional Checkers
- `uvx marimo check notebook.py`
- `python scripts/marimo_lint.py notebook.py --json`

`scripts/marimo_lint.py` serves only as a heuristic hint to catch issues "worth a second look" — it is not the final quality arbiter.

For design patterns and GitHub samples, see `references/design-patterns.md`.
