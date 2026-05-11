# Workflow

## Phase 1: Analyze

1. Inventory: enumerate all materials
2. Classify: group by file / topic / section / batch
3. Plan: determine parallelization and output structure

Suggested output structure:

```plain
{working_dir}/thorough-digest/{task-slug}/
├── _inputs/
├── group-a/findings.md
├── group-b/findings.md
└── synthesis.md
```

## Phase 2: Parallel Process

Each sub-agent must receive:

- An explicit item list
- Processing instructions
- An output path

Key constraints:

- Process EVERY item
- Do NOT skip any items
- Each item gets its own section

## Phase 3: Synthesize

1. Collect all findings
2. Check for missing items or gaps
3. Trigger an external research skill when needed
4. Output the synthesis report

## Grouping Strategy

| Strategy | When to Use |
| --- | --- |
| By file | Each file is independent |
| By topic | Materials cluster naturally by topic |
| By section | A single large file can be split by section |
| By batch | Large volumes of uniform materials divided evenly |
