Short answer: don't assume — inspect the repo's conventions first. Here's the breakdown.

## What base to use

Use the base the task/owner specifies. If none is specified, inspect the repository's normal integration point rather than guessing:

- Check the default branch and remote HEAD: `git -C <repo> symbolic-ref refs/remotes/origin/HEAD` or `git -C <repo> remote show origin`.
- Check repo conventions (CONTRIBUTING, release/versioning docs) — many repos integrate into `develop`, a release branch, or a specific feature/integration branch.
- For a current remote base, fetch first and resolve the ref, then branch from that: `git -C <repo> rev-parse --verify "<base-ref>^{commit}"`.

## Should you assume `main` is the integration target?

No. The **base** (where you start) and the **integration target** (where your work lands) are distinct and can differ. Don't assume `main`, `master`, `origin`, or current `HEAD` is either one. Determine the target explicitly and get it confirmed before you integrate. Keep path, branch, starting commit, and integration target explicit in the task record.

## Task branch vs disposable inspection checkout

These are two different jobs, and you should keep them separate:

**Task branch (development):**
- Create a real branch from the selected base: `git worktree add -b <task-branch> <worktree> <base-ref>`
- Reuse this branch/checkout for continuation; don't recreate it.
- Creation is not authorization to merge or push — integration needs its own authority.

**Disposable inspection checkout:**
- Use detached HEAD for read-only exploration/testing: `git worktree add --detach <worktree> <commit>`
- No branch is created. If you produce a valuable commit while detached, **anchor it to a branch before removing the checkout** — otherwise it's lost.

Rule of thumb: if it's throwaway inspection, detach. If it's the implementation of feature X, give it a branch.

## Practical sequence

```sh
# 1. Inspect source, base, and inventory
git -C <repo> worktree list --porcelain -z
git -C <repo> status --short --branch          # only if <repo> is a checkout
git -C <repo> rev-parse --verify "<base-ref>^{commit}"

# 2. Task worktree on a new branch
git -C <repo> worktree add -b <task-branch> <worktree> <base-ref>

# 3. Verify
git -C <worktree> rev-parse --show-toplevel
git -C <worktree> status --short --branch
git -C <worktree> rev-parse HEAD
```

A couple of gotchas: an existing branch already checked out elsewhere can't be checked out in a second worktree (reuse the owner's checkout or branch from the required commit instead), and uncommitted changes don't follow a raw `worktree add` — transfer only what's needed deliberately.

Also note: this environment isn't a Git repo, so these are general instructions. If you tell me the repo path and the intended integration branch, I can run the inspection and set the worktree up for you.
