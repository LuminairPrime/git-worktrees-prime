No — don't assume `main` is the integration target.

1. **Verify base:** check `git remote show origin | grep HEAD`, `git symbolic-ref refs/remotes/origin/HEAD`, `CONTRIBUTING.md`, and recent merged PR targets. Many repos use `main`, but `master`, `develop`, `trunk`, or release branches are common.
2. **Base:** once confirmed, `git fetch origin` and base off fresh `origin/<target>`.
3. **Task branch vs inspection:**
   - Task branch: named persistent branch for feature X, e.g. `git worktree add ../feature-X -b feature/X origin/main` — keep, commit, push from here.
   - Disposable inspection: `git worktree add --detach /tmp/inspect-<sha>` for read-only exploration — delete after with `git worktree remove`, no branch created.

No repo in `/tmp/skill-up-4221809376` to verify — what repo/path is feature X for?
