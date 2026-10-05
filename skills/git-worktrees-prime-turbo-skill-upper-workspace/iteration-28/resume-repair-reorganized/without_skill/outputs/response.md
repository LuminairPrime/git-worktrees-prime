In `case03/checkouts/adapter-current`, run in order:

1. `cd case03/checkouts/adapter-current && pwd`
   - confirm `adapter-current`, not `adapter-old`.
2. `git rev-parse --show-toplevel`
3. `git status --short --branch`
4. `git branch --show-current`
   - must be `task/adapter`, if not: `git checkout task/adapter`
5. `cat worker-status.json`
   - verify schema worker `schema/prep` = complete.
6. `git fetch origin schema/prep`
7. `git log --oneline -5 schema/prep`
8. `git show schema/prep --stat`
9. `grep -rn SCHEMA_VERSION .`
10. `grep -rn encode_record .`
11. `cat SCHEMA_VERSION` / `git show schema/prep:SCHEMA_VERSION`
12. Edit `encode_record` only:
    - `name.strip().lower()`
    - include `enabled` as `bool`
    - include `schema` from `SCHEMA_VERSION`
    - keep existing draft notes, do not delete/rename them.
13. `git diff --stat`
14. `git diff` - verify only `encode_record` changed, draft notes kept.
15. Validate: run project check, e.g. `make check` / `./check.sh` / `pytest` - use repo's defined check, must pass.
16. `git status --short --branch`
17. `git add <adapter-file-with-encode_record>`
18. `git commit -m "Finish encode_record: normalize name, enabled bool, schema version"`
19. `git log --oneline -3`
20. `git status --short --branch`
21. `pwd && git branch --show-current`
    - leave in `adapter-current` on `task/adapter` ready for review.

Do not: `cd adapter-old`, merge/rebase, push, integrate, or publish.

