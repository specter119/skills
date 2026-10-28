# Workflow

## Core Loop

```plain
1. Write or inspect Typst code
2. Run tinymist diagnostics
3. Fix errors with hover / definition as needed
4. Compile to PDF / PNG
5. Verify page count and rendered output
```

## Common Commands

```bash
typst compile input.typ output.pdf
typst watch input.typ output.pdf
typst init @preview/package-name name
typst compile --format png input.typ output-{0p}.png
```

## Output Verification

- `pdfinfo`: check page count
- `pdftoppm`: export screenshots for visual inspection

## Version Management

Typst packages require pinned versions.

Recommendations:

- Consult the latest documentation or Universe information first
- Do not carry over old version numbers when uncertain

## Diagram Solution Selection

- Simple flowchart: prefer `diagraph`
- Nested containers: consider `D2`
- Sequence / Gantt / pie: consider `oxdraw`
