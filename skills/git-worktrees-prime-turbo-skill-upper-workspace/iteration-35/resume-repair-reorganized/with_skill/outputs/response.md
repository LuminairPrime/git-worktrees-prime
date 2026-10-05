1. Enter the current checkout:

```bash
cd case03/checkouts/adapter-current
pwd
git status --porcelain --branch
git branch --show-current
```

2. Confirm branch and schema worker result; it must still be `task/adapter` and schema must be complete:

```bash
git checkout task/adapter
cat worker-status.json
git branch --list schema/prep
git show --stat --oneline -1 schema/prep
```

Check that `worker-status.json` says the schema worker is complete and that `schema/prep` contains the new `SCHEMA_VERSION`.

3. Locate the constant and adapter entry point:

```bash
git grep -n "SCHEMA_VERSION" schema/prep --
grep -R "encode_record" -n .
```

4. Edit the file containing `encode_record`. Preserve the existing draft notes and make the implementation effectively:

```python
def encode_record(record):
    # existing draft notes preserved here
    name = str(record["name"]).strip().lower()

    enabled = record["enabled"]
    if isinstance(enabled, str):
        enabled = enabled.strip().lower() in {"1", "true", "yes", "on"}
    else:
        enabled = bool(enabled)

    return {
        "name": name,
        "enabled": enabled,
        "schema": SCHEMA_VERSION,
    }
```

If `SCHEMA_VERSION` is not already imported in that module, add the existing import used elsewhere in the project; do not hardcode the schema string.

5. Review the change:

```bash
git diff -- <adapter-file>
git diff --check
```

6. Run the project’s documented check command exactly as configured in the checkout, then verify no TODO/draft body remains in `encode_record` except the preserved notes:

```bash
<project-check-command>
grep -R "encode_record" -n .
```

7. Commit only the adapter change on `task/adapter`:

```bash
git add <adapter-file>
git commit -m "Finish encode_record adapter encoding"
```

8. Verify the checkout is ready for review and unchanged otherwise:

```bash
git status --porcelain --branch
git branch --show-current
git log -1 --stat
```

Do not merge `schema/prep`, push, tag, publish, or switch to another checkout.
