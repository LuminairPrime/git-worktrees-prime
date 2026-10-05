In `case03/checkouts/adapter-current`, reuse only — no new checkout, no integration/publishing:

1. Confirm + repair moved registration first, preserve state:
```bash
pwd -P
git -C case03/checkouts/adapter-current worktree repair "$(pwd -P)/case03/checkouts/adapter-current"
git -C case03/checkouts/adapter-current worktree list --porcelain
```
Check: `adapter-current` listed with correct absolute path. Do not prune/move/delete/recreate `adapter-old` or `adapter-current`.

2. Establish starting state in same checkout:
```bash
git -C case03/checkouts/adapter-current branch --show-current
git -C case03/checkouts/adapter-current rev-parse HEAD
git -C case03/checkouts/adapter-current status --short --branch
git -C case03/checkouts/adapter-current log --oneline -5
```
Check: branch `task/adapter`, expected base/HEAD, uncommitted draft notes intact, no `MERGE_HEAD`/`CHERRY_PICK_HEAD`/`rebase-merge` in progress.

3. Consume completed schema worker, no checkout switch:
```bash
cat case03/checkouts/adapter-current/worker-status.json
git -C case03/checkouts/adapter-current log --oneline -3 schema/prep
git -C case03/checkouts/adapter-current show --stat schema/prep
```
Check: `schema/prep` complete, note `SCHEMA_VERSION` value for use.

4. Finish `encode_record` in place:
   - `name.strip().lower()`
   - `enabled` as boolean
   - `schema` from `SCHEMA_VERSION`
   - Keep existing draft notes untouched, verify with `git diff --stat`.

5. Validate from checkout root with project check:
```bash
git -C case03/checkouts/adapter-current status --short --branch
./project-check-from case03/checkouts/adapter-current
```
Check: clean except intended `encode_record` change, check passes.

6. Commit on `task/adapter`:
```bash
git -C case03/checkouts/adapter-current add <encode_record-path>
git -C case03/checkouts/adapter-current commit -m "Finish encode_record"
git -C case03/checkouts/adapter-current branch --show-current
git -C case03/checkouts/adapter-current log --oneline -2
```

7. Leave ready for review, no cleanup:
```bash
pwd -P
git -C case03/checkouts/adapter-current worktree list --porcelain
git -C case03/checkouts/adapter-current status --short --branch
```
Report: absolute path, `task/adapter`, tip commit, check passed, review location, checkout retained, no merge/push/prune/remove.

