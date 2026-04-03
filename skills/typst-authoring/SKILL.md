---
name: typst-authoring
description: >
  Provide Typst technical guidance for writing, compiling, and debugging Typst documents,
  including package selection and diagram solution choice. Use when the task is Typst syntax,
  toolchain usage, Touying/report implementation, or diagram rendering inside Typst.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Typst Authoring

负责 **Typst 的技术实现层**，不负责 slides / reports 的叙事设计。

## 适用边界

### 应该路由到这里

- Typst 语法、编译、调试
- Touying slides 的技术实现
- Report 模板、排版、导出
- 在 Typst 中选择和实现 diagram 方案

### 不应该路由到这里

- slide 的叙事主线与视觉方向
- report 的论证结构与内容框架
- 插图生成

## 执行骨架

1. 先按 `references/workflow.md` 走 diagnostics → compile → output check 的循环。
2. 再按文档类型分流：slides 看 `references/touying.md`，reports 看 `references/report.md`，diagrams 看 `references/diagraph.md`。
3. 包版本不确定时优先查最新资料，不依赖硬编码旧版本。

## 参考地图

- `references/workflow.md`: 核心工作流、常用命令、版本管理
- `references/touying.md`: Touying slides
- `references/report.md`: Typst 报告实现
- `references/diagraph.md`: diagram 方案与最佳实践
- `evals/trigger-cases.md`: 最小触发样例
- `reports/optimization-notes.md`: 本轮重构判断

## 输出契约

- 默认给出可编译的 Typst 实现或明确的修复建议
- 必要时附上应运行的诊断 / 编译命令
