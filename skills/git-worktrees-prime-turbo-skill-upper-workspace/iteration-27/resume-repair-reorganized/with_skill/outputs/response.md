Resume in-place in `case03/checkouts/adapter-current` — repair-first, no new checkout, no integration/publish:

1. Repair moved registration first, before any other work:
   `git worktree repair "$(pwd)/case03/checkouts/adapter-current"`

2. Verify new registration:
   `git worktree list --porcelain -z`

3. Confirm same checkout path/branch/HEAD in selected path:
   `git -C case03/checkouts/adapter-current rev-parse --show-toplevel`
   `git -C case03/checkouts/adapter-current branch --show-current`
   `git -C case03/checkouts/adapter-current rev-parse HEAD`
   `git -C case03/checkouts/adapter-current log --oneline -5`
   Expect branch `task/adapter`. Do not `-B`, move, delete, recreate, or prune.

4. Inspect uncommitted state and ongoing operations in that checkout only:
   `git -C case03/checkouts/adapter-current status`
   Check for `MERGE_HEAD/REBASE_HEAD/CHERRY_PICK_HEAD` — stop if active.

5. Confirm schema worker complete:
   `cat worker-status.json`
   `git -C case03/checkouts/adapter-current log --oneline -3 schema/prep`
   `git -C case03/checkouts/adapter-current show schema/prep:SCHEMA_VERSION`

6. Inspect current draft without switching branches:
   `git -C case03/checkouts/adapter-current diff`
   Read `encode_record` source + `SCHEMA_VERSION` in `case03/checkouts/adapter-current`.

7. Edit `encode_record` in `case03/checkouts/adapter-current` only:
   strip + lowercase `name`, `enabled` as boolean, `schema` from `SCHEMA_VERSION`. Preserve existing draft notes.

8. Review preservation:
   `git -C case03/checkouts/adapter-current diff`

9. Validate from task checkout with project check:
   `git -C case03/checkouts/adapter-current <project-check>`

10. Commit on `task/adapter` in same checkout:
    `git -C case03/checkouts/adapter-current add <encode_record-file>`
    `git -C case03/checkouts/adapter-current commit -m "<adapter: finish encode_record>"`
    `git -C case03/checkouts/adapter-current log --oneline -2`
    `git -C case03/checkouts/adapter-current status --short --branch`

11. Leave ready for review, verify retained:
    `git worktree list --porcelain -z`
    No merge, rebase, push, PR, integration, `remove`, `prune`, or publish. Retain `case03/checkouts/adapter-current` on `task/adapter`.

