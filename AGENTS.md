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
- Run `./scripts/validate-skills.sh` and `./scripts/check-skill-consistency.sh` before pushing.
