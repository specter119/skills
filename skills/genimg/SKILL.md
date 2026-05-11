---
name: genimg
description: >
  Generate or edit illustrative images with Gemini image models. Use when asked to
  "generate image", "create illustration", or "draw a picture". Excludes diagrams, charts, precise
  architecture visuals, and other code-first graphics.
---

# GenImg

Handles **illustrative image generation and editing**; does not handle precise structural diagrams, charts, or code-generated visuals.

## Routing Boundaries

### Route Here

- Generate cover illustrations, concept images, scene images, and decorative icons
- Edit existing images at the style, lighting, or detail level
- Generate multiple candidate images in batch and select a direction

### Do Not Route Here

- Flowcharts, architecture diagrams, charts, or visuals with strict text requirements
- Images requiring precise, controllable node relationships
- Tasks where the core problem is content structure or layout implementation

## Execution Skeleton

1. First determine whether the image is best solved with a generative model; if code-based drawing is more appropriate, switch tools instead of forcing generation.
2. Expand the user's short prompt into a 50–150 word narrative prompt following the rules in `references/prompt-enhancement.md`.
3. Decide whether to generate once, edit an existing image, or first run the `variants + grid` exploration workflow.
4. Execute via `scripts/generate.py`; see `references/cli-workflow.md` for model and parameter selection.

## Reference Map

- `references/prompt-enhancement.md`: prompt expansion rules, examples, and edit mode
- `references/cli-workflow.md`: CLI usage, model selection, variants/grid workflow
- `evals/trigger-cases.md`: minimal trigger cases
- `evals/execution-cases.md`: key execution scenarios
- `reports/optimization-notes.md`: current refactor rationale and remaining gaps

## Output Contract

- Default output is one image or a comparable set of images
- Unless the user explicitly requests text in the image, exclude `text/labels` by default
- If the image will be used in a layout later, provide recommended aspect ratio, style, and file naming

## Collaboration and Handoff

- If the image is destined for a presentation or document, hand off to a layout or structure-design skill for final placement
