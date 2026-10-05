I would run exactly the following from the workspace root:

```bash
cd /tmp/skill-up-3322275580/case03/checkouts/adapter-current

pwd
git status --short --branch
git branch --show-current
cat worker-status.json
```

Confirm:

- `worker-status.json` reports the schema worker as complete on `schema/prep`.
- The checkout is the moved adapter checkout, not `adapter-old`.
- The current branch is `task/adapter`; if it is not, run:

```bash
git switch task/adapter
```

Locate the adapter implementation and schema constant:

```bash
git grep -n "def encode_record"
git grep -n "SCHEMA_VERSION"
```

Open the reported adapter file:

```bash
${EDITOR:-vi} path/from/grep/to/adapter/file
```

Finish `encode_record` so that its returned record has, with existing input/field names otherwise preserved:

```python
{
    "name": name.strip().lower(),
    "enabled": bool(enabled),
    "schema": SCHEMA_VERSION,
}
```

Do not remove or rewrite the existing draft-note comments. If `SCHEMA_VERSION` is not already imported or defined in that module, add the existing import/reference indicated by `worker-status.json`; do not merge or publish `schema/prep`.

Check the edit:

```bash
git diff --check
git diff
```

The diff should show only the `encode_record` changes/import addition while the draft notes remain unchanged. Run the project’s designated check, for example:

```bash
if [ -x ./check.sh ]; then
  ./check.sh
elif [ -f Makefile ] && grep -q '^check:' Makefile; then
  make check
else
  python -m pytest -q
fi
```

Then commit only the adapter source change:

```bash
git add path/from/grep/to/adapter/file
git commit -m "Finish adapter record encoding"
git status --short --branch
git log --oneline -3
git branch --show-current
```

End state should be:

- working tree clean or containing only unrelated pre-existing untracked files,
- current branch `task/adapter`,
- new commit containing only the completed `encode_record`,
- no merge, push, integration, or publishing commands run.
