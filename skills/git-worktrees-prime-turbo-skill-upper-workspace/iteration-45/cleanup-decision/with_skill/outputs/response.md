`/repo` doesn't exist in this environment, so nothing can be run against it here — below is the ordered walkthrough for that exact path. Short answer: **yes for remove + prune, "not automatically" for the branch** — a squash merge breaks ancestry, so `branch -d` will (correctly) refuse, and `-D` needs your explicit authorization.

## Check 1 — Confirm the registration and canonical path

```sh
git -C /repo worktree list --porcelain -z
```

Verify `/repo/.worktrees/old-task` is listed as a linked worktree. Rule out:
- the primary checkout (`/repo` itself),
- your current working directory,
- its parent directory and any sibling task checkouts.

If the path was moved/renamed/mounted since the task started, stop and run `git -C /repo worktree repair /repo/.worktrees/old-task` first — repair before any removal or prune decision.

## Check 2 — Still in use?

Any agent, editor, terminal, service, or test still pointed at that directory? Retain until that use ends. Leave the directory before removal; stop only task-owned processes.

## Check 3 — Would anything disappear?

```sh
git -C /repo/.worktrees/old-task status --short --branch --untracked-files=all
git -C /repo/.worktrees/old-task status --short --ignored
git -C /repo/.worktrees/old-task rev-parse HEAD
```

- Untracked/ignored files (build outputs excepted) and any detached commits die with the directory — preserve or get authorization to discard.
- Check for unfinished operations (in-progress rebase/merge, `index.lock`).
- Check submodules/nested repositories separately.
- A clean status alone does **not** prove ignored files or detached commits are disposable.

## Check 4 — Verify the squash actually integrated

```sh
git -C /repo worktree list --porcelain -z   # find the branch name
git -C /repo merge-base --is-ancestor <task-tip> <integration-ref>
```

Expect **exit 1 here, and that's normal for squash** — ancestry is broken by design, so this command proves nothing either way. Instead verify the replacement commit and resulting changes:

```sh
git -C /repo log --oneline -5 <integration-ref>
git -C /repo diff <task-tip> <squash-commit>
```

Record the squash commit. The diff should show only unrelated post-merge changes, not your task's changes. A closed/merged PR alone is insufficient evidence.

## Check 5 — Remove the checkout

```sh
git -C /repo worktree remove /repo/.worktrees/old-task
```

Only if checks 1–4 pass. Remove exactly that path through Git — never by deleting the directory with `rm`/a file manager. If it refuses because of dirty state, resolve the state (Check 3); do **not** add `--force` without explicit authorization for the data being discarded.

## Check 6 — Delete the branch (separate decision)

```sh
git -C /repo branch -d <task-branch>
```

- Success is **not** proof of integration — `branch -d` may only check the branch's upstream, not your intended target.
- On a squash merge, `branch -d` will almost certainly refuse. That refusal is the safety net, not an obstacle: keep the branch until the obsolete history is verified safe (Check 4) **and** you have authorization to delete it. Only then `branch -D`.
- If review could still continue from the branch, retain it regardless.

## Check 7 — Prune (dry run first)

```sh
git -C /repo worktree prune --dry-run --verbose
```

Review **every** entry: prune only if each is an intentionally removed worktree. A missing directory may be an offline volume — do not prune it just because it's unavailable, and don't change expiry options from the reviewed dry run. Note that after a clean `worktree remove` there's usually nothing left to prune; prune clears stale metadata only, never branches or checkout directories.

```sh
git -C /repo worktree prune --verbose
```

## Check 8 — Verify

```sh
git -C /repo worktree list --porcelain -z
git -C /repo show-ref --verify --quiet refs/heads/<task-branch>
```

Confirm the path is gone from the registration and the branch state matches what you decided (deleted, or retained with the reason). Report anything retained and why — don't call it fully deleted if a branch or archive still exists.

**Expected outcome:** checks 1–5 should pass cleanly; step 6 is where a squash-merged branch parks until you confirm the squash commit replaces it; step 7 likely reports nothing to prune.
