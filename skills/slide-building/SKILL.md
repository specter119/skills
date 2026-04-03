---
name: slide-building
description: >
  Design slide narratives, audience-aware outlines, page-by-page deck plans, and visual
  direction for presentations, pitch decks, and talk decks. Use when asked to create or
  improve slides/slides decks/PPT narratives/演示文稿大纲/讲稿型 deck. Excludes deep topic
  research, report writing, and Typst or PPTX implementation details.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Slide Building

负责 **slides 的叙事结构、页面规划、视觉方向**，不负责替代调研 skill、报告写作 skill 或具体排版实现 skill。

## 适用边界

### 应该路由到这里

- 创建演示文稿、pitch deck、技术分享 deck
- 设计 page-by-page 大纲、演讲叙事主线、页数估算
- 优化 slide 的视觉方向、页面类型、信息密度、节奏
- 把已有材料转成适合演示的 slide 结构

### 不应该路由到这里

- 主题资料不足，需要先做调研 → `deep-research`
- 已有资料很多，需要批量消化 → `thorough-digest`
- 主要目标是写报告、论文、长文档 → `report-building`
- 主要目标是 Typst/PPTX/PDF 技术实现 → `typst-authoring` 或具体生成 skill

## 执行骨架

### Phase 0: 检查素材是否够支撑 deck

- 若缺少研究或原始材料，先调用研究类 skill
- 若用户直接给了笔记、文档、录音纪要，先抽取可用证据与案例
- 原则：没有证据的 slide 很容易退化成空洞口号

### Phase 1: 明确生成约束

至少确认以下 4 项，缺失时主动问：

1. 听众是谁
2. 使用媒介是什么（投影 / 线上 / 独立阅读）
3. 时长或目标页数是多少
4. 核心目标是什么（说服 / 汇报 / 教学 / 复盘）

### Phase 2: 先定大纲，再写页面

- 先给一句话主线，再拆成 3-5 个部分
- 先估算页数，再进入内容生成
- 每一页必须归类为明确的页面类型，避免“所有页都长得一样”
- 大纲冻结前，可按需委托 `@oracle` 做听众视角审视

页面类型与常见版式见：
- `references/slide-types.md`

### Phase 3: 建立设计系统

- 先定配色、字体层级、间距尺度、可复用组件
- 技术型/商业型/演讲型 deck 应使用不同密度和节奏
- 具体规则与 Typst starter 见：
  - `references/design-system.md`
  - `references/components.md`

### Phase 4: 生成 slide 方案

把材料从“资料结构”转成“演示结构”：

- 提炼 hook、pain point、so what
- 提取数字、对比、案例，不照搬原始资料目录
- 为每页写清楚：标题、核心 takeaway、证据、推荐版式
- 需要时再把结果交给 `typst-authoring` 或具体生成器实现

详细流程见：
- `references/workflow.md`

### Phase 5: 渲染审阅与迭代

- 先做结构检查，再做视觉检查
- 迭代重点：信息密度、视觉节奏、So What、投影可读性
- 视觉审阅和评分框架见：
  - `references/review-and-qa.md`
  - `references/frontend-delegation.md`

## 输出契约

默认至少交付以下 3 项中的 2 项，按用户需求裁剪：

1. 演示主线与受众定位
2. page-by-page 大纲或页面规格表
3. 视觉方向说明（配色、字体、页面类型、组件建议）

如用户继续推进到实现阶段，再额外交付：

4. 给 `typst-authoring` / PPTX 生成器的实现 handoff

## 委托策略

| 场景 | 委托对象 | 用途 |
| --- | --- | --- |
| 大纲冻结前 | `@oracle` | 扮演目标听众，审视 hook、痛点、主线 |
| 内容初稿后 | `@oracle` | 审视说服力、证据、行动性 |
| 视觉 polish | `@frontend-ui-ux-engineer` | 按 slide 而非 web UI 心智优化渲染效果 |
| 多张 AI 图片 | `genimg` + `@frontend-ui-ux-engineer` | 先定基准风格，再审阅一致性 |

委托模板见：

- `references/oracle-delegation.md`
- `references/frontend-delegation.md`

## 参考地图

| 文件 | 用途 |
| --- | --- |
| `references/workflow.md` | 详细执行流程、页数估算、占位内容处理 |
| `references/slide-types.md` | 页面类型、常见版式、失败信号 |
| `references/design-system.md` | 字体、配色、密度、Typst starter |
| `references/review-and-qa.md` | 结构检查、渲染审阅、评分框架 |
| `references/components.md` | 常用视觉组件代码片段 |
| `references/oracle-delegation.md` | Oracle 听众评审模板 |
| `references/frontend-delegation.md` | 视觉 polish 委托模板 |
| `evals/trigger-cases.md` | 路由正例 / 反例 / 近邻样例 |
| `reports/optimization-notes.md` | 本轮优化假设、差异与后续验证点 |

## 与其他 Skill 的协作

```plain
[deep-research / thorough-digest]
          ↓
[slide-building]
          ↓
[typst-authoring / PPTX generator]
          ↓
[frontend visual review / genimg]
```

原则：

- `slide-building` 先回答“讲什么、怎么讲、每页长什么样”
- 其他 skill 再回答“怎么实现、怎么编译、怎么生成图片”
