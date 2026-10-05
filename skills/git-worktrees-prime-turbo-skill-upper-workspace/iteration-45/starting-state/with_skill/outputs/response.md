Short answer: don't assume any of it. Here's how to decide each piece — with one blocker on my side.

## 1. What base to use

**Base** = the commit you start *from*. It is not necessarily the branch you merge *into*.

- If the task prompt names a base (a tag, a release branch, `origin/main`, a specific SHA), use exactly that.
- Otherwise, **inspect the repo's normal integration target** — don't guess `main`, `master`, `origin`, or current `HEAD`:
  ```sh
  git -C "<repo>" worktree list --porcelain -z
  git -C "<repo>" status --short --branch
  git -C "<repo>" symbolic-ref refs/remotes/origin/HEAD   # if set
  git -C "<repo>" config --get branch.<current>.merge     # upstream of what you're on
  ```
  plus whatever the repo's own docs/CONTRIBUTING say.
- If a *current* remote base is required: fetch first, then resolve the ref before creating the worktree (`git rev-parse --verify "<base-ref>^{commit}"`). Do not pull into someone else's checkout.

## 2. Should you assume `main` is the integration target?

No. Integration target = the branch intended to **receive** the work. Confirm it explicitly from repo convention, and note base and target can differ (e.g. base on `origin/main`, target a release branch or a PR). Also remember: creating a worktree grants no authority to merge or publish — integration happens later via the repo's normal merge/rebase/PR workflow.

## 3. Task branch vs. disposable inspection checkout

Two different tools for two different intents:

```sh
# Development: dedicated task branch off the chosen base (use -b, never -B)
git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"

# Continuing a task branch that isn't checked out elsewhere (verify it exists first)
git -C "<repo>" show-ref --verify --quiet "refs/heads/<task-branch>"
git -C "<repo>" worktree add "<worktree>" "<task-branch>"

# Disposable inspection/testing: detached HEAD, no branch created
git -C "<repo>" worktree add --detach "<worktree>" "<commit>"
```

Rules that matter:
- **Reuse** the task branch across continuations. If it's already checked out in another worktree, reuse *that* checkout via its owner, or branch a different name from the required commit — never override checkout protection.
- **Detached HEAD** for throwaway inspection. If you ever commit there and care about it, anchor it to a branch before removing the worktree.
- Cleanup is decided **separately**: removing a worktree leaves its branch. `branch -d` may check the wrong ref (upstream, not your integration target), so verify with `merge-base --is-ancestor <task-tip> <integration-ref>` before deleting, and keep the branch if review is pending.
- Location: `<primary-root>/.worktrees/<task>` (or a sibling dir for a bare repo), and if it's inside another checkout, prove the destination is ignored first: `git check-ignore -q -- "<relative-path>/"` must exit 0, before *and* after creation.

## Blocker

`/tmp/skill-up-2329342548` isn't a git repository, and I found no `.git` anywhere under `/tmp` — so I can't inspect the real integration target or pick a base for you.

Give me the repo path (and feature X's scope if you have it), and I'll determine the base and integration target from the repo, then create the task worktree. Or tell me explicitly "base on `main`" and I'll take that as your instruction.
