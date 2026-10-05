Run these in order, all from the resumed checkout:

```bash
cd case03/checkouts/adapter-current
pwd
git branch --show-current
git status --short --branch
cat worker-status.json
git rev-parse --verify schema/prep
git show --stat --oneline schema/prep
grep -R --line-number "def encode_record" .
grep -R --line-number "SCHEMA_VERSION" .
```

Checks: `pwd` ends with `case03/checkouts/adapter-current`, not `adapter-old`; branch is `task/adapter` or switch with `git checkout task/adapter`; `worker-status.json` shows the schema worker complete on `schema/prep`; locate the single adapter file defining `encode_record` and the `SCHEMA_VERSION` definition/import.

Edit only that function body, preserving existing draft notes/comments:

```python
def encode_record(name, enabled):
    # existing draft notes stay here unchanged
    return {
        "name": name.strip().lower(),
        "enabled": bool(enabled),
        "schema": SCHEMA_VERSION,
    }
```

Then review and validate:

```bash
git diff
grep -R --line-number "def encode_record" .
cat worker-status.json
git rev-parse --verify schema/prep
# Discover the documented project check from the repo metadata, e.g. Makefile/README/package scripts,
# then run exactly that project check command and require it to pass.
```

If the project check passes:

```bash
git add <adapter-file>
git commit -m "Finish adapter encode_record"
git status --short --branch
git log --oneline -1
```

Stop there: do not merge `schema/prep`, do not publish, do not push, do not create a PR, and leave the working directory at `case03/checkouts/adapter-current` on `task/adapter` with a clean tree except any expected ignored files.
