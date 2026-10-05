Short answer: **don't assume `main` for anything** — treat base and integration target as two separate facts to verify, and pick the branch mode based on whether the checkout produces work you intend to keep.

## 1. Base vs. integration target — keep them separate

The skill's glossary is explicit: the **base** (commit/ref you start from) and the **integration target** (branch meant to receive the work) may differ. Examples: branch off `release/2.4` but PR into `main`, or branch off `main` but target a hotfix branch.

Decision order for the base:
1. **A base was explicitly requested?** Use it exactly (e.g., "branch off `origin/release/2.4`").
2. **Otherwise, inspect the repo's normal integration target** — check the remote's default branch (`git remote show origin` / `git symbolic-ref refs/remotes/origin/HEAD`), contributing docs, and existing branch naming conventions.
3. **Never infer from `main`, `master`, `origin`, or the current `HEAD`** of whatever checkout you happen to be in.

If you need a *current* remote base, fetch first and resolve the ref — and don't pull into someone else's checkout to get it.

## 2. Should you assume `main` is the target?

No. `main` is a *common* target, but worktree creation alone doesn't tell you the workflow, and it certainly doesn't authorize merging or publishing. Record the intended target explicitly in the task context (along with checkout path, branch, and starting commit) and follow the repo's merge/rebase/squash/PR convention. If it's genuinely ambiguous, ask before integrating.

## 3. Task branch vs. disposable inspection checkout

| Purpose | Mode | Command shape | Notes |
|---|---|---|---|
| **Developing feature X** | Dedicated task branch | `git worktree add -b feature-x /path/to/checkout <base>` | Reuse this same branch for continuation. If it's already checked out elsewhere, reuse that checkout through its owner or create a *different* branch name — never override checkout protection. Never use `add -B` unless resetting that branch is authorized. |
| **Disposable inspection / testing** | Detached HEAD | `git worktree add --detach /path/to/checkout <commit>` | Nothing here is meant to survive. Before removing the checkout, **anchor any detached commit that turned out to be valuable onto a branch** — detached commits can silently disappear with the directory. |

Practical details:

- **Location**: prefer the repo's own convention; otherwise `<primary-root>/.worktrees/<task>`. If it's inside another checkout, ensure the destination is git-ignored (`.gitignore` or `info/exclude`, verified with `git check-ignore -q`).
- **Uncommitted changes don't travel** into a new raw-Git worktree — transfer only what you deliberately need; don't blanket-copy or stash across.
- **Communicate path and branch separately** — removing a worktree does *not* delete its branch.
- If a harness worktree tool is available, prefer it, but check its starting-state, dirty-file transfer, and cleanup behavior rather than assuming defaults.

So for feature X: confirm or discover the real integration target, fetch and base off the appropriate current ref, create `feature-x` as a task branch in its own worktree under `.worktrees/`, and reserve detached checkouts strictly for throwaway look-and-test runs.

If you point me at the actual repository, I can verify its default branch and conventions and set the worktree up.
