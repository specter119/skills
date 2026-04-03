# Trigger Cases

用于后续人工或脚本化评估 `slide-building` 的路由边界。

## Should Trigger

1. 帮我做一份给管理层汇报的 12 页 AI 项目复盘 deck，先出 page-by-page 大纲。
2. 我有一堆调研笔记，想整理成技术分享 slides，重点是叙事和每页怎么讲。
3. 请优化这个 pitch deck 的主线，感觉页面都有内容但没有节奏。
4. 为一次 20 分钟内部分享设计演示结构，听众是后端工程师。
5. 给我一个商业型 slide 的视觉方向方案，不用先写 Typst。

## Should Not Trigger

1. 帮我深入研究 MCP 和 A2A 的区别，并整理成报告。
2. 把这篇技术方案写成正式文档，输出 Markdown。
3. 修一下这个 Typst deck 的编译错误，`touying-slide` 宏报错了。
4. 用 PptxGenJS 直接生成一个可运行的 PPTX 文件。
5. 批量总结 `./meeting-notes` 目录里的所有会议记录。

## Near Neighbors

1. 我想做一份 slides，但目前没有任何素材，先帮我调研这个主题。
   期望：先 `deep-research`，再进入 `slide-building`

2. 我有一份汇报材料，既可能做成报告，也可能做成 deck，帮我决定结构。
   期望：根据输出介质区分 `report-building` 和 `slide-building`

3. 我已经有完整大纲和视觉方案，只差 Typst 实现。
   期望：优先 `typst-authoring`

4. 我想优化一份现有 slides 的视觉呈现，但不改叙事内容。
   期望：`slide-building` 可接，但应偏向 Phase 5 审阅与视觉策略
