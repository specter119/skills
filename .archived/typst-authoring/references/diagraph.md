# Diagraph Best Practices

> Graphviz diagrams in Typst. Scene-specific guidance for slides and reports.

## Quick Reference

```typst
#import "@preview/diagraph:0.3.6": *

#render(
  width: 80%,
  "digraph { rankdir=LR; A -> B -> C }",
  labels: (A: [Start], B: [Process], C: [End])
)
```

## When to Use Diagraph

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Simple flowchart | **diagraph** | Native Typst integration |
| Chinese labels | **diagraph** | `labels` parameter uses Typst rendering |
| Math in labels | **diagraph** | Only option supporting `$formula$` |
| Nested containers | D2 | Better subgraph layout control |
| Sequence/State diagrams | oxdraw | Mermaid syntax simpler |

---

## Slides Best Practices

### Problem: Compression in Constrained Space

Graphviz renders to "infinite canvas" then scales to fit. In slides with limited space:

- Text gets compressed
- Subgraph margins become uneven
- Vertical layouts (`rankdir=TB`) waste horizontal space

### Solutions

**1. Set ONLY ONE dimension to preserve aspect ratio**

> ⚠️ **Critical**: Setting both `width` AND `height` causes distortion (stretches to fit).
> Set only the constraining dimension; the other auto-calculates from original ratio.

```typst
// ✅ Vertical diagrams (rankdir=TB): Set height only
#render(
  height: 10cm,
  "digraph { rankdir=TB; A -> B -> C }"
)

// ✅ Horizontal diagrams (rankdir=LR): Set width only
#render(
  width: 100%,
  "digraph { rankdir=LR; A -> B -> C }"
)

// ❌ Bad: Both dimensions → distortion!
#render(
  width: 90%, height: 9cm,  // Will stretch/compress!
  "digraph { ... }"
)
```

**When to use which dimension:**

| Layout | Set | Auto |
|--------|-----|------|
| `rankdir=TB` (vertical) | `height` | width |
| `rankdir=LR` (horizontal) | `width` | height |

**2. Alternative: `stretch: false` with both dimensions**

If you must set both dimensions (for precise container sizing), use `stretch: false`:

```typst
#render(
  width: 8cm,
  height: 10cm,
  stretch: false,  // CSS contain mode: fit within, keep ratio
  "digraph { ... }"
)
```

Note: `stretch: false` requires **absolute lengths** (cm, pt), not ratios (%).

**3. Leave margins (Never use 100% width)**

```typst
// ❌ Bad: No breathing room
#render(width: 100%, ...)

// ✅ Good: 10-20% margin
#render(width: 80%, ...)
```

**4. Prefer horizontal layout**

```typst
// ❌ Bad: Vertical layout in half-width column
"digraph { rankdir=TB; A -> B -> C -> D }"

// ✅ Good: Horizontal layout
"digraph { rankdir=LR; A -> B -> C -> D }"
```

**5. Avoid nested subgraphs in slides**

```typst
// ❌ Bad: Nested subgraphs compress poorly
"digraph {
  subgraph cluster_a { label=\"Team A\";
    subgraph cluster_inner { ... }
  }
}"

// ✅ Good: Flat structure or use D2 for nesting
"digraph { A -> B -> C }"
```

**6. Constrain height with box (when needed)**

```typst
// Control maximum height to prevent page overflow
#box(width: 100%, height: 8cm)[
  #render(
    width: 100%,
    height: 7.5cm,
    "digraph { ... }"
  )
]
```

### Slides Sizing Guide

**Page geometry**: 28cm × 16cm with 1cm margin → content area ≈ 26cm × 14cm

**Height budget** (for 16cm slide):

- Title + spacing: ~2cm
- Available content: ~12cm
- **Safe diagram height: ≤ 8-10cm**

| Slide Layout | Diagram Position | Recommended Size |
|--------------|------------------|------------------|
| Full width | Center | width: 70-80%, height: ≤ 10cm |
| Two column | Half page | height: ≤ 8cm (TB) or width: 90% (LR) |
| With table | Side | height: ≤ 8cm |

> ⚠️ **Always verify**: If grid cell has other content (text, tables), reduce diagram height accordingly.

### Example: Agent Flow (Slide)

```typst
#grid(
  columns: (1.3fr, 0.7fr),
  gutter: 1em,
  [
    // Text content on left
    *Key metrics*
    #table(...)
  ],
  [
    // Diagram on right
    #render(
      width: 100%,
      "digraph { rankdir=TB; node [shape=box];
        A -> B -> C -> D }",
      labels: (
        A: text(10pt)[Quoting],
        B: text(10pt)[Orders],
        C: text(10pt)[Appointments],
        D: text(10pt)[Tracking],
      )
    )
  ]
)
```

---

## Reports Best Practices

Reports have more space, so compression is less of an issue. Focus on clarity and consistency.

### Use Figures with Captions

```typst
#figure(
  render(
    width: 70%,
    "digraph { rankdir=LR; A -> B -> C }",
    labels: (A: [Input], B: [Process], C: [Output])
  ),
  caption: [Data processing pipeline]
)
```

### Consistent Styling

```typst
// Define reusable style
#let flow-diagram(dot-code, ..labels) = render(
  width: 70%,
  dot-code,
  labels: labels.named(),
)

// Use throughout report
#figure(
  flow-diagram(
    "digraph { A -> B -> C }",
    A: [Step 1], B: [Step 2], C: [Step 3]
  ),
  caption: [Process overview]
)
```

### Complex Diagrams: Consider D2

For reports with complex architecture diagrams:

```bash
# Create .d2 file
d2 --layout dagre architecture.d2 architecture.svg
```

```typst
#figure(
  image("architecture.svg", width: 80%),
  caption: [System architecture]
)
```

---

## Graphviz Quick Reference

### Layout Directions

| Value | Direction |
|-------|-----------|
| `rankdir=TB` | Top to bottom (default) |
| `rankdir=BT` | Bottom to top |
| `rankdir=LR` | Left to right |
| `rankdir=RL` | Right to left |

### Node Shapes

```dot
node [shape=box]      // Rectangle
node [shape=ellipse]  // Oval
node [shape=diamond]  // Decision
node [shape=note]     // Document
node [shape=cylinder] // Database
```

### Styling

```dot
node [style=filled, fillcolor="#E3F2FD"]  // Fill color
edge [color="#1565C0", penwidth=2]        // Edge style
```

### Subgraphs (Use Sparingly in Slides)

```dot
subgraph cluster_name {
  label="Group Name";
  style=filled;
  fillcolor="#E8F5E9";
  A; B;
}
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| **Distorted aspect ratio** | Both `width` + `height` set | Set only ONE dimension |
| Nodes stretched vertically | `height` set on TB diagram | Use `height` only (correct) or switch to `width` only |
| Diagram cut off/truncated | Wrong dimension constrained | LR → use `width`; TB → use `height` |
| Text too small | Graphviz fontsize scaled down | Use `labels` parameter |
| Uneven margins | Subgraph auto-layout | Simplify or use D2 |
| Diagram too tall | `rankdir=TB` with many nodes | Switch to `rankdir=LR` |
| Page overflow | No height constraint | Wrap in `#box(height: Xcm)` |
| Chinese garbled | Graphviz font issue | Use `labels` with Typst text |
