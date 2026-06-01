# Research Formats

Format specifications for research artifacts. For full report templates, see [report-en](report-en.md) and [report-zh](report-zh.md).

---

## Source Archival Format

### File Naming

```plain
_sources/{hash}.md

hash = first 8 chars of MD5(url)
```

### File Format

```markdown
---
url: https://example.com/article
title: "Article Title"
fetched: 2024-12-24T10:30:00Z
author: "Author Name" (if available)
published: 2024-12-01 (if available)
relevance: high|medium|low
tags: [topic, subtopic]
---

# Article Title

[Complete original content preserved]

---

## AI Summary (Generated)

[2-3 sentence summary of key points relevant to research]
```

---

## Findings Template

Each subtopic produces a `findings.md`:

```markdown
## [Subtopic] Findings

### Key Facts
1. **[Fact]** (confidence: high, source: [_sources/xxx.md])
2. **[Fact]** (confidence: medium, source: [_sources/yyy.md])

### Cross-Validation
- [Claim] verified by [N] independent sources
- [Claim] conflict: Source A says X, Source B says Y

### Gaps
- [ ] [Information not found]
- [ ] [Needs deeper investigation]

### Sources Used
- [_sources/xxx.md]: [brief description]
- [_sources/yyy.md]: [brief description]
```

---

## Sub-agent Prompt Template

Each sub-agent receives:

```markdown
## Research Task: [Subtopic]

### Context
Research Brief: [Brief content]
Your Focus: [Specific subtopic]
Output Directory: [Path]

### Instructions

1. **Search Phase**
   - Execute 2-4 targeted searches
   - Use varied queries: overview, specific aspects, recent updates
   - Prefer: official docs > tech blogs > forums

2. **Fetch Phase**
   - Fetch full content from high-value URLs
   - Skip: paywalls, low-relevance results

3. **Archive Phase** (CRITICAL)
   For each valuable source, create:
   `research/[topic]/_sources/{url-hash}.md`

   With format: (see Source Archival Format above)

4. **Clean & Synthesize**
   Write findings.md with ONLY:
   - Key facts (not raw content)
   - Confidence assessment
   - Source references (link to _sources/)
   - Identified gaps

### Output
Write to: `{subtopic}/findings.md`
Use: Findings Template above
```

---

## Research Brief Template

```markdown
## Research Brief

**Topic**: [One-line description]
**Goal**: [What success looks like]
**Subtopics**: [List from decomposition]
**Key Questions**:
1. [Primary question]
2. [Secondary question]
3. [Tertiary question]
**Out of Scope**: [Explicit boundaries]
```
