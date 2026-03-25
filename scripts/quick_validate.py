#!/usr/bin/env python3
"""
Standalone skill validator with no third-party dependencies.

Adapted from Anthropic's skill-creator validator:
https://github.com/anthropics/skills/blob/main/skill-creator/scripts/quick_validate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_PROPERTIES = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}

BLOCK_SCALARS = {">", ">-", "|", "|-"}


def extract_frontmatter(content: str) -> str | None:
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.DOTALL)
    if match is None:
        return None
    return match.group(1)


def strip_outer_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def collect_indented_block(lines: list[str], start: int) -> tuple[list[str], int]:
    block: list[str] = []
    index = start

    while index < len(lines):
        line = lines[index]
        if line.startswith(" ") or line.startswith("\t") or line == "":
            if line.startswith(" "):
                block.append(line[1:])
            elif line.startswith("\t"):
                block.append(line[1:])
            else:
                block.append("")
            index += 1
            continue
        break

    return block, index


def fold_block_scalar(lines: list[str], style: str) -> str:
    stripped = [line.rstrip() for line in lines]
    if style.startswith(">"):
        parts = [line.strip() for line in stripped if line.strip()]
        return " ".join(parts)
    return "\n".join(stripped).strip()


def parse_frontmatter(frontmatter_text: str) -> dict[str, object]:
    parsed: dict[str, object] = {}
    lines = frontmatter_text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith(" ") or line.startswith("\t"):
            index += 1
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):(.*)$", line)
        if match is None:
            index += 1
            continue

        key = match.group(1)
        raw_value = match.group(2).strip()
        index += 1

        if raw_value in BLOCK_SCALARS:
            block, index = collect_indented_block(lines, index)
            parsed[key] = fold_block_scalar(block, raw_value)
            continue

        if raw_value == "":
            block, index = collect_indented_block(lines, index)
            parsed[key] = {} if block else ""
            continue

        parsed[key] = strip_outer_quotes(raw_value)

    return parsed


def validate_skill(skill_path: str) -> tuple[bool, str]:
    skill_dir = Path(skill_path)
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    frontmatter_text = extract_frontmatter(content)
    if frontmatter_text is None:
        return False, "Invalid frontmatter format"

    frontmatter = parse_frontmatter(frontmatter_text)
    unexpected_keys = set(frontmatter) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        return (
            False,
            f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)",
        )
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return (
            False,
            f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
        )
    if len(name) > 64:
        return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return (
            False,
            f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
        )

    compatibility = frontmatter.get("compatibility", "")
    if compatibility and not isinstance(compatibility, str):
        return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
    if isinstance(compatibility, str) and len(compatibility) > 500:
        return (
            False,
            f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters.",
        )

    return True, "Skill is valid!"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        return 1

    valid, message = validate_skill(sys.argv[1])
    print(message)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
