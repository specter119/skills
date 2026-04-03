# Workflow

## 默认顺序

1. 先写静态分析版本，确认问题和输出形式
2. 只有当交互明显提升探索效率时，才加入少量 UI
3. 避免把 notebook 当作长期承载复杂状态编排的地方
4. 某段逻辑或 UI 已稳定复用时，再抽到 module

## Hard Guardrails

### 1. 不要把 notebook 做成零散 UI 开发

警惕这些信号：

- 连续多个 cell 都只在定义 UI
- 一个简单探索动作被拆成很多相互依赖的 UI cells
- 交互只是为了“看起来更像产品”，不是为了分析效率

### 2. 让 UI 靠近它控制的分析

- control、derived result、output 尽量保持相邻
- 避免前面定义控件，后面很远才消费
- 避免一个参数影响链条长到难以追踪

### 3. 只导出稳定名字

默认只暴露：

- 需要被其他 cell 复用的数据
- 稳定 helper functions
- 当前 cell 的主要结果

中间值优先用 `_tmp`、`_filtered`、`_chart` 之类的局部名字。

### 4. 模式稳定后再抽象

这些通常是 extraction signal：

- 同一段 UI / logic 开始重复
- 已经形成明确输入输出边界
- 维护它需要很长的 cell 或复制粘贴
- 你已经在把 notebook 当 app source

## 完成前自检

- 这份 notebook 的主任务还是分析吗？
- UI 是否真的提升了探索效率？
- 一个探索动作是否足够集中？
- 是否只暴露了值得跨 cell 复用的名字？
- 有没有内容已经更适合移到 module？

## 检查命令

```bash
uvx marimo check notebook.py
python scripts/marimo_lint.py notebook.py --json
```
