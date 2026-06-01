# Essentials — Mental Model, Detection, Setup, and Commands

## Core Mental Model

jj revolves around **changes**, not branches. Key differences from Git:

- **No staging area.** File modifications are automatically part of the current change. There is no `git add`.
- **No stash.** Just `jj new` to start fresh work; previous changes stay where they are.
- **No detached HEAD.** `jj edit` lets you jump to any change and keep working; descendants auto-rebase.
- **Branches are called bookmarks** and are only needed when pushing to a remote.

The working copy IS a change. Every file modification is instantly tracked in the current change.

## Detecting a jj Repo

```bash
test -d .jj && echo "jj repo"   # If .jj/ exists, use jj — not git
```

When a repo has both `.jj/` and `.git/` (colocated mode), always prefer jj commands for local operations.

## Setup

```bash
jj git init --colocate              # Init in existing git repo (colocated mode)
jj bookmark track master@origin     # Track remote branch after init
```

jj will hint you if tracking is needed.

## Inspect State

```bash
jj log                    # Change graph + status (replaces git log + git status)
jj diff                   # Diff of current change vs parent
jj diff -r <change>       # Diff of a specific change
```

`jj log` shows `@` for the current change and short Change IDs (e.g., `kxryzmsp`). Change IDs are stable across rebases; use them or unique prefixes as references.

## Work on Changes

```bash
jj describe -m "feat: add auth module"   # Set/update description of current change
jj describe -r <change> -m "new msg"    # Update description of any change
jj new                                   # Finish current change, start new empty one
jj new <change>                          # Start work branching from a specific change
jj commit -m "feat: ..."                 # Shorthand: describe + new
jj edit <change>                         # Jump to existing change and continue editing
jj abandon                               # Discard current change entirely
jj abandon <change>                      # Discard a specific change
```

- **`jj new` is your primary "next task" command.** No add, no commit ceremony.
- **`jj abandon`** discards a change. Modifications absorb into the parent.
- **`jj edit` is safe:** immutable changes (already pushed) are blocked automatically. After `jj edit`, file modifications amend that change in place; descendants auto-rebase.

## Reorganize History

```bash
jj split                                 # Interactively split current change
jj split -r <change>                     # Split a specific change
jj rebase -s <source> -d <destination>   # Move change + descendants to new parent
jj rebase -d <destination>               # Rebase current branch onto destination
jj undo                                  # Undo the last jj operation (any operation)
jj op log                                # View operation-level history
jj op restore <operation-id>             # Restore to any previous operation state
```

`jj split` opens an interactive editor — select files/hunks for the first change; the rest become the second. `jj undo` is always safe; nothing is truly lost in jj.

## Parallel Workspaces

```bash
jj workspace add ../workspace-name       # Create parallel workspace (like git worktree)
```

Each workspace has its own directory but shares the repository store. Multiple agents can work simultaneously, then merge with `jj new <chg1> <chg2> ...`.
