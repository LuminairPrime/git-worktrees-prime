No — I won't do that, and there's nothing here to do it to anyway.

**Two blockers:**

1. **No repository.** `/tmp/skill-up-3815112649` isn't a Git repo (and has no subdirectories other than `.opencode`), so there's no worktree, branch, or registration to operate on.

2. **The shortcut itself is the unsafe path.** Each of the three commands you asked for needs authorization and/or a dry run first:

| Requested | Why it can't run as-is |
|---|---|
| `git worktree add -B` | `-B` *resets the named branch to the new base*. That rewrites a branch pointer — any commits only on the old tip become unreferenced. Needs explicit authorization for that branch and consequence. |
| `rm -rf <old worktree>` | Deletes the directory outside Git, so uncommitted tracked changes, untracked/ignored files, and detached commits go with it — silently. Correct form is `git worktree remove` after the cleanup checks. |
| `git worktree prune` (no dry run) | Prune removes registrations you haven't reviewed. A missing directory can be an offline volume or a relocated checkout needing `git worktree repair`, not deletion. |

**If you're in a hurry, the fast safe version is this** — it's about the same number of commands:

```sh
git -C "<repo>" worktree list --porcelain -z            # confirm paths/branches
git -C "<old-worktree>" status --short --branch --untracked-files=all
git -C "<repo>" show-ref --verify --quiet refs/heads/<task-branch>
git -C "<repo>" worktree add "<new-path>" "<task-branch>"   # no -B, keeps history
git -C "<repo>" worktree remove "<old-worktree>"
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```

**Give me the authorization and I'll run the forceful version immediately.** I need:
- the repo path, old worktree path, new base, and branch name;
- confirmation that resetting `<branch>` to the new base is intended (or that its old tip is disposable);
- confirmation that any uncommitted/untracked/detached state in the old worktree may be destroyed.

Also tell me if the workspace was moved or renamed — if so, the first command is `git worktree repair "<worktree>"`, not prune.
