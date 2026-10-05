`/repo` doesn't exist in this environment, so this is a walkthrough of the checks you'd run — in order, from a surviving checkout or the main repository.

The three operations are decided **separately**: removing the checkout, deleting the branch, and pruning stale registrations. One passing doesn't imply the others.

---

### 0. Confirm which checkout this is (before anything else)

```sh
git -C /repo worktree list --porcelain -z
```

Confirm `/repo/.worktrees/old-task` is registered, is a **linked** worktree (not the primary checkout), and that its path is yours. Exclude the primary checkout, your current working directory, and any sibling tasks from any removal.

> If the checkout had been moved/renamed, you'd run `git worktree repair "<current-path>"` first — not applicable here since you're removing it, but registration must be intact to remove it cleanly.

---

### 1. Still in use? (blocks removal)

Any agent, editor, terminal, service, or test still working there? Stop task-owned processes and leave the directory before removal. Don't clean another worker's checkout.

---

### 2. Would anything valuable disappear with the directory?

```sh
git -C /repo/.worktrees/old-task status --short --branch --untracked-files=all
git -C /repo/.worktrees/old-task status --short --ignored
git -C /repo/.worktrees/old-task rev-parse HEAD
```

A clean status is **not** sufficient: it doesn't cover ignored files or detached commits. Check submodules/nested repos separately, and any unfinished Git operations. Preserve valuable state outside the deletion path, or get explicit authorization to discard it. Reproducible build output needs no backup.

---

### 3. Safe to remove the checkout?

Only if 1 and 2 pass. Then:

```sh
git -C /repo worktree remove /repo/.worktrees/old-task
```

Use `git worktree remove` (or the harness manager), **not** `rm -rf`. If it refuses due to uncommitted changes, that's the safeguard working — resolve the state, don't reach for `--force` without explicit authorization for the consequence.

---

### 4. Safe to delete the branch? (independent decision)

The branch survives checkout removal. You said the work was **squash-merged**, which breaks ancestry — so expect the normal proof to fail:

```sh
git -C /repo merge-base --is-ancestor <task-tip> <integration-ref>
```

Exit 0 would prove integration; for a squash merge it will exit non-zero. So verify manually:

```sh
git -C /repo rev-parse <task-branch>
git -C /repo fetch <remote>          # if the target lives on a remote
git -C /repo log --oneline -1 <integration-ref>
git -C /repo diff <task-tip> <integration-ref> -- .   # expect empty for your files
```

Confirm the replacement commits actually contain the task's changes.

Then:

```sh
git -C /repo branch -d old-task
```

`-d` will refuse here (no ancestry), which is Git telling you it can't prove integration. **Do not switch to `-D` by default** — only after the obsolete history is verified safe *and* you're authorized to abandon it. Note also that `-d` may check the branch's upstream rather than your real integration target, so a successful `-d` isn't itself proof of integration. Retain the branch if review is still pending — a closed PR alone is not evidence of integration.

---

### 5. Prune only stale metadata

Pruning removes obsolete **registrations**, not branches and not directories.

```sh
git -C /repo worktree list --porcelain -z
git -C /repo worktree prune --dry-run --verbose
```

Review **every** dry-run entry: each must be an intentionally removed worktree. A missing directory may be an offline volume — do not prune or unlock it just because it's unavailable (lock it instead if the volume will come back). Then:

```sh
git -C /repo worktree prune --verbose
```

Don't use different expiry options than the ones you reviewed in the dry run.

---

### 6. Verify

```sh
git -C /repo worktree list --porcelain -z
git -C /repo show-ref --verify refs/heads/old-task
```

The path should be gone from the list; the branch ref should be gone if you deleted it. Report anything retained and why — don't claim full deletion if a branch, snapshot, or archive remains.

**Bottom line:** checkout removal and pruning are routine here (steps 1–3, 5–6). Branch deletion is the one that needs real judgment, because squash merging means Git can't verify it for you — confirm the changes landed in the target, then decide on `-d` vs. `-D` explicitly.
