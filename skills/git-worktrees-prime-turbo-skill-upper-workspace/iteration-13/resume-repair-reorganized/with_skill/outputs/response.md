In `case03/checkouts/adapter-current`, reuse only:

1. Check registrations:
`git worktree list --porcelain`
2. Repair moved checkout, using current absolute path:
`git -C <primary-root> worktree repair <abs-path>/case03/checkouts/adapter-current`
3. Verify, do not prune live registration:
`git worktree list --porcelain`
4. In same checkout, confirm reuse:
`cd case03/checkouts/adapter-current`
`git branch --show-current` — expect `task/adapter`
`git status --short --branch`
`git log --oneline -3` — confirm `HEAD`, no `MERGE_HEAD`/rebase in progress
5. Confirm schema dependency complete:
`cat worker-status.json` — expect `schema/prep: complete`
`git log --oneline -1 schema/prep`
`cat SCHEMA_VERSION`
6. Finish `encode_record` in place:
`name.strip().lower()`, `enabled` as `bool`, `schema` from `SCHEMA_VERSION`. Keep existing draft notes — no delete/reset/clean.
7. Validate in same path:
Run project check from `case03/checkouts/adapter-current`, must pass.
8. Commit on same branch:
`git add <adapter-file>`
`git commit -m "adapter: finish encode_record"`
`git log --oneline -1`
`git branch --show-current` — still `task/adapter`
9. Leave ready for review, no integration/publishing:
`git worktree list --porcelain`
`git status --short --branch`
Do NOT merge/rebase/push/PR, do NOT `worktree remove/prune`, do NOT delete `task/adapter`.

