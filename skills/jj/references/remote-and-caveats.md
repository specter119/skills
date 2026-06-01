# Remote Interaction, Common Mistakes, and Advanced Help

## Remote Interaction (Git Bridge)

### Fetch and Rebase

```bash
jj git fetch                             # Fetch from remote (like git fetch)
jj rebase -d master                       # Rebase current work onto latest master
```

### Bookmarks (Git Branches)

Remote Git branches map to jj **bookmarks** on fetch. The `master`/`main` in `jj log` IS the remote branch, accessed via bookmark.

After `jj git init --colocate` or when a new remote branch appears, you may need `jj bookmark track <name>@<remote>`. jj hints you when this is needed.

```bash
jj bookmark track master@origin          # Track a remote branch
jj bookmark create my-feature -r @       # Create bookmark pointing at current change
jj bookmark create my-feature -r <chg>   # Create bookmark pointing at specific change
jj bookmark set my-feature -r <change>   # Move existing bookmark to different change
```

### Push Workflow

1. Finish your work (`jj describe` the change)
2. `jj bookmark create <name> -r <change>` — give it a Git branch name
3. `jj push` — push to remote (or `--bookmark <name>` for just one)

```bash
jj push                                  # Push all changed bookmarks (uses jj-pre-push alias)
jj push --bookmark my-feature            # Push only a specific bookmark
jj push --deleted                         # Push bookmark deletions after jj abandon
```

> **Note:** `jj push` is a custom alias running `jj-pre-push push`, which checks pre-commit hooks. Use `jj git push` directly to bypass checks.

### Cleanup After Abandoning a Pushed Change

When you `jj abandon` a change whose bookmark was pushed to remote, the bookmark is deleted locally. Use `jj push --deleted` to sync the deletion to remote.

## Common Mistakes to Avoid

- **Do not use `git add`, `git commit`, `git stash`, or `git checkout` in a jj repo.** Use jj equivalents.
- **Do not `jj edit` an immutable (published) change.** jj blocks this. Use `jj new <change>` to create a follow-up instead.
- **Do not create bookmarks for local-only work.** Bookmarks are only for pushing to remote; local work uses Change IDs.
- **Do not worry about "losing" changes.** jj's operation log preserves everything; use `jj undo` or `jj op restore` to recover.

## Beyond This Skill

jf has rich functionality (revsets, templates, custom aliases, conflict resolution, etc.) not covered here:

```bash
jj help                  # List all commands
jj help <command>        # Detailed help for a specific command
jj help -k <keyword>     # Search help by keyword
```

Official documentation: https://jj-vcs.github.io/jj/
