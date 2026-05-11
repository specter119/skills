# Marimo Notebook Eval Fixtures

This list locks down the GitHub marimo notebooks currently used for regression evaluation.

The goal is not to achieve "zero hints across the board", but to ensure that every time `marimo_lint.py` is modified, the same set of samples can be used to judge:

- Whether noise has increased
- Whether any rule has clearly dulled
- Whether the `EDA / prototype-first` guardrails are still in place

## How To Use

Run:

```bash
python research/marimo-github-eval/collect_lint_results.py research/marimo-github-eval/_sources --json
```

To target a single notebook file, you can still run directly:

```bash
python skills/marimo-eda-prototype/scripts/marimo_lint.py <file> --json
```

`collect_lint_results.py` is a research helper, not the skill's official interface.

When evaluating, look at three things:

1. Whether the total hint count deviates from the sample's expected role
2. Whether key rules fire on the correct type of notebook
3. Whether false-positive probe hints are converging

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
  - `ui-scatter` may fire occasionally
  - Should not produce large numbers of `oversized-cell` hits

#### `nlp_span_comparison.py`

- Local: `research/marimo-github-eval/_sources/nlp_span_comparison.py`
- Source: `marimo-team/examples`
- GitHub: `https://github.com/marimo-team/examples/blob/main/nlp_span_comparison/nlp_span_comparison.py`
- Watch:
  - `ui-scatter` may fire reasonably
  - `oversized-cell`, if it appears, should remain infrequent

#### `interactive-matrices.py`

- Local: `research/marimo-github-eval/_sources/interactive-matrices.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/011-Vincent/interactive-matrices.py`
- Watch:
  - `ui-scatter` is the main observation point
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
- The combination of `ui-scatter` / `export-surface` / `oversized-cell` should be explainable

#### `bennet-meyers-notebook.py`

- Local: `research/marimo-github-eval/_sources/bennet-meyers-notebook.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/003-bennet-meyers/notebook.py`
- Watch:
  - `ui-scatter`
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

2. `Tutorial Sensitivity Probes`
   - `oversized-cell` should trend toward convergence, not growth

3. `App-Like Negatives`
   - Should still fire consistently

4. `Module-Boundary Probes`
   - Must not lose structural explanatory power

## Current Priorities

The most important regression targets right now:

1. Reduce `oversized-cell` false positives on tutorial / explanatory notebooks
2. Maintain the ability to fire on app-like notebooks
3. Avoid parse-stage warnings polluting CLI output
