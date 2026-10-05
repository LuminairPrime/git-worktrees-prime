No. Do not run `git worktree move` for both.

* Main checkout: `git worktree move` will refuse: `fatal: '<path>' is main working tree`.
* Linked checkout with submodules: `git worktree move` fixes only superproject linkage, leaves submodule `gitdir` absolute paths broken.

Run these in order, from main checkout:

### 1. Pre-checks

```bash
git --version # need >=2.34 for repair
git worktree list --verbose
git rev-parse --show-toplevel --git-dir --git-common-dir --is-bare-repository
git status --porcelain=v1 -uall
git submodule status --recursive
cat <task-worktree>/.git
cat $GIT_COMMON_DIR/worktrees/<task-name>/gitdir
cat <task-worktree>/<sub>/.git
cat .gitmodules
test -e <new-main> && echo "target exists, abort"
test -e <new-task> && echo "target exists, abort"
```

Require: clean `status`, no `MERGE_HEAD/REBASE_HEAD/CHERRY_PICK_HEAD`, no `locked` in `list --verbose`, targets do not exist.

### 2. Main checkout: manual `mv` + `repair`

```bash
# quit editors/shells with cwd inside old paths
mv /old/main /new/main
cd /new/main
git worktree repair
git worktree list --verbose
git -C /new/main rev-parse --git-dir --git-common-dir --show-toplevel
git -C /new/main status --short
```

This rewrites `.git/worktrees/*/gitdir` back-pointers. Verify linked worktrees now resolve before moving them.

### 3. Linked task with submodules: deinit -> move -> reinit

```bash
cd /old/task
git status --porcelain=v1 -uall
git submodule status --recursive
git submodule deinit -f --all

# from new main:
cd /new/main
git worktree move /old/task /new/task
cd /new/task
git submodule update --init --recursive
git worktree repair
git worktree list --verbose
git status --short
git submodule status --recursive
git submodule foreach --recursive 'git rev-parse --git-dir --show-toplevel; git status --short'
```

