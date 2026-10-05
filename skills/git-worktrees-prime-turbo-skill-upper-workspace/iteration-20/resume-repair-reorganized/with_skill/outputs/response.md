Resume in `case03/checkouts/adapter-current`, reuse only:

1. `git worktree list --porcelain`
   Check: `adapter-current` present, `adapter-old` stale/missing, `task/adapter` + `schema/prep` owners.
2. `git -C <primary-root> worktree repair <abs-path>/case03/checkouts/adapter-current`
   Relocated checkout, current absolute path only.
3. `git worktree list --porcelain`
   Check: `adapter-current` registered at new path. Do not prune.
4. `git -C case03/checkouts/adapter-current status`
   `git -C case03/checkouts/adapter-current branch --show-current`
   `git -C case03/checkouts/adapter-current log --oneline -5`
   `git -C case03/checkouts/adapter-current diff --stat; git diff --cached --stat`
   Check: on `task/adapter`, keep existing draft notes, no MERGE/REBASE/CHERRY_PICK in progress.
5. `cat case03/checkouts/adapter-current/worker-status.json`
   `git -C case03/checkouts/adapter-current log --oneline -3 schema/prep`
   `git -C case03/checkouts/adapter-current show schema/prep --stat`
   Check: schema worker complete, get `SCHEMA_VERSION` value/ref.
6. Inspect `encode_record` + `SCHEMA_VERSION` in `adapter-current` only.
7. Edit `encode_record` in `adapter-current` only:
   `name.strip().lower()`, `enabled` as `bool`, `schema` from `SCHEMA_VERSION`. Touch nothing else.
8. `git -C case03/checkouts/adapter-current diff`
   Check: only `encode_record` changed, draft notes retained.
9. Run project check from `case03/checkouts/adapter-current`.
   Check: must pass, fix `encode_record` only if failed.
10. `git -C case03/checkouts/adapter-current add <encode_record-file>`
    `git -C case03/checkouts/adapter-current commit -m "<task-convention>: finish encode_record"`
    Check: `branch --show-current` still `task/adapter`.
11. `git -C case03/checkouts/adapter-current status`
    `git -C case03/checkouts/adapter-current log --oneline -3`
    `git worktree list --porcelain`
    Check: clean, tip on `task/adapter`, `adapter-current` registered.

Stop: same checkout ready for review. No merge, no push/PR, no `remove`/`prune`.

