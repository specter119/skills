# Workflow

## Default Order

1. Write the static analysis version first to confirm the problem and output form
2. Add a small amount of UI only when interaction clearly improves exploration efficiency
3. Avoid treating the notebook as a long-term place to host complex state orchestration
4. Extract a piece of logic or UI to a module only once it has stabilized and is being reused

## Hard Guardrails

### 1. Do Not Turn the Notebook into Scattered UI Development

Watch for these signals:

- Multiple consecutive cells doing nothing but defining UI
- A simple exploration action split into many mutually dependent UI cells
- Interaction added just to "look more like a product", not for analysis efficiency

### 2. Keep UI Close to the Analysis It Controls

- Keep controls, derived results, and outputs adjacent
- Avoid defining a widget at the top and consuming it far below
- Avoid a parameter dependency chain so long it becomes hard to trace

### 3. Only Export Stable Names

By default, only expose:

- Data that needs to be reused by other cells
- Stable helper functions
- The primary result of the current cell

Use local names like `_tmp`, `_filtered`, `_chart` for intermediate values.

### 4. Abstract Only After a Pattern Stabilizes

These are typically extraction signals:

- The same UI / logic starts repeating
- A clear input/output boundary has formed
- Maintaining it requires a long cell or copy-paste
- You are already treating the notebook as an app source

## Pre-Completion Checklist

- Is the notebook's primary task still analysis?
- Does the UI genuinely improve exploration efficiency?
- Is each exploration action sufficiently concentrated?
- Are only names worth cross-cell reuse exposed?
- Is there anything that would be better moved to a module?

## Check Commands

```bash
uvx marimo check notebook.py
python scripts/marimo_lint.py notebook.py --json
```
