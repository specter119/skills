---
name: Typst Authoring
description: >
  Provides Typst technical foundation: syntax reference, toolchain commands, package management,
  and diagram solution selection (diagraph/D2/oxdraw).
  Use when working with Typst documents, compiling .typ files, or needing Typst syntax help.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Typst

Technical foundation for Typst document generation. For narrative and design guidance, refer to `slide-building` or `report-building` skills.

## Workflow

```plain
1. Write Typst code
2. Run tinymist diagnostics → check for errors
3. If errors → use tinymist hover to check API signatures → fix → repeat step 2
4. No errors → typst compile to generate PDF
5. Verify output with pdfinfo (page count) and pdftoppm (visual check)
```

## Document Type Routing

| Document Type | Reference File | Content |
|---------------|----------------|---------|
| Slides | `references/touying.md` | Touying framework, animations, themes, page validation |
| Reports | `references/report.md` | Report templates, academic formatting |
| Diagrams | `references/diagraph.md` | Diagraph best practices (slides vs reports scenarios) |

## Core Tools

### Compilation Commands

```bash
typst compile input.typ output.pdf      # Compile to PDF
typst watch input.typ output.pdf        # Watch mode (auto-recompile)
typst init @preview/package-name name   # Initialize from template
typst compile --format png input.typ output-{0p}.png  # Export PNG
```

### tinymist LSP-MCP Tools (Prefer These)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `mcp__tinymist__diagnostics` | Syntax check, error location | After writing code, before compile |
| `mcp__tinymist__hover` | Function signatures, types | When API is uncertain |
| `mcp__tinymist__definition` | Jump to definition | To understand package/function implementation |

## Package Version Management

Typst requires fixed version numbers. Query latest versions before generating code.

**Primary method**: Use Context7 MCP

```plain
1. mcp__context7__resolve-library-id → find package ID
2. mcp__context7__get-library-docs → get latest version and docs
```

**Fallback versions** (as of 2025-12, may be outdated):

| Package | Version | Purpose |
|---------|---------|---------|
| touying | 0.6.1 | Slide framework |
| diagraph | 0.3.6 | Graphviz diagrams |
| oxdraw | 0.1.0 | Mermaid diagrams |
| cetz | 0.3.4 | General drawing |
| tablem | 0.3.0 | Markdown tables |

## Diagram Solution Selection

**Default: diagraph > D2 > oxdraw** (see `references/diagraph.md` for scene-specific practices)

| Scenario | Tool | Reason |
|----------|------|--------|
| Simple flowchart | diagraph | Native Typst, `labels` for Chinese/math |
| Nested containers | D2 | Better subgraph layout |
| Sequence/Gantt/Pie | oxdraw | Mermaid-unique types |

### Quick Examples

```typst
// diagraph (preferred)
#import "@preview/diagraph:0.3.6": *
#render(width: 80%, "digraph { A -> B }", labels: (A: [Start], B: [End]))

// D2 (for architecture)
#figure(image("arch.svg", width: 80%), caption: [Architecture])

// oxdraw (for Gantt/Sequence only)
#import "@preview/oxdraw:0.1.0": *
#oxdraw(```mermaid
gantt
    Task A :a1, 2024-01-01, 30d
```)
```

## Tables

### Native Typst Table (Recommended)

```typst
#table(
  columns: (auto, 1fr, 1fr),
  stroke: (x, y) => if y == 0 { (bottom: 1pt) },
  [*Col 1*], [*Col 2*], [*Col 3*],
  [Data 1], [Data 2], [Data 3],
)
```

### tablem (Markdown Style)

```typst
#import "@preview/tablem:0.3.0": tablem

#tablem[
  | *Name* | *Age* |
  | :--- | :---: |
  | Alice | 25 |
]
```

## Error Handling

| Error | Common Cause | Solution |
|-------|--------------|----------|
| `unknown package` | Wrong package name/version | Check typst.app/universe |
| `expected X, found Y` | Syntax error | Check bracket matching, commas |
| `cannot find font` | Missing font | Use `--font-path` |
