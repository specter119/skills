# Marimo Notebook Design Patterns

这份文档沉淀当前样本池里值得吸收进 skill 的设计模式。

目标不是罗列 API，而是回答：

- 什么样的 notebook 结构更符合 `EDA / prototype-first`
- 哪些模式说明 notebook 还在“探索空间”内
- 哪些模式说明应该开始抽 helper 或 module

## 1. Create Stable Seams Early

### Pattern

先定义稳定 helper，再在后续 cell 中组合它们：

- `load_*`
- `build_*`
- `show_*`
- `annotate_*`

### Why it works

- notebook 主线更清楚
- 用户知道应该改哪里来适配自己的数据
- 后续交互和展示不会直接吞掉分析逻辑

### Example

来源：

- `explore_high_dimensional_data.py`

这个 notebook 先定义：

- `load_data`
- `embed_data`
- `scatter_data`
- `show_selection`

后面才把 embedding、chart、selection drill-down 串起来。

### Skill implication

如果你在写一个可以被用户替换数据源、嵌入算法、展示方式的 notebook，优先先定义 seam，再写 orchestration cell。

## 2. Keep UI Cells Thin

### Pattern

UI cell 主要负责：

- 生成 widget
- 包装 chart / table / rendered output
- 读取 `.value`

不要在同一个 UI cell 里继续塞大量数据清洗、过滤、状态同步。

### Why it works

- control 和 analysis 的边界清楚
- UI 更新更容易追踪
- notebook 不容易长成 notebook-local component

### Example

来源：

- `explore_high_dimensional_data.py`

`mo.ui.altair_chart(...)` 和 `mo.ui.table(...)` 分别只承担薄适配角色。

### Counterexample

来源：

- `laurium-prompt_engineering.py`

多个 cell 同时承担：

- 配置 UI
- 分阶段 reveal
- 文案说明
- 参数 wiring

这已经更接近 app flow，而不是轻量原型。

## 3. Close One Exploration Loop Locally

### Pattern

一个探索动作的：

- control
- derived result
- output

尽量保持在相邻 cell，最好局部闭合。

### Why it works

- 降低 `ui-scatter`
- 读者不需要跨很多 cell 才知道某个控件影响什么
- 参数试验的反馈路径更短

### Example

来源：

- `explore_high_dimensional_data.py`
- `interactive-matrices.py`

它们都把“小交互 + 对应输出”放得比较近。

### Counterexample

来源：

- `nlp_span_comparison.py`

这个 notebook 本身是好的，但 `index` UI 和实际使用位置偏远，所以 `ui-scatter` 仍然会命中。

### Skill implication

不要把“参数定义”放在 notebook 前面很远，再让多个下游 cell 分散消费。

## 4. Let the Notebook Orchestrate, Let Modules Own Capability

### Pattern

notebook 负责：

- 用户输入
- 状态 wiring
- 分析流程编排
- 展示组合

module / helper 负责：

- 领域逻辑
- 可复用算法
- 图表构建
- widget 组件

### Why it works

- notebook 保持 prototype-first
- 稳定能力不会继续膨胀在 notebook 里
- 可复用边界更清楚

### Example

来源：

- `bennet-meyers-notebook.py`

它已经把一部分能力沉到 `modules/`，而 notebook 保留了 orchestration 和 state wiring。

### Skill implication

当你发现某段逻辑已经可以被命名为“能力”而不是“本次分析步骤”，就该离开 notebook。

## 5. Multi-State Coordination Is an Extraction Signal

### Pattern

下面这些通常不是“再坚持一下 notebook 就好”的信号，而是抽模块的信号：

- 多组 `mo.state`
- 动态 UI collection
- 参数预填 / 参数同步
- add/remove controls
- 同一组 state 被多个 cell 共同维护

### Why it works

这类逻辑通常已经在形成组件协议：

- 输入是什么
- 内部状态是什么
- 输出是什么

只是还没被正式提炼。

### Example

来源：

- `bennet-meyers-notebook.py`

它在 problem、component、parameter 之间维护了多组状态，这正是 module boundary 的明确信号。

### Skill implication

当 notebook 开始做 state coordination，不要默认继续长代码；先评估是否该抽到 `widgets.py`、`components.py` 或领域模块。

## 6. Progressive Disclosure Can Help, But It Is Not the Default

### Pattern

`mo.stop(...)`、表单提交后逐段 reveal、阶段性提示，对以下场景有帮助：

- step-by-step workflow
- 高依赖顺序的配置流
- 用户容易漏填关键参数

### Why it works

- 可以减少用户在错误状态下继续探索
- 能把复杂操作拆成更清楚的阶段

### Example

来源：

- `laurium-prompt_engineering.py`

它把 notebook 做成了分阶段流程，适合 prompt engineering workflow。

### Risk

这类模式很容易把 notebook 推成 mini app。

### Skill implication

只在任务本身真的是 workflow / wizard 时用；默认 EDA notebook 不应该一上来就按这个方向长。

## 7. Repeated Presentation Skeletons Mean the Pattern Is Stabilizing

### Pattern

当 notebook 出现很多相似 cell：

- 相似筛选
- 相似 groupby / aggregation
- 相似图表骨架
- 只换字段或颜色

通常说明模式已经稳定。

### Why it works

这是抽 helper 的成熟信号，而不是继续复制的理由。

### Example

来源：

- `goodreads-eda.py`
- `polars_intro.py`

它们都包含大量相似展示 skeleton。

### Skill implication

当模式稳定后，优先抽：

- `build_*_chart`
- `compute_*_summary`
- `render_*_panel`

而不是继续堆平行 cell。

## 8. Long Narrative Cells Need Different Treatment From App-Like Cells

### Pattern

不是所有长 cell 都是坏味道。

两类长 cell 要区分：

1. narrative / teaching cell
2. app-like / pseudo-component cell

### Why it matters

第一类主要是在解释、展示、教学；第二类则在承担组件职责。

### Examples

更像 narrative / teaching：

- `polars_intro.py`
- `akatsuki-tutorial.py`
- `xdsl.py`

更像 app-like / pseudo-component：

- `laurium-prompt_engineering.py`
- `monitoring-ghg-emissions.py`

### Skill implication

写 notebook 时，不要因为 cell 稍长就机械拆散；先判断它是在讲解，还是在偷偷承载组件逻辑。

## Summary

最值得固化进 skill 主文档的只有这些短规则：

- create stable seams early
- keep UI cells thin
- close one exploration loop locally
- let notebooks orchestrate
- treat multi-state coordination as an extraction signal
- use progressive disclosure sparingly

其余细节和例子放在这里，作为写作和评审时的支撑材料。
