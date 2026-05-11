# Report 技术参考

> 本文档提供 Typst 报告生成的技术细节。内容结构请参考长文结构设计类 skill。

## 快速命令

```bash
# 编译
typst compile report.typ report.pdf

# 监视模式
typst watch report.typ report.pdf

# 从模板初始化
typst init @preview/basic-report:0.2.0 my-report
```

---

## 基础报告模板

```typst
#set document(title: "Report Title", author: "Author")
#set page(paper: "a4", margin: 2.5cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)
#set heading(numbering: "1.1")

= Executive Summary
// 核心结论

= Background
// 背景描述

= Analysis
// 详细分析

= Recommendations
// 行动建议

= Appendix
// 支持数据
```

---

## 学术论文模板 (IMRaD)

```typst
#set document(title: "Research Paper", author: "Authors")
#set page(paper: "a4", margin: 2.5cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 1em)
#set heading(numbering: "1.")

#align(center)[
  #text(17pt, weight: "bold")[Paper Title]
  #v(0.5em)
  Author Name \
  Institution
]

#v(1em)
*Abstract:* #lorem(50)

#v(1em)
*Keywords:* keyword1, keyword2, keyword3

= Introduction
// 研究背景、问题、假设

= Methods
// 研究设计、数据收集、分析方法

= Results
// 数据呈现、统计结果

= Discussion
// 解释发现、与现有研究对比、局限性

= Conclusion
// 核心贡献、未来方向

= References
// 参考文献
```

---

## 工厂函数模板

```typst
#let project(
  title: "",
  subtitle: "",
  authors: (),
  date: none,
  abstract: none,
  body,
) = {
  // Document metadata
  set document(title: title, author: authors.join(", "))

  // Page settings
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 {
        align(right, text(size: 9pt, fill: gray)[#title])
      }
    },
    footer: context {
      align(center, text(size: 9pt)[#counter(page).display()])
    },
  )

  // Text settings
  set text(font: "New Computer Modern", size: 11pt, lang: "en")
  set par(justify: true, first-line-indent: 1em, leading: 0.65em)

  // Heading settings
  set heading(numbering: "1.1")
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(1em)
    text(size: 16pt, weight: "bold")[#it]
    v(0.5em)
  }
  show heading.where(level: 2): it => {
    v(0.8em)
    text(size: 13pt, weight: "bold")[#it]
    v(0.3em)
  }

  // Title page
  align(center)[
    #v(3cm)
    #text(size: 24pt, weight: "bold")[#title]

    #if subtitle != "" {
      v(0.5em)
      text(size: 14pt)[#subtitle]
    }

    #v(2cm)

    #for author in authors {
      text(size: 12pt)[#author]
      linebreak()
    }

    #v(1cm)

    #if date != none {
      text(size: 11pt)[#date]
    }

    #v(2cm)

    #if abstract != none {
      align(left)[
        #text(weight: "bold")[Abstract]
        #v(0.5em)
        #block(width: 100%, par(first-line-indent: 0pt)[#abstract])
      ]
    }
  ]

  pagebreak()
  body
}

// 使用
#show: project.with(
  title: "Report Title",
  subtitle: "A Comprehensive Analysis",
  authors: ("Author One", "Author Two"),
  date: datetime.today().display("[month repr:long] [day], [year]"),
  abstract: [Brief summary of findings...],
)
```

---

## 图表集成

### 表格

```typst
// 简单表格
#table(
  columns: 3,
  table.header([*Metric*], [*Before*], [*After*]),
  [Accuracy], [85%], [92%],
  [Latency], [100ms], [45ms],
)

// Markdown 风格 (LLM 友好)
#import "@preview/tablem:0.3.0": tablem
#tablem[
  | *Item* | *Value* |
  | --- | ---: |
  | Total | 100 |
]
```

### 代码高亮

```typst
#import "@preview/zebraw:0.6.1": *

#zebraw(
  ```python
  def main():
      print("Hello")
  ```,
  highlight-lines: (2,),
)
```

### 流程图

参考本 skill 的流程图生成部分。推荐顺序：diagraph > D2 > oxdraw

---

## 常见模板包

| 包名 | 用途 |
|------|------|
| basic-report | 通用报告 |
| academic-alt | 学术作业 |
| thesist | 硕士论文 |
| modern-technique-report | 技术报告 |

---

## 编译验证

```bash
# 语法检查
typst query --check report.typ

# 编译
typst compile report.typ report.pdf

# 预览
typst compile --format png report.typ preview.png
```

## 实现层视觉护栏

以下规则属于实现层——当上游 skill 已给出设计方向时，按方向实现；当视觉选择未指定时，遵循这些默认护栏而非自行发明品牌风格。

### 排印层级保持

- 标题（`heading level 1`）与正文之间至少保持 1.4× 的字号比。如果上游未指定具体尺寸，16pt heading + 11pt body 是安全默认。
- 各级 heading 的 `v()` 间距不应全部相同——至少有一级的间距是其他的 1.5× 以上，以传递层级信息。
- 如果 heading 使用全大写（`.text(..)[#upper[...]]`），添加 `0.06em` 字距。

### 强调色纪律

- 报告全文中 accent 颜色的使用点应有限——表格表头高亮、图表关键系列、关键结论标记。不要让 accent 出现在每一页。
- 语义色（success / warn / error）仅用于传达状态语义，不用于装饰。

### 间距作为层级

- `v()` 间距是层级信号：章节间 > 节间 > 段间。三者应有明显梯度，不能全部相同。
- 标题与其后内容之间的间距应小于标题与前文之间的间距——让标题"属于"后面的内容。

### 不做的事

- 不发明品牌风格——如果上游未提供色板/字体选择，使用 Typst 默认或 §基础报告模板 中的保守值。
- 不做排版层面的叙事决策——如果发现内容结构有问题（论点不清、缺乏证据），应移交给 `report-building` skill 而非在实现层修改。
