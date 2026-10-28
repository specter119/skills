# Doctrine — Artifact Design, Prompt Engineering, and Systems Thinking

## Artifact Design

Output quality is part of skill quality. Before designing output:

1. Route by artifact type: high-trust report, tutorial, dashboard, review viewer, slide deck
2. Extract facts/claims/numbers before formatting
3. Pick a design system that matches the work

Non-negotiables for generated artifacts:

- Headings must be domain-specific, not generic
- Tables only for comparison, not for dumping data
- Citations must not interrupt reading flow
- No absolute local paths
- Must be usable on mobile

Reject: generic purple gradients, glass cards, repeated card grids, decorative screenshots.

## Output Quality Risk

Predict how output can fail in small but visible ways. Common failures: generic headings, dense footnotes, bad tables, wrong screenshots, polished summaries losing audience, commands missing assumptions.

Generate `reports/output-risk-profile.md` and `reports/artifact-design-profile.md` only when they matter (Production tier and above).

### Visual Quality Checklist

**P0 Must Fix**: no absolute paths, no placeholder titles/screenshots/citations, no invented evidence, no paragraph-length table cells, no copied palette.

**P1 Should Fix**: domain-specific headings, clear first-screen explanation, visual hierarchy, split dense content.

**P2 Polish**: consistent typography, whitespace rhythm, semantic use of cards/tables/callouts.

## Prompt Engineering Doctrine

Prompt quality is a skill-design input, not a long prompt to paste into SKILL.md.

Map need → prompt:

| Need Type | Task Family | RTF→Skill Mapping |
|-----------|-------------|-------------------|
| Explicit need | Execution | Role→operating stance, Task→workflow, Format→output contract |
| Implicit need | Creative | Discover through dialogue, then map |
| Scenario-based | Teaching | Structure as examples + rules |

Quality dimensions: completeness, clarity, consistency, practicality, specificity.

**Anti-pattern**: copying a meta-prompt wholesale into SKILL.md. A skill with a 500-token body that says "be a good X" is worse than one with a 200-token body that specifies exactly what X owns and refuses.

## Pattern Extraction

Borrow durable patterns, not surface style. A pattern passes the four-gate test:

1. **Recurrence** — appears in >1 source
2. **Generativity** — guides new cases
3. **Distinctiveness** — more specific than generic advice
4. **Boundary** — known limit

Borrow: workflow loops, quality gates, review checkpoints, crisp output shapes, boundary language.

Do not borrow: branding, long prose, roleplay style, platform-specific assumptions.

## Systems Thinking

Four questions for any skill:

1. What does this skill own?
2. What feedback tells us it's improving or drifting?
3. Which failure appears after repeated use?
4. Where is the smallest change with the largest quality gain?

Leverage points (in order): clarify boundary → tune description → add self-repair check → borrow external pattern → close feedback loop.
