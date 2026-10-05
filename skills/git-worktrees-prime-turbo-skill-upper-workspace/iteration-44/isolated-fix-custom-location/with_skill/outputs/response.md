Here is the exact sequence, in order. Every command runs against the project repo; nothing is merged, pushed, or touched in the colleague's checkout.

## Phase 1 — Baseline the colleague's checkout (read-only)

```sh
# 1. Inventory checkouts and confirm ownership/state before doing anything
git -C project worktree list --porcelain -z
git -C project status --short --branch
git -C project status --porcelain=v1 > /tmp/colleague-status.before   # snapshot to compare at the end
```

Keep that snapshot — you will diff against it in Phase 6 to prove the notes and untracked draft are untouched.

## Phase 2 — Pre-flight checks for the new checkout

```sh
# 2. Resolve the base; fail fast if release/next doesn't exist locally
git -C project rev-parse --verify "release/next^{commit}"

# 3. If release/next tracks a remote and must be current, fetch ONLY that ref
#    (never pull/checkout in the colleague's checkout)
git -C project fetch origin release/next
git -C project rev-parse --verify "release/next^{commit}"   # re-resolve after fetch

# 4. Destination is inside another checkout -> it must be ignored first (require exit 0)
git -C project rev-parse --path-format=absolute --git-path info/exclude
git -C project check-ignore -q -- "scratch-checkouts/normalize/"
echo $?   # must print 0; if not, add scratch-checkouts/ to .git/info/exclude (local-only) and re-run
```

If step 4 exits non-zero, append `scratch-checkouts/` to the file printed by `info/exclude` (that file is local and does not touch tracked content), then re-run the check.

## Phase 3 — Create the task worktree

```sh
# 5. New branch task/normalize from release/next (-b, never -B) in the requested path
git -C project worktree add -b task/normalize project/scratch-checkouts/normalize release/next

# 6. Verify the new checkout: correct path, branch, clean, and exactly at the base commit
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize rev-parse HEAD
git -C project rev-parse "release/next^{commit}"     # the two SHAs must match

# 7. Re-verify ignore coverage from the enclosing checkout AFTER creation (require exit 0)
git -C project check-ignore -q -- "scratch-checkouts/normalize/"
echo $?
```

## Phase 4 — Locate and fix `normalize_label`

```sh
# 8. Find the function inside the task checkout only
grep -rn "normalize_label" project/scratch-checkouts/normalize --include='*.py' --include='*.js' --include='*.ts' --include='*.rb'

# 9. Read the surrounding code and the repo's conventions before editing
```

Edit the file so the function body ends with a single whitespace-strip + lowercase, e.g.:

```python
def normalize_label(text):
    return text.strip().lower()
```

(Adjust to the repo's actual language/style; the contract is: strip surrounding whitespace, then lowercase — applied to the value actually returned, not to an intermediate copy.)

## Phase 5 — Run the project's check and commit

```sh
# 10. Discover the project's documented check (do not guess a tool)
grep -rn -i -E "^(check|test|lint)" project/scratch-checkouts/normalize/Makefile \
     project/scratch-checkouts/normalize/package.json \
     project/scratch-checkouts/normalize/pyproject.toml \
     project/scratch-checkouts/normalize/README* 2>/dev/null

# 11. Run it FROM the task checkout so it tests your change
git -C project/scratch-checkouts/normalize status --short   # confirm only your edit is present
#   e.g.  make check   |   npm test   |   pytest   (whichever step 10 identified)

# 12. Review exactly what will be committed
git -C project/scratch-checkouts/normalize diff
git -C project/scratch-checkouts/normalize diff --check    # whitespace-error check (exit 0 required)

# 13. Stage only the fix and commit on the task branch
git -C project/scratch-checkouts/normalize add -- <path-to-normalize_label-file>
git -C project/scratch-checkouts/normalize status --short
git -C project/scratch-checkouts/normalize commit -m "fix: normalize_label strips whitespace and lowercases"

# 14. Re-run the check on the committed state (guards against an uncommitted leftover)
git -C project/scratch-checkouts/normalize status --short --branch   # must show clean, on task/normalize
#   re-run the same check command from step 11
```

If the check fails at step 11, fix the code, re-run, and only commit once it passes.

## Phase 6 — Final verification (leave ready for review, no merge/push)

```sh
# 15. Record the review-ready state
git -C project/scratch-checkouts/normalize log --oneline -3
git -C project/scratch-checkouts/normalize rev-parse HEAD
git -C project/scratch-checkouts/normalize status --short --branch --untracked-files=all
git -C project/scratch-checkouts/normalize status --short --ignored

# 16. Prove the commit sits on top of the requested base (exit 0 = success)
git -C project merge-base --is-ancestor "release/next" task/normalize

# 17. Prove the colleague's checkout is byte-for-byte as you found it
git -C project status --short --branch
git -C project status --porcelain=v1 > /tmp/colleague-status.after
diff /tmp/colleague-status.before /tmp/colleague-status.after   # must be empty

# 18. Confirm final registration/locations
git -C project worktree list --porcelain -z
```

## What I would report

- **Task checkout:** `project/scratch-checkouts/normalize` (registered linked worktree)
- **Branch:** `task/normalize`, based on `release/next`, one fix commit at the recorded SHA
- **Check:** the project's own check, run and passing inside the task checkout
- **Colleague's checkout:** unchanged — dirty notes and untracked draft verified identical to the Phase 1 snapshot
- **Not done (as requested):** no merge, no push/publication; `task/normalize` is left in place ready for review

One caution worth stating explicitly: worktrees share the object database and refs with the colleague's checkout, so creating the branch and commit is visible there via `git log task/normalize` — but their working files, index, and `HEAD` are never modified by any command above, which is why every step uses `git -C <path>` scoped to the intended checkout rather than switching branches in `project/`.
