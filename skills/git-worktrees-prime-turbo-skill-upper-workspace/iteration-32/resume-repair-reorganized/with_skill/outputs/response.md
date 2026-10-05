Run this sequence from the parent directory of `case03`:

```bash
cd case03/checkouts/adapter-current || exit 1

pwd
git branch --show-current
git status --short --branch
git log --oneline --decorate -5

cat worker-status.json
python -m json.tool worker-status.json

git branch -a --list '*schema/prep*'
git log --oneline --decorate -5 schema/prep
git merge-base --is-ancestor schema/prep HEAD && echo "schema/prep already present" || git merge --no-edit schema/prep
# if the merge conflicts, resolve only the schema/adapter conflicts, then:
# git add <resolved-files>
# git merge --continue

git grep -n "SCHEMA_VERSION"
git grep -n "def encode_record"
git grep -n "encode_record"

git status --short
git diff --stat
```

Edit only the `encode_record` body. Preserve the existing draft-notes behavior/variables; change the record payload to have:

```python
name = str(record.get("name", "")).strip().lower()
enabled = bool(record.get("enabled", False))
# keep existing draft notes exactly as before

return {
    # ...existing draft-notes fields/object construction...
    "name": name,
    "enabled": enabled,
    "schema": SCHEMA_VERSION,
}
```

Then validate and inspect before committing:

```bash
git diff -- <adapter-file-containing-encode_record>

# Use the project’s documented check only; examples:
ls Makefile package.json pyproject.toml scripts 2>/dev/null
make check        # if the repo exposes a check target
# or: npm run check / pnpm check / pytest / ./scripts/check.sh
```

Commit on `task/adapter`, stage only intended files, and leave the tree clean:

```bash
git status --short
git add <adapter-file-containing-encode_record> <any other intended files>
git diff --cached --stat
git commit -m "Complete encode_record with normalized name, boolean enabled, and schema version"

git status --short --branch
git log --oneline --decorate -5
```

Do not run `git push`, do not merge `task/adapter` into main/master, and do not delete or move this checkout; leave `case03/checkouts/adapter-current` on `task/adapter` with a passing project check and a clean working tree.
