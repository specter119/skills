# Dialogue — Intent Capture, Reference Scan, and Decision Tree

## Intent Dialogue

Before deep authoring, run a short conversation (5-7 sharp questions, not a long form).

### What to Capture

- Recurring job: what does the user do repeatedly?
- Real inputs: what data/context do they work with?
- Required outputs: what must the skill produce?
- Near-neighbor refusals: what looks similar but is NOT this skill?
- Priorities: if only one thing works, what is it?
- References: existing workflows, templates, or examples
- Constraints: platform, model, token budget, tool access

### Opening Style

Start warm and companion-like, not like filling a form:

> "I see you want to turn this into a skill. Let me understand the real job first — what's the thing you keep doing that should just work?"

Chinese conversations should sound soft and natural, not procedural.

**Stop** once the skill can be described clearly in one sentence. Do not keep probing.

### Decision: Route or Answer Directly

If the user only needs a direct answer, explanation, or one-off artifact, do not create a skill. See the Non-Skill Decision Tree below.

## Reference Scan Protocol

Three layers, scan at most 3-5 objects from ≤3 categories:

1. **External Benchmark Scan** (primary): authoritative references — specifications, style guides, canonical examples
2. **User Reference Intake** (secondary): the user's own templates, past outputs, or style preferences
3. **Local Fit Check** (calibration): existing skills in the workspace that might conflict or overlap

Reference categories: method, structure, execution, portability, domain.

Output a short report: what to borrow, what not to borrow, and any conflicts.

Mandatory for Production tier and above. Optional for Scaffold.

## Non-Skill Decision Tree

Do not build a skill when the user really wants:

| User intent | Correct response |
|-------------|-----------------|
| Explain or summarize | Direct answer |
| Translate content | Direct translation |
| Brainstorm ideas | Direct brainstorm |
| One-off artifact | Produce it, don't package it |
| Wiki page / policy memo | Write the document |
| Deterministic repeatable task | Write a script, not a skill |

**Promote to skill only when**: the job is recurring, discoverability matters, boundary precision helps, or reusable instructions add value over a script.

When in doubt, answer directly. You can always package later.
