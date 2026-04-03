# Workflow

## Phase 1: Analyze

1. Inventory: 枚举所有材料
2. Classify: 按文件 / 主题 / 章节 / batch 分组
3. Plan: 决定并行度与输出结构

输出结构建议：

```plain
{working_dir}/thorough-digest/{task-slug}/
├── _inputs/
├── group-a/findings.md
├── group-b/findings.md
└── synthesis.md
```

## Phase 2: Parallel Process

每个 sub-agent 必须拿到：

- 明确 item list
- 处理指令
- 输出路径

关键约束：

- Process EVERY item
- Do NOT skip any items
- Each item gets its own section

## Phase 3: Synthesize

1. Collect 全部 findings
2. 检查是否有漏项或缺口
3. 需要时触发 `deep-research`
4. 输出综合报告

## 分组策略

| Strategy | When to Use |
| --- | --- |
| By file | 每个文件相互独立 |
| By topic | 材料天然按主题聚类 |
| By section | 单大文件可切章节 |
| By batch | 大量均质材料均分 |
