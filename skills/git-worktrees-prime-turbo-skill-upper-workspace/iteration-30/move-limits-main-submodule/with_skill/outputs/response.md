No to both `git worktree move`: it cannot move main or submodule-containing worktrees.

Check first, in order:

```sh
git -C "<repo>" worktree list --porcelain -z
git -C "<main>" status --short --branch --untracked-files=all
git -C "<linked>" status --short --branch --untracked-files=all
# submodules / nested repos separately, plus owner/process use
```

Correct procedure for each — filesystem move + repair, not `move`:

1. Main checkout:
```sh
# stop agents/editors/services using it, leave directory
mv "<old-main>" "<new-main>"
git -C "<new-main>" worktree repair "<new-linked-path-if-any>"
git -C "<new-main>" worktree list --porcelain -z
```

2. Linked checkout with submodules:
```sh
# same filesystem preserve of `.git` + contents, then:
mv "<old-linked>" "<new-linked>"
git -C "<repo>" worktree repair "<new-linked>"
git -C "<repo>" worktree list --porcelain -z
# then repair/update submodules inside `<new-linked>` per superproject instructions
```

Do not `prune/move/delete/recreate` to fix registration; `repair` preserves branch/index/state.
