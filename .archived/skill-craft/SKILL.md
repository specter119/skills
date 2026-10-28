---
name: skill-craft
description: >
  Create, refactor, evaluate, and package agent skills. USE FOR: "create a skill",
  "turn this workflow into a skill", "improve my skill", "add evals", "package for reuse".
  DO NOT USE FOR: one-off answers, brainstorming without reuse, translation,
  documentation without agent execution.
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Skill Craft

**META SKILL** — create, improve, and package agent skills with lean structure and clear triggering.

## USE FOR

- Turning a workflow into a reusable skill
- Improving triggering, boundary, or eval coverage
- Packaging a skill for team reuse

## DO NOT USE FOR

- One-off answers or translations (answer directly)
- Brainstorming with no workflow to package
- Documentation without agent execution

## Execution Skeleton

1. Decide: should this become a skill? If no, answer directly. See [method](references/method.md).
2. Capture intent: job, outputs, refusals, constraints. See [dialogue](references/dialogue.md).
3. Scan 2-3 external references. See [dialogue](references/dialogue.md).
4. Write `description` frontmatter first; test route quality.
5. Choose lightest archetype (Scaffold → Production → Library → Governed). See [method](references/method.md).
6. Build: SKILL.md + references/ + agents/interface.yaml + optional scripts/, evals/.
7. Validate: `waza check <skill>` and iterate.
8. Generate evals: `waza suggest <skill> --apply`.
9. Surface top three next iterations.

## Waza CLI

```bash
waza new skill <name>              # Scaffold skill + eval suite
waza check <skill>                 # Check readiness
waza dev <skill> --auto --target high  # Auto-iterate frontmatter
waza suggest <skill> --apply       # Generate eval tasks
```

## References

- [method](references/method.md): qualification, archetypes, boundaries, authoring discipline
- [doctrine](references/doctrine.md): artifact design, prompt engineering, pattern extraction
- [dialogue](references/dialogue.md): intent capture, reference scan, non-skill decision tree
