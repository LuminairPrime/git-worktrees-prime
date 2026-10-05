Since I can't inspect the actual tree, here is the exact command sequence I would run, in order, from the checkout:

```bash
cd case03/checkouts/adapter-current

# 1. Confirm checkout identity and branch state
git -C . rev-parse --show-toplevel
git status --short
git branch --show-current          # expect: task/adapter (or switch to it)
git branch                         # confirm task/adapter exists

# 2. Read the schema worker's recorded result
cat worker-status.json            # confirm schema/prep is "complete"/"done"
# and read the result path/branch it references, e.g.:
git log --oneline -5 schema/prep   # or the commit/branch named in worker-status.json

# 3. Apply the completed schema result to this checkout
git merge schema/prep             # or: git cherry-pick <sha from worker-status.json>
                                  # or however the workspace convention records it
git status                        # resolve any conflicts, then git add/git merge --continue

# 4. Finish encode_record in the adapter module (exact file per worker-status.json / repo)
#    e.g.:
$EDITOR <adapter-module>.py        # or .ts/.js — the file defining encode_record

# Requirements for encode_record:
#   - name: value.strip().lower()
#   - enabled: bool coercion of the source value
#   - schema: taken from SCHEMA_VERSION constant
#   - keep the existing draft notes/comments untouched

# 5. Sanity-check the edit
git diff                          # review only encode_record body + schema merge
grep -n "SCHEMA_VERSION" -r .     # confirm the source of schema

# 6. Validate with the project's check command
#    run whichever the repo defines, typically one of:
python -m pytest -q              # or: npm test / make check / ./scripts/check.sh
# Confirm encode_record tests pass and no regressions

# 7. Stage and commit on task/adapter
git add -A
git status                        # verify only intended files
git commit -m "adapter: finish encode_record (normalize name, bool enabled, schema from SCHEMA_VERSION)"

# 8. Leave the checkout ready for review
git status                        # clean
git log --oneline -3              # shows the new commit on task/adapter
git branch --show-current         # task/adapter

# Explicitly NOT done:
#   - no merge of task/adapter into main/develop
#   - no push / publish / release
```

If `worker-status.json` indicates the schema result should be vendored as a file rather than merged (e.g., a `SCHEMA_VERSION.json` or generated module), step 3 becomes copying that artifact into the checkout and `git add`ing it before step 4 — the rest of the sequence is unchanged.
