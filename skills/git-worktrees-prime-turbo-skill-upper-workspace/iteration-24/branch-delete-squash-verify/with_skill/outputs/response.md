No — `git branch -D task/export` now would bypass the safeguard that just fired.

`git branch -d` checks ancestry, not content. Squash-merge breaks ancestry, so refusal is expected even when fully integrated.

Verify patch-equivalence first, from a surviving checkout `<repo>`:

1. Refresh and resolve the integration target:
```sh
git -C "<repo>" fetch origin
git -C "<repo>" rev-parse --verify "main^{commit}"
git -C "<repo>" rev-parse --verify "task/export^{commit}"
git -C "<repo>" worktree list --porcelain -z
```

2. Confirm why `-d` refuses — this should fail for squash:
```sh
git -C "<repo>" merge-base --is-ancestor "task/export" "main"
```

3. Verify content is integrated:
```sh
git -C "<repo>" cherry main "task/export"
git -C "<repo>" log --oneline --cherry main..."task/export"
git -C "<repo>" diff main..."task/export" --stat
```
Integrated = `cherry` empty or only `-` lines, `log --cherry` empty, `diff` empty except changes landed on `main` after the squash.

`-D` is acceptable only when:
- all above prove `task/export` tip is superseded by `main`,
- branch is unused, task-owned, no checkout holds it,
- not needed for pending review — closed PR alone is insufficient,
- abandonment of the obsolete history is authorized.

Then:
```sh
git -C "<repo>" branch -D "task/export"
git -C "<repo>" branch --list "task/export"
git -C "<repo>" worktree list --porcelain -z
```
