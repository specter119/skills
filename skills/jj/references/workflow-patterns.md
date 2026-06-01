# Agent Workflow Patterns

Five patterns leveraging jj's strengths for agent-assisted development.

## Pattern 1: Start Next Task

Just `jj new` and begin. The previous change is automatically preserved.

```bash
jj new
jj describe -m "feat: implement avatar upload"
# start working...
```

## Pattern 2: Interrupt and Resume

Handle an urgent task mid-work, then resume:

```bash
jj new master              # Branch off master for the urgent fix
# ... do the fix ...
jj describe -m "fix: critical auth bug"
jj edit <previous-change>  # Jump back to previous work
# ... resume ...
```

No stash, no branch switching, no state to restore.

## Pattern 3: Split After the Fact

After producing a large change, split it into logical pieces:

```bash
jj split                  # Interactive: pick files/hunks for first change; rest becomes second
jj split                  # Split again if needed
```

If a split goes wrong, `jj undo` and try again.

## Pattern 4: Skeleton Planning (Recommended for Complex Tasks)

Create empty changes as a plan, then fill them in order:

```bash
jj commit -m "refactor: extract auth module"
jj commit -m "feat: add token refresh logic"
jj commit -m "test: update auth tests"
jj commit -m "docs: update API documentation"
```

Then work through them:

```bash
jj edit <first-change>    # Jump to first skeleton change
# ... implement ...
jj edit <next-change>     # Previous work auto-rebases descendants
# ... implement ...
```

Each change's description is both the commit message and acceptance criteria. The description field supports git-style format: first line title, blank line, then body (detailed specs with `-m`).

## Pattern 5: Undo and Recover

```bash
jj undo                  # Undo last operation, no questions asked
jj op log                # See full operation history
jj op restore <op-id>    # Jump to any point in operation history
```

Prefer `jj undo` over manually reversing changes. It is always correct and safe.
