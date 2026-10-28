# Marimo Notebook Eval Fixtures

This list locks down the GitHub marimo notebooks currently used for regression evaluation.

The goal is not to achieve "zero hints across the board", but to ensure that every time `marimo_lint.py` is modified, the same set of samples can be used to judge:

- Whether noise has increased
- Whether any rule has clearly dulled
- Whether the style guardrails (EDA and report) are still in place

## Rules and Presets

| rule                      | scope  | meaning                                                                                                                              |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `ui-split-cells`          | shared | consecutive cells that only define independent controls (a chain where each control depends on the previous one is exempt)           |
| `export-surface`          | shared | a cell exports a generic name (`chart`, `result`, ...), or 4+ names with mixed responsibilities. Not triggered by export count alone |
| `oversized-cell`          | shared | a cell with too much body to read as one action                                                                                      |
| `repeated-pattern`        | shared | similar cells that suggest a helper                                                                                                  |
| `control-upstream-impact` | shared | a control's effect reaches a visible cell above its display position                                                                 |
| `ui-far-consumer`         | eda    | a control's first consumer is 3+ visible cells below its display position                                                            |
| `control-zone-gap`        | report | a visible, unaffected, non-narrative cell sits inside a control's impact zone                                                        |

Presets: no `--style` runs only the shared rules; `--style eda` adds `ui-far-consumer`; `--style report` adds `control-zone-gap`. `--select` replaces the preset, `--ignore` removes rules. Suppress one hit with `# marimo-lint: ignore[rule-id]` in the cell where the hit is located.

## How To Use

Synthetic fixtures (fast, no network):

```bash
python skills/marimo-style/evals/fixtures/run_fixtures.py
```

It runs every notebook in `evals/fixtures/` in the three modes (`shared`, `eda`, `report`) and compares the set of rule ids with `expected.json`. Each fixture also passes `uvx marimo check`.

| fixture                             | shared                    | eda               | report             | what it proves                                                 |
| ----------------------------------- | ------------------------- | ----------------- | ------------------ | -------------------------------------------------------------- |
| `report_good_zone`                  | -                         | -                 | -                  | stable summary, control directly above its chart and narrative |
| `report_gap`                        | -                         | -                 | `control-zone-gap` | an unrelated chart between a control and its chart             |
| `report_summary_depends_on_control` | `control-upstream-impact` | same              | same               | the summary above a control reads its value                    |
| `report_global_filter`              | -                         | -                 | -                  | a document-wide filter is not a zone violation                 |
| `report_tabs_and_crossfilter`       | -                         | -                 | -                  | `mo.ui.tabs` is layout; chart selection is the control         |
| `report_hstack_display`             | -                         | -                 | -                  | defined upstream, displayed next to its chart: no hit          |
| `eda_far_consumer`                  | -                         | `ui-far-consumer` | -                  | the rule is EDA only                                           |
| `eda_dependent_chain`               | -                         | -                 | -                  | dependent controls in adjacent cells are exempt                |
| `eda_split_ui`                      | `ui-split-cells`          | same              | same               | independent controls in a run                                  |
| `generic_exports`                   | `export-surface`          | same              | same               | the message advises renaming, never an underscore prefix       |
| `app_function_edges`                | `control-upstream-impact` | same              | same               | a dependency that flows through `@app.function` is seen        |

Real notebooks (needs the downloaded samples):

```bash
python research/marimo-github-eval/collect_lint_results.py research/marimo-github-eval/_sources --json
```

`research/` is gitignored. Re-create `_sources/` by downloading the GitHub URLs below (swap `github.com/.../blob/` for `raw.githubusercontent.com/.../`). `collect_lint_results.py` is a local helper, not the skill's official interface.

To target a single notebook file:

```bash
python skills/marimo-style/scripts/marimo_lint.py <file> --style eda --json
```

When evaluating, look at three things:

1. Whether the total hint count deviates from the sample's expected role
1. Whether key rules fire on the correct type of notebook
1. Whether false-positive probe hints are converging

## Observed Snapshot (2026-10-28)

Counts per rule with no `--style` (shared), plus the extra rules from each preset. This is a snapshot for noticing drift, not a target.

| file                                 | shared                                           | `--style eda` adds | `--style report` adds |
| ------------------------------------ | ------------------------------------------------ | ------------------ | --------------------- |
| akatsuki-tutorial                    | oversized 2                                      | -                  | -                     |
| bennet-meyers-notebook               | oversized 1                                      | -                  | zone-gap 1            |
| comparing-regularizers-in-regression | -                                                | -                  | -                     |
| explore_high_dimensional_data        | export-surface 2                                 | -                  | -                     |
| geometric-mtf                        | export-surface 1, oversized 2                    | -                  | -                     |
| goodreads-eda                        | oversized 1, repeated 1                          | -                  | -                     |
| interactive-matrices                 | export-surface 1, ui-split-cells 1               | -                  | -                     |
| laurium-prompt_engineering           | export-surface 1, oversized 5                    | -                  | zone-gap 1            |
| lmsys                                | -                                                | -                  | -                     |
| monitoring-ghg-emissions             | upstream-impact 6, export-surface 2, oversized 4 | -                  | -                     |
| nlp_span_comparison                  | -                                                | -                  | zone-gap 1            |
| polars_intro                         | oversized 5                                      | -                  | -                     |
| stem-probes                          | upstream-impact 3, oversized 2                   | far-consumer 2     | -                     |
| trajectory-planning                  | export-surface 1, oversized 2                    | -                  | zone-gap 1            |
| xdsl                                 | upstream-impact 3, oversized 4                   | far-consumer 3     | -                     |

Notes:

- `export-surface` stopped firing on notebooks that export many semantically named values (xdsl, stem-probes, goodreads) and now fires on generic names (`data`, `chart` in `explore_high_dimensional_data` and `interactive-matrices`). This is the intended change.
- `control-upstream-impact` on `monitoring-ghg-emissions` is a true inversion: summary cells at the top react to selection charts defined at the bottom. On `stem-probes` and `xdsl` the hits are teaching notebooks that show a plot above the controls that drive it. Explainable, and acceptable on these stress samples.
- `control-zone-gap` fires once on 4 of 15 real notebooks, which is under the one-third false-positive threshold. The `nlp_span_comparison` hit (a static legend between a control and its annotation UI) is borderline.
- `ui-far-consumer` and `ui-split-cells` counts differ from the old `ui-scatter` because distance is now measured from the control's display position and counts visible cells only.

## Known Lint Limits

- Widgets read through traits other than `.value` (for example anywidget `.x`) are not impact reads, so control rules stay quiet for them.
- A control displayed through an intermediate variable (`layout = mo.hstack([slider])`, then a cell ending with `layout`) is not recognized as displayed; the defining cell is used.
- Transitive impact follows any name reference, so a layout cell that groups affected outputs counts as affected.
- A suppression comment silences only findings located at that cell.
- `hide_code` is not parsed.

## Fixture Classes

### 1. Low-Noise Positives

These samples represent "notebooks written with reasonable restraint".

Expected:

- Total hints should be low
- If hints fire, they should be few in number and explainable
- Should not be overwhelmed by large numbers of `oversized-cell` hits

#### `explore_high_dimensional_data.py`

- Local: `research/marimo-github-eval/_sources/explore_high_dimensional_data.py`
- Source: `marimo-team/examples`
- GitHub: `https://github.com/marimo-team/examples/blob/main/explore_high_dimensional_data/explore_high_dimensional_data.py`
- Watch:
  - `export-surface` may fire on generic names (`data`, `chart`)
  - Should not produce large numbers of `oversized-cell` hits

#### `nlp_span_comparison.py`

- Local: `research/marimo-github-eval/_sources/nlp_span_comparison.py`
- Source: `marimo-team/examples`
- GitHub: `https://github.com/marimo-team/examples/blob/main/nlp_span_comparison/nlp_span_comparison.py`
- Watch:
  - `control-zone-gap` (report) may fire once; it is borderline
  - `oversized-cell`, if it appears, should remain infrequent

#### `interactive-matrices.py`

- Local: `research/marimo-github-eval/_sources/interactive-matrices.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/011-Vincent/interactive-matrices.py`
- Watch:
  - `ui-split-cells` is the main observation point
  - Should not produce frequent `export-surface` or `oversized-cell` hits

#### `comparing-regularizers-in-regression.py`

- Local: `research/marimo-github-eval/_sources/comparing-regularizers-in-regression.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/005-cvxpy-nasa/comparing-regularizers-in-regression.py`
- Watch:
  - Primarily watch `repeated-pattern`
  - If `oversized-cell` fires heavily, the rule is likely over-sensitive

### 2. Stress Tests

These samples are large in volume, or contain many repeated display / explanation structures.

Expected:

- Multiple rules may fire
- Focus on whether hints are "valuable", not just the count
- Rules should not indiscriminately fire on all long notebooks

#### `goodreads-eda.py`

- Local: `research/marimo-github-eval/_sources/goodreads-eda.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/007-haleshot/goodreads-eda.py`
- Watch:
  - `repeated-pattern`
  - `export-surface`
  - A small number of `oversized-cell`

#### `stem-probes.py`

- Local: `research/marimo-github-eval/_sources/stem-probes.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/002-stem-probes/stem-probes.py`
- Watch:
  - `export-surface`
  - `oversized-cell`
  - Whether excessive teaching false positives appear

#### `xdsl.py`

- Local: `research/marimo-github-eval/_sources/xdsl.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/004-xdsl/xdsl.py`
- Watch:
  - `export-surface`
  - `oversized-cell`
  - This is one of the scientific / teaching noise probes

#### `geometric-mtf.py`

- Local: `research/marimo-github-eval/_sources/geometric-mtf.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/020-yoann-mocquin/geometric-mtf.py`
- Watch:
  - `export-surface`
  - `oversized-cell`

### 3. Tutorial Sensitivity Probes

These samples are not bad notebooks, but are easily false-positived by `oversized-cell`.

Expected:

- A small number of hints is acceptable
- If `oversized-cell` is clearly out of control, the rule has become over-sensitive again

#### `polars_intro.py`

- Local: `research/marimo-github-eval/_sources/polars_intro.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/014-ryan-parker/polars_intro.py`
- Watch:
  - Whether `oversized-cell` is out of control

#### `akatsuki-tutorial.py`

- Local: `research/marimo-github-eval/_sources/akatsuki-tutorial.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/019-smohspace/akatsuki-tutorial.py`
- Watch:
  - `repeated-pattern`
  - `oversized-cell`
  - Should not be treated as an obviously app-like notebook

### 4. Module-Boundary Probes

These samples are suitable for observing "when is a notebook crossing into module / component territory".

Expected:

- At least one structural signal fires
- The combination of `ui-split-cells` / `ui-far-consumer` / `control-zone-gap` / `export-surface` / `oversized-cell` should be explainable

#### `bennet-meyers-notebook.py`

- Local: `research/marimo-github-eval/_sources/bennet-meyers-notebook.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/003-bennet-meyers/notebook.py`
- Watch:
  - `control-zone-gap` (report)
  - `export-surface`
  - `oversized-cell`

#### `trajectory-planning.py`

- Local: `research/marimo-github-eval/_sources/trajectory-planning.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/005-cvxpy-nasa/trajectory-planning.py`
- Watch:
  - `export-surface`
  - `oversized-cell`

### 5. App-Like Negatives

These samples look more like workflow builders, rich prototypes, or notebook-local apps.

Expected:

- Should consistently fire obvious structural hints
- If these samples produce almost no hints, the rules may be too dull

#### `laurium-prompt_engineering.py`

- Local: `research/marimo-github-eval/_sources/laurium-prompt_engineering.py`
- Source: `moj-analytical-services/laurium`
- GitHub: `https://github.com/moj-analytical-services/laurium/blob/main/notebooks/marimo/prompt_engineering.py`
- Watch:
  - `oversized-cell`
  - `export-surface`

#### `monitoring-ghg-emissions.py`

- Local: `research/marimo-github-eval/_sources/monitoring-ghg-emissions.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/010-Mustjaab/Monitoring%20Flow%20of%20GHG%20Emissions.py`
- Watch:
  - `export-surface`
  - `oversized-cell`

### 6. Coverage Gaps

These samples remind us "what the current rules do not cover".

#### `lmsys.py`

- Local: `research/marimo-github-eval/_sources/lmsys.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/006-vrtnis/lmsys.py`
- Watch:
  - Currently usually fires only a small number of `export-surface` hits
  - If narrative / visual exploration rules are added in the future, it should re-enter the key watch list

## Regression Expectations

After each rule change, perform at least the following checks:

1. `Low-Noise Positives`

   - Should not show obvious hint inflation

1. `Tutorial Sensitivity Probes`

   - `oversized-cell` should trend toward convergence, not growth

1. `App-Like Negatives`

   - Should still fire consistently

1. `Module-Boundary Probes`

   - Must not lose structural explanatory power

## Current Priorities

The most important regression targets right now:

1. Reduce `oversized-cell` false positives on tutorial / explanatory notebooks
1. Maintain the ability to fire on app-like notebooks
1. Avoid parse-stage warnings polluting CLI output
1. Prevent discovery-first EDA from being overwritten by demo / presentation / app patterns
1. Preserve basic marimo semantics: visible final outputs, unique exported names, downstream widget `.value`, and semantic names for cross-cell variables (`_` only for `_fig`/`_ax`/loop variables)
1. Keep `control-zone-gap` false positives on real report notebooks under one third (currently 4 of 15)
