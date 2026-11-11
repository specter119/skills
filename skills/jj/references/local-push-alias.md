# Appendix — Configuring `jj push` (Author's Local Setup)

The rest of this skill uses `jj push` as the push command. That name is **not built into jj** — it is a user-level alias that wraps [`jj-pre-push`](https://github.com/acarapetis/jj-pre-push), so that pre-push checks run before a bookmark is pushed. This appendix records the exact configuration.

Do not check for the alias before pushing: call `jj push` and open this appendix only if it fails as an unknown command. In that case `jj git push` is the built-in replacement and accepts the same flags (`--bookmark`, `--deleted`, `--remote`, `--all`, ...).

## Requirements

| Tool                                                                          | Purpose                                                                              |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [jj](https://jj-vcs.github.io/jj/)                                            | the VCS itself                                                                       |
| [jj-pre-push](https://github.com/acarapetis/jj-pre-push)                      | runs pre-push hooks, then delegates to `jj git push`                                 |
| [prek](https://github.com/j178/prek) or [pre-commit](https://pre-commit.com/) | the hook runner (`prek` is the default here; `jj-pre-push` defaults to `pre-commit`) |

This repository has no `.pre-commit-config.yaml`; it keeps its hooks in `prek.toml`, which jj-pre-push reads when invoked as `--checker prek`.

## Install

```bash
uv tool install jj-pre-push
uv tool install prek            # or: pipx install pre-commit
```

## Configure the alias

```bash
jj config set --user aliases.push \
  '["util", "exec", "--", "jj-pre-push", "--checker", "prek", "push"]'
```

The same thing in `~/.config/jj/config.toml`:

```toml
[aliases]
push = ["util", "exec", "--", "jj-pre-push", "--checker", "prek", "push"]
```

`--checker prek` selects the hook runner; omit it to fall back to the `jj-pre-push` default of `pre-commit`. To avoid a global install entirely, point the alias at `uvx`:

```toml
[aliases]
push = ["util", "exec", "--", "uvx", "jj-pre-push", "--checker", "prek", "push"]
```

## Verify

```bash
jj push --help        # should print jj git push's option list, not an alias error
```

## What the alias actually does

1. Computes which bookmarks `jj git push` would update and how.
1. For each bookmark, checks it out, runs the pre-push hooks on the same file set pre-commit would use, and reports failures (plus the change IDs where hook-side edits landed).
1. Only if every hook passes, runs `jj git push` with the arguments you passed.
1. Restores your working copy to the original change.

By default it is silent unless a hook fails. Add `--log-level INFO` for detail:

```bash
jj push --log-level INFO
```

## Which hooks run on push

The stage is **not configurable from jj**. `jj-pre-push` hard-codes `prek run --hook-stage pre-push` (0.5.2) and exposes only `--checker`, `--config`, `--mode`, `--log-level` (env: `JJ_PRE_PUSH_CHECKER`, `JJ_PRE_PUSH_CONFIG`, `JJ_PRE_PUSH_MODE`, `JJ_PRE_PUSH_LOG_LEVEL`). There is no stage option and no `JJ_PRE_PUSH_STAGE`, so a jj alias cannot change it; only `jj-pre-push` itself could.

Config discovery (jj-pre-push 0.5.2): `.pre-commit-config.yaml`, plus `prek.toml` and `.pre-commit-config.yml` when `--checker prek` is used. A workspace with none of them delegates to `jj git push` immediately.

Stage filtering is entirely a `prek` concern, configured in `prek.toml`:

- `default_stages` (top level) — config-wide default for the `stages` property.
- `stages` on a hook — per-hook restriction.

**`prek` is not `pre-commit` here.** Per its schema, `stages` defaults to *all* stages, so a hook with no `stages` key runs on `pre-push` too. Verified in this repo: `prek run --stage pre-push -a --dry-run` selects every hook in `prek.toml`. This repository declares no `stages` anywhere, so `jj push` runs the whole `prek.toml` set, scoped to the pushed files (existing bookmark: files in `old...new`; new bookmark: files in ancestors of `new` not present on the remote).

To narrow or widen that, declare stages explicitly — e.g. keep a hook off pushes, or dedicate one to them:

```toml
[[repos]]
repo = "local"
hooks = [
  { id = "validate-skills", entry = "./scripts/validate-skills.sh", language = "script", stages = ["pre-push"] },
]
```

Note: `pre-commit`'s behaviour of confining undeclared hooks to the `pre-commit` stage does **not** apply — a plain hook is not skipped on push.

`--mode remote-ancestors` (experimental) narrows the checked file set to changes since the most recent commit already on the remote.

## Caveats

- Because the alias forwards through `jj util exec`, `jj push` does not appear in `jj help`'s command list, only under aliases.
- If a hook rewrites files, the edits are preserved in your working copy; `jj-pre-push` reports the affected change IDs so you can review or squash them.
- `jj push` inherits every `jj git push` safety rule (bookmark conflicts, force-with-lease-like remote checks). Fix with `jj git fetch` and bookmark conflict resolution, not by force.
