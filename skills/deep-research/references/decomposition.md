# Topic Decomposition Guide

## Quick Reference

| Research Type | Trigger Keywords | Template | Typical Dimensions |
|---------------|------------------|----------|-------------------|
| Technology | research, learn, explore [X] | [Technology](#technology) | 7 |
| Comparison | X vs Y, difference, compare | [Comparison](#comparison) | 7 |
| Concept | what is, how it works, understand | [Concept](#concept) | 7 |
| Problem | how to solve, solution, issue | [Problem](#problem) | 7 |
| Trend | current state, trends, development | [Trend](#trend) | 7 |

---

## Dynamic Adjustment Principles

### When to Add Dimensions

- Topic spans multiple domains → Add cross-domain dimension
- User mentions specific concerns → Add targeted dimension
- Initial search reveals unexpected complexity → Split dimension

### When to Remove Dimensions

- Topic is narrow/focused → Merge related dimensions
- Time constraints → Prioritize core dimensions (D1-D4)
- Information scarcity → Skip dimensions with no sources

### Dimension Prioritization

```plain
Priority 1 (Required): D1-D2 Core Concepts
Priority 2 (Important): D3-D4 Practical Application
Priority 3 (Supplemental): D5-D7 Advanced/Future
```

---

## Technology

**Use when**: "research X", "explore X framework", "learn X"

```plain
[Technology] Deep Research
├── D1. What (What) [Required]
│   ├── Core definition and one-line explanation
│   ├── Design philosophy
│   ├── Key concepts and terminology
│   └── Essential difference from similar technologies
│
├── D2. Why (Why) [Required]
│   ├── What problem it solves
│   ├── Historical background and evolution
│   ├── Advantages over existing solutions
│   └── Why choose it over alternatives
│
├── D3. How (How) [Important]
│   ├── Installation/configuration steps
│   ├── Core API/interfaces
│   ├── Hello World example
│   ├── Common use-case code
│   └── Debugging tips
│
├── D4. Ecosystem (Ecosystem) [Important]
│   ├── Official toolchain
│   ├── Community libraries/plugins
│   ├── IDE/editor support
│   ├── Community activity indicators
│   └── Learning resource quality
│
├── D5. Pros/Cons (Pros/Cons) [Supplemental]
│   ├── Main advantages (with specific metrics)
│   ├── Main drawbacks (real pain points)
│   ├── Suitable use cases
│   └── Unsuitable use cases
│
├── D6. Production (Production) [Supplemental]
│   ├── Performance benchmark data
│   ├── Stability assessment
│   ├── Case studies from large companies/notable projects
│   ├── Lessons learned and solutions
│   └── Operational notes
│
└── D7. Future (Future) [Supplemental]
    ├── Official roadmap
    ├── Version plans
    ├── Hot community discussions
    └── Potential risks and uncertainties
```

**Example Queries per Dimension**:

```bash
# D1: Core Concepts
"What is [Tech]? Core concepts and design philosophy? One-line explanation"
"[Tech] vs [Similar] what is the essential difference?"

# D2: Why
"Why do we need [Tech]? What problem does it solve? Historical background"
"What are the advantages of [Tech] compared to [Alternative]?"

# D3: How to Use
"[Tech] quick start guide getting started"
"[Tech] core API example code"
"[Tech] common patterns"

# D4: Ecosystem
"[Tech] ecosystem mainstream libraries and tools 2025"
"[Tech] community activity GitHub stars contributors"
"[Tech] learning resources tutorials documentation quality"

# D5: Pros/Cons
"[Tech] pros cons analysis"
"[Tech] suitable use cases"
"[Tech] when should you not use it"

# D6: Production
"[Tech] production environment experience"
"[Tech] performance benchmark"
"[Tech] large company case study [Company] uses [Tech]"

# D7: Future Trends
"[Tech] roadmap 2025"
"[Tech] future plans what's next"
"[Tech] community discussion RFC proposal"
```

---

## Comparison

**Use when**: "X vs Y", "difference between X and Y", "choose X or Y"

```plain
[A] vs [B] Comparative Analysis
├── D1. Positioning Differences [Required]
│   ├── A's design goals and philosophy
│   ├── B's design goals and philosophy
│   ├── Fundamental philosophy differences
│   └── Each one's "Why" story
│
├── D2. Architecture Comparison [Required]
│   ├── Core implementation differences
│   ├── Technology stack differences
│   ├── Dependency/runtime requirements
│   └── Internal working principles comparison
│
├── D3. Performance Comparison [Important]
│   ├── Official benchmark data
│   ├── Community benchmark data
│   ├── Memory usage
│   ├── Startup time
│   ├── Real-world performance
│   └── Scalability
│
├── D4. Developer Experience [Important]
│   ├── Learning curve
│   ├── Documentation quality
│   ├── Debugging tools
│   ├── Error message readability
│   ├── IDE support
│   └── Development efficiency
│
├── D5. Ecosystem Comparison [Supplemental]
│   ├── Community size
│   ├── Library/plugin richness
│   ├── Enterprise support
│   ├── Job market
│   └── Long-term maintenance outlook
│
├── D6. Use Cases [Supplemental]
│   ├── A's best use cases
│   ├── B's best use cases
│   ├── Scenarios where neither fits
│   └── Decision tree/selection guide
│
└── D7. Migration Considerations [Supplemental]
    ├── A→B migration cost
    ├── B→A migration cost
    ├── Interoperability
    ├── Incremental migration plan
    └── Migration risk assessment
```

**Comparison Matrix Template**:

```markdown
| Dimension | [A] | [B] | Conclusion |
|------|-----|-----|------|
| Design Philosophy | | | |
| Performance | | | |
| Learning Curve | | | |
| Ecosystem | | | |
| Community Activity | | | |
| Enterprise Adoption | | | |
| Best Fit Scenarios | | | |
```

---

## Concept

**Use when**: "what is X", "how X works", "understand X"

```plain
[Concept] Deep Understanding
├── D1. Definition (Definition) [Required]
│   ├── One-sentence definition
│   ├── Formal/academic definition
│   ├── Plain-language analogy
│   └── Common misconceptions clarified
│
├── D2. Context (Context) [Required]
│   ├── Historical origin
│   ├── What problem it solves
│   ├── Position within a larger system
│   └── Related fields
│
├── D3. Mechanism (Mechanism) [Important]
│   ├── How it works
│   ├── Core algorithm/mechanism
│   ├── Key components
│   └── Data/control flow
│
├── D4. Examples (Examples) [Important]
│   ├── Simplest example
│   ├── Real-world application cases
│   ├── Code implementation
│   └── Visualization/diagrams
│
├── D5. Variants (Variants) [Supplemental]
│   ├── Different implementation approaches
│   ├── Related concept comparisons
│   ├── Evolution history
│   └── Domain-specific variants
│
├── D6. Tradeoffs (Tradeoffs) [Supplemental]
│   ├── Advantages
│   ├── Drawbacks/limitations
│   ├── Applicable boundaries
│   └── Complexity analysis
│
└── D7. Practice (Practice) [Supplemental]
    ├── Usage recommendations
    ├── Common pitfalls
    ├── Debugging tips
    └── In-depth learning resources
```

---

## Problem

**Use when**: "how to solve X", "solutions for X", "handle X"

```plain
[Problem] Solution Research
├── D1. Problem Definition [Required]
│   ├── Problem description
│   ├── Symptoms
│   ├── Scope of impact
│   ├── Reproduction conditions
│   └── Severity assessment
│
├── D2. Root Cause Analysis [Required]
│   ├── Direct cause
│   ├── Deeper underlying cause
│   ├── Contributing factors
│   └── 5 Whys analysis
│
├── D3. Solution Enumeration [Important]
│   ├── Solution A: [description]
│   ├── Solution B: [description]
│   ├── Solution C: [description]
│   └── Other possible solutions
│
├── D4. Solution Comparison [Important]
│   ├── Implementation complexity
│   ├── Performance impact
│   ├── Maintenance cost
│   ├── Risk assessment
│   └── Required resources
│
├── D5. Recommended Solution [Supplemental]
│   ├── Preferred solution
│   ├── Rationale for selection
│   ├── Fallback solutions
│   └── Solution combinations
│
├── D6. Implementation Steps [Supplemental]
│   ├── Prerequisites
│   ├── Detailed steps
│   ├── Verification methods
│   ├── Rollback plan
│   └── Time estimates
│
└── D7. Risk Contingency [Supplemental]
    ├── Potential issues
    ├── Mitigation measures
    ├── Monitoring metrics
    └── Escalation path
```

**Solution Comparison Template**:

```markdown
| Solution | Complexity | Risk | Cost | Recommendation |
|------|--------|------|------|--------|
| A    | Low    | Low  | Low  | ⭐⭐⭐⭐ |
| B    | Medium | Med  | Med  | ⭐⭐⭐ |
| C    | High   | High | High | ⭐⭐ |
```

---

## Trend

**Use when**: "current state of X", "development trends of X", "the future of X"

```plain
[Topic] Current State and Trends
├── D1. Current State [Required]
│   ├── Maturity assessment
│   ├── Market adoption rate
│   ├── Standardization level
│   └── Current version/status
│
├── D2. Key Players [Required]
│   ├── Major projects/products
│   ├── Core companies/organizations
│   ├── Key contributors
│   └── Investment/funding status
│
├── D3. Latest Developments [Important]
│   ├── Recent major releases
│   ├── Significant updates
│   ├── Industry events
│   └── Media coverage
│
├── D4. Development Direction [Important]
│   ├── Official roadmap
│   ├── Hot community discussions
│   ├── Technical evolution direction
│   └── Research frontier
│
├── D5. Competitive Landscape [Supplemental]
│   ├── Main competitors
│   ├── Differentiated positioning
│   ├── Market share
│   └── Competitive dynamics changes
│
├── D6. Adoption Recommendations [Supplemental]
│   ├── Is it worth adopting now
│   ├── Suitable team/scenario types
│   ├── Learning ROI
│   └── Wait-and-see vs. entry timing
│
└── D7. Risk Factors [Supplemental]
    ├── Technical risks
    ├── Ecosystem risks
    ├── Business risks
    └── Regulatory/compliance risks
```

---

## How to Use

### Step-by-Step Process

1. **Identify type**: Choose the appropriate template based on the user question
2. **Customize dimensions**: Adjust D1-D7 for the specific topic
   - Add topic-specific sub-dimensions
   - Remove irrelevant sub-dimensions
   - Adjust priorities
3. **Generate plan**: Define specific questions and sources for each dimension
4. **Execute research**: Collect information per dimension (sequentially or in parallel)
5. **Assess completeness**: Check coverage for each dimension
6. **Iterate deeper**: Add research for under-covered dimensions
7. **Synthesize report**: Consolidate findings across all dimensions

### Dimension Quality Checklist

Each dimension should satisfy:

- [ ] Has a clear research question
- [ ] Has 2+ independent sources
- [ ] Information recency < 1 year (for technical topics)
- [ ] Credibility level noted
- [ ] Information gaps recorded

### Coverage Assessment

```markdown
| Dimension | Coverage | Quality | Status |
|------|--------|------|------|
| D1 | 90% | High | ✅ |
| D2 | 75% | Medium | ⚠️ Needs supplement |
| D3 | 60% | Low | ❌ Iterate |
| ... | ... | ... | ... |

Overall: 73% → Target 80%
```

---

## Parallel Research Assignment

Assign dimensions to Task agents:

```plain
Default assignment strategy:

Task 1 (Foundation): D1-D2 → Core concepts and background
Task 2 (Application): D3-D4 → Practical use and ecosystem
Task 3 (Advanced): D5-D7 → Tradeoffs and trends

When time is tight:

Task 1: D1-D3 (Required)
Task 2: D4-D7 (Supplemental)

For deep research:

Task 1: D1
Task 2: D2
Task 3: D3-D4
Task 4: D5-D7
```

---

## Source Quality Reference

### Source Credibility Rating

| Level | Source Type | Examples |
|------|----------|------|
| **High** | Official Docs | docs.*, github.com/[org] |
| **High** | Authoritative Orgs | IETF, W3C, CNCF |
| **High** | Core Maintainers | Project author blog/talks |
| **Medium** | Well-known Tech Blogs | engineering.*, InfoQ |
| **Medium** | Stack Overflow | High-vote answers, verified responses |
| **Low** | Personal Blogs | Cross-reference required |
| **Low** | Forum Discussions | Reddit, HN comments |
| **Verify** | AI-Generated Content | Must cross-verify with other sources |

### Timeliness Requirements

| Topic Type | Max Information Age |
|----------|--------------|
| Security Vulnerabilities | 1 month |
| Library Versions | 3 months |
| Best Practices | 1 year |
| Architecture Patterns | 2-3 years |
| Fundamental Concepts | 5+ years OK |
