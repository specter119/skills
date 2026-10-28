# Report Technical Reference

> This document covers the technical details of Typst report generation. For content structure, refer to the long-form document structure design skill.

## Quick Commands

```bash
# Compile
typst compile report.typ report.pdf

# Watch mode
typst watch report.typ report.pdf

# Initialize from template
typst init @preview/basic-report:0.2.0 my-report
```

---

## Basic Report Template

```typst
#set document(title: "Report Title", author: "Author")
#set page(paper: "a4", margin: 2.5cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)
#set heading(numbering: "1.1")

= Executive Summary
// Core conclusions

= Background
// Background

= Analysis
// Detailed analysis

= Recommendations
// Action recommendations

= Appendix
// Supporting data
```

---

## Academic Paper Template (IMRaD)

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
// Research background, problem, hypothesis

= Methods
// Research design, data collection, analysis methods

= Results
// Data presentation, statistical results

= Discussion
// Interpret findings, compare with existing research, limitations

= Conclusion
// Core contributions, future directions

= References
// References
```

---

## Factory Function Template

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

// Usage
#show: project.with(
  title: "Report Title",
  subtitle: "A Comprehensive Analysis",
  authors: ("Author One", "Author Two"),
  date: datetime.today().display("[month repr:long] [day], [year]"),
  abstract: [Brief summary of findings...],
)
```

---

## Chart and Figure Integration

### Tables

```typst
// Simple table
#table(
  columns: 3,
  table.header([*Metric*], [*Before*], [*After*]),
  [Accuracy], [85%], [92%],
  [Latency], [100ms], [45ms],
)

// Markdown style (LLM-friendly)
#import "@preview/tablem:0.3.0": tablem
#tablem[
  | *Item* | *Value* |
  | --- | ---: |
  | Total | 100 |
]
```

### Code Highlighting

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

### Flowcharts

Refer to the diagram generation section of this skill. Recommended order: diagraph > D2 > oxdraw

---

## Common Template Packages

| Package | Purpose |
|------|------|
| basic-report | General-purpose report |
| academic-alt | Academic assignments |
| thesist | Master's thesis |
| modern-technique-report | Technical report |

---

## Compilation Verification

```bash
# Syntax check
typst query --check report.typ

# Compile
typst compile report.typ report.pdf

# Preview
typst compile --format png report.typ preview.png
```

## Implementation-Layer Visual Guardrails

These rules belong to the implementation layer — when an upstream skill has already provided design direction, implement accordingly; when visual choices are unspecified, follow these default guardrails rather than inventing brand styles.

### Typography Hierarchy

- The font size ratio between headings (`heading level 1`) and body text must be at least 1.4×. If upstream does not specify sizes, 16pt heading + 11pt body is a safe default.
- The `v()` spacing for different heading levels should not all be identical — at least one level must have spacing ≥1.5× that of another, to convey hierarchy.
- If a heading uses all-caps (`.text(..)[#upper[...]]`), add `0.06em` letter-spacing.

### Accent Color Discipline

- Accent color usage throughout the report should be limited — table header highlights, key chart series, and critical conclusion markers. Do not let accent appear on every page.
- Semantic colors (success / warn / error) are used only to convey status semantics, not for decoration.

### Spacing as Hierarchy

- `v()` spacing is a hierarchy signal: between chapters > between sections > between paragraphs. The three must have a clear gradient and must not all be equal.
- The spacing between a heading and the content that follows it should be smaller than the spacing between the heading and the preceding content — making the heading "belong to" the content below.

### What Not to Do

- Do not invent brand styles — if upstream does not provide a color palette/font choices, use Typst defaults or the conservative values in the §Basic Report Template.
- Do not make narrative decisions at the typesetting level — if the content structure has problems (unclear arguments, lack of evidence), hand off to the `report-building` skill rather than fixing at the implementation layer.
