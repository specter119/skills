# Oracle Audience Review - Delegation Guide

Delegate to Oracle to play the role of the target audience for critical review.

## Core Value

It is difficult to fully adopt the audience's perspective for critical review on your own. Oracle plays the target audience and provides "outsider" feedback.

| Self-Review | Oracle Review |
|---------|------------|
| Knows all context — hard to "pretend not to know" | Genuinely starts from zero |
| Tends to assume own logic is clear | Will flag leaps / excessive assumptions |
| Easy to miss "expert blind spots" | Will ask "what does this term mean" |
| Emotionally resistant to rejection | Objective criticism, no softening |

**Key mindset**: Oracle's critique = what a real audience might react. Not "the AI doesn't understand" — but "what if the audience doesn't understand either".

---

## Prompt Template

```markdown
## Task: Audience-Perspective Review

**Role**: You are the target audience for this slide [{audience_description}].

**Context**:
- Talk goal: {goal}
- Duration: {duration}
- Audience background: {audience_background}

**Material**:
{outline_or_content}

**Review Focus**:
1. **Hook**: Does the opening grab my attention? Why should I keep listening?
2. **Pain Point**: Is this problem something I actually care about? Or is it what the speaker cares about?
3. **Story Arc**: Is the narrative throughline clear? Can I restate the core message in one sentence?
4. **So What**: After each section ends, do I know what to think or do?
5. **Evidence**: Are the data/cases persuasive? Or do they sound good but lack substance?
6. **Takeaway**: After listening, what actionable thing can I take away?

**Output Format**:
1. **Overall Impression** (1-2 sentences): First reaction as an audience member
2. **Strengths**: What genuinely engaged me
3. **Weaknesses**: Where I zoned out / got confused / wasn't convinced
4. **Specific Suggestions**: Improvement suggestions for specific pages/sections
5. **Missing Angles**: Things I as an audience member wanted to know but weren't covered
```

---

## How to Use

1. **Prepare materials**:
   - Text content: outline or content (Markdown, Typst, or other text format)
   - Or screenshots: use the `look_at` tool to view PDF screenshots, extract content, then pass to Oracle
2. **Fill the template**: Replace `{audience_description}`, `{goal}`, and other placeholders
3. **Delegate to Oracle**: `@oracle` + full prompt
4. **Process feedback**:
   - Accept reasonable suggestions
   - For those not adopted, record the reason (may be audience misunderstanding or different constraints)
5. **Iterative validation**: Review again after major changes

---

## Review Focus Details

| Focus | What to Check | Common Issues |
|-------|---------|---------|
| **Hook** | Can the opening 30 seconds capture attention | Background preamble too long, jumping straight into technical details |
| **Pain Point** | Does the problem definition resonate with the audience | Talking about "what I want to say" rather than "what they want to hear" |
| **Story Arc** | Is the narrative throughline clear and coherent | Feature lists, no causal relationships between parts |
| **So What** | Is each section's conclusion explicit | Only stating facts, not guiding thinking |
| **Evidence** | Are data/cases persuasive | Hollow slogans, lacking specific numbers |
| **Takeaway** | What can the audience take away | "Very interesting" but no idea what to do next |

---

## Typical Application Scenarios

| Scenario | Material | Focus |
|------|----------|---------|
| Outline review (Phase 2.5) | Outline markdown | Hook, Pain Point, Story Arc |
| Content review (Phase 4.5) | Full slide content or PDF screenshots | Evidence, So What, Takeaway |
| Iteration stuck | Current version + explanation of stalled score | Missing Angles, Specific Suggestions |
