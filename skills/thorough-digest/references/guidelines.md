# Thorough Digest Guide

## Knowledge Activation
**Core insight**: LLM context window limitations cause "lazy" behavior on long tasks (skipping items, premature completion). Apply agentic decomposition patterns by dividing work into isolated sub-tasks with small output scope.

**Key principles**:
- **Context isolation**: Prevent cross-contamination between sub-tasks.
- **Parallel execution**: Use a fan-out pattern for independent batches.
- **Narrative synthesis**: Map-reduce pattern for the final report.

## When to Trigger
- Multiple local files, sections, or batches need simultaneous processing.
- Batch analysis of similar items (reports, emails, documents, or structured records).
- Building a narrative or executive summary from existing materials.
- Tasks that would produce very long output if executed sequentially.
- Common phrases: "批量分析", "整理材料", "构建叙事", "汇总这些".

## When to Pass to Another Skill
- The request requires new internet research or crawling.
- It focuses on a single document needing a deep dive rather than batch processing.
- There are no existing local materials to digest (route to `deep-research`).

## Phases
### Phase 1 – Analyze
1. Inventory every material to process (see `references/templates.md` for inventory logging).
2. Classify inputs by topic, file, section, or batch.
3. Plan the parallelization strategy (choose by file, topic, section, or uniform batch). Document the grouping decision.

### Phase 2 – Parallel Process
- Launch one Task-driven sub-agent per group with explicit file paths, instructions, and output destinations.
- Each sub-agent must process every assigned item, avoiding skips or cross-group knowledge leakage.
- Enforce 5–10 items per sub-agent to keep contexts manageable.
- Refer to `references/templates.md` for sub-agent prompt structure.

### Phase 3 – Synthesize
1. Collect all `findings.md` files created by sub-agents.
2. Run a gap check: compare processed items against the original inventory.
3. If gaps appear or context requires external validation, trigger `deep-research` before finalizing.
4. Produce the final synthesis or report using the format in `references/templates.md`.

## Parallelization Guidelines
| Total Items | Suggested Groups | Items per Group |
|-------------|------------------|-----------------|
| 1–10 | 1–2 | 5–10 |
| 11–30 | 3–5 | 6–10 |
| 31–50 | 5–8 | 6–10 |
| 51–100 | 8–15 | 5–10 |
| 100+ | 15–20 | 5–10 |

## Integration with Deep Research
```
Thorough Digest → process local materials → identify gaps
       ↓
Deep Research → fill missing facts from the internet
       ↓
Thorough Digest → re-synthesize with new external evidence
```

## Bundled Resources
- `references/templates.md`: inventory, sub-agent, and synthesis templates — read it before issuing prompts.

## Error Handling
| Error | Action |
|-------|--------|
| Sub-agent skips items | Re-run with smaller groups and stricter instructions |
| File read fails | Note the failure in a gap log and proceed with remaining inputs |
| Sub-agent timeout | Accept partial results but flag missing items for reprocessing |
| Output format wrong | Re-prompt the sub-agent with explicit formatting requirements |

## Best Practices
1. Keep groups small (5–10 items) to reduce context fatigue.
2. Provide exact file paths rather than glob patterns for sub-agents.
3. Verify the processed count matches the input count before synthesis.
4. Maintain strict isolation between sub-agents; no sharing of intermediate findings.
5. Use file-based communication (structured `findings.md`) so the synthesis step can read predictable inputs.
