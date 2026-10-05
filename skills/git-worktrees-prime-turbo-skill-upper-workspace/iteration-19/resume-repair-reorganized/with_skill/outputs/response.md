In `case03/checkouts/adapter-current`, on `task/adapter`, no integration/publish:

1. `cd case03/checkouts/adapter-current && pwd`
2. `git status`
3. `git branch --show-current` — must be `task/adapter`, if not: `git checkout task/adapter`
4. `cat worker-status.json` — confirm `schema/prep` complete
5. `git fetch origin schema/prep`
6. `git log --oneline -5 origin/schema/prep`
7. `cat SCHEMA_VERSION`
8. `grep -rn encode_record -- .`
9. Edit `encode_record`: `name.strip().lower()`, `enabled` as `bool`, `schema` from `SCHEMA_VERSION`. Keep draft notes unmodified.
10. `git status` + `git diff` — confirm only adapter file changed, draft notes kept
11. Run project check, e.g. `make check` / `./check.sh` / `pytest` — must pass
12. `git add <adapter-file>`
13. `git commit -m "Finish encode_record: normalize name, add enabled bool and schema version"`
14. `git log -1 --stat && git status`
15. Stay in `case03/checkouts/adapter-current` on `task/adapter` ready for review. Do not merge, rebase to main, tag, or publish.

