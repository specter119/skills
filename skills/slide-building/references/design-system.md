# Design System

在写任何一页之前，先定视觉系统。这样能降低认知负担，也能提升后续迭代效率。

## 1. 字体层级

建议最多使用 2 个字体族：

- Sans：适合屏幕演示
- Mono：仅用于代码或术语

推荐优先级：

- Sans: `Inter`, `Noto Sans`, `Source Sans 3`, `Arial`
- Serif: `Source Serif 4`, `Noto Serif`, `Georgia`
- Mono: `JetBrains Mono`, `Fira Code`, `Consolas`

### 推荐字号

| 层级 | 用途 | 推荐尺寸 |
| --- | --- | --- |
| Display | 封面 / 转场 | 32-48pt |
| H1 | 页面标题 | 20-24pt |
| H2 | 小节标题 | 16-18pt |
| Body | 正文 | 14-16pt |
| Caption | 注释 / 来源 | 10-12pt |
| Code | 代码块 | 9-11pt |

规则：

- 标题行高 1.2-1.3
- 正文行高 1.4-1.6
- 强调用字重优先，不依赖颜色

## 2. 语义色板

至少定义：

- `primary`
- `accent`
- `success`
- `error`
- `muted`
- `surface`
- `background`
- `text`

推荐原则：

- 蓝色适合技术与商业
- 橙色适合作为少量强调
- muted 文本不要浅到投影时看不清
- 主色不要超过 4 种

### 可读性

对比度参考：

- 正文至少 4.5:1
- 大字至少 3:1

经验上，`#757575` 在白底通常比 `#999999` 安全。

## 3. 密度与风格

根据 deck 类型选择密度：

| 类型 | 特征 | 建议 |
| --- | --- | --- |
| 演讲型 | 一页一个观点，依赖讲者口播 | 留白大、信息轻 |
| 商业型 | 需要独立阅读 | 结构清晰、信息更密 |
| 技术型 | 代码、架构、流程较多 | 混合密度，强调图示和证据 |

### 风格选择

可借鉴 `pptx-generator` 的风格分层：

- Sharp: 适合数据密集、正式报告
- Soft: 适合大多数商业 deck
- Rounded: 适合产品介绍、较友好的视觉语气

## 4. 可复用组件

优先准备：

- badge
- card
- metric
- quote block
- timeline
- before/after
- vertical flow

示例代码见 `components.md`。

## 5. Typst Starter

```typst
#let t-display = 36pt
#let t-h1 = 20pt
#let t-h2 = 16pt
#let t-body = 12pt
#let t-caption = 9pt

#let c-primary = rgb("#1565C0")
#let c-accent = rgb("#E65100")
#let c-success = rgb("#2E7D32")
#let c-error = rgb("#C62828")
#let c-muted = rgb("#757575")
#let c-surface = rgb("#FFFFFF")
#let c-bg = rgb("#FAFAFA")
#let c-text = rgb("#212121")

#set page(fill: c-bg)
#set text(font: ("Inter", "Noto Sans", "Arial"), size: t-body, fill: c-text)
#set par(leading: 0.65em)
```

## 6. 常见失误

- 只定义颜色，不定义层级和间距
- 所有页都用同一套卡片布局
- 代码块不做深浅对比，导致投影难读
- 用 Web UI 思维做 slide，出现 dashboard 式平均分栏
