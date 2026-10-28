# Method — Qualification, Archetypes, Boundaries, and Iteration

## Qualification: Should This Become a Skill?

Promote to skill only when at least one is true:

- The workflow will be reused
- The workflow is easy to route incorrectly
- Deterministic scripts reduce repeated effort
- Governance or portability matters

**Reject** when the request is only: explanation, summary, translation, brainstorming, documentation without agent execution, or a one-off answer with no reuse value.

## Archetype Selection

Choose the lightest archetype that fits:

| Archetype | When | Package |
|-----------|------|---------|
| Scaffold | Exploratory or personal use | SKILL.md + agents/interface.yaml only |
| Production | Team reuse | Add references/, scripts/, evals/, manifest |
| Library | Shared org capability | Full suite with governance metadata |
| Governed | High-trust, regulated | Full suite + review cadence + lifecycle |

Stay Scaffold unless reuse is clearly real.

## Boundary Design

Define four things before expanding:

1. **Owned job**: one clear capability
2. **Output**: what the skill produces
3. **Near-neighbor refusals**: what looks similar but belongs elsewhere
4. **Detail placement**: SKILL.md for triggers and skeleton; references/ for depth

## Authoring Discipline

- Do not deepen the package on a guessed goal
- Build the smallest reliable package first
- Surgical changes when improving existing skills
- Tie each meaningful change to a check
- Failure patterns: creating a skill for a one-off answer, adding scripts when prose suffices, adding evals before route risk exists

## Trigger-First Authoring

Write the `description` frontmatter before expanding the body. Test that the USE FOR / DO NOT USE FOR phrases route correctly. Only then add references, scripts, and evals.

## Gate Selection

More gates are not automatically better. Match gates to risk:

- **Low risk**: validate + resource boundary
- **Medium risk**: add trigger eval
- **High risk**: add description optimization, route confusion checks, packaging
- **Critical risk**: add governance, regression history, promotion policy

## Iteration Philosophy

The first skill package is a routeable baseline, not the final answer. Improve by the smallest change that increases reliability more than context cost.

Default priority: trigger clarity → execution assets → promotion/governance/portability.

Always surface the top three next iteration directions.

## Context Budget Tiers

| Tier | SKILL.md tokens | References |
|------|----------------|------------|
| Scaffold | ≤700 | Optional |
| Production | ≤1000 | 2-3 modules |
| Library | ≤1300 | 3-5 modules |
| Governed | ≤1300 | 3-5 + governance |
