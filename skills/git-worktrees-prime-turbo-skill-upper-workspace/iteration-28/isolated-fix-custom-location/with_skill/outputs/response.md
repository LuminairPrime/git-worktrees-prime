1. Establish starting state in colleague's checkout, do not modify it:

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" status --short --branch
git -C "<repo>" rev-parse --verify "release/next^{commit}"
```

Base is `release/next`, integration target not authorized for merge. If `release/next` is remote-tracking, update it without pulling into colleague checkout:

```sh
git -C "<repo>" fetch origin release/next
git -C "<repo>" rev-parse --verify "release/next^{commit}"
```

2. Verify requested path `project/scratch-checkouts/normalize` is ignored inside enclosing checkout, require exit 0:

```sh
git -C "<repo>" rev-parse --path-format=absolute --git-path info/exclude
git -C "<enclosing-checkout>" check-ignore -q -- "scratch-checkouts/normalize/"
```

3. Create separate checkout on new branch from base, do not use `-B`:

```sh
git -C "<repo>" worktree add -b "task/normalize" "project/scratch-checkouts/normalize" "release/next"
```

4. Verify new checkout and ignore coverage:

```sh
git -C "project/scratch-checkouts/normalize" rev-parse --show-toplevel
git -C "project/scratch-checkouts/normalize" status --short --branch
git -C "project/scratch-checkouts/normalize" rev-parse HEAD
git -C "<enclosing-checkout>" check-ignore -q -- "scratch-checkouts/normalize/"
```

5. Fix in task checkout only:

- edit `normalize_label` to strip surrounding whitespace and return lowercase text.
- run project's documented check from `project/scratch-checkouts/normalize`.

6. Commit on task branch, leave colleague checkout intact, no stash/reset/copy:

```sh
git -C "project/scratch-checkouts/normalize" status --short --branch --untracked-files=all
git -C "project/scratch-checkouts/normalize" diff
git -C "project/scratch-checkouts/normalize" add <task-files>
git -C "project/scratch-checkouts/normalize" commit -m "<fix normalize_label>"
git -C "project/scratch-checkouts/normalize" log -1 --oneline
git -C "project/scratch-checkouts/normalize" status --short --branch
```

7. Leave ready for review, no merge/push/prune/remove:

```sh
git -C "<repo>" worktree list --porcelain -z
```

Retained: checkout `project/scratch-checkouts/normalize` on `task/normalize`, branch preserved, colleague's uncommitted notes/untracked draft untouched.

