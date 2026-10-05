Short answer: **don't assume `main` for anything** — verify it. Also, this working directory (`/tmp/skill-up-2166747799`) is not a git repository, so I can't inspect your actual repo yet. Here's how to decide each piece:

## 1. What base to use

- **If a base was specified in the task/request, use exactly that.** Otherwise, inspect the repository's *normal* integration target rather than guessing.
- Do **not** assume `main`, `master`, `origin/*`, or your current `HEAD` is correct. Common ways to find the real one:
  - `git remote show origin` → `HEAD branch`
  - `.github/workflows/*`, `.gitlab-ci.yml`, `Makefile` targets, `CONTRIBUTING.md` — they name the branch CI builds against
  - `git branch -r --sort=-committerdate` and recent merge history
- If a *current* remote base is required, fetch first and resolve the ref, e.g.:
  ```sh
  git -C "<repo>" fetch origin
  git -C "<repo>" rev-parse --verify "origin/main^{commit}"   # once you've confirmed the name
  ```
  Don't pull into someone else's checkout.

## 2. Base vs. integration target

These are **separate decisions**. The base is the commit you *start from*; the integration target is the branch that will eventually *receive* the work. They can differ (e.g., branch from `develop`, merge into `main`; or branch from a release tag but PR against `release/1.4`). Record both explicitly before creating anything.

## 3. Task branch vs. disposable inspection checkout

They serve different purposes — use both, in separate worktrees:

| Intent | Command |
|---|---|
| **Developing feature X** (persistent, has commits) | `git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"` |
| **Continuing an existing task branch** (not checked out elsewhere) | `git show-ref --verify --quiet refs/heads/<task-branch>` first (exit 0), then `git worktree add "<worktree>" "<task-branch>"` |
| **Disposable inspection/testing** (throwaway, no commits) | `git -C "<repo>" worktree add --detach "<worktree>" "<commit>"` |

Rules that matter:
- **Development needs a named branch.** A detached HEAD loses its commit when the worktree is removed unless you anchor it to a branch first. If the branch is already checked out in another worktree, reuse that checkout (via its owner) or pick a different branch — never override checkout protection.
- **Inspection should be detached** so you can't accidentally commit onto a real branch, and so removal is trivially safe.
- Use `-b` for creation; **never `-B`** (that resets an existing branch to your chosen commit).
- Location: follow the repo's convention, else `<primary-root>/.worktrees/<feature-x>`, with a unique task name. If you create it *inside* another checkout, confirm the destination is ignored first: `git check-ignore -q -- ".worktrees/feature-x/"` must exit 0, before **and** after creation. Never nest a worktree inside a disposable one.

## 4. Lifecycle, briefly

- Keep edits/builds/tests/commits in the task worktree; verify `git -C "<worktree>" rev-parse --show-toplevel`, `status --short --branch`, and `rev-parse HEAD` after creation.
- Cleanup is two *separate* decisions: remove the checkout, delete the branch. Prove integration first with `git merge-base --is-ancestor "<task-tip>" "<integration-ref>"` — `branch -d` may check the upstream instead of your intended target, so its success isn't proof. A closed PR alone isn't evidence either.
- If the checkout was moved/renamed since creation, run `git worktree repair "<worktree>"` **before** anything else — not `cd`, `status`, or pruning.

**If you point me at the actual repository path, I'll determine its real integration target and set up the worktree for you.**
