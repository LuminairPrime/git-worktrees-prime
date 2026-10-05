Below is the exact sequence I'd run, in order, entirely inside the reorganized checkout — no filesystem hunting, no `adapter-old`, no merge/push at the end. Each step has an explicit stop condition.

## Phase 0 — Confirm the checkout's new location

```bash
# 1. The checkout must be at the new path; fail hard if it isn't.
test -d case03/checkouts/adapter-current/.git || { echo "STOP: adapter-current missing"; exit 1; }

# 2. Warn only (don't use) if the stale path still exists.
test -e case03/checkouts/adapter-old && echo "WARN: stale adapter-old still present"

cd case03/checkouts/adapter-current
```

**Stop** if `adapter-current` doesn't exist — do not fall back to `adapter-old`.

## Phase 1 — Confirm branch state and inputs

```bash
# 3. Clean worktree, no in-progress operation, right branch.
git status --porcelain=v1
test -f .git/MERGE_HEAD -o -d .git/rebase-merge -o -d .git/rebase-apply && { echo "STOP: op in progress"; exit 1; }
git branch --show-current        # expect: task/adapter
```
**Check:** worktree clean, no merge/rebase in flight. If HEAD is on another branch or detached, `git switch task/adapter` (create with `git switch -c task/adapter` only if the branch genuinely doesn't exist: `git show-ref --verify refs/heads/task/adapter`).

```bash
# 4. Read the schema worker's status (path checked in order, no broad search).
for f in worker-status.json ../../worker-status.json ../worker-status.json; do test -f "$f" && { echo "$f"; break; }; done
jq . worker-status.json          # or: cat worker-status.json
```
**Check:** schema worker `status == complete`, source ref `schema/prep`, and note the result artifact path/commit it points to.

```bash
# 5. Verify schema/prep exists and inspect its result.
git rev-parse --verify schema/prep
git log --oneline -3 schema/prep
git show --stat schema/prep
git show schema/prep:<result-path-from-worker-status.json>
```
**Check:** the worker result actually defines what `encode_record` needs (schema field name / `SCHEMA_VERSION` value).

```bash
# 6. Locate the code to edit and confirm SCHEMA_VERSION exists on task/adapter.
grep -rn "encode_record" . --exclude-dir=.git
grep -rn "SCHEMA_VERSION" . --exclude-dir=.git

# 7. Locate the draft notes so they can be preserved.
git ls-files | grep -i note
```
**Check:** `encode_record` found; draft notes file identified and its path recorded (it must survive unchanged). **Stop** if `SCHEMA_VERSION` is not defined anywhere on `task/adapter` — in that case add it as a literal taken from the `schema/prep` result (a value, not a merge).

## Phase 2 — Implement `encode_record`

```bash
# 8. Edit only the encode_record file (editor of choice), making exactly:
#      name    -> .strip() then .lower()
#      enabled -> boolean (coerce/validate, not a string/int)
#      schema  -> SCHEMA_VERSION (the value confirmed in step 6)
```

**Check:** the draft notes file is *not* in the edit set.

## Phase 3 — Validate with the project check

```bash
# 9. Identify the project's canonical check from committed metadata only.
git ls-files | grep -E '(^|/)(package.json|Makefile|pyproject.toml|tox.ini|go.mod|Cargo.toml)$'

# 10. Run that check and require exit 0.
npm run check        # or: make check / pytest / go test ./...  — whichever the project defines
git diff --check     # whitespace/conflict-marker hygiene
```
**Check:** all exit 0. If a test targets `encode_record` specifically, confirm it exercises name normalization, boolean `enabled`, and `schema`.

## Phase 4 — Stage and commit on `task/adapter`

```bash
# 11. Review before staging: only the intended file(s) changed, notes untouched.
git status --porcelain=v1
git diff
git diff --stat

# 12. Stage ONLY the implementation file(s) — never the draft notes.
git add <path/to/encode_record-file>
git diff --cached --stat
git status --porcelain=v1        # staged set must match intent exactly

# 13. Commit on the task branch.
git branch --show-current          # must print: task/adapter
git commit -m "encode_record: strip/lowercase name, boolean enabled, add schema from SCHEMA_VERSION"
```

## Phase 5 — Leave this checkout review-ready

```bash
# 14. Post-commit verification.
git log -1 --stat
git branch --show-current          # task/adapter
git status --porcelain=v1          # empty = clean
```

**Checks:** commit exists on `task/adapter`; worktree clean; `git show HEAD` contains only the `encode_record` change; draft notes still present and unmodified in the working tree and history.

## Explicitly NOT run (no integration, no publishing)

```bash
# git switch main / git merge task/adapter   # no integration
# git push / git tag / npm publish / gh pr   # no publishing
```

Final state: `case03/checkouts/adapter-current`, branch `task/adapter`, clean, one new commit, schema result consumed from `schema/prep` as data — `schema/prep` itself is left unmerged.
