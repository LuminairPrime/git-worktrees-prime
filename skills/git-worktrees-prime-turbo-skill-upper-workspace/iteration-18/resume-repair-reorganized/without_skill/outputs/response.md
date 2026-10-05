In `case03/checkouts/adapter-current`, in order:

```sh
cd case03/checkouts/adapter-current
pwd
git worktree list
git branch --show-current
# expected: task/adapter
git status --short --branch
ls case03/checkouts/adapter-old || echo "old path gone, using adapter-current"

cat worker-status.json
# check: schema worker complete on schema/prep

git fetch origin schema/prep
git log --oneline -3 schema/prep
git show schema/prep:SCHEMA_VERSION
cat SCHEMA_VERSION

grep -rn "def encode_record" --include="*.py" .
grep -rn "SCHEMA_VERSION" --include="*.py" .

# finish encode_record in place:
# name = name.strip().lower()
# enabled = bool(enabled)
# schema = SCHEMA_VERSION
# keep existing draft notes file untouched

git status --short
git diff --name-only
git diff -- draft_notes NOTES.md 2>/dev/null || true
# check: draft notes unmodified

./project-check
# or: make check / pytest / npm test - use project check
# must pass

git add <adapter encode_record file> SCHEMA_VERSION
git status --short
git commit -m "Finish encode_record: normalize name, bool enabled, schema version"
git log --oneline -2
git branch --show-current
git status --short --branch
# leave on task/adapter in adapter-current, ready for review
# stop: no merge, no integration, no push/publish
```
