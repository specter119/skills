# Frontend Agent Delegation for Slides

Guidance for delegating slide visual optimization to `@frontend-ui-ux-engineer`.

## Core Problem: Cognitive Bias

The default mental model of `frontend-ui-ux-engineer` is **Web UI/Dashboard**:
- Card component → information container
- Grid layout → responsive
- Border + Shadow → hierarchy separation

This logic applied to slides becomes "box stacking". **The mental model must be switched in the prompt.**

## Mental Model Comparison

| Web Design (WRONG) | Slide/Print Design (CORRECT) |
|--------------------|------------------------------|
| Responsive layouts | Fixed 16:9 canvas |
| Interactive elements | Static frames |
| Scroll for more | One screen = one message |
| Card as default container | Use alignment and whitespace to imply grouping |
| Dashboard equal-split grid | Visual rhythm variation |
| Hover/Click interaction | No interaction — pure static |
| Viewport adaptation | Projector readability |

## Slide Types and Styles

| Type | Use Case | Style Characteristics | Authority Reference |
|------|----------|----------|----------|
| **Talk** | TED, Keynote, speaker present | Minimal, large whitespace, one point per slide | Garr Reynolds (*Presentation Zen*) |
| **Business** | Consulting reports, management briefings | Information-dense, clear structure | McKinsey/BCG style |
| **Technical** | Tech talks, architecture reviews | Mixed style, code/diagrams dominant | Engineering culture |

**How to determine**:
- Speaker present → can be minimal
- Needs standalone reading → information must be complete
- Primarily code/architecture → technical type

## Prohibited vs. Required

| Prohibited | Required |
|------|------|
| Card/Box as default container | Use alignment and proximity to imply relationships |
| Dashboard-style equal-split grid | Use weight and size to establish hierarchy |
| Skeleton loader / Loading state | Key numbers must be large and prominent |
| Hover effect / Click interaction | Code blocks use dark background |
| Responsive / Breakpoint suggestions | Consider projector readability |
| Gray-bordered white-background code blocks | Visual rhythm varies across slides |

## Design Principles (Knowledge Activation)

| Principle | Authority | Application |
|------|----------|------|
| **Data-ink ratio** | Edward Tufte | Remove visual noise that carries no information |
| **Gestalt principles** | Psychology | Use proximity and alignment to imply relationships, reduce border dependency |
| **Visual rhythm** | Nancy Duarte | Consecutive slides need visual variation |
| **CRAP** | Robin Williams | Contrast, Repetition, Alignment, Proximity |
| **Squint test** | General | After blurring vision, is the most important content still visible? |

## Prompt Template

```markdown
## Task: Visual Review of Slide Deck (PRESENTATION DESIGN)

**CRITICAL MINDSET:**
You are now a **presentation designer**, not a Web UI engineer.

| Web Design (WRONG) | Slide Design (CORRECT) |
|--------------------|------------------------|
| Responsive layouts | Fixed 16:9 canvas |
| Interactive elements | Static frames |
| Card as default container | Alignment and whitespace to imply grouping |
| Dashboard equal-split grid | Visual rhythm variation |
| Hover/Loading states | N/A |

**Authority references:** Edward Tufte (data-ink), Nancy Duarte (rhythm), Garr Reynolds (zen), Robin Williams (CRAP)

---

## Slide Type: [Talk / Business / Technical]

## Prohibited
- Card/Box as default container
- Dashboard-style equal-split grid
- Skeleton loader / Hover state and other Web patterns
- Gray-bordered white-background code blocks

## Required
- Use alignment and proximity to imply relationships
- Use weight and size to establish hierarchy
- Key numbers must be large and prominent
- Code blocks use dark background
- Consider projector readability (font >=11pt)

---

### Context
- Screenshot location: [path]
- Typst source: [path]
- Total pages: [N]

### Evaluation Criteria
- **Squint test**: Blur vision — is key information still visible?
- **Balance**: Is the visual center of gravity balanced?
- **Hierarchy**: Does the eye naturally flow to the most important element?
- **Contrast**: Are colors readable on a projector?
- **Rhythm**: Is there visual variation across slides?

### Output Format
- Overall assessment (2-3 sentences)
- Page-by-page issues with severity and fix
- Top 3 priority fixes

**MUST NOT:** Suggest Web patterns (skeleton loader, hover, responsive, etc.) or modify content/narrative
**MUST DO:** Focus exclusively on visual presentation quality for projection display
```

## Validating Agent Output

After receiving suggestions, check:

1. **Terminology check**: Did Web terms appear (skeleton, hover, responsive)?
2. **Feasibility check**: Are suggestions applicable to static PDFs?
3. **Evaluation criteria**: Are they based on projection display rather than screen display?

**If validation fails**, re-delegate and emphasize the cognitive bias correction.

## Iteration Improvement Log

Issues found after use, recorded here for continuous improvement:

- [x] 2026-01: On first use the agent suggested "skeleton loader", indicating the bias was not corrected → added comparison table
- [ ] To validate: which Gestalt sub-principles are most effective (proximity vs. similarity)
- [ ] To validate: whether McKinsey/BCG style terminology is correctly understood
