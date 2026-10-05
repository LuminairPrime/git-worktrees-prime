I won't touch the filesystem — here's the exact command sequence I'd run, in order. Every git invocation below is scoped with `-C` to an explicit directory, and **no command ever writes into `project/`'s working tree or index**.

## 0. Baseline: record the colleague's state (so I can prove it's intact later)

```bash
git -C project status --porcelain=v1 --untracked-files=all > /tmp/colleague.before
git -C project rev-parse HEAD            > /tmp/project-head.before
git -C project rev-parse release/next    > /tmp/release-next.before
git -C project stash list                > /tmp/stash.before
```

## 1. Confirm the base branch exists (local, else remote)

```bash
git -C project rev-parse --verify --quiet refs/heads/release/next \
  || git -C project rev-parse --verify --quiet refs/remotes/origin/release/next
```

## 2. Make sure the scratch dir won't show up as new untracked noise

```bash
git -C project check-ignore -v scratch-checkouts/ || echo "NOT IGNORED"
```

If it prints `NOT IGNORED`, add it **locally only** (this file is untracked, unshared, and touches no colleague files — no `.gitignore` edit, no commit):

```bash
printf 'scratch-checkouts/\n' >> project/.git/info/exclude
git -C project check-ignore -v scratch-checkouts/
```

## 3. Create the isolated checkout + branch (worktree, not a clone)

```bash
git -C project show-ref --verify --quiet refs/heads/task/normalize \
  && echo "BRANCH EXISTS — reuse it" || echo "will create fresh"

git -C project worktree add scratch-checkouts/normalize -b task/normalize release/next
```

*(If the branch already existed, I'd instead verify `git -C project merge-base --is-ancestor release/next task/normalize` before using it.)*

Path resolves to `project/scratch-checkouts/normalize` because `-C` makes the relative path resolve inside `project/`.

## 4. Verify the worktree is clean and starts exactly from `release/next`

```bash
git -C project/scratch-checkouts/normalize status --short --branch   # expect: ## task/normalize, no files
diff <(git -C project/scratch-checkouts/normalize rev-parse HEAD) /tmp/release-next.before   # expect: no output
git -C project worktree list
```

## 5. Locate `normalize_label`

```bash
git -C project/scratch-checkouts/normalize grep -n "normalize_label"
git -C project/scratch-checkouts/normalize ls-files | grep -Ei 'makefile|pyproject|tox\.ini|package\.json|\.pre-commit'
```

## 6. Make the edit (only inside the worktree)

```bash
$EDITOR project/scratch-checkouts/normalize/<file-with-normalize_label>
```

Target shape:

```python
def normalize_label(label: str) -> str:
    return label.strip().lower()
```

(`strip()` **then** `lower()` — the order the spec asks for.)

## 7. Determine what "the project's check" is, then run it **in the worktree**

```bash
git -C project/scratch-checkouts/normalize ls-files | grep -E 'Makefile|pyproject.toml|tox.ini|\.pre-commit-config'
```

Then, e.g.:

```bash
cd project/scratch-checkouts/normalize
# reuse the project's existing interpreter/venv read-only; do NOT install or modify anything in project/
../.venv/bin/python -m pytest -q      # or: make check / ruff check . / tox -e py
```

If the check is `make check`, I'd run `make -C project/scratch-checkouts/normalize check`.

## 8. Behavioural assertion

```bash
project/.venv/bin/python -c "
from <module> import normalize_label as n
assert n('  AbC  ') == 'abc'
assert n('\tXyZ\n') == 'xyz'
assert n('already lower') == 'already lower'
print('normalize_label OK')"
```

## 9. Review exactly what will be committed

```bash
git -C project/scratch-checkouts/normalize status --short     # expect: only the one file
git -C project/scratch-checkouts/normalize diff --check       # expect: no output (no whitespace errors)
git -C project/scratch-checkouts/normalize diff
```

## 10. Stage the single file and commit on `task/normalize`

```bash
git -C project/scratch-checkouts/normalize add -- <file-with-normalize_label>
git -C project/scratch-checkouts/normalize commit -m "fix: strip surrounding whitespace and lowercase in normalize_label"
```

Never `git add -A`, `git add -u`, or `git commit -a` — those could sweep in stray files.

## 11. Post-commit verification

```bash
git -C project/scratch-checkouts/normalize status            # clean
git -C project/scratch-checkouts/normalize log --oneline -2  # fix commit on top of release/next
git -C project/scratch-checkouts/normalize log --format='%H %P' -1   # parent == release/next
```

## 12. Prove the colleague's checkout is untouched

```bash
git -C project status --porcelain=v1 --untracked-files=all | diff /tmp/colleague.before -   # expect: no output
diff <(git -C project rev-parse HEAD)         /tmp/project-head.before                     # expect: no output
diff <(git -C project rev-parse release/next) /tmp/release-next.before                     # expect: no output
diff <(git -C project stash list)             /tmp/stash.before                            # expect: no output
git -C project worktree list
```

If step 2 added the exclude line and you want to leave zero trace:

```bash
sed -i '/^scratch-checkouts\/$/d' project/.git/info/exclude
```

## 13. Ready for review — explicit non-actions

Left in place, **deliberately not run**:

```bash
# git -C project/scratch-checkouts/normalize push origin task/normalize   # NO push
# git -C project checkout task/normalize                                   # NO — would disturb colleague
# git -C project merge task/normalize                                      # NO merge
# git -C project worktree remove ...                                       # keep checkout for review
# git -C project stash / clean / restore / switch                          # NEVER in project/
```

Final state: `task/normalize` = `release/next` + one fix commit, worktree clean, colleague's dirty tree, untracked draft, and `release/next` byte-for-byte identical to the baseline.
