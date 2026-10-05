In `case03/checkouts/adapter-current`, in order:

1. `cd case03/checkouts/adapter-current && pwd`
   Check: still in adapter task checkout, not `adapter-old`.

2. `git worktree list`
   Check: `adapter-current` listed, `adapter-old` stale/missing.

3. `git worktree repair`
   Then `git worktree list` again.
   Then `git worktree prune --dry-run` — only prune if it targets the old `adapter-old` path, preserve draft notes.

4. `git branch --show-current`
   Check: on `task/adapter`. If not: `git checkout task/adapter`.

5. `git status --short --branch`
   Check: working tree state, identify existing draft notes to keep. Do not delete/reset untracked files.

6. `cat worker-status.json`
   Check: schema worker `schema/prep` = complete. Note result/SHA.

7. `git branch -a --list "schema/prep" && git log --oneline -3 schema/prep`
   `cat SCHEMA_VERSION` or `grep -R SCHEMA_VERSION`
   Check: expected schema version value to use.

8. Finish `encode_record` in place:
   - `name.strip().lower()`
   - `enabled` as `boolean`
   - `schema` from `SCHEMA_VERSION`
   Keep existing draft notes unmodified.

9. `git diff -- encode_record-file`
   `git status --short`
   Check: only intended file changed, draft notes still present.

10. Run project check, e.g. `make check` / documented check script.
    Check: passes with no failures.

11. `git add <encode_record-file-only>`
    `git branch --show-current` — confirm still `task/adapter`
    `git commit -m "..."`
    Check: `git status --short --branch` clean except intentional draft notes, `git log --oneline -2`.

12. `git worktree list && pwd && git branch --show-current`
    Leave `adapter-current` on `task/adapter` ready for review.
    No merge, no integration, no push/publish.

