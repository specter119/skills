---
name: jj
description: "Use jj (Jujutsu) for local version control instead of git. Activate when: the repo has a .jj/ directory, the user or project config mentions jj, the user says 'use jj', or any version control operation is needed in a jj-managed repo."
---

# jj (Jujutsu) — Version Control for Agent Workflows

**UTILITY SKILL** for local version control. jj coexists with Git: use jj locally; the remote is standard Git.

## USE FOR

- Local version control in repos with a `.jj/` directory
- Committing, branching, rebasing, splitting, or undoing changes with jj
- Agent-assisted workflows requiring change-by-change iteration

## DO NOT USE FOR

- Repos without `.jj/` — use git instead
- Production CI/CD pipeline configuration
- Advanced jj features beyond common operations (use `jj help`)

## Execution Skeleton

1. Detect: `test -d .jj`. If absent, do not activate.
2. Use jj commands for all local VCS operations.
3. For workflows and remote interaction, see reference modules.

## Reference Map

- [essentials](references/essentials.md): Mental model, detection, setup, inspect/work/reorganize commands, parallel workspaces
- [workflow-patterns](references/workflow-patterns.md): Five agent workflow patterns (start task, interrupt/resume, split, skeleton planning, undo)
- [remote-and-caveats](references/remote-and-caveats.md): Git bridge, bookmarks, push, cleanup, common mistakes, advanced help

## Quick Reference

| Task | Command |
|------|---------|
| Init in git repo | `jj git init --colocate` |
| See status | `jj log` |
| Describe change | `jj describe -m "..."` |
| Start next task | `jj new` |
| Edit older change | `jj edit <change>` |
| Discard change | `jj abandon` |
| Split change | `jj split` |
| Undo anything | `jj undo` |
| Fetch remote | `jj git fetch` |
| Rebase onto master | `jj rebase -d master` |
| Create bookmark | `jj bookmark create <name> -r @` |
| Push | `jj push` / `jj push --bookmark <name>` |
