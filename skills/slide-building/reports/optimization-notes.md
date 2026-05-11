# Optimization Notes

Date: 2026-04-03

## Assessment

The original `slide-building` entry file contains a lot of information, but has 3 main issues:

1. Routing description too broad — easy to confuse with `report-building`, `typst-authoring`, `deep-research`
2. `SKILL.md` too long — routing, workflow, knowledge base, and code examples are all mixed together
3. Minimal evals missing — makes stable iteration difficult

## Optimization Actions

1. Restructured the entry to "boundaries + execution skeleton + output contract + reference map"
2. Migrated long-form content to standalone `references/`
3. Added `evals/trigger-cases.md` as a minimal baseline for scenarios without ground truth
4. Aligned display descriptions in `agents/openai.yaml`

## References

External references primarily drew from three practices in MiniMax `pptx-generator`:

1. Explicit skill boundaries and quick reference
2. Breaking details into `references/` rather than piling them at the entry
3. Defining slide/page type first, then deciding on page implementation

## Unresolved Issues

1. No real user prompt replay yet — routing accuracy cannot be verified
2. Visual references remain principle-oriented — real cases can be added later
3. No execution eval yet — currently only trigger-level regression prevention

## Next Round Options

1. Add a real prompt set and run a trigger replay
2. Add more page pattern examples for different deck types
3. Add an "implementation handoff template" for direct handoff to `typst-authoring`

---

Date: 2026-05-11

## Assessment

The design craft guidance in `design-system.md` and `review-and-qa.md` was too basic, lacking structured rules for typography hierarchy, color discipline, and anti-AI defaults.

## Optimization Actions

1. **`references/design-system.md`**:
   - Upgraded "font hierarchy" to "typography hierarchy", added hierarchy behavior (entry point, rhythm, information flow), five-vector model, three-level working model, and typography anti-patterns
   - Upgraded "semantic palette" to "color discipline", added four-tier palette structure, accent color discipline (≤2 per screen), contrast thresholds, dark theme rules, anti-AI default colors
   - Added "Anti-AI Defaults" section (P0/P1/P2 tiers)
   - Added visual rhythm rules
   - Extended common mistakes list

2. **`references/review-and-qa.md`**: Added P0 delivery threshold (6 deterministic checks) to run before subjective review

## References

Drew from the nexu-io/open-design design craft specification, primarily referencing:
- `craft/typography-hierarchy.md`: typography hierarchy behavior and anti-patterns
- `craft/color.md`: palette structure and accent color discipline
- `craft/anti-ai-slop.md`: P0/P1/P2 tiered anti-AI defaults rules

All content was adapted to principles — no CSS/HTML implementation details were carried over directly.

## Unresolved Issues

1. P0 thresholds have no automated checking mechanism yet
2. Typography hierarchy rules lack Typst code examples
3. Anti-AI defaults rule judgments still require manual assessment in some edge cases
