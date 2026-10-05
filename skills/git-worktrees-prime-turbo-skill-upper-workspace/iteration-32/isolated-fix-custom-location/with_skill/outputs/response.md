Here is the exact sequence I would run, in order. Replace `<project>` with the colleague's checkout path.

**1. Inspect the colleague's checkout (read-only; do not modify it):**

```sh
git -C "<project>" status --short --branch
git -C "<project>" worktree list --porcelain -z
git -C "<project>" rev-parse --verify "release/next^{commit}"
```

Confirm their uncommitted notes and untracked draft are present, and note the current branch — do not switch or reset anything there.

**2. Verify the scratch location is a git-ignored path:**

```sh
git -C "<project>" check-ignore -q -- "scratch-checkouts/normalize/"; echo $?
```

Require exit `0`. If it is not ignored, append `scratch-checkouts/` to the local exclude file (`.git/info/exclude`) rather than editing the tracked `.gitignore`, so the colleague's checkout stays untouched.

**3. Create the task checkout from `release/next` on a new branch:**

```sh
git -C "<project>" worktree add -b task/normalize "<project>/scratch-checkouts/normalize" release/next
```

**4. Verify the new checkout:**

```sh
git -C "<project>/scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "<project>/scratch-checkouts/normalize" status --short --branch
git -C "<project>/scratch-checkouts/normalize" rev-parse HEAD
```

HEAD should equal `release/next`'s commit, on branch `task/normalize`, clean status.

**5. Locate and fix `normalize_label`:**

```sh
grep -rn "normalize_label" "<project>/scratch-checkouts/normalize"
```

Edit the function so it strips surrounding whitespace and returns lowercase text, e.g. `return label.strip().lower()` (matching the surrounding style — whatever the existing function body/idioms are, apply `.strip().lower()` before returning).

**6. Run the project's check in the new checkout:**

First find the documented check command (`README*`, `Makefile`, `package.json`, `tox.ini`, `pyproject.toml`, CI config), e.g.:

```sh
ls "<project>/scratch-checkouts/normalize"
grep -rn -i "check\|test" "<project>/scratch-checkouts/normalize/README"* | head
```

Then run it, e.g.:

```sh
cd "<project>/scratch-checkouts/normalize"
make check        # or: pytest / npm test / ./scripts/check — whatever the repo documents
```

All commands from here are run with `git -C "<project>/scratch-checkouts/normalize"` (or from inside it).

**7. Commit the fix on the task branch:**

```sh
git -C "<project>/scratch-checkouts/normalize" add <edited-file>
git -C "<project>/scratch-checkouts/normalize" status --short
git -C "<project>/scratch-checkouts/normalize" commit -m "Fix normalize_label to strip surrounding whitespace and lowercase"
```

**8. Final verification / ready-for-review state:**

```sh
git -C "<project>/scratch-checkouts/normalize" status --short --branch
git -C "<project>/scratch-checkouts/normalize" log --oneline -3
git -C "<project>" worktree list --porcelain -z
git -C "<project>" status --short --branch
```

Expect: task branch clean at the new commit, the worktree registered at `scratch-checkouts/normalize`, and the colleague's checkout unchanged with their notes and untracked draft intact. No merge, push, or publication performed — the branch `task/normalize` with its commit is left ready for review.
