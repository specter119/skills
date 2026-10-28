# Visual Rhythm Components

Typst code examples for use with the Visual Rhythm Component Library referenced in SKILL.md.

## metric()

Large number display, suitable for showing statistics and comparison values.

```typst
#let metric(number, label, color: c-primary) = {
  align(center)[
    #text(size: 28pt, weight: "bold", fill: color)[#number]
    #v(-0.3em)
    #text(size: 9pt, fill: c-muted)[#label]
  ]
}

// Usage
#metric("3×", "duplicate logic")
#metric("~8K", "tokens / context")
#metric("75+", "providers", color: c-success)
```

## quote-block()

Quote authoritative statements with a highlighted left border + italic text.

```typst
#let quote-block(content, author) = {
  block(stroke: (left: 3pt + c-muted), inset: (left: 12pt, y: 4pt))[
    #text(size: 11pt, style: "italic")[#content]
    #v(0.2em)
    #align(right)[#text(size: 9pt, fill: c-muted)[— #author]]
  ]
}

// Usage
#quote-block(
  "There's a new kind of coding I call 'vibe coding'...",
  "Andrej Karpathy, Feb 2025"
)
```

## timeline

Time progression with horizontal gradient color blocks.

```typst
#align(center)[
  #rect(width: 90%, fill: c-surface, stroke: 1pt + c-muted, radius: 4pt, inset: 0.5em)[
    #stack(dir: ltr, spacing: 0pt,
      rect(width: 25%, fill: c-success.lighten(70%), inset: 0.4em)[
        #text(size: 9pt)[Week 1-4: "So fast!"]
      ],
      rect(width: 35%, fill: c-accent.lighten(70%), inset: 0.4em)[
        #text(size: 9pt)[Month 2-4: "Getting harder..."]
      ],
      rect(width: 40%, fill: c-error.lighten(70%), inset: 0.4em)[
        #text(size: 9pt)[Month 6+: "Need to rewrite"]
      ]
    )
  ]
]
```

## hub-spoke

Hub-and-spoke relationships with a central color block surrounded by cards.

```typst
#align(center)[
  #grid(
    columns: (1fr, auto, 1fr),
    gutter: 0.3em,
    align: center + horizon,
    [
      #grid(columns: 1, gutter: 0.4em,
        rect(fill: c-surface, stroke: 1pt + c-muted, radius: 4pt, inset: 0.3em)[
          #text(size: 9pt)[#text(weight: "bold")[Agent A] · Role]
        ],
        rect(fill: c-surface, stroke: 1pt + c-muted, radius: 4pt, inset: 0.3em)[
          #text(size: 9pt)[#text(weight: "bold")[Agent B] · Role]
        ]
      )
    ],
    [
      #rect(fill: c-primary, radius: 6pt, inset: 0.6em)[
        #text(fill: white, weight: "bold", size: 12pt)[Central Hub]
        #v(0.1em)
        #text(fill: white.transparentize(30%), size: 9pt)[Orchestrator]
      ]
    ],
    [
      #grid(columns: 1, gutter: 0.4em,
        rect(fill: c-surface, stroke: 1pt + c-muted, radius: 4pt, inset: 0.3em)[
          #text(size: 9pt)[#text(weight: "bold")[Agent C] · Role]
        ],
        rect(fill: c-surface, stroke: 1pt + c-muted, radius: 4pt, inset: 0.3em)[
          #text(size: 9pt)[#text(weight: "bold")[Agent D] · Role]
        ]
      )
    ]
  )
]
```

## before-after

Side-by-side split comparison with arrow.

```typst
#grid(
  columns: (1fr, 0.1fr, 1fr),
  gutter: 0.3em,
  [
    #align(center)[#text(weight: "bold", fill: c-error)[Before]]
    #v(0.2em)
    #rect(fill: c-error.lighten(90%), stroke: 1pt + c-error, radius: 4pt, inset: 0.5em)[
      // Before content
    ]
  ],
  [#align(center + horizon)[#text(size: 20pt, fill: c-muted)[→]]],
  [
    #align(center)[#text(weight: "bold", fill: c-success)[After]]
    #v(0.2em)
    #rect(fill: c-success.lighten(90%), stroke: 1pt + c-success, radius: 4pt, inset: 0.5em)[
      // After content
    ]
  ]
)
```

## vertical-flow

Vertical flow steps with downward arrows.

```typst
#align(center)[
  #stack(dir: ttb, spacing: 0.4em,
    rect(fill: c-light, stroke: 1pt + c-primary, radius: 4pt, width: 70%, inset: 0.5em)[
      #grid(columns: (auto, 1fr), gutter: 0.5em, align: horizon,
        badge("1", color: c-primary),
        text(size: 11pt)[Step description]
      )
    ],
    text(fill: c-muted)[↓],
    rect(fill: c-light, stroke: 1pt + c-primary, radius: 4pt, width: 70%, inset: 0.5em)[
      #grid(columns: (auto, 1fr), gutter: 0.5em, align: horizon,
        badge("2", color: c-primary),
        text(size: 11pt)[Step description]
      )
    ],
    text(fill: c-muted)[↓],
    rect(fill: c-success.lighten(80%), stroke: 1pt + c-success, radius: 4pt, width: 70%, inset: 0.5em)[
      #grid(columns: (auto, 1fr), gutter: 0.5em, align: horizon,
        badge("3", color: c-success),
        text(size: 11pt)[Final step]
      )
    ]
  )
]
```

## numbered-list

Scenario list with circular numbering, no card container.

```typst
#stack(dir: ltr, spacing: 0.5em,
  rect(fill: c-error, radius: 50%, width: 24pt, height: 24pt, inset: 0pt)[
    #align(center + horizon)[#text(fill: white, weight: "bold", size: 11pt)[1]]
  ],
  text(weight: "bold", size: 12pt)[Scenario Title]
)
#v(0.2em)
#text(size: 10pt)[
  Scenario description goes here...
]
```
