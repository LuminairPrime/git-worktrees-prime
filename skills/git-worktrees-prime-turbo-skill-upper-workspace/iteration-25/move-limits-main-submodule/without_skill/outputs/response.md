No. Do not run `git worktree move` for either:

* `move`: `Move a worktree to a new location. Note that the main worktree or linked worktrees containing submodules cannot be moved with this command.` Both cases will be refused, even with `--force`.

### 1. Checks first - from main checkout

```bash
git --version # need repair, >=2.30
git worktree list --verbose
git worktree list --porcelain
git rev-parse --show-toplevel --git-dir --git-common-dir --is-bare-repository
git status --porcelain=v1 -uall
git stash list
git submodule status --recursive
test -d .git && echo "main: .git is dir" || cat .git
test -f <linked>/.git && cat <linked>/.git # -> gitdir: /old/main/.git/worktrees/<name>
test -e <new-path> && echo "destination must not exist" || echo "dest ok"
# must show no `locked`, no `prunable`, no dirty/modified submodule `+`/`U`
```

Do not move with CWD inside moved dir, editors/servers using it open, or locked worktree (`move` requires `--force` twice for locked, still refuses main/submodules).

### 2. Main checkout: `mv` + `repair`, not `move`

```bash
mv /old/main /new/main
cd /new/main
git worktree repair
git worktree list --verbose
git status --porcelain=v1 -uall
git rev-parse --git-dir --git-common-dir
```

`repair` in the moved main reestablishes `linked -> main` links. Verify all linked paths resolve again.

### 3. Linked checkout with submodules: `remove`/`add`, not `move`

`repair` only fixes superproject `gitdir` link, not nested `submodule/.git` gitfiles + `$GIT_DIR/modules/...` absolute paths. Support is incomplete - `BUGS: Multiple checkout ... submodules is incomplete. NOT recommended`.

Safe procedure:

```bash
# record what it is:
cd /old/linked && git rev-parse HEAD && git branch --show-current && git submodule status --recursive
cd /old/main
git worktree remove --force /old/linked # only if willing to re-clone; use --force for unclean/submodules
git worktree add /new/linked <branch-or-commit-from-above>
cd /new/linked
git submodule update --init --recursive
git worktree list --verbose
git submodule status --recursive
```

If you must preserve uncommitted work: `mv /old/linked /new/linked; cd /new/linked; git worktree repair`, then verify each `cat <sub>/.git` and `git submodule foreach 'git rev-parse --absolute-git-dir --show-toplevel'` - broken ones must be `deinit/update` or re-added.
