Resume in `case03/checkouts/adapter-current`, reuse only, no integration/publish:

1. `git worktree list --porcelain` - confirm stale `adapter-old` registration, missing `adapter-current`.
2. `realpath case03/checkouts/adapter-current` - confirm current absolute path.
3. `git -C <primary-root> worktree repair "<abs>/case03/checkouts/adapter-current"` - reconnect relocated checkout. Do not prune.
4. `git worktree list --porcelain` - verify `adapter-current` registered.
5. `cd case03/checkouts/adapter-current`
6. `git rev-parse --show-toplevel; git branch --show-current` - expect `task/adapter`.
7. `git status --short --branch; git log --oneline -5` - inspect changes, starting commit.
8. Check for `MERGE_HEAD`, `rebase-merge/`, `rebase-apply/` - confirm no ongoing operation.
9. `cat worker-status.json` - verify schema worker complete on `schema/prep`, read `SCHEMA_VERSION`.
10. Edit `encode_record` only: `name.strip().lower()`, `enabled` as boolean, `schema` from `SCHEMA_VERSION`. Keep existing draft notes.
11. Run project check from this checkout - must pass before commit.
12. `git add <task-files>; git commit -m "<task-commit>"` - on `task/adapter` only.
13. `git status --short --branch; git log --oneline -1; git worktree list --porcelain` - leave checkout at `case03/checkouts/adapter-current` ready for review.

