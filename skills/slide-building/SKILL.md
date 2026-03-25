---
name: Slide Building
description: >
  Designs slide narrative frameworks and visual layouts.
  Use when creating slides, presentations, or pitch decks.
  Applies Nancy Duarte, Edward Tufte, Gestalt principles, and presentation design expertise.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Slides

Focus on **narrative framework** and **visual design** for presentations. For technical implementation, refer to `typst-authoring` skill.

## Knowledge Activation

Invoke these knowledge domains when generating slides (activation prompts, not rules):

| Domain        | Authority Sources                                                      | Key Concepts                                                     |
| ------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Narrative** | Nancy Duarte (_Resonate_), Chip Heath (_Made to Stick_), Barbara Minto | Story arc, SUCCESs principles, Pyramid principle                 |
| **Visual**    | Robin Williams, Edward Tufte, Gestalt psychology                       | CRAP principles, data-ink ratio, proximity/similarity/continuity |
| **Cognitive** | John Sweller                                                           | Cognitive load, chunking, progressive disclosure                 |
| **Business**  | McKinsey/BCG style                                                     | Assertion-Evidence structure, So What test                       |

## Workflow

```plain
Phase 0: Research (BEFORE any slide work)
├── Invoke deep-research skill for topic investigation
├── Verify research/sources/ has raw materials
└── Ensure 2-3 pages of research per slide page
      ↓
Phase 1: Pre-check
├── Audience, medium, duration, goal
└── Review research materials for content readiness
      ↓
Phase 2: Outline
├── Design narrative structure based on research
├── 大纲验证 + 页数估算
└── Freeze outline after user confirmation
      ↓
Phase 2.5: Oracle Audience Review (RECOMMENDED)  ← NEW
├── Delegate to @oracle: 扮演目标听众批判性审视
├── 验证: Hook、Pain Point、Story Arc、So What
└── 处理反馈后再进入内容生成
      ↓
Phase 3: Design System
└── Colors + typography + reusable components
      ↓
Phase 4: Content Generation
├── Transform research → slides (numbers, insights, cases)
├── Each slide traces back to research/sources/
└── Generate Typst code (technical details: typst-authoring skill)
      ↓
Phase 4.5: Oracle Content Review (OPTIONAL)  ← NEW
├── 初稿完成后，委托 @oracle 评估说服力
└── 特别检查: Evidence 是否充分、Takeaway 是否可行动
      ↓
Phase 5: Compilation & Validation
├── tinymist diagnostics → typst compile
└── 结构完整性检查: 预期页数 vs 实际页数
      ↓
Phase 6: Visual Review
├── pdftoppm → look_at 逐页检查
└── Scoring + Iterate until ≥ 42 分
```

## Agent Delegation

**slide-building skill 自身需要委托的能力**（这些是 slide-building skill 没有的能力，需要其他 agent 补充）：

| Phase             | Delegate To                | When                                       |
| ----------------- | -------------------------- | ------------------------------------------ |
| Outline Review    | `@oracle`                  | 大纲冻结前，扮演听众批判性审视             |
| Content Review    | `@oracle`                  | 内容完成后，评估说服力和切入点             |
| Visual Polish     | `@frontend-ui-ux-engineer` | 视觉优化，布局调整                         |
| Style Consistency | `@frontend-ui-ux-engineer` | genimg 生成多张图时保持风格统一 |

### Oracle Audience Review (Phase 2.5 & Phase 4.5)

委托 Oracle 扮演目标听众进行批判性审视。**On-demand 触发**，不是每次都需要。

| 时机         | 触发条件               | 目的                          |
| ------------ | ---------------------- | ----------------------------- |
| **大纲审视** | 大纲完成、冻结前       | 验证叙事主线和切入点          |
| **内容审视** | 初稿完成后             | 评估说服力、信息密度、So What |
| **迭代困境** | 评分停滞、不知如何改进 | 获得新视角突破                |

详细的 Prompt 模板、Review Focus 说明、使用方法见 `references/oracle-delegation.md`。

**核心心态**：Oracle 的批评 = 真实听众可能的反应。不是「AI 不理解」，而是「如果听众也不理解怎么办」。

### Visual Polish Delegation (Phase 6)

内容生成完成后，委托 `@frontend-ui-ux-engineer` 进行视觉优化。

详细的委托引导、Prompt 模板、术语验证清单见 `references/frontend-delegation.md`。

**核心要点**：

1. 切换思维：演示设计师，不是 Web UI 工程师
2. 指定 Slide 类型：演讲型 / 商业型 / 技术型
3. 禁止 Dashboard 模式（Card 堆砌、等分 grid）

### GenImg Style Consistency

当使用 `genimg` skill 生成多张图片时，genimg 本身是 one-shot 工作，无法保持风格统一。此时需要 slide-building skill 自己管理风格一致性：

1. 先生成一张定义风格的基准图
2. 记录风格参数（配色、线条粗细、图标风格）
3. 后续图片在 prompt 中显式约束这些参数
4. 或委托 `@frontend-ui-ux-engineer` 审阅整体风格一致性

---

# Phase 1: Pre-Generation

## Pre-Generation Checklist

Clarify these before generating slides (ask user if not provided):

1. **Audience** — Determines terminology depth, information density, persuasion strategy
2. **Medium** — Determines font size, contrast, density (cognitive load theory)
3. **Duration** — Determines page count and pacing (Nancy Duarte: ~1-2 min per slide)
4. **Core Goal** — Determines narrative framework (persuade/inform/educate/report)

## Narrative Framework Reference

| Goal               | Framework                            | Source                  |
| ------------------ | ------------------------------------ | ----------------------- |
| Business proposal  | Problem-Solution-Impact              | McKinsey/BCG consulting |
| Pitch deck         | 10-20-30 rule                        | Guy Kawasaki            |
| Case sharing       | STAR method                          | Behavioral interview    |
| Training           | Story arc, STAR moments              | Nancy Duarte            |
| Technical proposal | Status-Challenge-Solution-Validation | Engineering culture     |

These are references, not templates. Adapt based on content and audience.

---

# Phase 2: Planning

## 大纲验证原则

**大纲是 slide 的骨架，骨架错了，肉填得再好也没用。**

### 大纲验证 Checklist

- [ ] 叙事主线清晰（能用一句话概括整个 slide 在讲什么）
- [ ] 各部分有因果关系（不是并列的功能点）
- [ ] 符合听众关心的问题（不是我想讲的，是他们想听的）
- [ ] 经验分享类：围绕"我的经验"而非"功能罗列"

### 何时需要重新验证大纲

| 信号                             | 行动                           |
| -------------------------------- | ------------------------------ |
| 用户说"方向不对"                 | 停止内容生成，重新讨论大纲     |
| 用户说"这不是重点"               | 询问真正的重点是什么，调整大纲 |
| 用户提供新信息改变了问题定义     | 基于新理解重写大纲             |
| 发现之前调研的信息与新大纲不匹配 | 重新调研，不要硬套旧内容       |

## 页数估算

**在大纲阶段就估算页数，避免后期大改。**

经验法则（Nancy Duarte: ~1-2 min per slide）：

- 每个 Part 转场：1 页
- 每 2 个独立概念：1 页
- 对比（Before/After）：1 页
- 架构/流程图：1 页
- Demo/截图：每个 1 页
- Takeaway + Q&A：2 页

**公式**：目标页数 ≈ 转场页 + 内容点数 × 0.6（适用于 10-30 分钟演讲）

---

# Phase 3: Design System

**在写任何 slide 内容之前，先建立设计系统。**

为什么：

- **Gestalt 相似性原则**：相似的视觉元素被感知为相关
- **认知负荷理论**：一致的视觉语言减少处理成本
- **迭代效率**：修改一处颜色 = 全局生效

设计系统应包含：

1. 颜色变量（primary, accent, success, error, muted）
2. 字体层级（heading, body, caption, code）
3. 可复用组件函数（card, badge, icon 等）

## Typography System

**字体是信息层级的骨架。** 遵循 Robert Bringhurst (_The Elements of Typographic Style_) 和 Matthew Butterick (_Practical Typography_) 原则。

### 字体选择原则

| 场景         | 推荐字体类型 | 具体建议                                   |
| ------------ | ------------ | ------------------------------------------ |
| **屏幕演示** | Sans-serif   | Inter, Source Sans, Noto Sans, Arial       |
| **打印文档** | Serif        | Source Serif, Noto Serif, Georgia          |
| **代码块**   | Monospace    | JetBrains Mono, Fira Code, Source Code Pro |
| **中文**     | 思源系列     | Source Han Sans/Serif, Noto Sans/Serif CJK |

**跨平台安全字体**（优先使用，避免渲染差异）：

- Sans: `"Inter", "Noto Sans", "Source Sans 3", "Arial"`
- Serif: `"Source Serif 4", "Noto Serif", "Georgia"`
- Mono: `"JetBrains Mono", "Fira Code", "Consolas"`

**避免**：

- `sans-serif` / `serif` 等通用族名（各平台 fallback 不一致）
- 过于个性化的字体（可读性优先）
- 同一 slide 超过 2 种字体族

### 字体大小层级

**基于模块化比例 (Modular Scale)**，推荐 1.25 或 1.333 比例：

| 层级        | 用途          | 推荐尺寸 (16-9 屏幕) | 比例      |
| ----------- | ------------- | -------------------- | --------- |
| **Display** | 封面/转场标题 | 32-48pt              | 2.5×      |
| **H1**      | 页面标题      | 20-24pt              | 1.5×      |
| **H2**      | 小节标题      | 16-18pt              | 1.125×    |
| **Body**    | 正文内容      | 14-16pt              | 1× (基准) |
| **Caption** | 注释/来源     | 10-12pt              | 0.75×     |
| **Code**    | 代码块        | 9-11pt               | 0.7×      |

**行高 (Leading)**：

- 正文：1.4-1.6× 字体大小
- 标题：1.2-1.3× 字体大小
- 紧凑布局：1.2× 可接受

**Typst 示例**：

```typst
// Typography System
#let t-display = 36pt
#let t-h1 = 20pt
#let t-h2 = 14pt
#let t-body = 12pt
#let t-caption = 9pt
#let t-code = 10pt

#set text(font: ("Inter", "Noto Sans", "Arial"), size: t-body)
#set par(leading: 0.65em)  // ~1.5× line height
```

### 字重与强调

| 目的           | 方法            | 避免                     |
| -------------- | --------------- | ------------------------ |
| **强调关键词** | Bold (`*text*`) | 斜体（中文无效）、下划线 |
| **区分层级**   | 字重 + 大小配合 | 仅靠颜色区分             |
| **代码/术语**  | Monospace       | 引号                     |

**层级组合示例**：

- 标题：Bold + 大字
- 正文：Regular
- 次要信息：Regular + 灰色 (muted)
- 强调：Bold（同色）或 Accent 色

## Color System

**颜色传达语义和情绪。** 遵循 Josef Albers (_Interaction of Color_)、WCAG 可访问性标准。

### 语义色板设计

每个 slide 设计系统需要定义以下语义颜色：

| 语义           | 用途                   | 选色建议            |
| -------------- | ---------------------- | ------------------- |
| **Primary**    | 品牌色、标题、主要强调 | 饱和度中等，可辨识  |
| **Accent**     | 次要强调、CTA、高亮    | 与 primary 形成对比 |
| **Success**    | 正面结果、完成状态     | 绿色系              |
| **Error**      | 负面结果、警告         | 红色系              |
| **Muted**      | 次要信息、注释         | 灰色系              |
| **Surface**    | 卡片背景、容器         | 接近白色            |
| **Background** | 页面背景               | 纯白或极浅灰        |

**Typst 示例**：

```typst
// Color System (Material Design inspired)
#let c-primary = rgb("#1565C0")   // Blue 800
#let c-accent = rgb("#E65100")    // Orange 800
#let c-success = rgb("#2E7D32")   // Green 800
#let c-error = rgb("#C62828")     // Red 800
#let c-muted = rgb("#757575")     // Grey 600
#let c-surface = rgb("#FFFFFF")   // White
#let c-bg = rgb("#FAFAFA")        // Grey 50
#let c-text = rgb("#212121")      // Grey 900
#let c-light = rgb("#E3F2FD")     // Blue 50 (for highlights)
```

### 色彩对比与可访问性

**WCAG 2.1 对比度要求**（遵循 Web Content Accessibility Guidelines）：

| 文字类型       | 最小对比度 | 推荐对比度 |
| -------------- | ---------- | ---------- |
| 正文 (14pt+)   | 4.5:1      | 7:1        |
| 大文字 (18pt+) | 3:1        | 4.5:1      |
| 装饰性元素     | 无要求     | —          |

**常见问题**：

- 浅灰文字 (#999) 在白底 (#FFF) 对比度仅 2.8:1 → **不合格**
- 推荐 muted 色：#757575 在白底对比度 4.6:1 → **合格**

**检查工具**：

- 在线：[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- 原则：宁可深一点，不要浅到看不清

### 色彩搭配原则

**60-30-10 法则**（室内设计经典原则，适用于视觉设计）：

- **60%**：主色调（背景、大面积）→ Background, Surface
- **30%**：辅助色（内容区域）→ Primary, Text
- **10%**：强调色（焦点元素）→ Accent, Success/Error

**配色禁忌**：

- 红+绿直接相邻（色盲不友好）
- 高饱和色大面积使用（视觉疲劳）
- 超过 4 种主要颜色（认知负担）

### 色彩心理与应用

| 色系 | 心理联想         | 适用场景           |
| ---- | ---------------- | ------------------ |
| 蓝色 | 专业、信任、稳定 | 商业报告、技术分享 |
| 绿色 | 成长、成功、环保 | 正面数据、完成状态 |
| 橙色 | 活力、警示、创意 | CTA、重要提示      |
| 红色 | 紧急、错误、热情 | 警告、负面数据     |
| 灰色 | 中性、次要、专业 | 背景、次要信息     |

**技术分享推荐配色**：

- 主色：蓝色系（专业感）
- 强调：橙色系（对比突出）
- 避免：过多暖色（分散注意力）

## Design System 完整模板

```typst
// ============================================
// Design System
// ============================================

// Typography
#let t-display = 36pt
#let t-h1 = 20pt
#let t-body = 12pt
#let t-caption = 9pt

// Colors (Material Design based)
#let c-primary = rgb("#1565C0")
#let c-accent = rgb("#E65100")
#let c-success = rgb("#2E7D32")
#let c-error = rgb("#C62828")
#let c-muted = rgb("#757575")
#let c-surface = rgb("#FFFFFF")
#let c-bg = rgb("#FAFAFA")
#let c-text = rgb("#212121")
#let c-light = rgb("#E3F2FD")

// Global settings
#set text(font: ("Inter", "Noto Sans", "Arial"), size: t-body, fill: c-text)
#set par(leading: 0.65em)
#set page(fill: c-bg)

// Reusable components
#let card(content, fill: c-surface, stroke: none) = {
  rect(width: 100%, fill: fill, stroke: stroke, radius: 6pt, inset: 0.8em, content)
}

#let badge(label, color: c-primary) = {
  rect(fill: color, radius: 3pt, inset: (x: 6pt, y: 3pt),
    text(fill: white, weight: "bold", size: 0.8em, label))
}

#let check = text(fill: c-success)[✓]
#let cross = text(fill: c-error)[✗]
```

---

# Phase 4: Content

## Context → Slide Transformation

| Problem         | Cause                                       |
| --------------- | ------------------------------------------- |
| Feature list    | Copied research structure verbatim          |
| Jargon overload | Not translated for audience                 |
| Missing numbers | Numbers exist in research but not extracted |
| No story        | Pure logical listing                        |

**Transformation steps**:

1. Extract key numbers → build Before/After comparisons
2. Identify core insights → "solves what pain point" not "has these features"
3. Select strongest cases → 1-2 deep dives, others brief
4. Build narrative arc → Hook → Pain → Solution → Evidence → CTA

## Information Density

**Information density = actionable insights per slide**

Evaluate each slide for:

- Specific numbers (not "improve efficiency" but "save XX minutes")
- Comparisons (Before/After, current/target)
- Scenarios ("When customer sends email...")
- So What (audience knows what to think/do after reading)
- Necessity (if removing doesn't affect understanding, it's noise)

### Number Extraction Techniques

How to convert vague concepts into concrete numbers:

| 模糊表述           | 数字化方法   | 示例                        |
| ------------------ | ------------ | --------------------------- |
| "容易产生重复代码" | 估算倍数     | "3× duplicate logic"        |
| "上下文有限"       | 引用技术参数 | "~8K tokens / context"      |
| "长期积累问题"     | 时间维度     | "6mo until rewrite"         |
| "支持多种选择"     | 计数         | "75+ providers"             |
| "初期投入后收益"   | ROI 对比     | "30min setup → weeks saved" |

**数字类型处理**：

- 精确数字：必须有来源（官方文档、测量数据）
- 估算数字：标记 `~` 或 "approximately"
- 量级数字（3×, 75+）：用于强调规模，不需精确

## Placeholder 处理

**检测信号**：

| 信号                 | 示例                                   |
| -------------------- | -------------------------------------- |
| 明确标记             | "TBD", "TODO", "[placeholder]"         |
| 外部链接作为主要内容 | "详见 example.com/demo"                |
| 未来时态             | "我们将展示..."                        |
| 空架构               | "Experiment 1 / Experiment 2" 但无数据 |

**处理方式**：检测到 placeholder 后，每轮优化时询问用户：

> 「Page X 仍是占位内容：[描述]。要现在补充实际内容，还是保留待后续填充？」

**不自动删除**，由用户决定处理时机。

---

# Phase 5: Visual Design

## Visual Evaluation

After generating slides, evaluate using design knowledge (intuition, not checklist):

**Squint test**: After blurring vision, is the most important content seen first?

- If not → insufficient contrast (CRAP - Contrast)

**Whitespace test**: Is whitespace meaningful breathing room or filler for lack of content?

- Tufte: "data-ink ratio" — every drop of ink should convey information

**Rhythm test**: Flipping through 5 pages, is there visual variation?

- Nancy Duarte: "rhythm" — avoid monotonous repetition

**So What test**: After reading this slide, does audience know what to think/do?

- McKinsey: "one So What per slide"

## Visual Rhythm Component Library

当页面结构单调时，可选用以下组件增加变化：

| 组件类型        | 适用场景     | 视觉效果              |
| --------------- | ------------ | --------------------- |
| `metric()`      | 展示数字     | 大号数字 + 小号标签   |
| `quote-block()` | 引用权威     | 左边框高亮 + 斜体     |
| `timeline`      | 时间演进     | 水平渐变色块          |
| `hub-spoke`     | 中心辐射关系 | 主色块居中 + 周围卡片 |
| `before-after`  | 对比         | 左右分屏 + 箭头       |
| `vertical-flow` | 流程步骤     | 垂直堆叠 + 下箭头     |
| `numbered-list` | 场景列表     | 圆形编号 + 无 card    |

Typst 代码示例见 `references/components.md`。

---

# Phase 6: Iteration

## 结构完整性检查（编译后第一步）

**Typst 内容溢出不报错，会静默换页。** 文字、流程图、架构图、代码块都可能导致：

- 预期 1 页变成 2 页
- 第二页只有溢出内容 + 大片空白
- 页码、标题位置全乱

**必须在美学审阅之前检查**，否则截图看到的问题根源可能是溢出而非设计。

详细检查流程见 `typst-authoring` skill 的 `references/touying.md` → "Page Validation" 章节。

快速检查命令：

```bash
# 1. 预期页数：数源码里的 slide 标题（级别取决于 theme 配置，可能是 == 或 ===）
grep -c "^==+ " slide.typ       # 先看文件里用的是哪种

# 2. 实际页数
pdfinfo slide.pdf | grep Pages

# 3. 如果不匹配，定位溢出位置
pdftotext slide.pdf - | head -200   # 看标题顺序是否符合预期
```

**页数不匹配 → 先修溢出，再看美学。**

## 渲染审阅（结构检查通过后）

**源码评分 ≠ 渲染评分。** 源码看起来结构合理，渲染出来可能布局单调、留白失衡。

### 为什么必须截图审阅

| 源码能看到的 | 源码看不到的 |
| ------------ | ------------ |
| 组件结构     | 实际视觉节奏 |
| 文字内容     | 留白是否失衡 |
| 颜色变量名   | 颜色搭配效果 |
| 布局代码     | 视觉重心位置 |

**结论**：每轮迭代必须基于渲染结果评分，不能只看源码。

### 操作方法

```bash
# 编译后，将 PDF 转为 PNG 逐页审阅（150 DPI 足够）
pdftoppm -png -r 150 slide.pdf /tmp/review/page
# 输出：/tmp/review/page-01.png, page-02.png, ...
```

然后用 `look_at` 工具逐页审阅，检查：

- **视觉节奏**：连续翻 5 页，布局是否有变化？
- **留白平衡**：底部是否大片空白？视觉重心是否偏上？
- **信息密度**：每页是否有实质内容，还是只有标题？

**不要用 Playwright 打开 PDF** — 浏览器渲染不稳定，且无法逐页截取。

## Optimization Scoring Framework

每轮优化后，用以下 5 个维度评分（各 1-10 分，满分 50）：

| 维度                    | 评估问题                                 |
| ----------------------- | ---------------------------------------- |
| **Narrative Structure** | 叙事主线是否清晰，各部分是否有因果关系？ |
| **Information Density** | 每页是否有具体数字/对比/场景？           |
| **Visual Rhythm**       | 连续页面视觉结构是否有变化？             |
| **So What**             | 每页是否让观众知道该想什么/做什么？      |
| **Domain-Specific**     | 是否围绕核心问题/决策/结论展开？         |

**迭代目标**：每轮至少 +3 分，总分 ≥ 42 可交付。

---

# Special: 经验分享类 Slide

这类分享的本质是**传递可复用的经验与决策过程**，不是概念堆砌或资料搬运。

## 必须回答的问题

1. **我遇到了什么问题？**（痛点，与听众共鸣）
2. **我怎么解决的？**（方案 + 实际操作）
3. **效果如何？**（Demo / 截图 / 数据）
4. **你可以怎么用？**（Takeaway，可复制的经验）

## 禁止

| 禁止行为                   | 为什么                       | 应该怎么做                 |
| -------------------------- | ---------------------------- | -------------------------- |
| 功能罗列                   | 像官方文档，听众可以自己看   | 讲"我用这个功能解决了什么" |
| 概念孤立                   | 各部分无因果关系，散点无主线 | 建立因果链：问题→方案→效果 |
| 只讲"做了什么"不讲"为什么" | 细节会变，决策框架可迁移     | 交代约束→权衡→选择→结果    |

## 检查方法

每一页问自己：**"这对听众有什么用？"**

- 如果答案是"了解这个工具有这个功能" → 删除或改写
- 如果答案是"知道遇到类似问题可以这样解决" → 保留

## 方案类分享的内容大纲设计

**先确定要展示的核心点，再决定页数。** 页数是结果，不是目标。

### Step 1: 参考权威材料

介绍一个方案/方法/系统时，先收集权威与一手材料（官方文档/论文/RFC/ADR/事故复盘/基准测试），了解：

- 权威来源如何定义该方案/问题（一句话描述）
- 关键概念/机制有哪些
- 与替代方案的真正差异是什么

避免用自己的理解替代权威定位，容易产生偏差。

### Step 2: 列出核心概念清单

把主题的关键要素列出来（概念/决策/机制/数据/风险），然后筛选：

| 要素                | 是否讲 | 理由                         |
| ------------------- | ------ | ---------------------------- |
| 入门背景/必要前提   | ✅     | 入门必备                     |
| 关键机制/决策 A     | ✅     | 解决痛点 X                   |
| 高级扩展/边界条件 B | ❌     | 听众用不到                   |
| 与替代方案对比      | ⚠️     | 只讲事实差异，不贬低对比对象 |

### Step 3: 根据分享类型选择叙事结构

| 分享类型      | 推荐结构                         | 适用场景            |
| ------------- | -------------------------------- | ------------------- |
| 方案/工具分享 | 问题→解决方案→实践→Takeaway      | "我用 X 解决了 Y"   |
| 踩坑复盘      | 背景→问题→排查→根因→修复→教训    | 线上故障、bug 排查  |
| 技术选型      | 需求→候选→评估维度→对比→决策     | "为什么选 X 不选 Y" |
| 架构演进      | 历史→痛点→新设计→迁移→效果       | 重构、架构升级      |
| 方法论        | 问题定义→核心原则→方法→案例→边界 | "如何做好 X"        |

**选择原则**：根据「听众最想知道什么」选择结构，Part 数量控制在 3-4 个，太多记不住。

## 方案对比的原则

| 禁止               | 应该                     |
| ------------------ | ------------------------ |
| 故意贬低替代方案   | 客观陈述差异             |
| 使用过时信息       | 核实最新状态（搜索验证） |
| "X 只能做 Y"       | "X 侧重 Y，Z 侧重 W"     |
| 主观评价（"更好"） | 适用场景对比             |

**原则**：对比信息与关键事实容易过时，写之前必须检索验证并标注时间点。

---

# Integration

## Skill Integration

```plain
[deep-research skill] → Gather new information from web
         ↓
[thorough-digest skill] → Process existing materials in batch
         ↓
[slide-building skill] → Narrative design + content transformation
         ↓
[typst-authoring skill] → Technical implementation
         ↓
[genimg skill] → AI-generated illustrations (OPTIONAL)
```

## Research Prerequisites (CRITICAL)

**No research = empty slides.** Before any slide generation:

1. **Check `research/` directory** in project folder
2. **If missing or empty**: Invoke research skills first
   - `deep-research` → for gathering new information from web
   - `thorough-digest` → for processing existing local materials
3. **Verify source coverage**: Each slide topic should have corresponding sources

### Expected Research Output

```plain
{project}/research/
├── sources/              # Raw materials (Markdown/HTML/PDF)
│   └── {topic}-{source}-{date}.md
└── notes/                # Extracted key points
    ├── 01-{topic}.md
    └── synthesis.md
```

**Traceability requirement**: Every data point, quote, or claim in slides should trace back to a file in `research/sources/`.

## GenImg Integration (OPTIONAL)

概念插图、封面图等**可选**使用 `genimg` skill。大多数技术分享不需要 AI 生成图片。

### 风格统一（多张图时必须注意）

Gemini 每次独立生成，**不会自动保持风格一致**。

**方法**：

1. 在 prompt 里显式约束配色：`"blue accent #1565C0, white background, clean lines"`
2. 或先生成一张定风格，后续用 edit 模式（`-e base.png`）保持一致

### When to Use

| 用途                   | 用 GenImg | 用 Diagraph/Code |
| ---------------------- | --------- | ---------------- |
| 抽象概念（创新、协作） | ✅        | ❌               |
| 封面/分隔页            | ✅        | ❌               |
| 流程图                 | ❌        | ✅               |
| 架构图                 | ❌        | ✅               |

详细参数和 workflow 见 `genimg` skill。
