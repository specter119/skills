# Marimo Notebook Eval Fixtures

这份清单把当前用于回归评估的 GitHub marimo notebook 固定下来。

目的不是追求“全部 0 提示”，而是让每次修改 `marimo_lint.py` 后，都能用同一批样本判断：

- 噪音有没有上升
- 某条规则有没有明显变钝
- `EDA / prototype-first` 的护栏是不是还在

## How To Use

执行方式：

```bash
python research/marimo-github-eval/collect_lint_results.py research/marimo-github-eval/_sources --json
```

单文件定位某个 notebook 时，仍可直接运行：

```bash
python skills/marimo-eda-prototype/scripts/marimo_lint.py <file> --json
```

`collect_lint_results.py` 是 research helper，不是 skill 正式接口。

评估时看三件事：

1. 总提示数是否偏离样本角色
2. 关键规则是否命中正确类型的 notebook
3. 误报探针的提示是否在收敛

## Fixture Classes

### 1. Low-Noise Positives

这些样本代表“写得比较克制的 notebook”。

期望：

- 总提示应偏低
- 如果命中，也应是少量、可解释的提示
- 不应被 `oversized-cell` 大量淹没

#### `explore_high_dimensional_data.py`

- Local: `research/marimo-github-eval/_sources/explore_high_dimensional_data.py`
- Source: `marimo-team/examples`
- GitHub: `https://github.com/marimo-team/examples/blob/main/explore_high_dimensional_data/explore_high_dimensional_data.py`
- Watch:
  - `ui-scatter` 可偶发命中
  - 不应出现大量 `oversized-cell`

#### `nlp_span_comparison.py`

- Local: `research/marimo-github-eval/_sources/nlp_span_comparison.py`
- Source: `marimo-team/examples`
- GitHub: `https://github.com/marimo-team/examples/blob/main/nlp_span_comparison/nlp_span_comparison.py`
- Watch:
  - `ui-scatter` 可合理命中
  - `oversized-cell` 若出现，应保持低频

#### `interactive-matrices.py`

- Local: `research/marimo-github-eval/_sources/interactive-matrices.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/011-Vincent/interactive-matrices.py`
- Watch:
  - `ui-scatter` 是主要观察点
  - 不应出现高频 `export-surface` 或 `oversized-cell`

#### `comparing-regularizers-in-regression.py`

- Local: `research/marimo-github-eval/_sources/comparing-regularizers-in-regression.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/005-cvxpy-nasa/comparing-regularizers-in-regression.py`
- Watch:
  - 主要看 `repeated-pattern`
  - 若大量命中 `oversized-cell`，通常表示规则过敏

### 2. Stress Tests

这些样本体量较大，或包含大量重复展示/讲解结构。

期望：

- 可以命中多个规则
- 重点看提示是否“有价值”，不是单纯数量
- 规则不应把所有长 notebook 都无差别打爆

#### `goodreads-eda.py`

- Local: `research/marimo-github-eval/_sources/goodreads-eda.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/007-haleshot/goodreads-eda.py`
- Watch:
  - `repeated-pattern`
  - `export-surface`
  - 少量 `oversized-cell`

#### `stem-probes.py`

- Local: `research/marimo-github-eval/_sources/stem-probes.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/002-stem-probes/stem-probes.py`
- Watch:
  - `export-surface`
  - `oversized-cell`
  - 是否出现过量教学误报

#### `xdsl.py`

- Local: `research/marimo-github-eval/_sources/xdsl.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/004-xdsl/xdsl.py`
- Watch:
  - `export-surface`
  - `oversized-cell`
  - 这是科学/教学型噪音探针之一

#### `geometric-mtf.py`

- Local: `research/marimo-github-eval/_sources/geometric-mtf.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/020-yoann-mocquin/geometric-mtf.py`
- Watch:
  - `export-surface`
  - `oversized-cell`

### 3. Tutorial Sensitivity Probes

这些样本不是坏 notebook，但很容易被 `oversized-cell` 误报。

期望：

- 可以有少量提示
- 如果 `oversized-cell` 明显失控，说明规则又过敏了

#### `polars_intro.py`

- Local: `research/marimo-github-eval/_sources/polars_intro.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/014-ryan-parker/polars_intro.py`
- Watch:
  - `oversized-cell` 是否失控

#### `akatsuki-tutorial.py`

- Local: `research/marimo-github-eval/_sources/akatsuki-tutorial.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/019-smohspace/akatsuki-tutorial.py`
- Watch:
  - `repeated-pattern`
  - `oversized-cell`
  - 不应被当成明显 app-like notebook

### 4. Module-Boundary Probes

这些样本适合观察“什么时候 notebook 正在越界到 module / component”。

期望：

- 至少命中一个结构信号
- `ui-scatter` / `export-surface` / `oversized-cell` 的组合要有解释力

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

这些样本更像 workflow builder、rich prototype、或 notebook-local app。

期望：

- 应该稳定命中明显结构提示
- 如果这些样本几乎不报，说明规则可能过钝

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

这些样本用于提醒我们“当前规则没覆盖到什么”。

#### `lmsys.py`

- Local: `research/marimo-github-eval/_sources/lmsys.py`
- Source: `marimo-team/spotlights`
- GitHub: `https://github.com/marimo-team/spotlights/blob/main/006-vrtnis/lmsys.py`
- Watch:
  - 当前通常只命中少量 `export-surface`
  - 如果未来增加 narrative / visual exploration 规则，它应重新进入重点观察

## Regression Expectations

每次调规则后，至少做下面检查：

1. `Low-Noise Positives`
   - 不应出现明显提示膨胀

2. `Tutorial Sensitivity Probes`
   - `oversized-cell` 应趋于收敛，而不是增长

3. `App-Like Negatives`
   - 仍应稳定命中

4. `Module-Boundary Probes`
   - 不能失去结构解释力

## Current Priorities

当前最重要的回归目标：

1. 压低 `oversized-cell` 对 tutorial / explanatory notebook 的误报
2. 保持对 app-like notebook 的命中能力
3. 避免解析阶段的 warning 污染 CLI 输出
