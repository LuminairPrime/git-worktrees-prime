No — do not run `git worktree move` on both as-is.

* Main checkout: `git worktree move` will refuse: `fatal: '<path>' is a main working tree`.
* Linked checkout with submodules: `git worktree move` only fixes top-level `gitdir`, leaves `<submodule>/.git` files and `.../.git/worktrees/<name>/modules/...` pointing at old path. Move is incomplete without repair.

Checks first, in order:

1. `git --version` — need >=2.39 for `git worktree repair`.
2. `git -C <main-path> worktree list --porcelain --verbose` — identify main vs linked, `bare`, `locked`, `prunable`, branch.
3. `git -C <main-path> rev-parse --git-dir --git-common-dir --show-toplevel --is-bare-repository`
   `git -C <task-path> rev-parse --git-dir --git-common-dir --show-toplevel`
   `ls -ld <main-path>/.git <task-path>/.git; cat <task-path>/.git`
   Expect: main: `--git-dir` == `--git-common-dir`, `.git` is directory. Linked: `--git-dir` != `--git-common-dir`, `.git` is file: `gitdir: <main>/.git/worktrees/<name>`.
4. Cleanliness:
   `git -C <main-path> status --porcelain=v1 -uall`
   `git -C <task-path> status --porcelain=v1 -uall`
   Must be empty. No `MERGE_HEAD/CHERRY_PICK_HEAD/REBASE_HEAD/BISECT_LOG` in `$(git -C <path> rev-parse --git-dir)`.
5. Submodules:
   `git -C <task-path> submodule status --recursive`
   `git -C <task-path> submodule foreach --recursive 'git status --porcelain=v1 -uall'`
   Must be empty, no `-` uninitialized / `+` mismatched. Also `cat <task-path>/<sub>/.git` — file: `gitdir: .../worktrees/<name>/modules/<sub>`.
6. Destination:
   `test ! -e <new-main> || echo exists`
   `test ! -e <new-task> || echo exists`

Correct procedure:

Main — plain `mv` + repair:
1. `mv <old-main> <new-main>`
2. `cd <new-main> && git worktree repair`
3. `git worktree list --porcelain --verbose`
4. `git status --porcelain=v1 -uall; git submodule status --recursive`
5. `git -C <unchanged-linked-path> rev-parse --git-common-dir` — must resolve to `<new-main>/.git`.

Linked with submodules:
1. `git -C <new-main> worktree move <old-task> <new-task>`
2. `git -C <new-task> worktree repair`
3. `git -C <new-task> submodule foreach --recursive git worktree repair || git -C <new-task> worktree repair --help` — repair submodules recursively; inspect `cat <new-task>/.git` and `cat <new-task>/<sub>/.git` for old path remnants.
4. Verify: `git -C <new-task> rev-parse --absolute-git-dir --git-common-dir`
   `git -C <new-task> status --porcelain=v1 -uall`
   `git -C <new-task> submodule status --recursive`
   `git -C <new-task>/<sub> status --porcelain=v1 -uall`

