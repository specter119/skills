#!/usr/bin/env python3
"""Run the synthetic fixtures through marimo_lint and compare with expected.json.

For each fixture notebook and each mode (shared = no --style, eda, report),
the set of rule ids that fire is compared with expected.json. Keys starting
with "_" in expected.json are notes and are skipped.

Usage: python3 run_fixtures.py
"""

import importlib.util
import json
import sys
from pathlib import Path

FIXTURE_DIR = Path(__file__).resolve().parent
LINTER_PATH = FIXTURE_DIR.parents[1] / "scripts" / "marimo_lint.py"
MODES = ("shared", "eda", "report")


def load_linter():
    spec = importlib.util.spec_from_file_location("marimo_lint", LINTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import linter from {LINTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    # dataclasses with slots resolve cls.__module__ via sys.modules at class
    # creation time, so the module must be registered before exec_module.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    linter = load_linter()
    expected = json.loads((FIXTURE_DIR / "expected.json").read_text(encoding="utf-8"))

    failures = 0
    for fixture_name in sorted(expected):
        fixture_path = FIXTURE_DIR / fixture_name
        if not fixture_path.exists():
            print(f"FAIL {fixture_name}: file missing")
            failures += 1
            continue
        source = fixture_path.read_text(encoding="utf-8")
        modes = expected[fixture_name]
        for mode in MODES:
            if mode not in modes:
                print(f"FAIL {fixture_name} [{mode}]: missing expectation")
                failures += 1
                continue
            style = None if mode == "shared" else mode
            rules = linter.resolve_active_rules(style=style)
            suggestions = linter.generate_suggestions(source, rules)
            actual = sorted({suggestion.rule_id for suggestion in suggestions})
            want = modes[mode]
            if actual == want:
                print(f"PASS {fixture_name} [{mode}] rules={actual}")
            else:
                print(f"FAIL {fixture_name} [{mode}] expected={want} actual={actual}")
                failures += 1

    if failures:
        print(f"{failures} case(s) failed")
        return 1
    print("all fixture cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
