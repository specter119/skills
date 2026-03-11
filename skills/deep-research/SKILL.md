---
name: deep-research
description: >
  Searches the web to investigate topics in depth. Decomposes questions, dispatches parallel
  sub-agents to search and fetch, archives raw sources, and produces a structured report.
  Use when asked to "research", "调研", "研究", "深入了解", "investigate", "explore".
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Deep Research

Inspired by LangChain Open Deep Research. Key features:

- **3-Phase workflow**: Scope → Research → Write
- **Persistent output**: Sources archived with metadata
- **Dynamic parallelization**: Supervisor decides strategy
- **Result cleaning**: Sub-agents clean findings before returning

## When to Activate

- User asks to "research", "investigate", "explore"
- Chinese: "调研", "研究", "深入了解", "全面分析"
- Complex topics requiring multi-source synthesis

---

## Workflow Overview

```plain
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: SCOPE (minimal user interaction)                      │
│  ├── Clarify: Single question only if critical ambiguity        │
│  ├── Decompose: Break into subtopics (internal)                 │
│  ├── Brief: Generate focused research brief                     │
│  └── Structure: Create directories (autonomous)                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: RESEARCH (autonomous execution)                       │
│  ├── Supervisor decides parallelization strategy                │
│  ├── Sub-agents: search → fetch → archive → clean               │
│  └── Supervisor reviews, spawns follow-up if gaps exist         │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: WRITE (one-shot)                                      │
│  └── Generate report.md from all findings                       │
└─────────────────────────────────────────────────────────────────┘
```

**Design Principle**: User defines intent, skill handles execution. Minimize interruptions.

---

## Phase 1: Scope

1. **Clarify** (optional): Ask only if critical ambiguity exists
2. **Decompose**: Break into subtopics internally (see `references/decomposition.md`)
3. **Brief**: Generate research brief (see `references/formats.md`)
4. **Structure**: Create output directory and inform user

**Working Directory Logic:**

```plain
场景 1: 用户没指定目录
  → 使用当前工作目录: {cwd}/research/{topic-slug}/

场景 2: 用户指定了目录 (如 "输出到 ./docs")
  → 使用: {指定目录}/research/{topic-slug}/

场景 3: 用户很明确 (如 "调研 A2A，存到项目文档里")
  → Double confirm: "研究结果会存到 ./docs/research/a2a-xxx/，确认？"

场景 4: 为 slide/report 项目调研
  → 检测当前目录是否在 slides/ 或 reports/ 下
  → 如果是，输出到 {project}/research/ 目录
  → 使用 sources/ (而非 _sources/) 匹配项目规范
```

**Output Structure:**

```plain
# 独立调研项目
{cwd}/research/{topic-slug}/
├── _sources/           # Archived originals
├── {subtopic-1}/findings.md
├── {subtopic-2}/findings.md
└── report.md           # Final output

# Slide/Report 项目调研 (自动检测)
{project}/research/
├── sources/            # 原始材料 (无下划线，匹配项目规范)
│   └── {topic}-{source}-{date}.md
├── notes/              # 调研笔记
│   └── {nn}-{topic}.md
└── synthesis.md        # 综合分析
```

**DO NOT ask user to confirm:** Subtopic names, internal directory structure, file naming.

**Inform user and proceed** (no confirmation needed for subtopics):

```plain
开始研究 [topic]
输出目录: ./research/{topic-slug}/
研究方向: 1. [subtopic-1] 2. [subtopic-2] 3. [subtopic-3]
预计 [N] 分钟，开始...
```

---

## Phase 2: Research

**Supervisor decides parallelization:**

| Type | Strategy | Rationale |
|------|----------|-----------|
| Single focused topic | Sequential | No benefit from parallel |
| Compare A vs B vs C | Parallel per item | Context isolation needed |
| Multi-faceted topic | Parallel per subtopic | Faster coverage |
| Deep dive on one thing | Sequential with iteration | Depth over breadth |

**Sub-agent workflow:**
1. Search (2-4 queries)
2. Fetch high-value URLs
3. Archive to `_sources/{hash}.md`
4. Write `findings.md`

See `references/formats.md` for sub-agent prompt and findings format.

**Supervisor review:** Check coverage → identify gaps → spawn follow-up if needed.

---

## Phase 3: Write

Generate final report from all findings in one pass.

Copy template to output directory, then fill placeholders:

```bash
# English
cp {skill_dir}/assets/report-en.md {output_dir}/report.md

# Chinese
cp {skill_dir}/assets/report-zh.md {output_dir}/report.md
```

---

## Bundled Resources

| File | Purpose | Usage |
|------|---------|-------|
| `references/decomposition.md` | Topic breakdown patterns | Read for guidance |
| `references/examples.md` | Usage examples | Read for guidance |
| `references/formats.md` | Source, findings, sub-agent formats | Read for guidance |
| `references/tools.md` | Tool selection guide | Read for guidance |
| `assets/report-en.md` | English report template | Copy to output, fill placeholders |
| `assets/report-zh.md` | Chinese report template | Copy to output, fill placeholders |

---

## Error Handling

| Error | Action |
|-------|--------|
| Sub-agent timeout | Use partial results, note gaps |
| Search fails | Try alternative queries/tools |
| Fetch fails | Try Exa crawl, note as gap |
| All searches fail | Report limitation, suggest manual research |

---

## Best Practices

1. **Brief first**: Always generate research brief before diving in
2. **Archive everything**: Every valuable URL → `_sources/` or `sources/`
3. **Clean before return**: Sub-agents summarize, don't dump raw
4. **One-shot write**: Final report in single pass
5. **Note gaps honestly**: Missing info is valuable metadata
6. **Source traceability**: Every claim links to archived source

## Raw Material Archival (CRITICAL)

**总结 ≠ 原始材料。两者都要保存。**

| 只保存总结 | 保存原始材料 |
|-----------|-------------|
| 丢失细节和上下文 | 可随时回溯验证 |
| 无法追溯来源 | 可引用具体出处 |
| 难以补充内容 | 可从原始材料中挖掘新内容 |
| 总结可能有偏差 | 原始材料是 ground truth |

**Sub-agent 必须做的事**：
1. Fetch 完整网页内容（不是只取摘要）
2. 保存到 `sources/` 目录，包含完整原文
3. 元数据：URL、抓取时间、来源类型
4. 然后才能写 findings.md（基于原始材料提炼）

**命名规范** (for slide/report projects):
- `{topic}-{source}-{YYYY-MM-DD}.md`
- 示例: `opencode-github-readme-2026-01.md`
