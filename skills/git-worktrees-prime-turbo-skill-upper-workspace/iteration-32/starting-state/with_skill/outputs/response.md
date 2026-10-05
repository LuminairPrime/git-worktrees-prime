Based on the skill guidance:

## What base to use

- **Use the explicitly requested base** if one was given.
- Otherwise, **inspect the repository's normal integration target** rather than assuming. Check the default branch, where PRs/merges normally land, or ask the user/manager.
- **Do not assume** `main`, `master`, `origin/...`, or the current `HEAD` is correct.
- If a *current remote base* is required, fetch that remote and resolve its ref **before** creating the worktree — and don't pull/reset inside someone else's checkout.

## Should you assume `main` is the integration target?

**No.** The base (where the task starts) and the integration target (where it lands) may differ — e.g., a feature branch integrates into a release branch, or `develop` rather than `main`. Determine it from repo convention (PR base, default branch, manager inventory) and keep it explicit in the task context.

## Task branch vs. disposable inspection checkout

| Purpose | Ref to use |
|---|---|
| Implementing feature X (development) | Create a **task branch** from the resolved base commit (`git worktree add -b <task-branch> ...`). Reuse that same branch/checkout for continuation. |
| Disposable inspection/testing | Use a **detached HEAD** checkout (`git worktree add --detach ...`). |

Key rules:
- Never use `git worktree add -B` just to force the branch — that resets the branch ref, which is only OK if authorized; prefer `-b`.
- If the desired task branch is already checked out in another worktree, don't fight checkout protection — reuse that checkout via its owner or pick a different branch from the required commit.
- Anchor any valuable commits made in a detached checkout to a branch **before** removing that disposable worktree, or they'll be lost.

If you want me to set this up for you, I can check the repo's remote/default branch and create the worktree — just tell me the task name and (if known) the intended base/target.
