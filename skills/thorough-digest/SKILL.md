---
name: Thorough Digest
description: >
  Exhaustively reviews local materials with parallel sub-agents — nothing skipped.
  Inventories, groups, dispatches parallel agents to process every item, then synthesizes findings.
  Use when asked to "digest materials", "batch analysis", "process these files", "summarize all",
  "批量分析", "整理这些材料", "构建叙事", "thorough review".
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep
---

# Thorough Digest

Inspired by Manus Wide Research and grapeot's Codex implementation.

## Knowledge Activation

**Core insight**: LLM context window limitations cause "lazy" behavior on long tasks (skipping items, premature completion). Apply **agentic decomposition patterns**: divide work into isolated sub-tasks with small output scope.

**Key principles** (Claude knows the theory):
- **Context isolation**: Prevent cross-contamination between sub-tasks
- **Parallel execution**: Fan-out pattern for independent tasks
- **Narrative synthesis**: Map-reduce pattern for final output

---

## When to Activate

- User wants to process multiple local files/documents
- Batch analysis of similar items (reports, emails, documents)
- Building narrative from existing materials
- Tasks that would produce very long output if done sequentially
- Chinese: "批量分析", "整理材料", "构建叙事", "汇总这些"

## When NOT to Use (Use Deep Research Instead)

- Need to search the internet for new information
- Single topic requiring deep investigation
- No existing local materials to process

---

## Workflow Overview

```plain
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: ANALYZE                                               │
│  ├── Inventory: List all materials to process                   │
│  ├── Classify: Group into independent sub-tasks                 │
│  └── Plan: Decide parallelization strategy                      │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: PARALLEL PROCESS                                      │
│  ├── Launch N sub-agents (one per sub-task group)               │
│  ├── Each sub-agent: read → process → write findings            │
│  └── Sub-agents write to isolated output files                  │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: SYNTHESIZE                                            │
│  ├── Collect all sub-agent outputs                              │
│  ├── Identify gaps → trigger Deep Research if needed            │
│  └── Generate final narrative/report                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Analyze

1. **Inventory**: Enumerate all materials (see `references/templates.md`)
2. **Classify**: Group by topic/file/section/batch
3. **Plan**: Decide parallelization strategy

**Grouping strategies**:

| Strategy | When to Use | Example |
|----------|-------------|---------|
| By file | Each file is independent | 53 student blog posts |
| By topic | Files cluster by subject | Research papers by domain |
| By section | One large file with sections | Long report with chapters |
| By batch | Arbitrary even distribution | Any large uniform set |

**Output structure**:
```plain
{working_dir}/thorough-digest/{task-slug}/
├── _inputs/                    # Symlinks or copies of inputs
├── group-a/findings.md
├── group-b/findings.md
├── group-c/findings.md
└── synthesis.md                # Final output
```

---

## Phase 2: Parallel Process

Launch sub-agents with Task tool. Each receives:
- Explicit item list (file paths, not patterns)
- Processing instructions
- Output path

**Critical rules for sub-agents**:
- Process EVERY item
- Do NOT skip any items
- Each item gets its own section

See `references/templates.md` for sub-agent prompt template.

---

## Phase 3: Synthesize

1. **Collect**: Read all findings.md files
2. **Gap check**: Missing items? Incomplete data?
3. **Deep Research**: Trigger for external info if needed
4. **Synthesize**: Generate final report

See `references/templates.md` for synthesis report template.

---

## Parallelization Guidelines

| Total Items | Groups | Items/Group |
|-------------|--------|-------------|
| 1-10 | 1-2 | 5-10 |
| 11-30 | 3-5 | 6-10 |
| 31-50 | 5-8 | 6-10 |
| 51-100 | 8-15 | 5-10 |
| 100+ | 15-20 | 5-10 |

**Rule**: Keep 5-10 items per sub-agent to prevent slacking.

---

## Integration with Deep Research

```plain
Thorough Digest → process local materials → identify gaps
       ↓
Deep Research → fill gaps from internet
       ↓
Thorough Digest → re-synthesize with new info
```

---

## Bundled Resources

| File | Purpose | Usage |
|------|---------|-------|
| `references/templates.md` | All templates | Read for guidance |

---

## Error Handling

| Error | Action |
|-------|--------|
| Sub-agent skips items | Re-run with smaller group |
| File read fails | Note in gaps, continue |
| Sub-agent timeout | Use partial results |
| Output format wrong | Re-prompt with explicit format |

---

## Best Practices

1. **Small groups**: 5-10 items per sub-agent
2. **Explicit lists**: Give exact file paths, not patterns
3. **Verify counts**: Output item count = input count
4. **Isolated context**: Sub-agents don't know about other groups
5. **File-based communication**: Write to files, supervisor reads
