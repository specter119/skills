# Trigger Cases

For subsequent manual or scripted evaluation of `slide-building` routing boundaries.

## Should Trigger

1. Help me build a 12-page AI project retrospective deck for a management briefing — outline it page by page first.
2. I have a pile of research notes and want to organize them into a technical talk — focus on the narrative and what each slide should say.
3. Please optimize the throughline of this pitch deck — the slides all have content but there's no rhythm.
4. Design a presentation structure for a 20-minute internal talk, audience is backend engineers.
5. Give me a visual direction plan for a business-type slide deck — no need to write Typst first.

## Should Not Trigger

1. Help me deeply research the difference between MCP and A2A and compile it into a report.
2. Turn this technical proposal into a formal document, output as Markdown.
3. Fix the compilation error in this Typst deck — the `touying-slide` macro is throwing an error.
4. Use PptxGenJS to directly generate a runnable PPTX file.
5. Batch summarize all meeting notes in the `./meeting-notes` directory.

## Near Neighbors

1. I want to build slides but currently have no materials — help me research this topic first.
   Expected: `deep-research` first, then enter `slide-building`

2. I have a briefing document that could become either a report or a deck — help me decide on the structure.
   Expected: differentiate `report-building` and `slide-building` based on output medium

3. I already have a complete outline and visual plan — only the Typst implementation is missing.
   Expected: prioritize `typst-authoring`

4. I want to optimize the visual presentation of an existing slide deck without changing the narrative.
   Expected: `slide-building` can handle this, but should lean toward Phase 5 review and visual strategy
