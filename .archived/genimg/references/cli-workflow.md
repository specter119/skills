# CLI and Workflow

## Initialization

```bash
cp .env.example .env
# edit .env and add GEMINI_API_KEY
```

Main script:

```bash
SCRIPT=scripts/generate.py
```

## Common Commands

```bash
uv run $SCRIPT "a futuristic city" -o city.png
uv run $SCRIPT "landscape" -s photo -o photo.png
uv run $SCRIPT "cloud" -s icon -r 1:1 -o icon.png
uv run $SCRIPT "add rainbow" -e source.png -o edited.png -m gemini-3-pro-image-preview
uv run $SCRIPT "abstract tech concept" --variants 4 --grid comparison.png
uv run $SCRIPT --list-styles
```

## Parameter Summary

```plain
-o, --output
-s, --style
-r, --ratio
--size
-m, --model
-n, --negative
-e, --edit
--variants
--grid
--grid-cols
--output-dir
--json
```

## Model Selection

| Model | Best For |
| --- | --- |
| `gemini-2.5-flash-image` | Fast exploration, batch variants |
| `gemini-3-pro-image-preview` | Refinement, editing, text-sensitive scenarios |

Rule of thumb:

- Use Flash first to find direction
- Use Pro to refine the final version

## Variants Workflow

```bash
uv run $SCRIPT "futuristic city" --variants 4 --grid grid.png -s tech
uv run $SCRIPT "enhance lighting, add more details" \
  -e output/futuristic_city_xxx/v2.png \
  -o final.png \
  -m gemini-3-pro-image-preview
```

## Slides Integration

| Use Case | Style | Ratio |
| --- | --- | --- |
| Cover | `tech` / `corporate` | `16:9` |
| Section divider | `minimalist` | `16:9` |
| Concept | `isometric` / `illustration` | `4:3` |
| Icon | `icon` / `flat` | `1:1` |

Tips:

- Exclude text by default: `-n "text, words, letters, labels"`
- Leave layout titles, labels, and annotations to Typst / Figma
