# Oracle Reader Review - Delegation Guide

Delegate to Oracle to act as the target reader for a critical review.

## Core Value

It is hard to fully adopt the reader's perspective and critique your own work critically. Oracle acts as the target reader and provides "outsider" feedback.

| Self-Review | Oracle Review |
|---------|------------|
| Already knows all context, hard to "pretend not to know" | Starts from zero understanding |
| Tends to think own logic is clear | Will flag leaps / excessive assumptions |
| Easily misses "expert blind spots" | Will ask "what does this term mean?" |
| Emotionally resistant to criticism | Objective critique, pulls no punches |

**Key mindset**: Oracle's criticism = what real readers might feel. Not "the AI doesn't understand" — but "what if the reader doesn't understand either?"

---

## Prompt Template

```markdown
## Task: Reader-Perspective Review

**Role**: You are the target reader of this report [{reader_description}].

**Context**:
- Report goal: {goal}
- Reader background: {reader_background}
- Intended use: {intended_use}

**Material**:
{outline_or_content}

**Review Focus**:
1. **Opening**: Does the opening grab my attention? Why should I keep reading?
2. **Problem Definition**: Is this problem something I actually care about, or just what the author cares about?
3. **Logic Chain**: Is the argument chain clear? Can I restate the core conclusion in one sentence?
4. **So What**: After each section, do I know what to think or do next?
5. **Evidence**: Is the data / are the citations convincing? Or does it sound good but lack evidence?
6. **Actionability**: After reading, what actionable takeaway can I leave with?

**Output Format**:
1. **Overall Impression** (1-2 sentences): First reaction as a reader
2. **Strengths**: What is genuinely valuable
3. **Weaknesses**: Where I'm confused / unconvinced / find it redundant
4. **Specific Suggestions**: Improvement suggestions for specific sections
5. **Missing Angles**: What I as a reader wanted to know but wasn't covered
```

---

## How to Use

1. **Prepare material**:
   - Text content: outline or content (Markdown, Typst, or other text format)
   - Or screenshot: use the `look_at` tool to view a PDF screenshot, extract the content, and pass it to Oracle
2. **Fill in the template**: replace `{reader_description}`, `{goal}`, and other placeholders
3. **Delegate to Oracle**: `@oracle` + complete prompt
4. **Handle feedback**:
   - Adopt reasonable suggestions
   - For suggestions not adopted, record the reason (the reader may have misunderstood, or constraints differ)
5. **Iterate and validate**: after major revisions, review again

---

## Review Focus Details

| Focus | What to Check | Common Issues |
|-------|---------|---------|
| **Opening** | Does the opening draw the reader in to continue? | Executive Summary too vague, no hook |
| **Problem Definition** | Does the problem definition resonate with the reader? | Talks about "what I researched" rather than "what they care about" |
| **Logic Chain** | Is the argument chain clear and coherent? | Leaping assumptions, MECE not satisfied |
| **So What** | Is each section's conclusion explicit? | Only states findings without drawing implications |
| **Evidence** | Are data / citations convincing? | Sources not authoritative, data outdated, cherry-picking |
| **Actionability** | What can the reader take away? | "Interesting" but no clear next step |

---

## Typical Use Cases

| Scenario | Material | Focus |
|------|----------|---------|
| Outline review (Phase 2.5) | Outline markdown | Opening, Problem Definition, Logic Chain |
| Content review (Phase 4.5) | Full section content | Evidence, So What, Actionability |
| Iteration impasse | Current version + description of the impasse | Missing Angles, Specific Suggestions |

---

## Report vs Slide Review Differences

| Dimension | Slide Review | Report Review |
|------|-----------|-------------|
| Audience mode | Audience (passive reception, limited time) | Reader (active reading, can re-read) |
| Focus | Hook, Story Arc, Takeaway | Logic Chain, Evidence, Actionability |
| Information density | Low (one point per slide) | High (requires complete argumentation) |
| Feedback emphasis | "Where did I zone out?" | "Where did I get confused / unconvinced?" |
