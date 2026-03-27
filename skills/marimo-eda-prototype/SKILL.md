---
name: marimo-eda-prototype
description: >
  Guides Codex to write marimo notebooks for EDA and prototype-first work with restrained UI,
  cohesive cells, clear variable scoping, and deliberate extraction into modules. Use when
  creating or editing exploratory marimo notebooks where analysis comes first and UI stays light.
allowed-tools: Read, Write, Edit, Bash
---

# Marimo EDA Prototype

面向 `EDA / prototype-first` 的 marimo notebook 写作护栏。

这个 skill 的目标不是教完整 marimo API，而是让 Codex 默认写出：

- 以分析和验证为先的 notebook
- 少量但有价值的 UI
- 内聚的 cell 组织
- 清晰的 notebook / module 边界

> 技术性检查（syntax errors、multiple definitions、cycles）优先使用 `uvx marimo check`。
> `scripts/marimo_lint.py` 只能当可选辅助，不是这个 skill 的核心价值。
> 批量扫 GitHub fixture 的脚本属于 `research/marimo-github-eval/`，不属于这个 skill 的正式工作流。

## What This Skill Optimizes

- **Insight first**: notebook 先服务于观察、比较、验证，不先做成 mini app
- **Prototype before product**: 先在 notebook 里试出交互和分析模式，再决定是否抽成模块
- **Cell cohesion**: 一个探索动作相关的 UI、logic、output 尽量放近
- **Graph hygiene**: 只暴露真正需要跨 cell 复用的名字

## Default Stance

默认按下面的顺序思考：

1. 先写静态分析版本，确认问题和输出形式
2. 只有当交互明显提升探索效率时，才加少量 UI
3. 不把 notebook 当作长期承载复杂 UI 状态的地方
4. 当某段逻辑或 UI 组合已经稳定复用，再抽到 module

## Hard Guardrails

### 1. Do not turn the notebook into scattered UI development

避免这些信号：

- 连续多个 cell 都只是在定义 UI
- 一个简单探索动作被拆成很多互相依赖的 UI cells
- 为了“看起来可交互”而加入控件，而不是为了分析效率

如果交互已经需要明显的状态编排、复用或封装，说明它正在越过 notebook 边界。

### 2. Keep UI close to the analysis it controls

优先把同一个探索动作的 UI、计算、结果放在相邻位置，通常尽量在一个 cell 内完成。

目标不是机械地追求“永远同 cell”，而是避免：

- UI 在前面，真正使用逻辑散落很远
- 读 notebook 时很难判断一个控件到底影响哪里
- 改一个探索参数时需要追很多 downstream cells

### 3. Export only stable names

在 marimo 里，未加 `_` 的名字会进入依赖图。默认只暴露这些内容：

- 需要被别的 cell 复用的数据
- 稳定的 helper functions
- 这个 cell 的主要结果

中间步骤、临时 dataframe、组装图表时的中间值，默认优先用 `_` 前缀留在 cell 内。

### 4. Extract when a pattern becomes reusable

如果某段内容已经表现出“组件 / 模块”特征，就不该继续长在 notebook 里：

- 同一段 UI/logic 在多个 notebook 中复用
- 一个交互块已经有明确输入输出边界
- 为了维护它，不得不写很长的 cell 或复制粘贴
- 你已经在把 notebook 当成 app source，而不是探索空间

这时优先提炼到 `utils.py`、`charts.py`、`widgets.py` 或更明确的 module 中。

## Knowledge Activation

写 marimo notebook 时，主动激活这些判断模型，而不是只记 API：

- **Prototype vs product**: 这是探索原型，还是已经进入长期维护的 UI 组件？
- **Notebook vs module boundary**: 这段逻辑是为了本次分析，还是已经值得沉淀？
- **Reactive graph hygiene**: 哪些名字应该进入依赖图，哪些只该留在本 cell？
- **Cell cohesion**: 读者能否在局部区域看懂一个探索动作？
- **Delayed extraction**: 在模式成型之前先保持轻量，成型后再抽象

## Design Patterns

优先遵守这些高价值 pattern：

- **Create stable seams early**: 先定义稳定的 `load_*`, `build_*`, `show_*` 或 `annotate_*` helper，再让后面的 cell 组装分析流。
- **Keep UI cells thin**: UI cell 主要负责 control 或 rendering adapter，不要同时吞下大量分析逻辑。
- **Close one exploration loop locally**: 一个探索动作的 control、derived result、output 尽量保持在相邻 cell，避免前面定义 UI、后面很远才消费。
- **Let notebooks orchestrate**: notebook 负责串联数据、状态和展示；可复用能力优先沉淀到 helper 或 module。
- **Treat multi-state coordination as an extraction signal**: 一旦开始维护多组 `mo.state`、动态 UI 集合、参数同步或 add/remove controls，就该认真考虑抽 module。
- **Use progressive disclosure sparingly**: `mo.stop(...)` 和阶段性 reveal 可以用来引导探索，但不要默认把 notebook 做成长流程 app。

## Decision Table

| Situation | Preferred Move | Avoid |
|-----------|----------------|-------|
| 一次性分析、固定参数 | Plain variables + direct computation | 先加 slider / dropdown |
| 需要快速试几个参数 | 加少量 UI，贴近分析 cell | 把参数面板拆成多个独立 UI cells |
| 某段过滤/绘图逻辑开始重复 | 提炼 helper function | 继续复制相似 cells |
| 一个交互块已经很像组件 | 抽到 module | 继续把 notebook 当 UI 容器 |
| 中间值只服务当前 cell | `_tmp`, `_filtered`, `_chart` | 暴露成全局名字 |

## Good / Bad Examples

### Good: UI stays close to the exploration

```python
threshold = mo.ui.slider(0, 100, value=50, label="Threshold")
_filtered = df[df["score"] >= threshold.value]
mo.vstack([
    threshold,
    mo.md(f"{len(_filtered)} rows match"),
    _filtered.head(),
])
```

### Bad: UI state is scattered across the notebook

```python
# Cell 1
threshold = mo.ui.slider(0, 100, value=50)
threshold

# Cell 7
_filtered = df[df["score"] >= threshold.value]

# Cell 12
chart = draw_chart(_filtered)
```

### Good: extract when the pattern stabilizes

```python
# charts.py
def build_sales_chart(df: pd.DataFrame, metric: str) -> alt.Chart:
    ...

# notebook
metric = mo.ui.dropdown(["revenue", "margin"], value="revenue")
chart = build_sales_chart(df, metric.value)
mo.vstack([metric, chart])
```

### Bad: keep growing a pseudo-component inside the notebook

```python
metric = mo.ui.dropdown(["revenue", "margin"], value="revenue")
theme = mo.ui.dropdown(["light", "dark"], value="light")
show_labels = mo.ui.checkbox(value=True)
_base = alt.Chart(df) ...
_styled = _apply_theme(_base, theme.value)
_final = _toggle_labels(_styled, show_labels.value)
_final
```

如果这段交互已经有明确输入输出和样式变体，就该抽出去。

## Writing Pattern

推荐采用这个节奏：

1. Imports / lightweight config
2. Data loading
3. Cleaning / transformation
4. EDA cells
5. Optional prototype interactions
6. Summary or next-step outputs

不是硬模板；重点是让 notebook 保持“分析主线清楚，交互只为探索服务”。

## Final Checklist

在生成或修改 notebook 后，快速自检：

- 这份 notebook 的主任务还是分析，而不是 UI 堆砌吗？
- UI 是否确实提高了探索效率？
- 一个探索动作的相关代码是否足够集中？
- 是否只暴露了值得跨 cell 复用的名字？
- 有没有哪段内容已经更适合移到 module？
- 如果删掉一半 UI，这份 notebook 会不会更清楚？

## Optional Checker

推荐顺序：

- `uvx marimo check notebook.py`
- `python scripts/marimo_lint.py notebook.py --json`

可选使用 `scripts/marimo_lint.py` 做启发式提示，但要把它当作弱信号：

- `python scripts/marimo_lint.py notebook.py`
- `python scripts/marimo_lint.py notebook.py --json`

它适合发现一些“可能值得再看一眼”的问题，不适合作为 notebook 设计质量的最终裁判。

设计模式和 GitHub 样本依据见 `references/design-patterns.md`。
