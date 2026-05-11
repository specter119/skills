# Deep Research Examples

## Example 1: Technology Research with Parallel Tasks

**Query**: "Research the Claude Code Skills system"

### Phase 0: Decomposition

```plain
Claude Code Skills Deep Research (Technology Template)
├── D1. What: Skill definition, difference from MCP/Tool, architecture design
├── D2. Why: What problem it solves, design philosophy, vs traditional tools
├── D3. How: Creating a skill, SKILL.md structure, debugging tips
├── D4. Ecosystem: Official skills, community resources, plugin marketplace
├── D5. Best Practices: Design principles, common patterns, anti-patterns
├── D6. Advanced Features: Task integration, allowed-tools, model override
└── D7. Limitations & Future: Current limitations, roadmap, community feedback
```

### Phase 1: Parallel Tasks

```plain
Launch 3 parallel Tasks:

**Task 1: Core Concepts (D1-D2)**
- Search: "Claude Code Skills official documentation"
- Search: "Claude Skills vs MCP vs Tools difference"
- Fetch: docs.anthropic.com/skills
- Output: scratch/research-d1-d2.md

**Task 2: Usage (D3-D4)**
- Search: "Claude Code Skills tutorial 2025"
- Search: "Claude Skills ecosystem community"
- Context7: get-library-docs for claude-code
- Output: scratch/research-d3-d4.md

**Task 3: Advanced Practices (D5-D7)**
- Search: "Claude Skills best practices"
- Search: "Claude Skills limitations roadmap"
- Fetch: github.com/anthropics/skills
- Output: scratch/research-d5-d7.md
```

### Phase 2: Synthesis

```markdown
## Completeness Assessment

| Dimension | Coverage | Credibility | Gaps |
|------|--------|--------|------|
| D1 | 90% | High | None |
| D2 | 85% | High | None |
| D3 | 80% | High | Code examples need supplement |
| D4 | 70% | Medium | Community resources incomplete |
| D5 | 75% | Medium | Few anti-pattern examples |
| D6 | 65% | Medium | Limited model override docs |
| D7 | 50% | Low | Limited roadmap information |

Overall: 74% → Need to iterate D6, D7
```

### Phase 3: Iteration

```plain
Supplemental Task: D6-D7 deep research
- Search: "Claude Skills advanced features model"
- Search: "Claude Code roadmap 2025"
- Fetch: anthropic.com/engineering related articles
```

**Expected Output**: Comprehensive 15-page report with architecture diagrams, code examples, and actionable recommendations.

---

## Example 2: Comparison Research

**Query**: "Tokio vs async-std vs smol comparative analysis"

### Decomposition (Comparison Template)

```plain
Rust Async Runtime Comparative Analysis
├── D1. Positioning Differences: Design goals and philosophy of each
├── D2. Architecture Comparison: Core implementation differences (executor, reactor)
├── D3. Performance Comparison: Benchmarks, memory usage, latency
├── D4. Developer Experience: API design, documentation, error handling
├── D5. Ecosystem Comparison: Library support, community size
├── D6. Use Cases: Best use cases for each
└── D7. Migration Considerations: Interoperability, migration cost
```

### Parallel Tasks

```plain
Task 1: Foundation Comparison (D1-D2)
- Search: "Tokio vs async-std design philosophy"
- Context7: Tokio docs, async-std docs

Task 2: Performance and Experience (D3-D4)
- Search: "Rust async runtime benchmark 2025"
- Search: "async-std vs tokio developer experience"

Task 3: Ecosystem and Use Cases (D5-D7)
- Search: "Tokio ecosystem libraries"
- Search: "when to use smol vs tokio"
```

### Expected Output

```markdown
## Comparison Matrix

| Feature | Tokio | async-std | smol | Conclusion |
|------|-------|-----------|------|------|
| Design Philosophy | Performance-first | std-compatible | Minimal | Choose as needed |
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Tokio slightly ahead |
| Learning Curve | Medium | Low | Low | async-std most beginner-friendly |
| Ecosystem | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Tokio most extensive |
| Best Fit | High-performance services | Simple apps | Embedded/small | - |
```

---

## Example 3: Problem-Solving Research

**Query**: "How to solve the Rust async ecosystem fragmentation problem"

### Decomposition (Problem Template)

```plain
Rust Async Ecosystem Fragmentation Solution Research
├── D1. Problem Definition: What is fragmentation, symptoms
├── D2. Root Cause Analysis: Why fragmentation occurs
├── D3. Solution Enumeration: Available solutions
├── D4. Solution Comparison: Pros and cons of each
├── D5. Recommended Solution: Best practices
├── D6. Implementation Steps: How to execute
└── D7. Risk Contingency: Possible issues
```

### Key Findings

```markdown
## Solution Comparison

| Solution | Complexity | Risk | Cost | Recommendation |
|------|--------|------|------|--------|
| Standardize on Tokio | Low | Low | Low | ⭐⭐⭐⭐⭐ |
| Use async-compat | Medium | Low | Low | ⭐⭐⭐⭐ |
| Build custom abstraction layer | High | High | High | ⭐⭐ |
| Wait for standardization | N/A | N/A | Time | ⭐⭐⭐ |
```

---

## Example 4: Trend Research

**Query**: "AI Agent frameworks 2025 current state and trends"

### Decomposition (Trend Template)

```plain
AI Agent Framework Current State and Trends
├── D1. Current State: Maturity, adoption rate
├── D2. Key Players: LangChain, AutoGPT, CrewAI, Claude Code
├── D3. Latest Developments: Recent releases, major updates
├── D4. Development Direction: Multi-agent, tool use, memory systems
├── D5. Competitive Landscape: Open source vs closed source
├── D6. Adoption Recommendations: Is it worth entering now
└── D7. Risk Factors: Technical/ecosystem/business risks
```

### Parallel Tasks with Different Focus

```plain
Task 1: Market Overview (D1-D2)
- Exa Search: "AI agent frameworks comparison 2025"
- Fetch: state of AI agents report

Task 2: Technical Developments (D3-D4)
- WebSearch: "LangChain updates 2025"
- WebSearch: "AI agent memory systems research"

Task 3: Evaluation and Recommendations (D5-D7)
- WebSearch: "AI agent framework production experience"
- WebSearch: "AI agent framework risks"
```

---

## Search Query Patterns

### For Different Research Types

**Technology**

```plain
"[tech] official documentation"
"[tech] architecture design"
"[tech] getting started tutorial 2025"
"[tech] vs [alternative] comparison"
"[tech] production case study"
```

**Comparison**

```plain
"[A] vs [B] benchmark 2025"
"[A] vs [B] which is better for [use case]"
"migrate from [A] to [B]"
"[A] [B] feature comparison"
```

**Concept**

```plain
"what is [concept] explained simply"
"[concept] how it works internally"
"[concept] real world examples"
"[concept] common misconceptions"
```

**Problem**

```plain
"[problem] solution best practices"
"how to solve [problem] in [context]"
"[problem] root cause analysis"
"[problem] prevention strategies"
```

**Trend**

```plain
"[topic] state of 2025"
"[topic] market trends"
"[topic] future predictions"
"[topic] adoption statistics"
```

---

## Tool Selection Guide

| Scenario | Recommended Tool | Reason |
|------|----------|------|
| Broad discovery | WebSearch, Exa Search | Wide coverage |
| Official docs | Context7, WebFetch | Precise content |
| Code examples | Exa Code Context | Code-specific |
| Latest updates | Exa Search (livecrawl) | Real-time crawling |
| Deep content | WebFetch, Exa Crawl | Full page retrieval |
| Parallel speed-up | Task Agents | Save time |

---

## Quality Assurance Checklist

Check before completing each research:

- [ ] All dimension coverage > 50%
- [ ] Key findings verified with 2+ sources
- [ ] Information recency meets requirements
- [ ] Conflicting information flagged
- [ ] Information gaps documented
- [ ] Report structure complete
- [ ] Recommendations are specific and actionable

---

## Quick Start: Full Workflow Demo

Shows the complete user-facing interaction flow.

```plain
User: "Research commercial deployment cases of the A2A protocol"
Current working directory: /path/to/project

→ Phase 1: Scope

  [Internal decomposition]
  Subtopics: saas-integration, cross-org-collaboration, platform-orchestration

  [Generate brief - internal]
  Topic: A2A Protocol Commercial Deployments
  Goal: Identify real production cases, not demos
  ...

  [Inform user and proceed - NO confirmation needed]
  "Starting research on A2A commercial cases

   Output directory: ./research/a2a-commercial-cases/

   Research directions:
   1. SaaS product integration cases
   2. Cross-organization collaboration cases
   3. Platform orchestration cases

   Estimated 5-8 minutes, starting now..."

→ Phase 2: Research (autonomous)

  - Launch 3 parallel sub-agents
  - Each archives sources to _sources/
  - Each writes {subtopic}/findings.md
  - Supervisor reviews, no critical gaps → proceed

→ Phase 3: Write

  - One-shot report from all findings
  - Output: ./research/a2a-commercial-cases/report.md

→ Done

  "Research complete

   Report: ./research/a2a-commercial-cases/report.md
   Sources: 12 documents archived in _sources/

   Key findings:
   1. [Key finding 1]
   2. [Key finding 2]
   3. [Key finding 3]"
```

**Example with user-specified directory:**

```plain
User: "Research A2A, store it in the docs directory"

→ Double confirm:
  "Confirm storing research results in ./docs/research/a2a-xxx/ ?"

User: "Yes"

→ Proceed as above...
```
