Run this from the parent workspace; do not use `adapter-old`.

```bash
cd case03/checkouts/adapter-current

# Confirm location, branch, and pre-existing changes
pwd
git branch --show-current
git status --short --branch

# Confirm the completed schema worker and matching branch commit
python -m json.tool worker-status.json
git branch --list task/adapter schema/prep
git log -1 --format='%H %s' schema/prep

# Locate the work to finish and the schema constant
grep -RIn -- 'def encode_record' .
grep -RIn -- 'SCHEMA_VERSION' .
git grep -n 'SCHEMA_VERSION' schema/prep -- .
```

Check that:

- `pwd` ends with `case03/checkouts/adapter-current`
- `git branch --show-current` reports `task/adapter`
- `worker-status.json` reports the schema worker as complete on `schema/prep`
- the `schema/prep` commit in `worker-status.json` matches `git log`
- the checkout contains the same `encode_record` draft notes recorded before the move

If the branch is not already correct:

```bash
git switch task/adapter
```

Locate and edit the adapter module:

```bash
FILE=$(grep -Rsl 'def encode_record' --include='*.py' . | head -n 1)
printf '%s\n' "$FILE"
${EDITOR:-vi} "$FILE"
```

Make the minimal body change while retaining all existing comments, docstrings, TODOs, and draft notes:

```python
return {
    "name": record["name"].strip().lower(),
    "enabled": bool(record["enabled"]),
    "schema": SCHEMA_VERSION,
}
```

Use the existing `SCHEMA_VERSION` import if one is present. If it is unavailable on `task/adapter` but defined by the completed `schema/prep` result, make the corresponding import/constant available in the adapter source using the project’s existing pattern. Do not merge or switch to `schema/prep`.

Then validate:

```bash
python -m py_compile "$FILE"
```

Run the project’s documented check command and require exit status `0`—for a Python project check, normally:

```bash
python check.py
```

Review the exact edit before staging:

```bash
git diff -- "$FILE"
```

Confirm that only normalization, boolean conversion, and the schema field changed and that the draft notes remain. Then commit on the existing adapter branch:

```bash
git add "$FILE"
git commit -m "Finish adapter encode_record"

git status --short --branch
git log -1 --format='%H %s'
```

Expected final state: branch `task/adapter`, clean working tree, the project check passed before commit, and the checkout at `case03/checkouts/adapter-current` remains ready for review. Do not merge, publish, tag, or `git push`.
