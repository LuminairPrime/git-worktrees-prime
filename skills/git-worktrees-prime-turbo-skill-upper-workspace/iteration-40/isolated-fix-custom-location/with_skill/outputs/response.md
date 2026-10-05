Since no repo is attached, here is the exact command sequence I would run, in order. Replace `<absolute-path-to>/project` if the checkout lives elsewhere; I assume it is at `project`.

**1. Inspect the existing (colleague's) checkout — extract-only, do not modify it:**

```sh
git -C project worktree list --porcelain -z
git -C project status --short --branch          # note the unrelated dirty "notes" and untracked "draft"
git -C project rev-parse --verify "release/next^{commit}"
```

Do not run `git stash`, `git reset`, `git checkout`, or `git clean` in `project`.

**2. Confirm the planned worktree destination is ignored before creating it:**

```sh
git -C project check-ignore -q -- scratch-checkouts/normalize/   # require exit 0
```

If not ignored, add `scratch-checkouts/` to `.git/info/exclude` in the main checkout (do not touch the colleague's tracked files), then re-run the check.

**3. Create the task worktree on a new branch from `release/next`:**

```sh
git -C project worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```

**4. Verify the new checkout:**

```sh
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel
git -C project/scratch-checkouts/normalize status --short --branch   # expect branch task/normalize, clean
git -C project/scratch-checkouts/normalize rev-parse HEAD            # should equal release/next's commit
git -C project check-ignore -q -- scratch-checkouts/normalize/
```

**5. Locate and fix `normalize_label`:**

```sh
git -C project/scratch-checkouts/normalize grep -n "def normalize_label"
```

Edit the function body so it strips surrounding whitespace and lowercases, e.g.:

```python
return text.strip().lower()
```

(adapt the expression to the existing variable/parameters of that function).

**6. Run the project's check in the task checkout:**

```sh
cd project/scratch-checkouts/normalize
# use the repo's documented check, e.g. one of:
./check        # or: make check | pytest | npm test | tox
```

Require a clean pass before committing; fix and re-run if it fails.

**7. Review, stage, and commit on `task/normalize`:**

```sh
git -C project/scratch-checkouts/normalize diff
git -C project/scratch-checkouts/normalize add <edited-file>
git -C project/scratch-checkouts/normalize commit -m "fix: strip whitespace and lowercase in normalize_label"
```

**8. Final verification for review readiness:**

```sh
git -C project/scratch-checkouts/normalize status --short --branch   # clean, on task/normalize
git -C project/scratch-checkouts/normalize log --oneline -1 -2
git -C project status --short --branch                              # colleague's notes + draft still intact
git -C project worktree list --porcelain -z                         # both checkouts registered
```

No merge, push, or publication — the branch `task/normalize` in `project/scratch-checkouts/normalize` is left ready for review; the colleague's checkout and its unrelated changes are untouched.
