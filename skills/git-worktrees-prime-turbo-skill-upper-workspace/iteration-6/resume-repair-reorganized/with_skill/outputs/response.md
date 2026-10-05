Resume in `case03/checkouts/adapter-current` — reuse, do not create:

1. Confirm stale registration:
   `git worktree list --porcelain`
2. Repair relocated checkout from `adapter-old`:
   `git -C <primary-root> worktree repair "$(realpath case03/checkouts/adapter-current)"`
   Do not prune.
3. Verify registration:
   `git worktree list --porcelain`
   `realpath case03/checkouts/adapter-current`
4. Enter task checkout and verify state:
   `cd case03/checkouts/adapter-current`
   `git rev-parse --show-toplevel; git branch --show-current`
   Require: `task/adapter`
   `git status --short --branch`
   `git log --oneline -5`
   `test ! -f .git/MERGE_HEAD -a ! -f .git/REBASE_HEAD -a ! -f .git/CHERRY_PICK_HEAD`
   `git diff --stat; git diff`
5. Confirm schema worker done:
   `cat worker-status.json`
   Require: `schema/prep` complete, get `SCHEMA_VERSION`.
6. Finish `encode_record` in place only:
   `name.strip().lower()`, `enabled` as `bool`, `schema` from `SCHEMA_VERSION`. Keep existing draft notes — verify with `git diff` that only `encode_record` changed.
7. Validate:
   run project check from this checkout, e.g. `pytest -q`
   Require exit 0.
8. Commit on `task/adapter`:
   `git add <adapter-file>`
   `git commit -m "Finish encode_record"`
   `git log --oneline -3; git status --short --branch`
9. Leave ready for review, no integration/publishing:
   `git worktree list --porcelain`
   Do not merge, push, `remove`, or `prune`. Report path, `task/adapter` tip, and check result.

