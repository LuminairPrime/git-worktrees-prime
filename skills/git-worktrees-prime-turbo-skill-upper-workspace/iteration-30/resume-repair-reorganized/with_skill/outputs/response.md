Resume in `case03/checkouts/adapter-current` on `task/adapter` — repair first:

1. Repair moved registration:
   `git -C case03/checkouts/adapter-current worktree repair case03/checkouts/adapter-current`
2. Verify registration:
   `git -C case03/checkouts/adapter-current worktree list --porcelain -z`
   Confirm `adapter-current` listed at new path, no `adapter-old` recreation.
3. Confirm checkout/branch state:
   `git -C case03/checkouts/adapter-current branch --show-current`
   `git -C case03/checkouts/adapter-current status -sb`
   `git -C case03/checkouts/adapter-current log --oneline -3`
   Expect `task/adapter`, existing work intact.
4. Check for unfinished operation:
   `git -C case03/checkouts/adapter-current status`
   Do not proceed if `MERGE_HEAD/REBASE_HEAD/CHERRY_PICK_HEAD` present.
5. Confirm schema dependency:
   `cat worker-status.json`
   Verify `schema/prep` complete, read `SCHEMA_VERSION`.
6. Finish `encode_record` in `adapter-current` only:
   `name.strip().lower()`, `enabled` as `bool`, `schema` from `SCHEMA_VERSION`. Keep existing draft notes unchanged.
7. Validate from task checkout:
   `project check` from `case03/checkouts/adapter-current`
8. Commit on `task/adapter`:
   `git -C case03/checkouts/adapter-current add <adapter-file-only>`
   `git -C case03/checkouts/adapter-current commit -m "<task commit>"`
   `git -C case03/checkouts/adapter-current log -1 --oneline`
   `git -C case03/checkouts/adapter-current status`
9. Leave ready for review in same checkout:
   `git -C case03/checkouts/adapter-current worktree list --porcelain -z`
   No move/delete/prune, no integration to base, no push/publish.

