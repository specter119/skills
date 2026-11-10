# Report Style

A report notebook communicates a conclusion that is already reached, as an image-and-text document that can respond to the reader. The reader did not do the analysis and should not follow the analyst's detours. Narrative leads; code supports. Controls are welcome when they help the reader look closer, and each one must make clear what it changes.

Live-session mechanics belong to marimo-pair, and file-format questions to marimo-notebook. This file covers shape. If the job is still finding out what the data says, use [eda-style](eda-style.md).

## Structure

Write conclusion-first. A reader should get the answer from the first screen.

1. **Title and scope**: the question, the audience, and the data snapshot date.
1. **Summary**: the conclusion, the two or three numbers that carry it, and the recommended action. Prefer `mo.stat` or a short `mo.callout` over a paragraph. See [Stable Conclusions](#stable-conclusions).
1. **Findings**: one section per claim. Each is a claim as the heading or first sentence, then the evidence (chart or table) directly after it. Controls for that claim sit inside the section. See [Control Zones](#control-zones).
1. **Caveats**: put important ones next to the claim they qualify; collect the rest here.
1. **Recommendations**: only what follows from the findings.
1. **Appendix**: methods, definitions, extra tables, and a link to the EDA notebook.

Keep sections in the order a reader needs them, not the order the analyst learned them.

## Stable Conclusions

The summary and every claim heading must not change when a reader moves a control. A reader who drags a slider should never find that the first screen now says something different.

- Compute the summary and headings from fixed defaults, or label them explicitly ("At the default threshold of 30 days, ...").
- Anything that reads a control must be below that control's display position. Lint: `control-upstream-impact`.
- If the conclusion truly depends on a parameter, make that parameter a visible part of the claim and place the claim after its control.
- Numbers in prose should come from the same cells that draw the charts (f-strings over `mo.md`), so text and figures cannot drift apart.

## Control Zones

A control may be coupled to other controls and charts. The rule is about distance and visibility: the reader should see at a glance **what a control changes**.

- **Impact zone**: the cells a control affects (directly or through derived values). It must start at the control's display position and be **contiguous**. Between the control and the last affected output there should be nothing unrelated.
- **Narrative is welcome inside a zone**: markdown cells that explain or interpolate the control's value belong there. Unrelated charts or tables do not.
- **Mark the zone clearly**: put a section heading above the control and end the zone at the next heading or divider. Where it helps, show the control and its output together in one `mo.hstack` / `mo.vstack`, so the effect is visibly local. Defining the control upstream and displaying it next to its chart is a good pattern; the display position is what counts.
- **Document-wide filters** (date range, cohort) are allowed. Their zone is everything below them, so put them near the top, state that they apply to the whole report, and place nothing that ignores them below.
- **Dependent controls** (options depend on another control's `.value`) go in adjacent cells; marimo requires `.value` to be read in a different cell.
- **Chart selection** (`mo.ui.altair_chart` and similar) that filters another view: the chart is the control. Place the dependent view right after it.
- **`mo.ui.tabs` and `mo.accordion`** are layout, not controls. Use them for secondary views so the main thread stays short.
- **Expensive recomputation**: wrap with `mo.ui.run_button` or `mo.ui.form` so one click triggers it, and say so next to the button.
- Reach for `mo.state` only for real two-way sync. Reactive cells cover almost everything else.

Lint: `control-zone-gap` flags a visible cell inside a zone that the control does not affect. It does not apply to notebooks that use a grid or slides layout. Suppress a deliberate exception with `# marimo-lint: ignore[control-zone-gap]` in that cell.

## Code Visibility and Delivery

A report is delivered as dynamic HTML, so it is interactive when it has controls.

| Situation                       | Deliver with                                                                                                                 |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Controls, read-only for readers | `marimo run notebook.py` (code hidden by default), or `marimo export html-wasm notebook.py -o out --mode run --no-show-code` |
| No controls at all              | Static `marimo export html` is lighter and avoids the WASM cold start                                                        |
| Sharing with minimal setup      | [molab](https://docs.marimo.io/guides/molab/)                                                                                |

WASM exports run Python in the reader's browser, so:

- Read data with `mo.notebook_location()` and a `public/` directory, not absolute paths. A `--single-file` export does not bundle `public/`; the default export must be served over HTTP.
- Every package must be available in Pyodide. Run `marimo check notebook.py --select MW` before exporting.
- Keep the source runnable: a fresh run from the top must reproduce the report. Hidden code is presentation, not permission to skip graph hygiene.

## Layout

Composition is allowed here because the reader consumes rather than inspects.

- `mo.hstack` for a short row of related metrics, or a control beside its chart.
- `mo.ui.tabs` / `mo.accordion` for secondary or alternate views.
- `mo.callout` for the summary, warnings, and caveats. Not for every paragraph.
- `mo.stat` for headline numbers.
- Plain markdown cells for narrative. Do not wrap prose in containers without a reason.
- One intended visible output per cell; a composed layout counts as one.

If a layout does not help the reader reach the conclusion faster, remove it. A grid or slides layout is fine as a deliberate choice and is outside the zone lint.

## Handoff from EDA

Keep the EDA notebook and the report notebook separate.

- The report starts from decisions, not raw exploration. Load the derived result (a parquet file, a module function, or recorded decisions), not the discovery pipeline.
- Re-derive only what the report needs to draw its own charts. Do not copy every diagnostic cell.
- Carry decisions across as explicit inputs with a one-line reason each, and link back to the EDA notebook.
- Rebuild exploratory charts cleanly for the reader (clear title, labeled axes, one message) instead of pasting the diagnostic.
- If writing the report exposes a gap in the evidence, go back to EDA. Do not paper over it.

If the same logic is needed in both notebooks, extract it into a shared helper module.

## Guardrails

- Do not drift into exploration: no raw-first ordering, no "let's look at the data" sections, no hypothesis lists in the main thread.
- Do not drift into an app: no multi-page navigation, no state machines, no widget chains that span the document. If one is needed, write a real app.
- Do not hide inconvenient evidence. Conclusion-first is an ordering choice, not permission to be selective.
- Do not use a control to hide uncertainty. Show the default view's uncertainty and caveats.
- Do not leave exploratory scaffolding visible: debug prints, aimless `df.head()`, commented-out cells.
- Render every control unconditionally; do not hide one behind `if` or `mo.stop`.
- Name exports for what they are. Bundle headline numbers into one `summary_metrics` export instead of many scalars. Use `_` only for throwaway values.

## Checking

```bash
uvx marimo check notebook.py
python scripts/marimo_lint.py notebook.py --style report
```

`--style report` runs the shared rules plus `control-zone-gap`. The linter is heuristic; a false positive on a deliberate layout is expected, so use the suppression comment or ignore the hint.

## Checklist

- Can a stakeholder get the conclusion and the recommended action from the first screen?
- Do the summary and claim headings stay the same when any control moves?
- Does every claim sit next to its one supporting chart or table?
- For every control: is its impact zone contiguous, starting at the control, with no unrelated output in between?
- Are document-wide filters near the top and labeled as such?
- Are decisions, exclusions, and assumptions stated and linked to the EDA notebook?
- Are caveats near the claims they qualify?
- Is code hidden, and does a fresh run from the top reproduce the report?
- If delivered as WASM: data via `mo.notebook_location()`, packages in Pyodide, `marimo check --select MW` clean?
- Is any control or layout there only for polish?
- Did `uvx marimo check notebook.py` pass?
