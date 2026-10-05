Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> default: `<primary-root>/.worktrees/<task>`
* Use unique task name, unused path. Do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage — require `exit 0`:

```sh
git rev-parse --path-format=absolute --git-path info/exclude
# .git may be a file; locate exclude from enclosing checkout
git -C "/repo" check-ignore -q -- ".worktrees/checkout-api/"
```

Repeat `check-ignore` after creation.

Also before `add`: read `references/raw-git-commands.md:5-40`, verify `worktree list --porcelain -z`, base ref via `rev-parse --verify "<base>^{commit}"`.

