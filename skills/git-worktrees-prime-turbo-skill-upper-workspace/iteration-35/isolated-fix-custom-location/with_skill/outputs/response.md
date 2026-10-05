Here is the exact sequence I would run, in order. Placeholders: `<repo>` = the current project checkout (the colleague's), typically `project`.

## 1. Inspect the existing checkout, without touching its uncommitted state

```sh
git -C project worktree list --porcelain -z
git -C project status --short --branch
git -C project rev-parse --verify "release/next^{commit}"
```

Do **not** stash, reset, or clean anything in `project`. Your colleague's uncommitted notes and untracked draft stay where they are.

## 2. Verify the scratch location is ignored before creating a worktree inside it

```sh
git -C project check-ignore -q -- "scratch-checkouts/" ; echo $?
```

Require exit `0`. If it is not ignored, add `scratch-checkouts/` to the repo's local exclude file (`git -C project rev-parse --path-format=absolute --git-path info/exclude`) **after** confirming with the colleague, or put the worktree outside the checkout instead.

## 3. Create the task worktree on branch `task/normalize`, based on `release/next`

```sh
git -C project worktree add -b task/normalize project/scratch-checkouts/normalize release/next
```

## 4. Verify the new checkout

```sh
git -C project/scratch-checkouts/normalize rev-parse --show-toplevel
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize rev-parse HEAD
git -C project status --short --branch   # colleague's checkout untouched
```

Expect `HEAD` to equal `release/next`'s commit, and the colleague's notes/draft still present.

## 5. Locate and fix `normalize_label` in the task worktree

```sh
grep -rn "def normalize_label" project/scratch-checkouts/normalize
```

Edit that file so the function strips surrounding whitespace and lowercases, e.g.:

```python
def normalize_label(label):
    return label.strip().lower()
```

(Apply `.strip()` before `.lower()`; adjust to the surrounding code's style and type handling.)

## 6. Run the project's check in the task worktree

First identify the check command from the repo's own instructions, e.g.:

```sh
cat project/scratch-checkouts/normalize/package.json   # "scripts": {...}
ls project/scratch-checkouts/normalize/Makefile project/scratch-checkouts/normalize/justfile 2>/dev/null
```

Then run the matching one, for example:

```sh
cd project/scratch-checkouts/normalize && npm test
# or: make check / pytest / cargo test / go test ./... — whichever the repo defines
```

Require it to pass before committing.

## 7. Review, stage, and commit only the fix

```sh
git -C project/scratch-checkouts/normalize diff
git -C project/scratch-checkouts/normalize add <path-to-fixed-file>
git -C project/scratch-checkouts/normalize commit -m "fix: normalize_label strips surrounding whitespace and lowercases"
```

## 8. Final verification for review handoff

```sh
git -C project/scratch-checkouts/normalize status --short --branch
git -C project/scratch-checkouts/normalize log -1 --oneline
git -C project worktree list --porcelain -z
git -C project status --short --branch   # still shows only colleague's notes/draft
```

Leave the worktree and branch in place for review. Do **not** merge into `release/next`, push, or publish anything.
