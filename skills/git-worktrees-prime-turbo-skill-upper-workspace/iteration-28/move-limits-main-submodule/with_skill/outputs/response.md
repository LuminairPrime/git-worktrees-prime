No. Do not run `git worktree move` for either:

* `git worktree move` cannot move main or submodule-containing worktrees.

### 1. Checks first — both cases

Run from main checkout or bare repo, `<repo>` is existing checkout/bare repo:

```sh
git -C "<repo>" worktree list --porcelain -z
```

Verify from output: canonical absolute path, main vs linked, branch/HEAD, ownership. Scripts must parse `--porcelain -z`.

Then for the checkout to be relocated `<worktree>`:

```sh
git -C "<worktree>" status --short --branch --untracked-files=all
git -C "<worktree>" rev-parse HEAD
```

Also verify: no agent/editor/terminal/service/test using it, leave directory before relocation, no unfinished Git operation, check submodules/nested repos separately. Do not prune, delete, or recreate live checkout to fix registration.

### 2. Main checkout — correct procedure

`git worktree move` will refuse. Manual relocate + repair:

```sh
# 1. list + checks above
# 2. filesystem move outside Git, preserving .git and contents:
mv "<old-primary-root>" "<new-primary-root>"
# 3. resume after move before any other work, from new main location:
git -C "<new-primary-root>" worktree list --porcelain -z
git -C "<new-primary-root>" worktree repair "<linked-worktree-current-absolute-path>"
git -C "<new-primary-root>" worktree list --porcelain -z
```

Repair preserves branch/index/state. Repeat `repair` for each linked checkout with its current absolute path.

### 3. Linked checkout containing submodules — correct procedure

`git worktree move` will refuse. Manual relocate + repair, superproject multi-checkout discouraged:

```sh
# 1. list + checks above, plus submodule state separately
# 2. filesystem move preserving .git file and contents:
mv "<old-worktree-abs>" "<new-worktree-abs>"
# 3. repair from main/bare repo, arg is current absolute path:
git -C "<repo>" worktree list --porcelain -z
git -C "<repo>" worktree repair "<new-worktree-abs>"
git -C "<repo>" worktree list --porcelain -z
```

Verify new registration in re-list before any other work in that checkout.

