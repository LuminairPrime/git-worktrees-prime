`/repo` doesn't exist in this environment, so nothing can be created right now — but here's the answer per the worktree skill's rules:

## Where to place it

No repository location convention exists, so use the default for raw Git:

```
/repo/.worktrees/checkout-api
```

- `<primary-root>` is the **main worktree's directory** (`/repo`), regardless of branch name.
- Use the task name as the leaf: unique, descriptive, and an unused path.
- The rule would differ only if `/repo` were a bare repository (then it's a *sibling* of the repo directory), or if a convention existed. Never place it inside another disposable worktree.

## What to verify before creating inside another checkout

Because the destination lives inside the main checkout, Git would see the new worktree's files as untracked noise. The destination must be **ignored** — via `.gitignore` or a local exclusion in the exclude file:

1. **Locate the exclude file** (`.git` may be a *file*, not a directory, so don't guess the path):
   ```sh
   git -C /repo rev-parse --path-format=absolute --git-path info/exclude
   ```
   Add `.worktrees/` there (or ensure `.gitignore` covers it) if not already ignored.

2. **Verify ignore coverage from the enclosing checkout — exit 0 required before creation**, with a trailing `/` on the destination's relative path:
   ```sh
   git -C /repo check-ignore -q -- ".worktrees/checkout-api/"
   ```

3. **Re-run the same check after creation** to confirm coverage still holds.

## Prerequisite checks before `worktree add`

```sh
git -C /repo worktree list --porcelain -z   # confirm /repo is the main worktree; find an unused path
git -C /repo status --short --branch         # /repo is a checkout, not bare
git -C /repo rev-parse --verify "<base-ref>^{commit}"   # explicit base — don't assume main/master
```

Then create with a **new** branch (`-b`, never `-B`):

```sh
git -C /repo worktree add -b "checkout-api" /repo/.worktrees/checkout-api "<base-ref>"
```

Finally verify the result:

```sh
git -C /repo/.worktrees/checkout-api rev-parse --show-toplevel
git -C /repo/.worktrees/checkout-api status --short --branch
git -C /repo/.worktrees/checkout-api rev-parse HEAD
```

Two more things worth noting: uncommitted changes in `/repo` do **not** follow the worktree — transfer anything needed deliberately; and if the checkout was ever moved/renamed, run `git -C /repo worktree repair "<worktree>"` first, before any other command.

If you mount or create `/repo`, I can run these steps for you.
