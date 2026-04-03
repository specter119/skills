# Marimo EDA Prototype Boundaries & Execution Notes

## 目标与输出
- 目标 job：快速写出以 EDA / prototype-first 为核心的 marimo notebook，分析和验证先行，UI 只在探索效率明显提升时才加入。
- 核心输出：一份分析主线清晰、交互受控、模块提炼明确的 notebook；必要时附带 helper module 或简短 summary cell。
- 不是这个 skill 的工作：全面讲授 marimo API、批量扫描 GitHub fixture，也不是把 `scripts/marimo_lint.py` 当作必需 gate。

## 关键能力偏好
1. 先用静态分析验证问题 / 输出形式，确认主线。
2. 只有在交互能显著加快探索时才引入 UI，并保持 UI cell 简洁。
3. 不把 notebook 当作面向用户的复杂 UI 容器；只让它串联数据、状态和展示。
4. 一旦某段逻辑或控件组合重复、协调状态复杂或复用明确，就及时抽到 module（如 `utils.py`、`charts.py`、`widgets.py`）。

## 硬性护栏

### 1. 不让 notebook 变成杂乱的 UI 开发
- 忌：连续多个 cell 都在定义 UI、分析逻辑被拆散、控件只是为了“看起来交互”。
- 信号：多 cell 早期就沉在状态 wiring、单 cell 里大量 UI 定义与逻辑混合。此时说明需要提炼到模块。

### 2. UI 要靠近它控制的分析
- 把 control、计算、结果尽量放在一个 cell 或相邻 cell，避免读者不知道一个控件到底影响哪些后续 cell。
- 避免 UI 先出现在前面、而使用它的逻辑散落多处。

### 3. 只导出真正需要跨 cell 复用的名字
- 只有稳定 helper、必要的数据或主要结果才保留在依赖图；中间值 / temp 用 `_` 前缀，避免污染图。

### 4. 发现复用信号就抽模块
- 交互 / 逻辑在多个 notebook 中复用、状态协调越来越复杂、维护成本提高，就该将相应 UI / chart / helper 提至 module。

## 知识激活模型
- Prototype vs product：这是一次性探索还是已经进入长期维护？
- Notebook vs module：当前逻辑是本次分析的临时内容还是值得沉淀？
- Reactive graph hygiene：哪些名字得进入依赖图，哪些只能留 cell 内？
- Cell cohesion：读者能否局部理解一个探索动作？
- Delayed extraction：在模式成型之前保持轻量，成型后再抽象。

## 决策参照表
| 情景 | 首选动作 | 避免 |
| --- | --- | --- |
| 一次性分析、固定参数 | 用 plain variables + 直接 computation | 先加 slider / dropdown |
| 快速试多个参数 | 加少量 UI，靠近分析 cell | 拆成多个独立 UI cells |
| 过滤 / 绘图逻辑开始重复 | 提炼 helper function | 继续复制相似 cells |
| 交互块已经像组件 | 抽到 module | 继续让 notebook 充当 UI 容器 |
| 中间值只服务当前 cell | `_tmp`, `_filtered`, `_chart` | 暴露成全局名字 |

## 好 / 差示例
### 好：UI 紧贴探索
```python
threshold = mo.ui.slider(0, 100, value=50, label="Threshold")
_filtered = df[df["score"] >= threshold.value]
mo.vstack([
    threshold,
    mo.md(f"{len(_filtered)} rows match"),
    _filtered.head(),
])
```

### 差：UI 状态散落
```python
# Cell 1
threshold = mo.ui.slider(0, 100, value=50)
threshold

# Cell 7
_filtered = df[df["score"] >= threshold.value]

# Cell 12
chart = draw_chart(_filtered)
```

### 好：稳定模式抽 helper
```python
# charts.py
def build_sales_chart(df: pd.DataFrame, metric: str) -> alt.Chart:
    ...

# notebook
metric = mo.ui.dropdown(["revenue", "margin"], value="revenue")
chart = build_sales_chart(df, metric.value)
mo.vstack([metric, chart])
```

### 差：伪组件继续长在 notebook
```python
metric = mo.ui.dropdown(["revenue", "margin"], value="revenue")
theme = mo.ui.dropdown(["light", "dark"], value="light")
show_labels = mo.ui.checkbox(value=True)
_base = alt.Chart(df) ...
_styled = _apply_theme(_base, theme.value)
_final = _toggle_labels(_styled, show_labels.value)
_final
```

## 写作节奏
1. Imports / 简单配置
2. 数据加载
3. 清洗 / 转换
4. EDA cells
5. 可选的 prototype interactions（UI 需有分析理由）
6. Summary / next-step outputs

不是固定模板，重点是保持分析主线清晰、交互只为探索服务。

## 最终自检清单
- 这份 notebook 的主任务还是分析？
- UI 是否确实提高了探索效率？
- 一个探索动作的相关代码是否集中？
- 是否只暴露了值得跨 cell 复用的名字？
- 有没有段逻辑更适合 module？
- UI 可删一半是否更清楚？

## 可选检查器
- `uvx marimo check notebook.py`
- `python scripts/marimo_lint.py notebook.py --json`

`scripts/marimo_lint.py` 仅作为启发式提示，用来捕捉“值得再看一眼”的潜在问题，不当最终质量裁判。

设计模式和 GitHub 样本参见 `references/design-patterns.md`。
