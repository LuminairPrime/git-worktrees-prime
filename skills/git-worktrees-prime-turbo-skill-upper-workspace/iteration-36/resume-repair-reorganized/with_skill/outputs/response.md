Run this sequence from the workspace root:

```bash
cd case03/checkouts/adapter-current
pwd
git rev-parse --show-toplevel
git status --porcelain --branch
git branch --show-current
```

Confirm that the checkout is `adapter-current`, not `adapter-old`, and note whether there are uncommitted draft notes.

Ensure the adapter task branch is active. Do not discard local changes:

```bash
git switch task/adapter
git branch --show-current
git status --porcelain --branch
```

Review the completed schema worker result:

```bash
cat worker-status.json
python -m json.tool worker-status.json
```

Verify it records the schema worker as complete on `schema/prep`, then copy its `SCHEMA_VERSION` value/reference.

Locate the adapter and schema-version definitions:

```bash
grep -RIn --exclude-dir .git 'def encode_record' .
grep -RIn --exclude-dir .git 'SCHEMA_VERSION' .
```

Open the reported adapter file:

```bash
${EDITOR:-vi} <adapter-file>
```

Edit only the body/implementation of `encode_record`; keep the existing draft notes intact. The result should normalize the name, preserve `enabled` as a Boolean, and use the worker-provided schema version, for example:

```python
def encode_record(record):
    # Existing draft notes remain here.

    name = str(record.get("name", "")).strip().lower()

    raw_enabled = record.get("enabled", False)
    if isinstance(raw_enabled, str):
        enabled = raw_enabled.strip().lower() in {"1", "true", "yes", "on"}
    else:
        enabled = bool(raw_enabled)

    return {
        "name": name,
        "enabled": enabled,
        "schema": SCHEMA_VERSION,
    }
```

If `SCHEMA_VERSION` is not already available in that file, add the appropriate import/reference from the completed schema worker near the other imports; do not merge `schema/prep`.

Review the change:

```bash
git diff -- <adapter-file>
```

Check that:

- `name` is stripped and lowercased.
- `enabled` is converted to a Boolean.
- `"schema"` comes from `SCHEMA_VERSION`.
- The existing draft notes have not been removed or overwritten.
- No schema branch integration or publication changes were made.

Run the project’s existing check command. First confirm the configured target:

```bash
grep -nE '^check:|"check"[[:space:]]*:' Makefile package.json pyproject.toml 2>/dev/null
```

Most likely:

```bash
make check
```

If the project defines a different check command, run that exact command instead. Do not substitute an ad-hoc test command.

Stage only the intended adapter/schema reference changes:

```bash
git add <adapter-file>
git diff --cached -- <adapter-file>
git commit -m "Finish encode_record normalization and schema tagging"
```

Leave the checkout on `task/adapter`, with the working tree clean:

```bash
git status --porcelain --branch
git branch --show-current
git log -1 --stat
```

Do not merge `schema/prep`, integrate with other branches, or publish.
