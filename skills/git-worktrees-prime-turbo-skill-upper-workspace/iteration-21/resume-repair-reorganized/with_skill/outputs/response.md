Reuse `case03/checkouts/adapter-current`, repair it, work only there on `task/adapter`:

1. Check registrations:
   `git worktree list --porcelain -z`
2. Repair moved checkout from primary repo with current absolute path, do not prune:
   `git -C <primary-root> worktree repair <abs-path>/case03/checkouts/adapter-current`
3. Verify repair:
   `git worktree list --porcelain -z`
   Confirm `adapter-current` registered, `adapter-old` stale entry gone, live entry kept.
4. Confirm checkout:
   `git -C case03/checkouts/adapter-current branch --show-current`
   Expect `task/adapter`
   `git -C case03/checkouts/adapter-current status --short --branch`
   `git -C case03/checkouts/adapter-current rev-parse HEAD`
   `git -C case03/checkouts/adapter-current log --oneline -3`
   Check no MERGE_HEAD/REBASE/MERGE in progress.
5. Confirm schema dependency:
   read `worker-status.json`, verify `schema/prep` complete
   `git log --oneline -3 schema/prep`
   Get `SCHEMA_VERSION` value from that result.
6. In `case03/checkouts/adapter-current` only, finish `encode_record`:
   `name.strip().lower()`, `enabled` as bool, `schema` from `SCHEMA_VERSION`.
   Keep existing draft notes: no reset, no `clean`, no delete.
7. Review:
   `git -C case03/checkouts/adapter-current diff`
   `git -C case03/checkouts/adapter-current status --short`
8. Validate in same checkout:
   run project check from `case03/checkouts/adapter-current`
9. Commit on `task/adapter`:
   `git -C case03/checkouts/adapter-current add <encode_record file>`
   `git -C case03/checkouts/adapter-current commit -m "Finish encode_record"`
10. Leave ready for review, same checkout:
    `git -C case03/checkouts/adapter-current branch --show-current`
    `git -C case03/checkouts/adapter-current status --short --branch`
    `git worktree list --porcelain -z`

No new worktree, no `-B`, no integration/merge/rebase, no push/PR/publish, no `worktree remove`, no branch `-d/-D`, no `prune`.

