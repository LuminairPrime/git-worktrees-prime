No. Do not run `git worktree move` for either case:

> `move`: Note that the main worktree or linked worktrees containing submodules cannot be moved with this command.

Checks first, in order:

1. `git --version` - `repair` required
2. `git worktree list --porcelain -v` - main first, then linked; check `locked`/`prunable`/branch/HEAD
3. `git rev-parse --show-toplevel --git-dir --git-common-dir --is-bare-repository` - from each checkout
4. `cat .git` - main: directory `.git/`; linked: file `gitdir: <common>/worktrees/<id>`
5. `git status --porcelain=v1 -b` + `git stash list` - must be clean/recorded
6. Linked only: `git submodule status --recursive` + `cat .gitmodules` + `git config --file .gitmodules --list`
7. `test -e <new-path> && echo TAKEN || echo FREE` + confirm not in `git worktree list --porcelain`

Main checkout - correct procedure:

1. `mv /old/main /new/main` - OS move only, no `git worktree move`
2. `cd /new/main`
3. `git worktree repair` - reestablishes `commondir`/`gitdir` to linked worktrees. If linkeds: `git worktree repair <path-to-linked>...`
4. Verify: `git worktree list --porcelain -v`, `git rev-parse --git-dir --git-common-dir`, `git status`, `git worktree prune -n -v`

Linked with submodules - correct procedure:

1. `mv /old/task /new/task` - OS move only, no `git worktree move`
2. `cd /new/task`
3. `git worktree repair` - fixes superproject linkage only
4. Verify superproject: `cat .git`, `git worktree list --porcelain -v`, `git rev-parse --git-dir --git-common-dir`
5. Verify submodules: `git submodule status --recursive`, `git submodule foreach --recursive 'git rev-parse --show-toplevel --git-dir; git status --porcelain=v1 -b'`, `cat <sub>/.git`
6. If submodule `gitdir:` pointers broken, do not hand-edit; recreate via `git worktree remove --force <new/task>` + `git worktree add <new/task> <branch>` + `git submodule update --init --recursive`

