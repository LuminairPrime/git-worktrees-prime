---
name: git-worktrees-prime-turbo
description: Manage Git worktrees for isolated or parallel development. Use when creating, listing, reusing, or removing worktrees; working in a separate checkout; integrating task branches; repairing moved checkouts; or pruning stale worktree registrations.
---

# Git worktrees

Follow user instructions and repository conventions; keep ownership and the integration target explicit.

## Glossary

| Term | Meaning |
|---|---|
| Repository | The shared commit history and named references used by its worktrees. |
| Worktree / checkout | A directory of checked-out files with its own `HEAD` and index (staging area). Here, the noun **checkout** means this workspace. |
| Branch | A named reference to the latest commit in a line of development. A commit records a project snapshot and its history links. A branch can exist without a checkout. |
| `HEAD` / detached HEAD | Each worktree's `HEAD` normally names its checked-out branch. A detached `HEAD` points directly to a commit, so new commits do not advance a branch. |
| Main (primary) / linked worktree | The main worktree is the repository's original checkout; additional worktrees are linked worktrees. `<primary-root>` means the main worktree's directory, regardless of its branch name. A bare repository has no main worktree. |
| Base / integration target | The base is the commit or ref used to start the task. The integration target is the branch intended to receive the result. They may differ. |
| Registration | Git's administrative record connecting a linked worktree's path to the repository. Repair reconnects a live checkout; prune removes obsolete registrations. |

Removing a worktree leaves its branch. Name the checkout path and branch/ref separately when communicating about them.

## Choose the checkout

1. **An existing checkout already belongs to this task?** Reuse it if no other worker owns it. Confirm its current absolute path and branch against the manager's inventory or `git worktree list --porcelain -z`; inspect changes and ongoing Git operations.
2. **A worktree is requested, or concurrent tasks, conflicting branches, or unrelated local changes require separation?** Create a task worktree. Parallel tasks need separate branches and checkouts.
3. **Otherwise:** use the current checkout.

Worktrees separate working files and indexes, but share objects, most refs, remotes, and much Git configuration. `HEAD`, `refs/bisect/*`, `refs/worktree/*`, and `refs/rewritten/*` are per-worktree. Coordinate shared mutations. They provide no security boundary; concurrent services may also need distinct ports, databases, and output locations.

## Choose the manager and location

- Prefer available harness worktree tools. Check their starting-state, dirty-file transfer, and cleanup behavior; do not assume universal tool names or defaults.
- Supply the intended base. Wait for creation to finish and verify the returned path and commit. Creation need not switch the agent's working directory: run subsequent commands explicitly in the returned path.
- Use the harness to finalize, remove, or archive its managed checkouts. Use raw Git for unmanaged worktrees or a supported fallback.
- If a live checkout was relocated, reconnect it through its manager or, for raw Git, `git -C "<repo>" worktree repair "<worktree>"` using its current absolute path. Re-list worktrees to verify the new registration. Do not prune the live checkout's registration.
- For raw Git, follow the repository's location convention; otherwise use `<primary-root>/.worktrees/<task>`, or a sibling of the repository directory for a bare repository. Do not place a worktree inside another disposable worktree. Use a unique, descriptive task name and an unused path.
- Before creating inside another checkout, ensure the actual selected destination is ignored through `.gitignore` or a local exclusion. Locate the exclude file with `git rev-parse --path-format=absolute --git-path info/exclude`; `.git` may be a file. Run `git check-ignore -q` from the enclosing checkout, with a trailing `/` on the destination's relative path, and require exit 0. Verify again after creation.

## Establish the starting state

Keep the checkout path, branch, starting commit, integration target, and manager in the existing task context.

- Use the requested base; otherwise inspect the repository's normal integration target. Do not assume `main`, `master`, `origin`, or the current `HEAD` is correct.
- If a current remote base is required, fetch the relevant remote and resolve its ref before creation. Do not pull into someone else's checkout.
- Uncommitted changes do not follow a raw Git worktree automatically. Transfer required changes deliberately; do not silently stash, reset, or copy the whole checkout.
- Create a task branch for development; reuse it for continuation. If it is checked out elsewhere, reuse that checkout through its owner or create a different branch from the required commit. Never override checkout protection.
- Use detached HEAD for disposable inspection or testing. Anchor valuable detached commits to a branch before removal.

### Generic Git commands

Substitute all placeholders. Run only the selected alternative. `<repo>` is an existing checkout or bare repository; `<worktree>` is the task's exact absolute path.

```sh
git -C "<repo>" worktree list --porcelain -z
# Only when <repo> is a checkout, not a bare repository.
git -C "<repo>" status --short --branch
git -C "<repo>" rev-parse --verify "<base-ref>^{commit}"

# Only for a destination inside another checkout; require exit 0 before creation.
git -C "<enclosing-checkout>" check-ignore -q -- "<selected-relative-path>/"

# New branch, explicitly based on the selected commit/ref.
git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"

# Alternative: continue an existing branch that is not checked out elsewhere.
# Require exit 0; do not let a missing local branch resolve to a remote branch.
git -C "<repo>" show-ref --verify --quiet "refs/heads/<task-branch>"
git -C "<repo>" worktree add "<worktree>" "<task-branch>"

# Alternative: disposable inspection of a specific commit.
git -C "<repo>" worktree add --detach "<worktree>" "<commit>"

git -C "<worktree>" rev-parse --show-toplevel
git -C "<worktree>" status --short --branch
git -C "<worktree>" rev-parse HEAD
```

## Develop and integrate

- Set up dependencies and local configuration using the task checkout's repository instructions. Ignored dependencies, secrets, and build outputs may be absent; do not bulk-copy them from another checkout.
- Keep edits, builds, tests, and commits in the selected path. Review and test the task changes before integration.
- Use the repository's merge, rebase, squash, or PR workflow within the task's authority. Worktree creation alone does not authorize publishing or merging.
- For local integration, verify the target checkout's branch, cleanliness, and owner. Coordinate with its owner if already in use. Validate the integrated result, especially after conflict resolution.
- Record the integration commit or pending review location. A pushed branch or open PR preserves work but does not establish integration.

## Cleanup decision tree

Evaluate checkout removal and branch deletion separately. Routine cleanup of this task's disposable resources is part of finishing; ask only when authority, ownership, or possible data loss is unresolved.

1. **Still used by an agent, editor operation, terminal, service, or test?** Retain it until that use ends. Stop only task-owned processes; leave the directory before removal. Do not clean another worker's checkout.
2. **Still needed for local development or review?** Retain it. If review can continue from preserved commits without this checkout, the checkout may be removed before merge; retain the necessary branch/ref.
3. **Any state would disappear with the directory?** Inspect tracked changes, untracked and ignored files, detached commits, and unfinished Git operations. Check submodules or nested repositories separately. Preserve valuable state outside the deletion path or obtain authorization to discard it. Reproducible build products need no backup.
4. **Safe to remove the checkout?** Confirm its canonical absolute path and ownership against `worktree list` or the harness inventory. Exclude the primary checkout, the current working directory, the worktree's parent directory, and sibling tasks. Remove only the exact task checkout through its manager or `git worktree remove`.
5. **Safe to delete its branch?** Delete only an unused, task-owned branch whose work is verified integrated into the intended target, preserved under another durable ref, or explicitly authorized for abandonment. Retain branches needed for pending review. A closed PR alone is insufficient evidence.
6. **Stale metadata remains?** Prune only if every dry-run entry is an intentionally removed worktree. A missing directory may be an offline volume; do not prune or unlock it just because it is unavailable.
7. **Verify the result.** Re-list worktrees and check the removed path and chosen refs. Report anything retained and why. Do not claim complete deletion if a branch, harness snapshot, or archive remains.

### Inspect and remove with Git

```sh
# Clean status does not establish preservation of ignored files or detached commits.
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" status --short --ignored
git -C "<worktree>" rev-parse HEAD

# Exit 0 proves this tip is an ancestor of this target. Other outcomes need review.
git -C "<repo>" merge-base --is-ancestor "<task-tip>" "<integration-ref>"

# Run from a surviving checkout or bare repository after the checks above.
git -C "<repo>" worktree remove "<worktree>"
git -C "<repo>" branch -d "<task-branch>"
git -C "<repo>" worktree list --porcelain -z

# Only for intentionally removed worktrees; review every dry-run entry before pruning.
git -C "<repo>" worktree prune --dry-run --verbose
git -C "<repo>" worktree prune --verbose
```

- Compare the actual task tip against a verified, current integration ref. `branch -d` may check the branch's upstream rather than the intended integration target; success is not integration evidence.
- Squash or rebase integration may break ancestry. Verify the replacement commits and resulting changes. If `branch -d` refuses, retain the branch until its obsolete history is verified safe and authorized to delete; only then consider `branch -D`.
- Submodules and managed checkouts may require another supported removal method.
- Pruning removes stale worktree metadata, not branches or existing checkout directories. Delete remote branches only when separately in scope and no collaborator still needs them.
- Harness archives may retain snapshots and omit ignored files. Check before relying on an archive for preservation or calling it deletion. Do not purge shared Git objects, reflogs, or repository history as worktree cleanup.

## Completion report

Before reporting a retained task checkout ready, verify its absolute path, branch (or intended detached commit), current registration, and any required ignore coverage.

Report completed work and checks, integration/review status, and removed or retained checkouts, branches, or archives. Include paths/refs useful for locating remaining work.

## Safety constraints

- DON'T discard work or bypass safeguards without user authorization for the target and consequence; tool access and agent-written plans confer none. Resolve safeguard causes before using force flags, resets, unlocking, or filesystem operations. Read lock reasons; an absent reason is not permission. Never override branch checkout protection.
- DON'T remove or relocate worktrees, hard-reset, or clean files without verifying the repository, absolute path, branch name (or detached state), and HEAD commit. Scripts must parse `git worktree list --porcelain -z`.
- DON'T use `git worktree add -B` unless resetting the named branch to the selected commit is authorized; use `-b` for creation.
- DON'T relocate through filesystem tools without preserving `.git` and contents. Repair from the current main/bare repository with new absolute linked-worktree paths, and verify inventory. `git worktree move` cannot move main or submodule-containing worktrees.
- DON'T create, relocate, or remove superproject worktrees without checking submodule limitations; multiple superproject checkouts are discouraged.
- DON'T remove worktrees by deleting directories through filesystem commands or file managers; use the worktree manager or `git worktree remove` after the cleanup checks.
- DON'T prune with different expiry options from the reviewed dry run. Git gc can prune missing registrations automatically (`gc.worktreePruneExpire`): repair relocated worktrees promptly and lock intermittently mounted worktrees before storage goes offline.
- DON'T expect `git config --worktree` isolation unless `extensions.worktreeConfig` is enabled. Before enabling it, migrate existing `core.worktree` and `core.bare` from shared configuration to `config.worktree`, resolved with `git rev-parse --git-path config.worktree` from the main checkout or bare repository. Never share `core.worktree` or `core.bare=true`. Share `core.sparseCheckout` only when all worktrees use sparse checkout.
- DON'T enable `extensions.worktreeConfig` or relative worktree paths unless all required Git installations support the resulting extensions.
- DON'T edit refs or worktree metadata as files; use Git commands and resolve paths with `git rev-parse --git-path` from the target worktree.
