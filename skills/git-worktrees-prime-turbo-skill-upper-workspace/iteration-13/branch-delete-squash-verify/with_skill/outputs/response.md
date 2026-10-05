No - do not run `git branch -D task/export` yet. Refusal is expected after squash-merge.

`git branch -d` checks ancestry, often against upstream, not your integration target. A squash creates a new commit on `main` - `task/export` tip never becomes an ancestor, so `-d` correctly refuses. `-D` bypasses that safeguard.

Verify integration first, in order:

1. Confirm checkout is gone and branch state:

```sh
git worktree list --porcelain -z
git show-ref --verify --quiet refs/heads/task/export; echo $?
git rev-parse --verify "task/export^{commit}"
```

2. Update and resolve current integration ref:

```sh
git fetch origin
git rev-parse --verify "main^{commit}"
git rev-parse --verify "origin/main^{commit}"
```

3. Test ancestry - expect failure for squash:

```sh
git merge-base --is-ancestor "task/export" "main"; echo $?
git merge-base --is-ancestor "task/export" "origin/main"; echo $?
```

Exit `1` does not prove loss, only non-ancestry.

4. Verify squash content equivalence:

```sh
git log --oneline -10 main
git log --oneline -10 origin/main
git cherry main task/export
git diff main task/export --stat
git diff origin/main task/export --stat
```

You want: `cherry` shows all `-` / no `+` lines, and `diff` shows no task-only changes left unapplied. Identify the squash commit with `log` and inspect it:

```sh
git show --stat <squash-commit>
```

A closed PR alone is insufficient.

5. `-D` is acceptable only when all hold:
* branch is task-owned, not checked out in any remaining worktree,
* work is verified in current `main`/`origin/main` per step 4, or preserved under another durable ref, or abandonment is explicitly authorized,
* no review still needs the ref.

Then:

```sh
git branch -D task/export
git branch --list "task/export"
git worktree list --porcelain -z
```

