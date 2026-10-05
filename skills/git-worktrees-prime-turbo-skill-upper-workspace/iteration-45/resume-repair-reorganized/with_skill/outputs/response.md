Here is the exact sequence I would run, in order, from the workspace root. Nothing merges, pushes, or publishes; the checkout stays where it is now.

## Phase 1 — Re-anchor the moved checkout

```bash
# 1. Locate the main repo and confirm the checkout's recorded path
git -C <main-repo> worktree list
```

Expect a line pointing at the old `case03/checkouts/adapter-old`. Because the directory moved, the worktree registration and the checkout's `.git` gitdir pointer both reference the dead path.

```bash
# 2. Repair the registration from the moved checkout itself
cd case03/checkouts/adapter-current
git worktree repair
```

```bash
# 3. Verify the checkout is healthy and on the right branch
git rev-parse --abbrev-ref HEAD     # must print: task/adapter
git status --porcelain              # note existing dirty files (draft notes)
git worktree list                   # must now show .../adapter-current
```

Check: HEAD is `task/adapter` (not detached), the path is updated, and the pre-existing dirty entries are exactly the draft notes / in-progress `encode_record` work — do **not** discard them, no `git checkout -- .`, no `git stash`.

## Phase 2 — Read the schema worker result (read-only, no integration)

```bash
# 4. Confirm the worker is actually complete
git show schema/prep:worker-status.json     # or cat worker-status.json if it sits in the workspace
```

Check: status field = complete/success; extract `SCHEMA_VERSION` and the schema payload.

```bash
# 5. Inspect the result branch without switching to it
git log --oneline -3 schema/prep
git show schema/prep --stat
```

Do **not** check out `schema/prep` in this checkout and do **not** merge or rebase it into `task/adapter` — the value is transcribed, not integrated.

## Phase 3 — Finish `encode_record`

```bash
# 6. Open the current implementation and the draft notes
git diff                     # shows in-progress encode_record edits
```

Apply the three changes:

1. `name`: trim + lowercase (`name.trim().toLowerCase()` / `.strip().lower()` per language).
2. `enabled`: emitted as a real boolean (coerce, don't pass through a string/0-1).
3. `schema`: emitted from `SCHEMA_VERSION` exactly as reported by `worker-status.json` on `schema/prep`.

```bash
# 7. Leave the draft notes untouched
git status --porcelain       # draft-notes entry still present, unmodified
```

Check: the notes file was neither edited nor deleted. If it is tracked and already part of this task's change set, it rides along in the commit; if it is untracked scratch, it stays untracked in the working tree — either way it is kept.

## Phase 4 — Validate

```bash
# 8. Run the project's check (the repo's documented one)
<project check>              # e.g. make check / npm test / pytest — whatever the project defines
```

Check: exit code 0.

```bash
# 9. Inspect exactly what will be committed
git diff --check              # whitespace/conflict-marker errors
git diff --stat
```

Check: only `encode_record` (and the intended test/fixture updates) changed; no unrelated files, no leftover merge state.

## Phase 5 — Commit on `task/adapter`

```bash
# 10. Re-verify branch immediately before committing
git rev-parse --abbrev-ref HEAD          # task/adapter

# 11. Stage only the finished work
git add <encode_record source file> <its test/fixture files>

# 12. Commit
git commit -m "encode_record: normalize name, boolean enabled, schema from SCHEMA_VERSION"
```

```bash
# 13. Post-commit verification
git log --oneline -2
git status --porcelain        # only the intentionally kept draft notes remain
git rev-parse --abbrev-ref HEAD
git worktree list             # still .../case03/checkouts/adapter-current
```

## Phase 6 — Ready for review (stop here)

```bash
# 14. Final state assertions
git log origin/task/adapter..HEAD --oneline   # local-only commits, or upstream not configured yet
git stash list                                # empty — nothing was stashed away
```

Confirm: branch = `task/adapter`, check passed, commit present, draft notes kept, checkout at `adapter-current`, and **no** `git merge`, `git push`, `git rebase`, tag, or release command was run anywhere in the sequence.
