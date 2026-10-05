Place at `/repo/.worktrees/checkout-api`:

* No repo convention -> default is `<primary-root>/.worktrees/<task>`.
* `/repo` is main checkout, not bare.
* Use unused path, do not place inside another disposable worktree.

Before creating inside another checkout, verify ignore coverage - require exit `0`:

```sh
git rev-parse --path-format=absolute --git-path info/exclude
git -C "/repo" check-ignore -q -- ".worktrees/checkout-api/"
```

Destination must be ignored via `.gitignore` or local exclusion. Verify again after creation.

