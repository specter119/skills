#!/bin/bash
# Validate skills using the vendored quick validator.

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATE_SCRIPT="$ROOT_DIR/scripts/quick_validate.py"

if [ ! -f "$VALIDATE_SCRIPT" ]; then
    echo "Missing validator script: $VALIDATE_SCRIPT"
    exit 1
fi

# Find skills directory
SKILLS_DIR="$ROOT_DIR/skills"
if [ ! -d "$SKILLS_DIR" ]; then
    echo "No skills/ directory found"
    exit 0
fi

# Validate each skill
FAILED=0
for skill in "$SKILLS_DIR"/*/; do
    if [ -f "$skill/SKILL.md" ]; then
        if ! python3 "$VALIDATE_SCRIPT" "$skill"; then
            FAILED=1
        fi
    fi
done

exit $FAILED
