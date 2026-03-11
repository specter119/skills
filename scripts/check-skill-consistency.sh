#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

MARKETPLACE_FILE=".claude-plugin/marketplace.json"

if [ ! -f "$MARKETPLACE_FILE" ]; then
    echo "Missing $MARKETPLACE_FILE"
    exit 1
fi

mapfile -t MARKETPLACE_SKILLS < <(jq -r '.plugins[].skills[]' "$MARKETPLACE_FILE")

if [ "${#MARKETPLACE_SKILLS[@]}" -eq 0 ]; then
    echo "No skills declared in $MARKETPLACE_FILE"
    exit 1
fi

FAILED=0

for skill_path in "${MARKETPLACE_SKILLS[@]}"; do
    skill_dir="${skill_path#./}"
    skill_file="$skill_dir/SKILL.md"

    if [ ! -d "$skill_dir" ]; then
        echo "Missing marketplace skill directory: $skill_dir"
        FAILED=1
        continue
    fi

    if [ ! -f "$skill_file" ]; then
        echo "Missing SKILL.md for marketplace skill: $skill_dir"
        FAILED=1
        continue
    fi

    dir_name="$(basename "$skill_dir")"
    frontmatter_name="$(sed -n 's/^name:[[:space:]]*//p' "$skill_file" | head -n 1)"

    if [ -z "$frontmatter_name" ]; then
        echo "Missing frontmatter name in $skill_file"
        FAILED=1
        continue
    fi

    if [ "$frontmatter_name" != "$dir_name" ]; then
        echo "Frontmatter name mismatch in $skill_file: expected '$dir_name', got '$frontmatter_name'"
        FAILED=1
    fi
done

for skill_dir in skills/*; do
    [ -d "$skill_dir" ] || continue
    skill_ref="./$skill_dir"
    if ! printf '%s\n' "${MARKETPLACE_SKILLS[@]}" | rg -qx --fixed-strings "$skill_ref"; then
        echo "Skill directory not listed in marketplace: $skill_dir"
        FAILED=1
    fi
done

exit "$FAILED"
