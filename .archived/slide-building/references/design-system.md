# Design System

Define the visual system before writing any individual slide. This reduces cognitive load and improves iteration efficiency.

## 1. Typography Hierarchy

Use at most 2 font families:

- Sans: suitable for screen presentations
- Mono: for code and technical terms only

Recommended priority:

- Sans: `Inter`, `Noto Sans`, `Source Sans 3`, `Arial`
- Serif: `Source Serif 4`, `Noto Serif`, `Georgia`
- Mono: `JetBrains Mono`, `Fira Code`, `Consolas`

### Recommended Type Sizes

| Level | Use | Recommended Size |
| --- | --- | --- |
| Display | Cover / Transition | 32-48pt |
| H1 | Page title | 20-24pt |
| H2 | Section title | 16-18pt |
| Body | Body text | 14-16pt |
| Caption | Notes / Source | 10-12pt |
| Code | Code block | 9-11pt |

### Hierarchy Behavior

Type size is just one dimension of hierarchy. Typography hierarchy on each slide must satisfy three conditions:

1. **One dominant entry point.** Only one element is seen first visually — not two, not three.
2. **Intentional rhythm between levels.** Adjacent levels must have sufficient contrast — a 2pt difference is not enough.
3. **Recoverable information flow.** Even if hierarchy is inverted (e.g., body text larger than a heading), readers can still understand structure through reading order.

Five vectors for establishing hierarchy — at least two should act in the same direction on the dominant element:

| Vector | Controls | Direction |
| --- | --- | --- |
| Type size | Size contrast | Large → Small = Primary → Secondary |
| Weight | Mass contrast | Heavy → Light = Primary → Secondary |
| Spacing | Breathing room | More space = more important |
| Letter-spacing | Tight vs. loose | Tight = fast; Wide = ceremonial |
| Alignment | Relationship to grid | Breaking alignment = signals importance |

### Three-Level Working Model

Most slide pages can be mapped to three functional levels:

| Level | Role | Typical Implementation |
| --- | --- | --- |
| Primary | Entry point — one per slide | Type size + spacing, or alignment break |
| Secondary | Structural support | Weight change or type size step |
| Tertiary | Ancillary information (labels, notes) | Smaller size, lower weight |

More than three visual levels above the fold is usually a layout problem, not a hierarchy opportunity.

### Typography Anti-Patterns

- Staircase weights (regular → medium → semibold → bold) — looks like a default gradient, not design intent
- Uniform spacing across all sections — spacing carries no hierarchy information
- Relying on type size alone for hierarchy, with weight, spacing, and alignment all uniform

### Base Rules

- Heading line height: 1.2–1.3
- Body line height: 1.4–1.6
- Use weight for emphasis first — do not rely on color
- All-caps text must add ≥0.06em letter-spacing

## 2. Color Discipline

### Palette Structure

A controllable palette has four tiers — plan before writing styles:

| Tier | Pixel Share | Role |
| --- | --- | --- |
| Neutrals | 70-90% | Backgrounds, surfaces, text, borders |
| Accent (one only) | 5-10% | Accent only — do not invent a second accent |
| Semantic colors | 0-5% | success / warn / error |
| Effects | <1% | Gradients, glows — use sparingly |

### Semantic Naming

Name by purpose, not by hue:

- ✅ `c-primary`, `c-accent`, `c-success`
- ❌ `c-blue-500`, `c-green-600`

Define at minimum: `primary`, `accent`, `success`, `error`, `muted`, `surface`, `background`, `text`

### Accent Color Discipline

The most common readability issue in AI-generated interfaces is overuse of accent color. Hard caps:

- **At most 2 visible accent uses per screen.** Typical combinations: one eyebrow/label + one primary CTA; or one highlight card + one selected tab.
- If both a CTA and hyperlinks appear on the same screen, hyperlinks are demoted to underline — not accent color.

### Contrast Thresholds

Use as pass/fail threshold checks:

| Combination | Minimum Contrast |
| --- | --- |
| Body text (≤16pt) on background | 4.5:1 |
| Large text (>18pt or 14pt bold) on background | 3:1 |
| UI elements on adjacent surfaces | 3:1 |

In practice, `#757575` on white is generally safer than `#999999`.

### Dark Theme

Avoid pure black and pure white — both cause visual vibration and fatigue:

| Role | Dark Theme | Light Theme |
| --- | --- | --- |
| Background | `#0f0f0f` (not `#000`) | `#FAFAFA` (not `#FFF`) |
| Foreground | `#f0f0f0` (not `#FFF`) | `#212121` (not `#000`) |

On dark surfaces, prefer **semi-transparent white borders** over solid dark borders — 1px `white.transparentize(92%)` implies structure without adding visual noise.

### Avoid AI Default Colors

- **Do not default to indigo** (`#6366f1`, `#4f46e5`, `#8b5cf6`, etc.). This is the most reliable marker of AI-generated design. Indigo is only acceptable if explicitly requested by the user.
- **Do not use two-color "trust" gradients on the cover page** (purple→blue, blue→cyan, purple→pink). Flat color + typography hierarchy is almost always the better choice.

## 3. Density and Style

Choose density based on deck type:

| Type | Characteristics | Recommendation |
| --- | --- | --- |
| Talk | One point per slide, relies on speaker narration | Large whitespace, light information density |
| Business | Needs to be self-readable | Clear structure, denser information |
| Technical | Heavy on code, architecture, process | Mixed density, emphasize diagrams and evidence |

### Style Selection

Reference the style tiers from `pptx-generator`:

- Sharp: suitable for data-dense, formal reports
- Soft: suitable for most business decks
- Rounded: suitable for product introductions and friendlier visual tone

### Visual Rhythm

Consecutive slides need density and skeleton variation. Rules of thumb:

- Do not use the same visual skeleton for 3 consecutive slides
- Alternate intentionally — one dense slide, one open slide — so rhythm feels designed
- Symmetric equal-division layouts (dashboard-style 2×2 grid) almost always fail in slides

## 4. Anti-AI Defaults

Patterns that AI commonly falls into when generating slides — actively correct when these signals appear:

### P0 (Must Fix)

1. **Fabricated metrics** — "10× faster", "99.9% uptime", "users save 4 hours/week". Do not invent numbers without a source; use `—` or mark `[data needed]`.
2. **Filler text** — lorem ipsum, "Feature One / Two / Three", "seamless innovation", "streamline your workflow". Missing content is a layout design problem to solve — not a gap to fill with invented words.
3. **Emoji used as icons** — `✨ 🚀 🎯 ⚡ 🔥 💡` appearing in headings or list items. Use typographic hierarchy or simple shapes instead.
4. **Contrast unreadable on projection** — does not meet the §2 contrast thresholds.

### P1 (Should Fix)

5. Standardized flow "Cover → Agenda → Features → Summary" with zero variation. Introduce at least one unconventional section (full-bleed quote, embedded mini-demo, status comparison timeline).
6. Default palette — unmodified Tailwind/Material color palette used directly.
7. More than 2 accent uses per screen.
8. Decorative gradients or blob/wave backgrounds — geometric decoration with no functional purpose.

### P2 (Can Improve)

9. Perfectly symmetric layouts with no visual tension.
10. All card components with identical shape (rounded corners + left-border accent).

## 5. Reusable Components

Prioritize preparing:

- badge
- card
- metric
- quote block
- timeline
- before/after
- vertical flow

See `components.md` for example code.

## 6. Typst Starter

```typst
#let t-display = 36pt
#let t-h1 = 20pt
#let t-h2 = 16pt
#let t-body = 12pt
#let t-caption = 9pt

#let c-primary = rgb("#1565C0")
#let c-accent = rgb("#E65100")
#let c-success = rgb("#2E7D32")
#let c-error = rgb("#C62828")
#let c-muted = rgb("#757575")
#let c-surface = rgb("#FFFFFF")
#let c-bg = rgb("#FAFAFA")
#let c-text = rgb("#212121")

#set page(fill: c-bg)
#set text(font: ("Inter", "Noto Sans", "Arial"), size: t-body, fill: c-text)
#set par(leading: 0.65em)
```

## 7. Common Mistakes

- Defining colors only, without hierarchy and spacing
- Using the same card layout on every slide
- Code blocks without dark/light contrast, making them hard to read on projection
- Applying Web UI thinking to slides, resulting in dashboard-style equal-column splits
- Staircase weights replacing intentional hierarchy jumps
- Uniform spacing that carries no structural information
- Accent color overuse, exceeding 2 uses per screen
