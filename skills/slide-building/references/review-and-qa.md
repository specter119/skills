# Review And QA

Slide quality must be evaluated from rendered output — not from source code alone.

## 0. P0 Delivery Threshold

Before any subjective assessment, run this set of deterministic checks. Any failure must be fixed before proceeding:

- [ ] **No fabricated metrics**: All numbers must have a source or be marked `~` / `[data needed]`. Numbers without sources like "10× faster" or "99.9% uptime" must be removed or flagged.
- [ ] **No filler text**: Does not contain lorem ipsum, "Feature One", "seamless innovation", "streamline your workflow", or similar hollow copy.
- [ ] **No emoji icons**: `✨ 🚀 🎯 ⚡ 🔥 💡` must not appear in headings or list items.
- [ ] **Contrast passes**: Body text ≥ 4.5:1, large text ≥ 3:1 (see `design-system.md` §2).
- [ ] **Page count matches**: Actual page count equals expected page count, no unexpected overflow.
- [ ] **Every slide has a takeaway**: Each content slide can answer "what should the audience remember after this slide".

After passing P0, proceed to the structural check and subjective review below.

## 1. Structural Check First

Typst / Touying text overflow often doesn't raise an error — it silently adds an extra page.

Check first:

```bash
grep -c "^==+ " slide.typ
pdfinfo slide.pdf | grep Pages
pdftotext slide.pdf - | head -200
```

If expected and actual page counts differ, fix structural issues before addressing aesthetics.

## 2. Render Review Second

```bash
pdftoppm -png -r 150 slide.pdf /tmp/review/page
```

Check page by page:

- Is the visual center of gravity stable
- Is the whitespace intentional
- Do 5 consecutive slides have rhythm variation
- Is the most important information immediately clear when projected

## 3. Four Core Tests

### Squint Test

Can you still see the most important information first when squinting?

### Whitespace Test

Is whitespace there for emphasis, or is the slide just sparse?

### Rhythm Test

Do consecutive slides have structural variation, or does every slide look like copy-paste?

### So What Test

After reading this slide, does the audience know how to interpret it or what action to take?

## 4. Scoring Framework

Each dimension scored 1–10:

| Dimension | Question |
| --- | --- |
| Narrative Structure | Is the throughline clear? Do parts have causal relationships? |
| Information Density | Are there numbers, comparisons, and scenarios — not just vague descriptions? |
| Visual Rhythm | Do consecutive slides have variation? |
| So What | Does each slide have a clear takeaway? |
| Domain-Specific Value | Does the content genuinely serve the topic's judgment or decision-making? |

Suggested targets:

- Improve by at least 3 points per round
- Treat as deliverable only after reaching 42/50

## 5. Special Checks for Experience-Sharing Decks

Must answer:

1. What problem was encountered
2. How it was solved
3. What the results were
4. How the audience can reuse it

If the entire deck is only "feature introduction", it usually reads more like documentation than a talk.

## 6. When to Request External Review

- Before the outline is finalized, ask `@oracle` to review the throughline and pain points
- After the content first draft, ask `@oracle` to review evidence and persuasiveness
- When visual score plateaus, ask `@frontend-ui-ux-engineer` to review projection quality
