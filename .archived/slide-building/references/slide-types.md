# Slide Types

Based on the `pptx-generator` principle of "classify every slide first", but oriented toward **narrative and layout planning** — not a specific PPTX API.

## Usage Principles

- Determine page type first, then decide on layout
- Do not use the same visual skeleton for 3 consecutive slides
- Each slide serves only one primary takeaway

## 1. Cover

- Purpose: set the tone, establish expectations, introduce the topic
- Required elements: main title, subtitle, speaker/date/organization info
- Common layouts:
  - Text left, image right
  - Center title + background visual
- Failure signals:
  - Title and subtitle are nearly the same size
  - Cover has too much information — looks like a table of contents

## 2. Agenda / Overview

- Purpose: tell the audience how the talk will proceed
- Required elements: 3–5 sections, optionally one goal sentence
- Common layouts:
  - Numbered vertical list
  - Two-column agenda
- Failure signals:
  - Outline is too granular, like a report table of contents
  - Too many sections — audience can't scan in 3 seconds

## 3. Section Divider

- Purpose: shift pace between parts
- Required elements: section number, section title, optional one-line transition
- Common layouts:
  - Centered large title
  - Left-aligned + accent color block
- Failure signals:
  - Looks like a regular content slide
  - Insufficient visual weight — no "scene cut" feel when advancing

## 4. Evidence Slide

- Purpose: support conclusions with numbers, cases, screenshots, quotes
- Required elements: conclusion sentence + evidence
- Common layouts:
  - Large number + small label
  - Screenshot / chart + annotation
  - Quote block + explanation
- Failure signals:
  - Conclusion without evidence
  - Material exists but it's unclear what the audience should focus on

## 5. Comparison Slide

- Purpose: before/after, option A/B, trade-offs and decisions
- Required elements: comparison dimensions, conclusion, applicable conditions
- Common layouts:
  - Left/right comparison
  - pros/cons dual columns
  - Decision matrix
- Failure signals:
  - Only "better/worse" with no evaluation criteria
  - Entire slide describing details with no final conclusion

## 6. Process / Architecture Slide

- Purpose: explain processes, phases, system relationships, migration paths
- Required elements: sequential or structural relationships
- Common layouts:
  - Horizontal timeline
  - Vertical flow
  - hub-and-spoke
- Failure signals:
  - Many arrows but no primary path
  - All boxes are equally weighted — eyes don't know where to look first

## 7. Summary / CTA

- Purpose: wrap up ideas, let the audience leave with a conclusion
- Required elements: 3–5 takeaways or next steps
- Common layouts:
  - Key takeaways list
  - Summary + next steps dual columns
  - Thank you + contact
- Failure signals:
  - Merely repeats previous slide headings
  - Does not answer "so what now"

## Visual Rhythm Recommendations

Consecutive slides should alternate between:

- `text + visual`
- `metric / quote / timeline`
- `comparison`
- `process`
- `dense evidence`
- `lightweight divider`

See `components.md` for specific components.

## Quick Questions for Choosing Slide Type

Ask one question for each slide first:

- Is this slide setting the tone?
- Is it navigating?
- Is it transitioning?
- Is it proving?
- Is it comparing?
- Is it explaining a process?
- Is it wrapping up into action?

If none of the above, the slide's purpose is not yet defined.
