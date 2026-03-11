# Frontend Agent Delegation for Slides

委托 `@frontend-ui-ux-engineer` 进行 slide 视觉优化时的指导。

## 核心问题：认知偏差

`frontend-ui-ux-engineer` 的默认心智模型是 **Web UI/Dashboard**：
- Card 组件 → 信息容器
- Grid 布局 → 响应式
- Border + Shadow → 层级区分

这套逻辑用在 Slide 上会变成"方框堆砌"。**必须在 prompt 中切换思维模式。**

## 心智模型对比表

| Web Design (WRONG) | Slide/Print Design (CORRECT) |
|--------------------|------------------------------|
| Responsive layouts | Fixed 16:9 canvas |
| Interactive elements | Static frames |
| Scroll for more | One screen = one message |
| Card 作为默认容器 | 用对齐和留白暗示分组 |
| Dashboard 等分 grid | 视觉节奏变化 |
| Hover/Click 交互 | 无交互，纯静态 |
| Viewport 适配 | 投影仪可读性 |

## Slide 类型与风格

| 类型 | 适用场景 | 风格特征 | 权威参考 |
|------|----------|----------|----------|
| **演讲型** | TED、Keynote、有演讲者 | 极简，大留白，每页一个点 | Garr Reynolds (*Presentation Zen*) |
| **商业型** | 咨询报告、管理层汇报 | 信息密集，结构清晰 | McKinsey/BCG style |
| **技术型** | 技术分享、架构评审 | 混合风格，代码/图表为主 | 工程文化 |

**判断方法**：
- 有演讲者陪同 → 可以极简
- 需独立阅读 → 信息完整
- 主要是代码/架构 → 技术型

## 禁止 vs 必须

| 禁止 | 必须 |
|------|------|
| Card/Box 作为默认容器 | 用对齐和接近暗示关系 |
| Dashboard 风格等分 grid | 用字重和大小建立层级 |
| Skeleton loader / Loading state | 关键数字要大、要突出 |
| Hover effect / Click 交互 | 代码块用深色背景 |
| Responsive / Breakpoint 建议 | 考虑投影仪可读性 |
| 灰框白底的代码块 | 视觉节奏跨页变化 |

## 设计原则（知识唤醒）

| 原则 | 权威来源 | 应用 |
|------|----------|------|
| **Data-ink ratio** | Edward Tufte | 删除不传达信息的视觉噪音 |
| **Gestalt 原则** | 心理学 | 用接近和对齐暗示关系，减少边框依赖 |
| **Visual rhythm** | Nancy Duarte | 连续页面需要视觉变化 |
| **CRAP** | Robin Williams | Contrast, Repetition, Alignment, Proximity |
| **Squint test** | 通用 | 模糊视线后，最重要的内容是否仍可见？ |

## Prompt 模板

```markdown
## Task: Visual Review of Slide Deck (PRESENTATION DESIGN)

**CRITICAL MINDSET:**
你现在是**演示设计师**，不是 Web UI 工程师。

| Web Design (WRONG) | Slide Design (CORRECT) |
|--------------------|------------------------|
| Responsive layouts | Fixed 16:9 canvas |
| Interactive elements | Static frames |
| Card 默认容器 | 对齐和留白暗示分组 |
| Dashboard 等分 grid | 视觉节奏变化 |
| Hover/Loading states | N/A |

**Authority references:** Edward Tufte (data-ink), Nancy Duarte (rhythm), Garr Reynolds (zen), Robin Williams (CRAP)

---

## Slide 类型: [演讲型 / 商业型 / 技术型]

## 禁止
- Card/Box 作为默认容器
- Dashboard 风格等分 grid
- Skeleton loader / Hover state 等 Web 模式
- 灰框白底代码块

## 必须
- 用对齐和接近暗示关系
- 用字重和大小建立层级
- 关键数字要大、要突出
- 代码块用深色背景
- 考虑投影仪可读性（字体 ≥11pt）

---

### Context
- Screenshot location: [path]
- Typst source: [path]
- Total pages: [N]

### Evaluation Criteria
- **Squint test**: 模糊视线，关键信息是否可见？
- **Balance**: 视觉重心是否均衡？
- **Hierarchy**: 眼睛是否自然流向最重要元素？
- **Contrast**: 颜色在投影仪上是否可读？
- **Rhythm**: 跨页是否有视觉变化？

### Output Format
- Overall assessment (2-3 sentences)
- Page-by-page issues with severity and fix
- Top 3 priority fixes

**MUST NOT:** 建议 Web 模式（skeleton loader, hover, responsive 等），改动内容/叙事
**MUST DO:** 专注于投影显示的视觉呈现质量
```

## 验证 Agent 输出

收到建议后检查：

1. **术语验证**：是否出现 Web 术语（skeleton, hover, responsive）？
2. **建议可行性**：是否适用于静态 PDF？
3. **评判标准**：是否基于投影显示而非屏幕显示？

**如果验证失败**，重新委托并强调认知偏差扭转。

## 迭代改进记录

使用后发现的问题，记录于此以持续优化：

- [x] 2026-01: 首次使用时 agent 建议 "skeleton loader"，说明偏差未扭转 → 增加对比表
- [ ] 待验证：Gestalt 子原则中哪些最有效（proximity vs similarity）
- [ ] 待验证：McKinsey/BCG 风格术语是否被正确理解
