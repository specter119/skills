# Optimization Notes

Date: 2026-04-03

## Assessment

The original `genimg` entry point piled prompt methodology, CLI reference, slides integration, and model selection all together — the entry point was too heavy and boundaries were unclear.

## Actions Taken

1. Trimmed `SKILL.md` down to boundaries, execution skeleton, and reference map
2. Retained existing prompt enhancement documentation; migrated CLI details to `references/cli-workflow.md`
3. Added minimal trigger cases to provide a baseline for future routing regression

## Future Work

1. Add execution evals covering three scenario types: single image generation, edit mode, and variants
2. Accumulate more prompt recipes for common styles

---

Date: 2026-05-11

## Assessment

`prompt-enhancement.md` lacked guidance on the default aesthetic tendencies of AI image models, making it easy to produce "generic AI-style" images.

## Actions Taken

1. **`references/prompt-enhancement.md`**: Added "Visual Anti-Defaults" section
   - Listed 4 common AI image default patterns (blue-purple gradients, floating geometry, fake UI, excessive glow)
   - Provided a reference negative prompt template
   - Clearly distinguished "user requests = respect" vs "model defaults = avoid"
   - Added an evaluation criterion (does removing the visual element change the core message?)

## References

Adapted the anti-AI-default approach from nexu-io/open-design `craft/anti-ai-slop.md` for the image generation context.

## Open Issues

1. Lack of real prompt + output sample comparison cases
2. Anti-default rules may need to differ across style parameters
