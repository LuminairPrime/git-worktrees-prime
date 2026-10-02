Short answer: I’m not aware of an **official Git/GitHub/Microsoft “agent skill”** specifically for `git worktrees`. The official primitive is Git’s built-in **`git worktree`** command, documented by the Git project. If you need something official or defensible, the best approach is a thin, testable agent skill grounded in:

- Official Git docs: <https://git-scm.com/docs/git-worktree>
- Git’s own source/test suite, especially the `worktree` tests in `git/git` under `t/`  
- Conservative lifecycle rules for agents: create isolated worktrees, avoid destructive cleanup, prune stale state, delete branches only when merged/confirmed.

Below is a production-style, copy-paste **Git worktrees agent skill** you can drop into `AGENTS.md`, `.github/copilot-instructions.md`, `.claude/skills/git-worktrees/SKILL.md`, Cursor rules, Codex instructions, etc.

---

# Drop-in agent skill: Git worktrees for parallel development

```md
---
name: git-worktrees
description: >
  Safe creation, use, and cleanup of Git worktrees for parallel development.
  Use when an AI coding agent needs to work on multiple branches/checkouts
  simultaneously, review a PR without disturbing current work, run isolated
  builds/tests, or clean up temporary branch worktrees.
---

# Git Worktrees Skill

## Purpose

Teach programming agents how to safely use Git worktrees for parallel development.

A Git worktree is a linked working directory attached to the same repository.
It allows multiple branches or commits to be checked out at the same time without
cloning the repository multiple times.

Official reference: https://git-scm.com/docs/git-worktree

## Non-negotiable safety rules

The agent MUST:

1. Never delete or remove the primary working tree.
2. Never run `rm -rf` on a worktree as the primary cleanup mechanism.
3. Prefer `git worktree remove` before deleting any worktree directory.
4. Run `git worktree prune` after removing worktrees or when worktree paths are missing.
5. Never use `git worktree remove --force` unless:
   - the worktree was explicitly created as disposable, and
   - the user or policy explicitly allows destructive cleanup, or
   - the agent has verified there is no uncommitted or unpushed work.
6. Never delete a local branch unless:
   - it is fully merged, or
   - the associated PR/task is confirmed merged/closed, or
   - the user explicitly approves force deletion.
7. Avoid checking out the same branch in multiple worktrees unless explicitly requested.
8. Prefer creating worktrees outside the primary working tree, for example:

   ```text
   repo/
   repo.worktrees/
     feature-a/
     pr-123/
   ```

9. Never create worktrees in unsafe locations such as `/`, `$HOME`, or paths outside the project workspace unless explicitly requested.
10. Report before/after state when creating or cleaning up worktrees.

## When to use a worktree

Use a worktree when:

- The agent must work on a different branch without disturbing uncommitted work.
- The agent needs to review or test a PR while continuing current work.
- Multiple tasks/features need parallel checkouts.
- A long-running build/test should run in one branch while the agent edits another.
- A hotfix must be prepared while preserving an in-progress feature.
- Multiple agents or tasks need isolated working directories for the same repository.

Do not create a worktree when:

- The current branch and working tree are already appropriate.
- The task only needs reading history, diffs, or metadata.
- The repository/tooling is known to be incompatible with linked worktrees.
- The target branch is already checked out in another worktree and no separate copy is required.
- The change is trivial and switching branches safely is possible.

## Recommended directory layout

Prefer a sibling directory next to the repository:

```text
parent/
  myrepo/
  myrepo.worktrees/
    feature-login/
    issue-123-fix/
    pr-456-review/
```

Example setup:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"
WT_ROOT="$(dirname "$REPO_ROOT")/$REPO_NAME.worktrees"
mkdir -p "$WT_ROOT"
```

If the environment cannot write outside the repository, use an ignored directory such as:

```bash
WT_ROOT="$REPO_ROOT/.worktrees"
mkdir -p "$WT_ROOT"
```

Then ensure `.worktrees/` is ignored. However, sibling directories are usually less surprising for tools, IDEs, build systems, and file watchers.

## Branch and path naming

Sanitize branch names for filesystem paths:

```bash
sanitize() {
  printf '%s' "$1" | LC_ALL=C tr -c '[:alnum:]._' '-'
}

BRANCH="feature/login-rate-limit"
SAFE_NAME="$(sanitize "$BRANCH")"
WT_PATH="$WT_ROOT/$SAFE_NAME"
```

Recommended branch naming:

```text
feature/<short-description>
fix/<issue-or-task-id>
experiment/<short-description>
review/pr-<number>
```

## Creating a new worktree

### 1. Create a new branch from a base ref

Use this when starting new work from `main`, `develop`, or another base branch.

```bash
BASE_REF="origin/main"
BRANCH="feature/login-rate-limit"
SAFE_NAME="$(sanitize "$BRANCH")"
WT_PATH="$WT_ROOT/$SAFE_NAME"

git fetch origin main

git worktree add -b "$BRANCH" "$WT_PATH" "$BASE_REF"
```

This creates a new branch named `feature/login-rate-limit` starting at `origin/main` and checks it out in `$WT_PATH`.

### 2. Create a worktree for an existing local branch

```bash
BRANCH="feature/login-rate-limit"
SAFE_NAME="$(sanitize "$BRANCH")"
WT_PATH="$WT_ROOT/$SAFE_NAME"

git worktree add "$WT_PATH" "$BRANCH"
```

If Git reports the branch is already checked out elsewhere, find the existing worktree:

```bash
git worktree list --porcelain
```

Then either use the existing worktree or create a different branch.

### 3. Create a worktree tracking an existing remote branch

```bash
BRANCH="feature/login-rate-limit"
SAFE_NAME="$(sanitize "$BRANCH")"
WT_PATH="$WT_ROOT/$SAFE_NAME"

git fetch origin "$BRANCH"

git worktree add --track -b "$BRANCH" "$WT_PATH" "origin/$BRANCH"
```

If the local branch already exists, use:

```bash
git worktree add "$WT_PATH" "$BRANCH"
```

### 4. Create a detached worktree for inspection

Use this for reviewing tags, commits, or CI artifacts without creating a branch.

```bash
WT_PATH="$WT_ROOT/review-v1.2.3"

git worktree add --detach "$WT_PATH" v1.2.3
```

Or:

```bash
WT_PATH="$WT_ROOT/review-abc1234"

git worktree add --detach "$WT_PATH" abc1234
```

## Using a worktree

Prefer `git -C` so the agent does not need to maintain shell state:

```bash
git -C "$WT_PATH" status
git -C "$WT_PATH" diff
git -C "$WT_PATH" add -p
git -C "$WT_PATH" commit -m "feat: add login rate limiting"
git -C "$WT_PATH" push -u origin HEAD
```

Rules while using a worktree:

- Treat each worktree as an isolated checkout.
- Do not modify files in another worktree unless explicitly instructed.
- Do not assume `node_modules`, `.venv`, `target`, `dist`, `.env`, or build caches are shared.
- Initialize submodules per worktree if the repository uses them:

  ```bash
  git -C "$WT_PATH" submodule update --init --recursive
  ```

- Remember that stashes are repository-wide, not worktree-local.
- Remember that hooks are shared from the common Git directory.
- In a linked worktree, `.git` is usually a file, not a directory. Tools that assume `.git` is a directory may need special handling.

## Inspecting worktrees

List worktrees:

```bash
git worktree list
```

Machine-readable output:

```bash
git worktree list --porcelain
```

Porcelain output can include:

```text
worktree /path/to/worktree
HEAD <sha>
branch refs/heads/<branch>
detached
bare
locked
prunable
```

The agent should use `git worktree list --porcelain` when making programmatic decisions.

## Cleaning up a worktree

### Standard cleanup

Before removing, verify state:

```bash
git worktree list --porcelain
git -C "$WT_PATH" status --porcelain
```

If the worktree is clean and no longer needed:

```bash
git worktree remove "$WT_PATH"
git worktree prune
```

### Delete the local branch only when safe

If the branch is merged:

```bash
git branch -d "$BRANCH"
```

If `git branch -d` fails, do not automatically use `-D`. Stop and verify:

- Was the PR merged?
- Was the branch squash-merged?
- Are there local commits not pushed?
- Did the user explicitly approve force deletion?

Only then:

```bash
git branch -D "$BRANCH"
```

### Delete the remote branch only when allowed

If policy allows and the branch is no longer needed:

```bash
git push origin --delete "$BRANCH"
```

For GitHub pull requests, also consider:

```bash
gh pr close "$PR_NUMBER" --delete-branch
```

or delete the branch through the merged PR.

## Handling dirty worktrees

If `git worktree remove` fails because the worktree is dirty:

1. Show the user or log:

   ```bash
   git -C "$WT_PATH" status --porcelain
   ```

2. Preserve work if needed:

   ```bash
   git -C "$WT_PATH" add -A
   git -C "$WT_PATH" commit -m "wip: preserve work before cleanup"
   git -C "$WT_PATH" push -u origin HEAD
   ```

   or stash if appropriate:

   ```bash
   git -C "$WT_PATH" stash push -u -m "worktree cleanup stash"
   ```

3. Only force-remove if explicitly allowed:

   ```bash
   git worktree remove --force "$WT_PATH"
   git worktree prune
   ```

## Handling stale or broken worktrees

If the worktree directory was manually deleted:

```bash
git worktree prune
```

If a worktree was manually moved:

```bash
git worktree repair
```

Or, if you know the new path:

```bash
git worktree move "$OLD_PATH" "$NEW_PATH"
```

Prefer `git worktree move` over manually moving directories.

## Locking worktrees

Use locking when a worktree is on removable storage, network storage, or may be temporarily unavailable.

```bash
git worktree lock "$WT_PATH" --reason "external disk may be disconnected"
git worktree unlock "$WT_PATH"
```

## Parallel PR review example

To review a GitHub PR in an isolated worktree:

```bash
PR_NUMBER=123
BRANCH="pr-$PR_NUMBER"
SAFE_NAME="$(sanitize "$BRANCH")"
WT_PATH="$WT_ROOT/$SAFE_NAME"

git fetch origin "pull/$PR_NUMBER/head:$BRANCH"
git worktree add "$WT_PATH" "$BRANCH"
```

Then inspect:

```bash
git -C "$WT_PATH" status
git -C "$WT_PATH" log --oneline -10
git -C "$WT_PATH" diff origin/main...HEAD
```

Cleanup after review:

```bash
git worktree remove "$WT_PATH"
git worktree prune
git branch -D "$BRANCH"
```

Only use `-D` here if the local review branch is disposable and not pushed as a working branch.

## Recommended agent decision procedure

Before creating a worktree, the agent should ask:

1. Is the current worktree correct for this task?
2. Is there uncommitted work that would be disturbed by switching branches?
3. Does another task need the current branch to remain checked out?
4. Is the target branch already checked out in another worktree?
5. Will this worktree be temporary or long-lived?
6. Who is responsible for cleanup?

Before cleanup, the agent should ask:

1. Is the worktree clean?
2. Are there unpushed commits?
3. Is the branch merged or the PR closed?
4. Was the worktree explicitly disposable?
5. Has the user approved destructive operations?

## Reporting requirements

After creating worktrees, report:

```text
Created worktree:
  Branch: <branch>
  Path: <path>
  Base: <base-ref-or-commit>
```

After cleanup, report:

```text
Removed worktree:
  Path: <path>
  Branch action: kept | deleted safely | force deleted with approval
  Pruned stale metadata: yes/no
```

If cleanup cannot be completed safely, the agent should stop and ask.
```

---

# Example: full lifecycle

```bash
# Setup
REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"
WT_ROOT="$(dirname "$REPO_ROOT")/$REPO_NAME.worktrees"
mkdir -p "$WT_ROOT"

sanitize() {
  printf '%s' "$1" | LC_ALL=C tr -c '[:alnum:]._' '-'
}

BRANCH="feature/login-rate-limit"
SAFE_NAME="$(sanitize "$BRANCH")"
WT_PATH="$WT_ROOT/$SAFE_NAME"

# Create
git fetch origin main
git worktree add -b "$BRANCH" "$WT_PATH" origin/main

# Use
git -C "$WT_PATH" status
# ... edit files ...
git -C "$WT_PATH" add -p
git -C "$WT_PATH" commit -m "feat(auth): add login rate limiting"
git -C "$WT_PATH" push -u origin HEAD

# Cleanup after PR is merged and worktree is clean
git -C "$WT_PATH" status --porcelain
git worktree remove "$WT_PATH"
git worktree prune
git branch -d "$BRANCH"
```

---

# Minimal evaluation tests

If you want the skill to be “substantially evaluated,” add a small CI test like this:

```bash
#!/usr/bin/env bash
set -euo pipefail

TMP="$(mktemp -d)"
cd "$TMP"

git init -b main source
cd source

git commit --allow-empty -m "init"

# Create worktree
git worktree add -b test/worktree ../wt HEAD

# Verify linked worktree exists
test -e ../wt/.git

# Make a commit in the worktree
git -C ../wt commit --allow-empty -m "worktree commit"

# Verify listed
git worktree list | grep -F "../wt"

# Clean worktree should remove
git worktree remove ../wt
git worktree prune

# Should no longer be listed
if git worktree list | grep -F "../wt"; then
  echo "worktree still listed after removal"
  exit 1
fi

# Dirty worktree should refuse removal
git worktree add -b test/dirty ../dirty HEAD
touch ../dirty/untracked.txt

if git worktree remove ../dirty; then
  echo "dirty worktree removed without force"
  exit 1
fi

git worktree remove --force ../dirty
git worktree prune

# Branch cleanup
git branch -D test/worktree test/dirty

echo "git worktree eval passed"
```

This does not evaluate “agent judgment,” but it validates the core commands and safety expectations.

---

# Official / authoritative references

Use these as the source of truth:

- Git worktree command:  
  <https://git-scm.com/docs/git-worktree>

- Git repository layout, including worktree metadata under `.git/worktrees`:  
  <https://git-scm.com/docs/gitrepository-layout>

- Git branch deletion semantics:  
  <https://git-scm.com/docs/git-branch>

- Git source repository, including worktree tests:  
  <https://github.com/git/git>

For “substantially evaluated” behavior, the Git project’s own test suite is the strongest official reference. Look in `t/` for worktree-related tests, especially the `t240*` worktree tests.

---

# Practical recommendation

If you need something official, do not depend on a random third-party “git worktrees agent skill.” Instead:

1. Keep the skill thin.
2. Anchor it to `git worktree` official docs.
3. Add hard safety rules for agents.
4. Add a few automated evals in your repo.
5. Require explicit approval for force removal and branch force deletion.

That gives you a defensible, official-adjacent skill without depending on an unmaintained community prompt.