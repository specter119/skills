# Deep Research Reference Guide

## Source Validation Framework

### Credibility Assessment Matrix

| Source Type | Base Score | Verification Needed |
|-------------|------------|---------------------|
| Official Docs | 90/100 | Check version/date |
| GitHub (>1k stars) | 80/100 | Check last commit |
| Academic Paper | 85/100 | Check citations |
| Tech Company Blog | 75/100 | Check author credentials |
| Stack Overflow | 70/100 | Check votes, verify answer |
| Tutorial Site | 60/100 | Cross-reference |
| Personal Blog | 50/100 | Must cross-reference |
| Forum/Reddit | 40/100 | Multiple sources required |
| AI-Generated | 30/100 | Always verify externally |

### Verification Checklist

For each key finding:

- [ ] Identified original source
- [ ] Checked publication/update date
- [ ] Verified author credentials (if applicable)
- [ ] Cross-referenced with 2nd source
- [ ] Flagged any contradictions

---

## Completeness Assessment Framework

### Dimension Coverage Scoring

```plain
Coverage Level:
- 90-100%: 完整 - 所有子问题有答案，多个来源验证
- 70-89%:  良好 - 主要问题有答案，部分待验证
- 50-69%:  部分 - 核心问题有答案，存在明显缺口
- 30-49%:  不足 - 仅有基础信息，需要迭代
- 0-29%:   缺失 - 几乎无有效信息
```

### Quality Indicators

| Indicator | High Quality | Medium Quality | Low Quality |
|-----------|--------------|----------------|-------------|
| Sources | 3+ independent | 2 sources | 1 source |
| Recency | < 6 months | 6-12 months | > 1 year |
| Depth | Detailed analysis | Overview level | Surface only |
| Validation | Cross-verified | Partially verified | Not verified |
| Confidence | Can recommend | With caveats | Need more info |

### Overall Research Quality Score

```markdown
## 研究质量评估

| 指标 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| 维度覆盖度 | [X]/100 | 30% | |
| 来源质量 | [X]/100 | 25% | |
| 信息时效性 | [X]/100 | 20% | |
| 交叉验证度 | [X]/100 | 15% | |
| 深度分析 | [X]/100 | 10% | |
| **总分** | | | **[X]/100** |

质量等级:
- A (85+): 可直接用于决策
- B (70-84): 可用，建议验证关键点
- C (55-69): 仅供参考，需补充研究
- D (<55): 不可靠，需重新研究
```

---

## Information Gap Analysis

### Gap Categories

1. **Critical Gaps** (Must address)
   - Core concepts unclear
   - No authoritative source found
   - Conflicting information unresolved

2. **Important Gaps** (Should address)
   - Missing recent data
   - Single source only
   - Expert opinion not verified

3. **Minor Gaps** (Nice to have)
   - Edge case coverage
   - Historical context
   - Future predictions

### Gap Resolution Strategies

| Gap Type | Strategy | Tool |
|----------|----------|------|
| No info found | Broaden search terms | WebSearch |
| Outdated info | Search with year filter | "topic 2025" |
| Conflicting info | Find authoritative source | Official docs |
| Single source | Search alternative terms | Different query |
| Technical depth | Check library docs | Context7 |

---

## Search Query Templates

### By Research Phase

**Phase 1: Discovery (Broad)**

```plain
[topic] overview guide
[topic] introduction tutorial
what is [topic] explained
[topic] getting started
```

**Phase 2: Deep Dive (Specific)**

```plain
[topic] [specific aspect] detailed
[topic] architecture internals
[topic] how it works under the hood
[topic] deep dive analysis
```

**Phase 3: Validation (Cross-reference)**

```plain
[topic] [claim] evidence
[topic] benchmark comparison
[topic] real world usage
[topic] production experience
```

**Phase 4: Current State (Recent)**

```plain
[topic] 2025 update
[topic] latest version changes
[topic] roadmap future
[topic] state of 2025
```

### By Source Type

**Official Sources**

```plain
site:docs.* [topic]
site:github.com/[org] [topic]
[topic] official documentation
```

**Community Sources**

```plain
[topic] site:stackoverflow.com
[topic] site:dev.to
[topic] site:medium.com best practices
```

**Expert Sources**

```plain
[topic] conference talk
[topic] [expert name] blog
[topic] engineering blog
```

---

## Conflict Resolution

### When Sources Disagree

1. **Identify the conflict clearly**
   - What exactly do they disagree on?
   - Are they talking about the same version/context?

2. **Check source authority**
   - Official docs > Community > Individual
   - Recent > Old (for technical facts)

3. **Look for context differences**
   - Different versions?
   - Different use cases?
   - Different assumptions?

4. **Report both perspectives**

   ```markdown
   ### 存在争议: [Topic]

   **观点 A** ([Source]): [Description]
   **观点 B** ([Source]): [Description]

   **分析**: [Why they differ]
   **建议**: [What to trust and why]
   ```

---

## Report Quality Checklist

### Before Finalizing Report

- [ ] All dimensions have coverage > 50%
- [ ] No critical gaps remaining
- [ ] Key findings cross-verified
- [ ] Sources properly cited
- [ ] Confidence levels assigned
- [ ] Conflicts acknowledged
- [ ] Actionable recommendations provided
- [ ] Information gaps documented

### Report Metadata Template

```markdown
---
研究主题: [Topic]
研究类型: Technology / Comparison / Concept / Problem / Trend
调研日期: [YYYY-MM-DD]
研究迭代: [N] 轮
总体完整度: [X]%
质量等级: A/B/C/D
主要来源数: [N]
信息缺口: [N] 个
置信度: High/Medium/Low
---
```

---

## Tool-Specific Tips

### WebSearch

- Use quotes for exact phrases
- Add year for recent info
- Try multiple query variations
- Check 3-5 results minimum

### WebFetch

- Prioritize official documentation
- Check for login walls
- Verify page loads correctly
- Extract key sections only

### Context7

- Best for library/framework docs
- Use specific topic parameter
- Check version compatibility
- Combine with WebSearch for context

### Exa Search

- Better for technical content
- Use for code examples
- Good for recent blog posts
- Supports natural language queries

### Task Agents

- Assign clear, bounded scope
- Specify output format
- Set file output location
- Don't overlap dimensions

---

## Time Management

### Research Time Estimates

| Research Depth | Dimensions | Est. Time | Iterations |
|----------------|------------|-----------|------------|
| Quick Overview | 3-4 | 5-10 min | 0-1 |
| Standard | 5-6 | 10-20 min | 1 |
| Comprehensive | 7 | 20-40 min | 1-2 |
| Deep Dive | 7+ | 40-60 min | 2-3 |

### When to Stop Iterating

- Overall completeness > 80%
- Critical dimensions > 70%
- 2 iterations completed
- User indicates time constraint
- Diminishing returns (same results)

---

## Common Pitfalls

### Avoid These Mistakes

1. **Skipping decomposition** → Unfocused research
2. **Single source reliance** → Unreliable findings
3. **Ignoring dates** → Outdated information
4. **Over-iterating** → Diminishing returns
5. **Missing conflicts** → False confidence
6. **No gap documentation** → Hidden limitations
7. **Vague queries** → Poor search results
8. **Parallel without coordination** → Duplicate work
