Below is the exact command sequence I'd run, in order. It assumes the working directory contains `project/` (the colleague's primary checkout, which is also the repository root). Nothing is run inside the colleague's checkout except read-only inspection and one local-exclude addition — their uncommitted notes and untracked draft are never stashed, reset, or committed.

## Phase 0 — Baseline the colleague's checkout (so I can prove it's untouched)

```sh
git -C project status --short --branch --untracked-files=all
```
Save this output; it should show the unrelated uncommitted notes and the untracked draft.

## Phase 1 — Preflight checks

```sh
# 1. Inventory: confirm primary checkout, and that neither the path nor branch is taken
git -C project worktree list --porcelain -z

# 2. Resolve the requested base (must succeed before creating anything)
git -C project rev-parse --verify "release/next^{commit}"
```
- If step 2 fails because `release/next` exists only on the remote, fetch (never pull/checkout in the colleague's checkout) and resolve the remote ref instead:
  ```sh
  git -C project fetch origin release/next
  git -C project rev-parse --verify "refs/remotes/origin/release/next^{commit}"
  ```
  Use that resolved ref wherever `release/next` appears below.

```sh
# 3. Destination is inside another checkout -> it must be ignored first (require exit 0)
git -C project check-ignore -q -- "scratch-checkouts/normalize/"
```
- If it exits non-zero, add a **local** exclusion (no tracked file is modified):
  ```sh
  git -C project rev-parse --path-format=absolute --git-path info/exclude
  # append this line to that file:
  # scratch-checkouts/
  git -C project check-ignore -q -- "scratch-checkouts/normalize/"   # require exit 0 now
  ```

## Phase 2 — Create the task checkout

```sh
git -C project worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```
`-b` creates the branch and fails loudly if `task/normalize` already exists — I would **not** use `-B` (that would reset an existing branch).

Verify the result:

```sh
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel   # ends in project/scratch-checkouts/normalize
git -C project/scratch-checkouts/normalize rev-parse HEAD              # equals the base commit from Phase 1
git -C project/scratch-checkouts/normalize status --short --branch     # ## task/normalize...release/next, clean
git -C project check-ignore -q -- "scratch-checkouts/normalize/"       # repeat ignore check (exit 0)
```

## Phase 3 — Locate and fix `normalize_label`

```sh
git -C project/scratch-checkouts/normalize grep -n "normalize_label" -- .
```
Read the definition, then edit **only** that function so it trims surrounding whitespace and returns lowercase (e.g. `text.strip().lower()` in Python, `text.strip().toLowerCase()` in JS). Edits happen only in the worktree path.

## Phase 4 — Run the project's check

```sh
# Discover the project's own check (in the worktree only): CI config, Makefile, package.json, tox.ini...
git -C project/scratch-checkouts/normalize ls-files | grep -Ei 'makefile|tox|package.json|pyproject|\.github/workflows'
```
Run that check with the worktree as cwd, and require exit 0:

```sh
(cd project/scratch-checkouts/normalize && <the-project's-check-command>)
```
If it fails, fix and re-run. I would not weaken, skip, or substitute the check.

## Phase 5 — Review and commit on the task branch

```sh
# Only the intended file changed; no stray artifacts
git -C project/scratch-checkouts/normalize status --short --untracked-files=all

# Review the change and check for whitespace errors
git -C project/scratch-checkouts/normalize diff
git -C project/scratch-checkouts/normalize diff --check

# Stage only the fixed file, confirm the staged set, then commit
git -C project/scratch-checkouts/normalize add -- <path/to/file-with-normalize_label>
git -C project/scratch-checkouts/normalize diff --cached
git -C project/scratch-checkouts/normalize commit -m "Fix normalize_label to strip surrounding whitespace and return lowercase"
```

Post-commit verification:

```sh
git -C project/scratch-checkouts/normalize status --short --branch --untracked-files=all   # clean, on task/normalize
git -C project/scratch-checkouts/normalize log -1 --format='%H %P %s'                     # parent == base commit from Phase 1
git -C project merge-base --is-ancestor release/next task/normalize                        # exit 0: branch is based on release/next
```
Optionally re-run the project's check once more on the committed tree (same command as Phase 4).

## Phase 6 — Leave it ready for review; confirm nothing else moved

```sh
# 1. Colleague's checkout matches the Phase 0 baseline exactly (same notes, same untracked draft, no new entries)
git -C project status --short --branch --untracked-files=all

# 2. Registration intact: primary checkout + the new task checkout
git -C project worktree list --porcelain -z
```

**Deliberately not run:** no merge, no push, no `worktree remove`, no `branch -d`, no `worktree prune`, no stash/reset in the colleague's checkout.

**Final report would state:** checkout path `project/scratch-checkouts/normalize`, branch `task/normalize`, base `release/next` (with its commit SHA), fix commit SHA, the exact check command and its passing result, and confirmation that the colleague's checkout status is byte-for-byte what it was before.
