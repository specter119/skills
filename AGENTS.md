# Agent & Developer Notes

## Local Development

Clone and validate before publishing:

```bash
git clone https://github.com/specter119/skills.git /tmp/skills
cd /tmp/skills
claude plugins validate .
./scripts/validate-skills.sh
```

## Mine History-Derived Eval Seeds

Extract real skill invocation traces from agent conversation history into anonymized eval candidates:

```bash
uv run scripts/build_history_eval_report.py --global-history
```

This uses `xurl` to retrieve session history and generates `reports/history-derived-evals.md`. Results are candidate seeds, not a replacement for formal `evals/` ground truth.

## Project Conventions

- All user-facing text and documentation must be in English.
- Skills follow the [waza](https://github.com/microsoft/waza/tree/main/skills) spec structure.
- Skill manifests are registered in `.claude-plugin/marketplace.json`.
- Only `jj` and `marimo-style` are actively maintained. Everything else lives in `.archived/` at the repo root, deliberately **outside** `skills/`. [skm](https://github.com/specter119/skm) scans only `skills/` when it exists, but it recurses into dot-directories there (it skips only `.git`), so `skills/.archived/` would still be installed. Keep archived skills out of `skills/`. To revive one, move it into `skills/` and add it to the marketplace.
- Run `./scripts/validate-skills.sh` and `./scripts/check-skill-consistency.sh` before pushing.
