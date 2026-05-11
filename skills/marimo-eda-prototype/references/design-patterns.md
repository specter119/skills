# Marimo Notebook Design Patterns

This document captures design patterns from the current sample pool that are worth absorbing into the skill.

The goal is not to enumerate APIs, but to answer:

- What notebook structure fits `EDA / prototype-first` better
- Which patterns indicate the notebook is still within "exploration space"
- Which patterns indicate it is time to extract a helper or module

## 1. Create Stable Seams Early

### Pattern

Define stable helpers first, then compose them in subsequent cells:

- `load_*`
- `build_*`
- `show_*`
- `annotate_*`

### Why it works

- The notebook's main thread is clearer
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

If you are writing a notebook where users can swap out the data source, embedding algorithm, or display style, define the seams first, then write the orchestration cell.

## 2. Keep UI Cells Thin

### Pattern

A UI cell is primarily responsible for:

- Generating widgets
- Wrapping charts / tables / rendered output
- Reading `.value`

Do not pack large amounts of data cleaning, filtering, or state synchronization into the same UI cell.

### Why it works

- The boundary between control and analysis is clear
- UI updates are easier to trace
- The notebook is less likely to grow into a notebook-local component

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

## 3. Close One Exploration Loop Locally

### Pattern

For a single exploration action, keep the:

- control
- derived result
- output

as close together as possible — ideally closed locally.

### Why it works

- Reduces `ui-scatter`
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

This notebook is good overall, but the `index` UI is placed far from where it is actually used, so `ui-scatter` will still fire.

### Skill implication

Do not place "parameter definitions" far up in the notebook and then let multiple downstream cells consume them in scattered fashion.

## 4. Let the Notebook Orchestrate, Let Modules Own Capability

### Pattern

The notebook is responsible for:

- User input
- State wiring
- Analysis flow orchestration
- Display composition

The module / helper is responsible for:

- Domain logic
- Reusable algorithms
- Chart construction
- Widget components

### Why it works

- The notebook stays prototype-first
- Stable capabilities do not keep expanding inside the notebook
- Reusable boundaries are clearer

### Example

Source:

- `bennet-meyers-notebook.py`

It has already moved some capabilities into `modules/`, while the notebook retains orchestration and state wiring.

### Skill implication

When you find that a piece of logic can be named as a "capability" rather than "a step in this analysis", it is time to leave the notebook.

## 5. Multi-State Coordination Is an Extraction Signal

### Pattern

The following are usually not signals to "hold on a bit longer in the notebook" — they are signals to extract a module:

- Multiple groups of `mo.state`
- Dynamic UI collections
- Parameter pre-filling / parameter synchronization
- Add/remove controls
- The same group of state maintained jointly by multiple cells

### Why it works

This kind of logic is usually already forming a component protocol:

- What is the input
- What is the internal state
- What is the output

It just has not been formally extracted yet.

### Example

Source:

- `bennet-meyers-notebook.py`

It maintains multiple groups of state across problem, component, and parameter — a clear signal of a module boundary.

### Skill implication

When the notebook starts doing state coordination, do not default to writing more code inline; first evaluate whether it should be extracted to `widgets.py`, `components.py`, or a domain module.

## 6. Progressive Disclosure Can Help, But It Is Not the Default

### Pattern

`mo.stop(...)`, staged reveal after form submission, and phased prompts are useful for:

- Step-by-step workflows
- Configuration flows with high dependency ordering
- Cases where users easily miss a key parameter

### Why it works

- Reduces users exploring further in an invalid state
- Breaks complex operations into clearer stages

### Example

Source:

- `laurium-prompt_engineering.py`

It turns the notebook into a staged workflow, suited to a prompt engineering workflow.

### Risk

This pattern can easily push the notebook toward being a mini app.

### Skill implication

Use only when the task itself is genuinely a workflow / wizard; a default EDA notebook should not grow in this direction from the start.

## 7. Repeated Presentation Skeletons Mean the Pattern Is Stabilizing

### Pattern

When the notebook contains many similar cells:

- Similar filtering
- Similar groupby / aggregation
- Similar chart skeletons
- Only changing fields or colors

This usually means the pattern has stabilized.

### Why it works

This is a mature signal to extract a helper, not a reason to keep copying.

### Example

Source:

- `goodreads-eda.py`
- `polars_intro.py`

Both contain large numbers of similar presentation skeletons.

### Skill implication

Once a pattern stabilizes, prefer extracting:

- `build_*_chart`
- `compute_*_summary`
- `render_*_panel`

rather than continuing to stack parallel cells.

## 8. Long Narrative Cells Need Different Treatment From App-Like Cells

### Pattern

Not all long cells are a bad smell.

Distinguish between two types of long cells:

1. Narrative / teaching cell
2. App-like / pseudo-component cell

### Why it matters

The first type is primarily explaining, displaying, and teaching; the second type is carrying component responsibilities.

### Examples

More like narrative / teaching:

- `polars_intro.py`
- `akatsuki-tutorial.py`
- `xdsl.py`

More like app-like / pseudo-component:

- `laurium-prompt_engineering.py`
- `monitoring-ghg-emissions.py`

### Skill implication

When writing a notebook, do not mechanically split a cell just because it is slightly long; first determine whether it is explaining something or secretly carrying component logic.

## Summary

Only these short rules are worth hardening into the main skill document:

- create stable seams early
- keep UI cells thin
- close one exploration loop locally
- let notebooks orchestrate
- treat multi-state coordination as an extraction signal
- use progressive disclosure sparingly

Remaining details and examples are kept here as supporting material for writing and review.
