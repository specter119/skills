---
name: genimg
description: >
  Generates AI images using Gemini API.
  Use when asked to "生成图片", "画一张", "generate image", "create illustration".
  Not for diagrams, charts, or flowcharts.
---

# GenImg

Generate images using Gemini.

## Prompt Enhancement (Default Behavior)

**IMPORTANT**: Before calling generate.py, transform user's simple description into a structured, Gemini-optimized prompt.

### Why Enhancement Matters

Gemini excels at deep language understanding—**narrative descriptions** outperform keyword lists:

```plain
❌ 用户输入直接透传: "机器人咖啡师"
✅ 增强后: "A photorealistic image of a stoic robot barista with glowing
   blue optics, brewing coffee in a futuristic cafe. Soft ambient lighting
   from overhead neon tubes, shallow depth of field, modern tech aesthetic."
```

### Enhancement Rules

Expand user input into a **narrative paragraph** (50-150 words) containing:

| Element | Description | Example |
|---------|-------------|---------|
| **Subject** | Specific description of main subject | "a stoic robot barista with glowing blue optics" |
| **Action** | What the subject is doing | "brewing coffee" |
| **Setting** | Scene/environment | "in a futuristic cafe" |
| **Lighting** | Light type and direction | "soft ambient lighting from overhead neon tubes" |
| **Technical** | Camera/depth of field/quality | "shallow depth of field, 4K quality" |
| **Style** | Overall style (from -s parameter) | "modern tech aesthetic" |

### Automatic Additions

- If user does not explicitly request text, add `-n "text, words, letters, labels"`
- Based on `-s` style parameter, incorporate corresponding style descriptors
- Based on scene type, add appropriate lighting and composition suggestions

### Enhancement Example

**User says**: "画一个 A2A 协议的概念图，要有科技感"

**Enhanced prompt**:
```plian
An isometric 3D illustration depicting the A2A protocol concept.
Multiple AI agents represented as glowing geometric nodes connected
by flowing data streams. Clean, modern tech aesthetic with blue
accent lighting. Soft diffused top-down lighting creates depth.
Professional, corporate style suitable for technical presentation.
Sharp focus, high quality rendering.
```

**Execute command**:
```bash
uv run $SCRIPT "An isometric 3D illustration depicting..." \
  -s tech -r 16:9 -n "text, words, letters" -o a2a_concept.png
```

### Edit Mode Enhancement

When editing existing images, enhance user's modification instructions:

**User says**: "把光线改暖一点"

**Enhanced**:
```plain
Adjust the lighting to warmer tones. Add golden hour warmth with
soft orange highlights. Maintain the original composition and
subject placement. Keep all other elements unchanged.
```

## Use Cases

- Abstract concept visualization ("innovation", "collaboration", "growth")
- Scene/atmosphere creation (product usage scenarios, team photos)
- Decorative elements (icons, backgrounds, badges)
- Emotional connection (storytelling illustrations)

**Not suitable for**: Logic flowcharts, system architecture diagrams, data charts (use code generation for precision)

## Configuration

Copy `.env.example` to `.env` and add API key:

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Usage

```bash
SCRIPT=scripts/generate.py

# Basic generation (uv run auto-reads PEP 723 dependency declarations)
uv run $SCRIPT "a futuristic city" -o city.png

# With style
uv run $SCRIPT "landscape" -s photo -o photo.png

# Icon
uv run $SCRIPT "cloud" -s icon -r 1:1 -o icon.png

# Edit image (Pro model recommended for higher quality)
uv run $SCRIPT "add rainbow" -e source.png -o edited.png -m gemini-3-pro-image-preview

# Batch variants + grid comparison (Flash model recommended for quick exploration)
uv run $SCRIPT "abstract tech concept" --variants 4 --grid comparison.png

# List styles
uv run $SCRIPT --list-styles
```

## Batch Variant Workflow

**Recommended workflow**: Explore with Flash first, refine with Pro

```bash
# 1. Generate 4 variants (auto-creates version directory)
uv run $SCRIPT "futuristic city" --variants 4 --grid grid.png -s tech
# Output: output/futuristic_city_20251225_143052/v1.png...v4.png + grid.png

# 2. Review grid.png and select preferred version (e.g., v2)

# 3. Refine with Pro model
uv run $SCRIPT "enhance lighting, add more details" \
  -e output/futuristic_city_xxx/v2.png \
  -o final.png \
  -m gemini-3-pro-image-preview
```

**Variant parameters**:
- `--variants N` - Generate N variants
- `--grid PATH` - Output comparison grid image
- `--grid-cols N` - Grid columns (default: 2)
- `--output-dir DIR` - Custom output directory

## Styles

| Style | Description |
|-------|-------------|
| `photo` | Realistic photo |
| `illustration` | Digital illustration |
| `flat` | Flat design |
| `3d` | 3D rendering |
| `minimalist` | Minimal |
| `corporate` | Business style |
| `tech` | Tech aesthetic |
| `sketch` | Hand-drawn |
| `isometric` | Isometric view |
| `icon` | Icon style |

## Parameters

```plain
-o, --output    Output path
-s, --style     Style
-r, --ratio     Aspect ratio (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)
--size          Resolution (1K, 2K, 4K), 4K only for Pro model
-m, --model     Model selection
-n, --negative  Content to avoid
-e, --edit      Edit existing image
--variants N    Generate N variants
--grid PATH     Output comparison grid
--grid-cols N   Grid columns (default: 2)
--output-dir    Variant output directory
--json          JSON output
```

## Models

| Model | Output Format | Resolution | Notes |
|-------|---------------|------------|-------|
| `gemini-2.5-flash-image` | PNG | 1K, 2K | Default, fast exploration |
| `gemini-3-pro-image-preview` | JPEG→PNG | 1K, 2K, 4K | High quality, for refinement |

**Model selection guide**:
- **Batch variant exploration** → Flash (fast, cheap)
- **Edit/refinement** → Pro (high quality, accurate text)

**Auto format conversion**: Pro model returns JPEG; script auto-converts to PNG if output path is .png.

## Slide/Presentation Integration

Use `genimg` + `slides` + `typst` together to enhance technical presentations.

### Recommended Configuration for Presentations

| Use Case | Prompt Example | Style | Ratio |
|----------|----------------|-------|-------|
| Cover | "futuristic logistics network" | `tech`, `corporate` | 16:9 |
| Section divider | "abstract data flow" | `minimalist` | 16:9 |
| Concept | "AI agents collaborating" | `isometric`, `illustration` | 4:3 |
| Icon | "shipping container" | `icon`, `flat` | 1:1 |
| Background | "subtle tech pattern" | `minimalist` + `-n "text, logo"` | 16:9 |

### Workflow

```bash
# 1. Navigate to slide project directory
cd /path/to/slide/project
SCRIPT=scripts/generate.py

# 2. Generate cover image
uv run $SCRIPT "AI agents in supply chain network, abstract, professional" \
  -s tech -r 16:9 -o images/cover.png

# 3. Generate concept image
uv run $SCRIPT "three pillars supporting platform, integration communication authentication" \
  -s isometric -r 4:3 -o images/pillars.png

# 4. Import in Typst
# #image("images/cover.png", width: 100%)
```

### Tool Division with Diagraph

| Image Type | Tool | Reason |
|------------|------|--------|
| Flowchart | Diagraph | Precise control of nodes and connections |
| Architecture | Diagraph/D2 | Needs precise labels and hierarchy |
| Data chart | Typst native | Data accuracy |
| Abstract concept | **GenImg** | Visual impact |
| Emotional connection | **GenImg** | Creates resonance |
| Decorative element | **GenImg** | Adds design appeal |

### Prompt Tips (Presentations)

```bash
# Avoid text (Typst adds text more precisely)
-n "text, words, letters, labels"

# Keep it simple
"concept, minimal, clean, professional"

# Consistent color scheme
"blue accent color, #1565C0, corporate style"
```

## Text Control

**Industry consensus**: Text in AI-generated images is hard to control precisely. Even Ideogram (best at text) recommends post-processing overlays.

**Recommended workflow**:
1. Generate without text: auto-add `-n "text, words, letters, labels"`
2. Overlay precise text later with Typst/Figma

**If user truly needs text**:
- Use Pro model (more accurate text)
- Keep text under 25 characters
- Mark text in prompt with quotes: `"Hello World"`
