Resume in `case03/checkouts/adapter-current` — do not create/remove worktree:

1. Resolve current path:
```bash
realpath case03/checkouts/adapter-current
```

2. Repair relocated registration from old `adapter-old`:
```bash
git -C case03/checkouts/adapter-current worktree repair "$(realpath case03/checkouts/adapter-current)"
```

3. Verify registration — do not prune:
```bash
git -C case03/checkouts/adapter-current worktree list --porcelain -z
```
Check: `adapter-current` listed, `adapter-old` not used.

4. Confirm reuse of task checkout:
```bash
git -C case03/checkouts/adapter-current branch --show-current
git -C case03/checkouts/adapter-current status --short --branch
git -C case03/checkouts/adapter-current log --oneline -5
ls case03/checkouts/adapter-current/.git/MERGE_HEAD case03/checkouts/adapter-current/.git/REBASE_HEAD case03/checkouts/adapter-current/.git/CHERRY_PICK_HEAD 2>&1 || true
```
Required: branch `task/adapter`, no other owner, no active merge/rebase, keep draft notes — no `reset/clean/checkout -- .`.

5. Confirm schema worker complete:
```bash
cat case03/checkouts/adapter-current/worker-status.json
git -C case03/checkouts/adapter-current branch --list schema/prep
git -C case03/checkouts/adapter-current log --oneline -3 schema/prep
```
Required: status shows complete on `schema/prep`.

6. Read inputs in-place:
```bash
cat case03/checkouts/adapter-current/SCHEMA_VERSION
grep -n "encode_record\|SCHEMA_VERSION\|draft" -R case03/checkouts/adapter-current --exclude-dir=.git
```

7. In `adapter-current` only, finish `encode_record`: `name.strip().lower()`, include `enabled` as `bool`, include `schema` from `SCHEMA_VERSION`. Preserve existing draft notes/comments.

8. Review change:
```bash
git -C case03/checkouts/adapter-current diff
git -C case03/checkouts/adapter-current status --short
```

9. Validate from task checkout with project check:
```bash
git -C case03/checkouts/adapter-current status --short --branch
./case03/checkouts/adapter-current/project-check
```
Use repo-documented check path; must pass before commit.

10. Commit on `task/adapter` only:
```bash
git -C case03/checkouts/adapter-current add -p
git -C case03/checkouts/adapter-current commit -m "Finish encode_record"
git -C case03/checkouts/adapter-current log --oneline -2
git -C case03/checkouts/adapter-current branch --show-current
```

11. Leave ready for review, no integration/publishing:
```bash
git -C case03/checkouts/adapter-current worktree list --porcelain -z
git -C case03/checkouts/adapter-current status --short --branch
```
Do not: `merge/rebase/push/prune/remove`, do not touch integration target, do not use `adapter-old`.

