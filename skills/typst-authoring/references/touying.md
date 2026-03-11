# Touying Slides Framework

> Typst slide framework. For narrative and design guidance, refer to `slide-building` skill.

## Decision Guide: Touying vs Native Typst

```plain
Need animations (#pause, #only)?
├─ Yes → Use Touying
└─ No → Need consistent theme/branding?
         ├─ Yes → Use Touying
         └─ No → Native Typst `#page[]` is sufficient
```

| Scenario | Recommendation | Reason |
|----------|----------------|--------|
| One-off internal presentation | Native Typst | Less overhead, full control |
| Team template for reuse | Touying | Theme system, consistency |
| Progressive reveal needed | Touying | `#pause`, `#only` built-in |
| Video conference, simple | Native Typst | No framework learning curve |
| Conference talk | Touying | Professional themes, speaker notes |

### Native Typst Alternative

When Touying is overkill:

```typst
// Simple slide setup without Touying
#set page(width: 28cm, height: 16cm, margin: 1cm)
#set text(size: 14pt)

#let slide-title(title) = text(20pt, weight: "bold", fill: rgb("#1565C0"))[#title]

#page[
  #slide-title[Slide Title]
  #v(0.5em)
  Content here...
]
```

---

## Quick Start

```bash
# Initialize from template
typst init @preview/touying:0.6.1 my-slides

# Compile
typst compile slides.typ slides.pdf

# Watch mode
typst watch slides.typ slides.pdf
```

## Basic Structure

```typst
#import "@preview/touying:0.6.1": *

// 1. Choose theme
#let s = themes.simple.register(
  aspect-ratio: "16-9",
  primary: rgb("#1e88e5"),
)

// 2. Set document info
#let s = (s.methods.info)(
  self: s,
  title: [Presentation Title],
  author: [Author Name],
  date: datetime.today().display(),
  institution: [Institution],
)

// 3. Initialize
#show: s.methods.init.with(s)

// 4. Title slide
#s.methods.title-slide(s)[]

// 5. Content slides
#s.methods.slide(s)[
  = Slide Title

  - Point 1
  #pause
  - Point 2
  #pause
  - Point 3
]
```

---

## Animations

### #pause (Progressive Reveal)

```typst
#s.methods.slide(s)[
  = Incremental Reveal

  - First point
  #pause
  - Second point (appears on click)
  #pause
  - Third point (appears on click)
]
```

### #only (Conditional Display)

```typst
#s.methods.slide(s)[
  = Conditional Content

  #only(1)[Content for subslide 1]
  #only(2)[Content for subslide 2]
  #only("2-")[Content from subslide 2 onwards]
]
```

### #meanwhile (Simultaneous Display)

```typst
#s.methods.slide(s)[
  #meanwhile
  // Appears at same time as previous #pause content
]
```

---

## Layout

### Two Columns

```typst
#s.methods.slide(s)[
  = Two Columns

  #grid(
    columns: (1fr, 1fr),
    gutter: 2em,
    [*Left*
    - Item A
    - Item B],
    [*Right*
    - Item C
    - Item D]
  )
]
```

### Centered

```typst
#s.methods.slide(s)[
  #align(center + horizon)[
    #text(36pt, weight: "bold")[Thank You!]
    #v(2em)
    Questions?
  ]
]
```

---

## Theme Selection

| Theme | Style | Best For |
|-------|-------|----------|
| `simple` | Minimal, clean | Internal meetings, tech talks |
| `university` | Academic, formal | Conference, thesis defense |
| `metropolis` | Modern, bold headers | Tech conferences |
| `aqua` | Fresh, light colors | Marketing, product demos |
| `dewdrop` | Elegant, subtle | Executive presentations |

```typst
// Simple - 简洁现代
#let s = themes.simple.register()

// University - 学术风格
#let s = themes.university.register(
  institution: "University Name",
)

// Metropolis - 类 Beamer Metropolis
#let s = themes.metropolis.register()

// Aqua - 清新配色
#let s = themes.aqua.register()

// Dewdrop - 优雅风格
#let s = themes.dewdrop.register()
```

### Custom Colors

```typst
#let s = themes.simple.register(
  primary: rgb("#1e88e5"),
  secondary: rgb("#ff8f00"),
)
```

---

## Diagrams in Touying

See `references/diagraph.md` for detailed best practices.

```typst
#s.methods.slide(s)[
  = Process Flow

  #render(
    width: 70%,
    "digraph { rankdir=LR; A -> B -> C }",
    labels: (A: [Input], B: [Process], C: [Output])
  )
]
```

---

## Compilation

```bash
# PDF（默认）
typst compile slides.typ slides.pdf

# PNG 预览
typst compile --format png slides.typ slide-{0p}.png

# 高质量 PDF
typst compile --pdf-standard a-2b slides.typ slides.pdf
```

---

## Complete Example: Business Proposal

```typst
#import "@preview/touying:0.6.1": *

#let s = themes.simple.register(aspect-ratio: "16-9")
#let s = (s.methods.info)(self: s,
  title: [Business Proposal],
  author: [Team],
)
#show: s.methods.init.with(s)
#s.methods.title-slide(s)[]

// Problem (Slides 1-3)
#s.methods.slide(s)[
  = The Challenge

  Current situation:
  - Pain point 1
  #pause
  - Pain point 2
  #pause

  *Impact:* Loss of \$X million annually
]

// Solution (Slides 4-6)
#s.methods.slide(s)[
  = Our Approach

  #grid(columns: 2, gutter: 2em,
    [*Strategy*
    - Step 1
    - Step 2],
    [*Timeline*
    - Phase 1: Q1
    - Phase 2: Q2]
  )
]

// Impact (Slides 7-9)
#s.methods.slide(s)[
  = Expected Results

  #table(
    columns: 3,
    [*Metric*], [*Current*], [*Target*],
    [Revenue], [\$1M], [\$2M],
    [Efficiency], [60%], [85%],
  )
]

// Call to Action
#s.methods.slide(s)[
  #align(center + horizon)[
    #text(24pt, weight: "bold")[Next Steps]
    #v(1em)
    - Action item 1
    - Action item 2
  ]
]
```

---

## Page Validation (Required After Generation)

Typst/Touying pagination is controlled by headings (`=`, `==`, `===` depending on theme) and `#pagebreak()`. After generating slides, verify actual page count matches expected.

### Validation Steps

```plain
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Determine expected page count (auto-count with tools)  │
│  ├── Grep pattern="^=+ " file.typ → count headings              │
│  ├── Grep pattern="#pagebreak" file.typ → count pagebreaks      │
│  ├── Grep pattern="#page\\[" file.typ → count standalone pages  │
│  └── Expected = cover pages + headings + extra pagebreaks       │
│                                                                 │
│  Note: Heading level (=, ==, ===) depends on Touying theme      │
│        Check which pattern is used in the file                  │
├─────────────────────────────────────────────────────────────────┤
│  Step 2: Compile and verify                                     │
│  ├── tinymist diagnostics file.typ → check syntax errors        │
│  └── typst compile file.typ output.pdf                          │
├─────────────────────────────────────────────────────────────────┤
│  Step 3: Check actual page count                                │
│  └── pdfinfo output.pdf | grep Pages                            │
├─────────────────────────────────────────────────────────────────┤
│  Step 4: If mismatch, locate issue with pdftotext               │
│  └── pdftotext output.pdf - | head -200                         │
│  └── Find which heading split across pages                      │
├─────────────────────────────────────────────────────────────────┤
│  Step 5: If still unclear, screenshot check                     │
│  └── pdftoppm -png -r 72 output.pdf /tmp/page                   │
│  └── Read /tmp/page-N.png                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Auto-count Examples

```bash
# Count headings (any level)
Grep pattern="^=+ " file.typ output_mode="count"

# Count pagebreaks
Grep pattern="#pagebreak" file.typ output_mode="count"

# Count standalone pages (#page[...])
Grep pattern="#page\\[" file.typ output_mode="count"
```

### Common Overflow Causes

| Cause | Symptom |
|-------|---------|
| Extra content between heading and block (e.g., `#grid`) | Heading and content split to two pages |
| diagraph with `rankdir=TB` (vertical layout) | Diagram too tall, causes overflow |
| Image/diagram width set too large | Content exceeds page height |
| Too much content in single grid cell | Single page can't fit |
| Font size or line spacing too large | Text takes more space than expected |

### Bad Examples and Fixes

**Bad: Description text between heading and content**

```typst
// ❌ Will cause page split
== Better Agent Integration

*Scenario: Decouple dev cycles*  // <- This line causes split!

#grid(
  columns: (1fr, 1fr),
  ...
)
```

```typst
// ✅ Correct: Description in heading
== Better Agent Integration: Decouple dev cycles with Agent Card

#grid(
  columns: (1fr, 1fr),
  ...
)
```

**Bad: Vertical diagraph too tall**

```typst
// ❌ rankdir=TB with many nodes is very tall
#render(
  width: 100%,
  "digraph { rankdir=TB; A -> B -> C -> D -> E }"
)
```

```typst
// ✅ rankdir=LR horizontal layout is more compact
#render(
  width: 100%,
  "digraph { rankdir=LR; A -> B -> C -> D -> E }"
)
```

### Quick Validation Commands

```bash
# 1. Count expected pages (use Grep tool)
Grep pattern="^=+ " file.typ output_mode="count"        # headings
Grep pattern="#pagebreak" file.typ output_mode="count"  # pagebreaks
Grep pattern="#page\\[" file.typ output_mode="count"    # standalone pages

# 2. Check syntax before compile (use tinymist MCP)
mcp__tinymist__diagnostics(filePath="file.typ")

# 3. Compile
typst compile file.typ output.pdf

# 4. Check actual page count
pdfinfo output.pdf | grep Pages

# 5. Locate overflow pages
pdftotext output.pdf - | head -200

# 6. Screenshot check (only when needed)
pdftoppm -png -r 72 output.pdf /tmp/page
# Then use Read tool to view /tmp/page-1.png etc.
```

### Self-check Checklist

After generating slides, check each item:

- [ ] Actual page count = expected page count?
- [ ] Each `==` heading at top of page?
- [ ] No content truncated or overflowing to next page?
- [ ] diagraph and image sizes appropriate?
