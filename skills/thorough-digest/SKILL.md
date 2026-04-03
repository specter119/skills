---
name: thorough-digest
description: >
  Exhaustively review local materials with parallel sub-agents so no item is skipped. Use when a
  user asks to batch process many local files, digest a folder, or synthesize a narrative from
  existing materials rather than searching the web.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep
---

# Thorough Digest

负责 **本地材料的全量处理与并行归纳**，不负责外部网络调研。

## 适用边界

### 应该路由到这里

- 批量处理本地文件、目录、章节或材料集合
- 逐项提取要点，要求不能漏项
- 从既有材料中构建统一叙事或综合报告

### 不应该路由到这里

- 需要去网上补新信息
- 只处理一两份材料
- 主要目标是写 slides 或正式报告，而不是先消化材料

## 执行骨架

1. 先 inventory 全部输入项，确保范围清楚。
2. 按 `references/workflow.md` 决定分组方式和并行策略。
3. 给每个 sub-agent 明确 item list、输出路径和“不许漏项”的约束。
4. 汇总各组 findings，必要时再串联 `deep-research` 补缺口。

## 参考地图

- `references/workflow.md`: 分阶段流程、分组策略、输出结构
- `references/guidelines.md`: 并行粒度、错误处理、最佳实践
- `references/templates.md`: inventory / classify / sub-agent / synthesis 模板
- `evals/trigger-cases.md`: 最小触发样例
- `reports/optimization-notes.md`: 本轮重构判断

## 输出契约

- 默认交付 inventory、分组结果、各组 findings 和最终 synthesis
- 必须能说明总输入数、已处理数和覆盖情况
