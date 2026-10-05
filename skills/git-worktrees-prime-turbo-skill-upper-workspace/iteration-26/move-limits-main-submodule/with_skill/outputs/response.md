No. Do not run `git worktree move` for either — it fails for both cases:

> `Linked checkouts only; cannot move main or submodule-containing worktrees.` — `references/raw-git-commands.md:82-83`

### 1. Checks first — both moves

Run in order, from current main/bare repo. `<repo>` = current primary-root or bare repo:

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<worktree-to-move>" status --short --branch --untracked-files=all
git -C "<worktree-to-move>" status --short --ignored
git -C "<worktree-to-move>" rev-parse HEAD
```

Verify: canonical absolute path, branch/detached `HEAD`, clean index, owner, no `MERGE_HEAD/REBASE/BISECT` in progress, no agent/editor/terminal/service using it. Leave the directory. Check submodules/nested repos separately. Parse `list --porcelain -z` in scripts. Do not `prune`, `unlock`, `remove`, or filesystem-delete to fix registration.

### 2. Main checkout — correct procedure

`move` cannot move main. Filesystem-move + repair:

```sh
# after checks above
mv "<primary-root>" "<new-primary-root>"
git -C "<new-primary-root>" worktree repair "<linked-worktree-abs-path>"
git -C "<new-primary-root>" worktree list --porcelain -z
```

`"<repo>"` is now the new location. Repair each linked checkout by its current absolute path. Repair preserves branch/index/state. Then verify new registration.

### 3. Linked checkout with submodules — correct procedure

`move` cannot move submodule-containing worktrees. Multiple superproject checkouts are discouraged — check submodule limits first. Filesystem-move + repair:

```sh
# after checks above + submodule state check
mv "<worktree>" "<new-path>"
git -C "<primary-root>" worktree repair "<new-path>"
git -C "<primary-root>" worktree list --porcelain -z
```

Preserve `.git` file + contents on move. Repair from current main/bare repo with the new absolute linked path, then re-list to verify. Handle submodule gitdirs separately; do not assume superproject repair fixed them.

