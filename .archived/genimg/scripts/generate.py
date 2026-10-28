#!/usr/bin/env python3
# /// script
# dependencies = ["google-genai", "Pillow"]
# ///
"""
GenImg - AI Image Generation Tool
Uses Gemini for image generation
"""

import os
import sys
import json
import base64
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Skill root directory (relative to this script)
SKILL_DIR = Path(__file__).parents[1]
ENV_FILE = SKILL_DIR / ".env"

# Available models
MODELS = ["gemini-2.5-flash-image", "gemini-3-pro-image-preview"]


def verify_image(path: str) -> dict:
    """Verify that a file is a valid image using the `file` command."""
    try:
        result = subprocess.run(
            ["file", "--mime-type", "-b", path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        mime_type = result.stdout.strip()
        is_image = mime_type.startswith("image/")
        return {
            "valid": is_image,
            "mime_type": mime_type,
            "message": f"Valid {mime_type}"
            if is_image
            else f"Not an image: {mime_type}",
        }
    except Exception as e:
        return {
            "valid": False,
            "mime_type": "unknown",
            "message": f"Verification failed: {e}",
        }


STYLES = {
    "photo": "Photorealistic, high quality photograph, natural lighting",
    "illustration": "Digital illustration, clean lines, vibrant colors",
    "flat": "Flat design, vector style, minimal shadows, clean",
    "3d": "3D rendered, subtle shadows, depth, realistic materials",
    "minimalist": "Minimalist design, lots of whitespace, simple composition",
    "corporate": "Professional corporate style, clean, modern, business",
    "tech": "Modern tech aesthetic, gradients, geometric shapes, futuristic",
    "sketch": "Hand-drawn sketch style, pencil strokes, artistic",
    "isometric": "Isometric perspective, 3D blocks, clean geometric",
    "watercolor": "Watercolor painting style, soft edges, artistic",
    "anime": "Anime/manga style illustration, vibrant, expressive",
    "icon": "Simple icon, flat design, single subject, transparent friendly",
}


def load_env():
    """Load .env from skill directory."""
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    value = value.strip().strip('"').strip("'")
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value


def get_api_key() -> str:
    """Get API key from env."""
    load_env()
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError(f"GEMINI_API_KEY not set. Add to {ENV_FILE} or environment.")
    return key


def get_base_url() -> str:
    """Get base URL from env (optional)."""
    load_env()
    return os.getenv("GOOGLE_GEMINI_BASE_URL")


class ImageGenerator:
    """Gemini image generator."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_api_key()
        self.base_url = get_base_url()

        from google import genai
        from google.genai import types

        self.genai = genai
        self.types = types

        # Support custom base URL
        if self.base_url:
            self.client = genai.Client(
                api_key=self.api_key, http_options={"base_url": self.base_url}
            )
        else:
            self.client = genai.Client(api_key=self.api_key)

        self.model = MODELS[0]

    def set_model(self, model: str):
        """Set model name."""
        self.model = model

    def generate(
        self,
        prompt: str,
        output_path: str = "generated.png",
        style: str | None = None,
        negative_prompt: str | None = None,
        aspect_ratio: str = "16:9",
        image_size: str | None = None,
    ) -> dict:
        """Generate an image."""
        full_prompt = self._build_prompt(prompt, style, negative_prompt)

        # Build image config
        image_config_params = {"aspect_ratio": aspect_ratio}
        if image_size:
            image_config_params["image_size"] = image_size

        config = self.types.GenerateContentConfig(
            temperature=0.7,
            response_modalities=["image", "text"],
            image_config=self.types.ImageConfig(**image_config_params),
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[full_prompt],
            config=config,
        )

        return self._save_image(response, output_path)

    def generate_variants(
        self,
        prompt: str,
        count: int = 4,
        output_dir: str | None = None,
        style: str | None = None,
        negative_prompt: str | None = None,
        aspect_ratio: str = "16:9",
        image_size: str | None = None,
    ) -> dict:
        """Generate multiple variants of an image."""
        # Create output directory with timestamp
        if output_dir is None:
            slug = self._slugify(prompt)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"output/{slug}_{timestamp}"

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        results = []
        for i in range(count):
            output_path = f"{output_dir}/v{i + 1}.png"
            result = self.generate(
                prompt=prompt,
                output_path=output_path,
                style=style,
                negative_prompt=negative_prompt,
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            )
            result["variant"] = i + 1
            results.append(result)

            if result["success"]:
                print(f"  [{i + 1}/{count}] {result['path']}")
            else:
                print(f"  [{i + 1}/{count}] Failed: {result.get('error')}")

        return {
            "success": any(r["success"] for r in results),
            "output_dir": output_dir,
            "variants": results,
            "successful": sum(1 for r in results if r["success"]),
            "total": count,
        }

    def create_grid(self, image_paths: list, output_path: str, cols: int = 2) -> dict:
        """Create a comparison grid from multiple images."""
        from PIL import Image

        # Filter valid images
        valid_paths = [p for p in image_paths if Path(p).exists()]
        if not valid_paths:
            return {"success": False, "error": "No valid images found"}

        images = [Image.open(p) for p in valid_paths]

        # Calculate grid dimensions
        n = len(images)
        rows = (n + cols - 1) // cols

        # Use first image dimensions as reference
        w, h = images[0].size

        # Create grid
        grid = Image.new("RGB", (w * cols, h * rows), color="white")

        for i, img in enumerate(images):
            row, col = divmod(i, cols)
            # Resize if needed
            if img.size != (w, h):
                img = img.resize((w, h), Image.Resampling.LANCZOS)
            grid.paste(img, (col * w, row * h))

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        grid.save(output_path)

        return {
            "success": True,
            "path": output_path,
            "images": len(valid_paths),
            "grid_size": f"{cols}x{rows}",
        }

    def _slugify(self, text: str, max_len: int = 30) -> str:
        """Create a filename-safe slug from text."""
        import re

        # Keep only alphanumeric and spaces
        slug = re.sub(r"[^\w\s-]", "", text.lower())
        # Replace spaces with underscores
        slug = re.sub(r"[\s]+", "_", slug)
        return slug[:max_len].rstrip("_")

    def _build_prompt(self, prompt: str, style: str, negative: str) -> str:
        """Build optimized prompt."""
        parts = [prompt]

        if style:
            parts.append(STYLES.get(style, style))

        parts.append("high quality, detailed")

        if negative:
            parts.append(f"Avoid: {negative}")

        return ". ".join(parts)

    def _save_image(self, response, output_path: str) -> dict:
        """Save image from response, verify it, and auto-convert JPEG to PNG if needed."""
        if hasattr(response, "candidates") and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    # Get API-reported mime type
                    getattr(part.inline_data, "mime_type", "unknown")

                    raw_data = part.inline_data.data
                    data_type = type(raw_data).__name__

                    # Handle different data types
                    if isinstance(raw_data, bytes):
                        image_data = raw_data
                    elif isinstance(raw_data, str):
                        image_data = base64.b64decode(raw_data)
                    else:
                        return {
                            "success": False,
                            "error": f"Unknown data type: {data_type}",
                        }

                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(image_data)

                    # Verify the saved file is actually an image
                    verification = verify_image(output_path)
                    if not verification["valid"]:
                        # Remove invalid file
                        Path(output_path).unlink(missing_ok=True)
                        return {
                            "success": False,
                            "error": f"Generated file is not a valid image: {verification['message']}",
                            "verification": verification,
                        }

                    # Auto-convert JPEG to PNG if output path expects PNG
                    actual_mime = verification["mime_type"]
                    if (
                        output_path.lower().endswith(".png")
                        and actual_mime == "image/jpeg"
                    ):
                        self._convert_to_png(output_path)
                        verification = verify_image(output_path)

                    return {
                        "success": True,
                        "path": output_path,
                        "verified": True,
                        "mime_type": verification["mime_type"],
                    }

        return {"success": False, "error": "No image in response"}

    def _convert_to_png(self, path: str):
        """Convert JPEG to PNG in place."""
        from PIL import Image

        img = Image.open(path)
        # Remove and resave as PNG
        img.save(path, "PNG")

    def edit(
        self,
        prompt: str,
        image_path: str,
        output_path: str = "edited.png",
        aspect_ratio: str | None = None,
        image_size: str | None = None,
    ) -> dict:
        """Edit an existing image."""
        if not Path(image_path).exists():
            return {"success": False, "error": f"Image not found: {image_path}"}

        with open(image_path, "rb") as f:
            image_data = f.read()

        suffix = Path(image_path).suffix.lower()
        mime_types = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
        mime_type = mime_types.get(suffix, "image/png")

        contents = [
            prompt,
            self.types.Part.from_bytes(data=image_data, mime_type=mime_type),
        ]

        # Build image config if any params specified
        config_params = {
            "temperature": 0.7,
            "response_modalities": ["image", "text"],
        }
        if aspect_ratio or image_size:
            image_config_params = {}
            if aspect_ratio:
                image_config_params["aspect_ratio"] = aspect_ratio
            if image_size:
                image_config_params["image_size"] = image_size
            config_params["image_config"] = self.types.ImageConfig(
                **image_config_params
            )

        config = self.types.GenerateContentConfig(**config_params)

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        return self._save_image(response, output_path)


def list_styles():
    """List available styles."""
    print("Available styles:\n")
    for key, desc in STYLES.items():
        print(f"  {key:12} - {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s "a futuristic city at sunset"
  %(prog)s "mountain landscape" -s photo -o landscape.png
  %(prog)s "cloud icon" -s icon -r 1:1 -o cloud.png
  %(prog)s "add rainbow" -e source.png -o edited.png

  # Batch variants with grid comparison
  %(prog)s "abstract tech" --variants 4 --grid comparison.png

Config: {ENV_FILE}
        """,
    )

    parser.add_argument("prompt", nargs="?", help="Image description")
    parser.add_argument("-o", "--output", default="generated.png", help="Output path")
    parser.add_argument("-s", "--style", help="Style preset or custom description")
    parser.add_argument(
        "-r",
        "--ratio",
        default="16:9",
        choices=[
            "1:1",
            "2:3",
            "3:2",
            "3:4",
            "4:3",
            "4:5",
            "5:4",
            "9:16",
            "16:9",
            "21:9",
        ],
        help="Aspect ratio",
    )
    parser.add_argument(
        "--size",
        default=None,
        choices=["1K", "2K", "4K"],
        help="Image size/resolution (4K only for gemini-3-pro)",
    )
    parser.add_argument("-n", "--negative", help="What to avoid")
    parser.add_argument(
        "-m",
        "--model",
        default=MODELS[0],
        choices=MODELS,
        help=f"Model name (default: {MODELS[0]})",
    )
    parser.add_argument("-e", "--edit", metavar="IMAGE", help="Edit existing image")
    parser.add_argument("--variants", type=int, metavar="N", help="Generate N variants")
    parser.add_argument("--grid", metavar="PATH", help="Output comparison grid")
    parser.add_argument(
        "--grid-cols", type=int, default=2, help="Grid columns (default: 2)"
    )
    parser.add_argument("--output-dir", help="Output directory for variants")
    parser.add_argument("--api-key", help="Override API key")
    parser.add_argument("--list-styles", action="store_true", help="List styles")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.list_styles:
        list_styles()
        return 0

    if not args.prompt:
        parser.error("prompt required (or use --list-styles)")

    try:
        gen = ImageGenerator(api_key=args.api_key)
        if args.model:
            gen.set_model(args.model)

        if args.edit:
            result = gen.edit(
                args.prompt, args.edit, args.output, args.ratio, args.size
            )
        elif args.variants:
            # Batch variant generation
            result = gen.generate_variants(
                prompt=args.prompt,
                count=args.variants,
                output_dir=args.output_dir,
                style=args.style,
                negative_prompt=args.negative,
                aspect_ratio=args.ratio,
                image_size=args.size,
            )

            # Generate grid if requested
            if args.grid and result["success"]:
                image_paths = [v["path"] for v in result["variants"] if v["success"]]
                grid_result = gen.create_grid(image_paths, args.grid, args.grid_cols)
                result["grid"] = grid_result
                if grid_result["success"]:
                    print(f"Grid: {grid_result['path']} ({grid_result['grid_size']})")
        else:
            result = gen.generate(
                args.prompt,
                args.output,
                args.style,
                args.negative,
                args.ratio,
                args.size,
            )

        if args.json:
            print(json.dumps(result))
        elif result["success"]:
            if "variants" in result:
                print(
                    f"Generated {result['successful']}/{result['total']} variants in {result['output_dir']}"
                )
            else:
                mime_info = (
                    f" ({result.get('mime_type', 'unknown')})"
                    if result.get("verified")
                    else ""
                )
                print(f"Generated: {result['path']}{mime_info} [verified]")
        else:
            print(f"Error: {result.get('error')}", file=sys.stderr)
            return 1

        return 0 if result["success"] else 1

    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
