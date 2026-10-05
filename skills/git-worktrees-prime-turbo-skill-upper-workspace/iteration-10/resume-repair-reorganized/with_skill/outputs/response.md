In `case03/checkouts/adapter-current`, reuse only — no new checkout, no integration:

1. Confirm relocated registration:
```sh
pwd
git worktree list --porcelain
```
Expected: entry for `case03/checkouts/adapter-current` on `task/adapter`, stale `adapter-old` path.

2. Repair live checkout, do not prune:
```sh
git worktree repair "$(pwd)"
git worktree list --porcelain
```
Check: new absolute path registered, `task/adapter` still checked out there. Do NOT run `prune`, `remove`, `move`.

3. Verify reuse state in same checkout:
```sh
git -C case03/checkouts/adapter-current rev-parse --show-toplevel
git -C case03/checkouts/adapter-current branch --show-current
git -C case03/checkouts/adapter-current status --short --branch
git -C case03/checkouts/adapter-current log --oneline -5
git -C case03/checkouts/adapter-current rev-parse --git-path MERGE_HEAD; git -C case03/checkouts/adapter-current rev-parse --git-path REBASE_HEAD; git -C case03/checkouts/adapter-current rev-parse --git-path CHERRY_PICK_HEAD
```
Check: `task/adapter`, uncommitted draft notes retained, no merge/rebase in progress. Do NOT `reset --hard`, `clean`, `checkout -- .`.

4. Consume completed schema work:
```sh
cat case03/checkouts/adapter-current/worker-status.json
git -C case03/checkouts/adapter-current log --oneline schema/prep -3
git -C case03/checkouts/adapter-current show schema/prep --stat
```
Check: `schema/prep` complete, note `SCHEMA_VERSION` value/source.

5. Finish `encode_record` only, keep draft notes:
- edit `encode_record`: `name.strip().lower()`, `enabled` as `bool`, `schema` from `SCHEMA_VERSION`.
- verify:
```sh
git -C case03/checkouts/adapter-current diff --check
git -C case03/checkouts/adapter-current diff --stat
git -C case03/checkouts/adapter-current diff
```

6. Validate with project check from that checkout:
```sh
git -C case03/checkouts/adapter-current status --short --branch
# run repo-defined check from case03/checkouts/adapter-current, e.g. discovered check script
```

7. Commit on same branch, no publishing:
```sh
git -C case03/checkouts/adapter-current add <edited-adapter-file>
git -C case03/checkouts/adapter-current commit -m "Finish encode_record"
git -C case03/checkouts/adapter-current log --oneline -3
git -C case03/checkouts/adapter-current status --short --branch
git worktree list --porcelain
```
Check: `HEAD` on `task/adapter` in `case03/checkouts/adapter-current`, clean, ready for review.

Retained: checkout + `task/adapter`. Not done: merge/rebase/push/PR, `worktree remove`, `branch -d/-D`, `prune`, `gc`.

