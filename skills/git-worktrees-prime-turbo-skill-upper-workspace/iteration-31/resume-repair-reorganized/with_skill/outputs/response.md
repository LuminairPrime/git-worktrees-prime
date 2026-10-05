In `case03/checkouts/adapter-current`, in order:

1. Repair move first, no other work before:
```sh
git worktree repair "case03/checkouts/adapter-current"
git worktree list --porcelain -z
```
Check: `adapter-old` registration gone, `adapter-current` registered. Do not prune/move/delete/recreate.

2. Enter same checkout, confirm reuse:
```sh
cd case03/checkouts/adapter-current
pwd
git branch --show-current
git status
git log -1 --oneline
```
Check: branch `task/adapter`, no in-progress merge/rebase, existing changes intact.

3. Confirm schema worker done:
```sh
cat worker-status.json
git fetch origin schema/prep
git log -1 --oneline schema/prep
```
Check: worker `complete` on `schema/prep`.

4. Read its result + current state, preserve notes:
```sh
git show schema/prep:worker-status.json
cat SCHEMA_VERSION
grep -n "encode_record\|SCHEMA_VERSION\|draft" -R .
git diff --stat
```
Check: `SCHEMA_VERSION` value, current `encode_record` body, location of existing draft notes.

5. Finish `encode_record` only:
   - `name.strip().lower()`
   - `enabled` as `bool`
   - `schema` from `SCHEMA_VERSION`
   - Keep existing draft notes untouched.

6. Validate:
```sh
git diff
git status --short
```
Check: only `encode_record` changed, draft notes kept.

7. Run project check from this checkout:
```sh
# repo-defined check, e.g.:
./check.sh
# or make check / pytest / npm test per repo docs
```
Check: must pass. Fix only in `adapter-current` if fails, re-run.

8. Commit on `task/adapter`:
```sh
git add <encode_record file>
git commit -m "Finish encode_record"
git log -1 --oneline
git status
```

9. Leave ready for review, no integration/publishing:
```sh
git worktree list
git branch --show-current
git status
```
Check: still in `case03/checkouts/adapter-current` on `task/adapter`, clean except intended commit. Do not merge/rebase/push/PR, do not remove/prune worktree or delete branch.

