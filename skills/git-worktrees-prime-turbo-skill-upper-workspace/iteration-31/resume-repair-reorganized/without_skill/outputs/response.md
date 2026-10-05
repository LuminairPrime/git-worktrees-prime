In `case03/checkouts/adapter-current`, on `task/adapter`:

1. Confirm relocated checkout:
```bash
pwd
git rev-parse --show-toplevel
git status
git branch --show-current
git log --oneline -3
# expected: .../case03/checkouts/adapter-current, branch task/adapter
# do not use adapter-old
```

2. Confirm schema worker done, do not change branches:
```bash
cat ../../worker-status.json
# or: cat ../worker-status.json / worker-status.json in workspace root
git branch -a | grep -E "schema/prep|task/adapter"
git log --oneline -3 schema/prep
git show schema/prep --stat
```

3. Locate current work without touching drafts:
```bash
git status --short
grep -rn "encode_record\|SCHEMA_VERSION" --include="*.py" .
ls -la
# note untracked/draft notes files to keep
```

4. Read schema result to reuse:
```bash
git show schema/prep:worker-status.json
git show schema/prep -- <schema file from step 3>
```

5. Finish `encode_record` only, keep draft notes:
- `name.strip().lower()`
- `enabled` as `bool`
- `schema` from `SCHEMA_VERSION`
- no delete of draft/notes files, no `git clean`, no `git checkout .`

6. Verify only intended file changed:
```bash
git status --short
git diff -- <adapter file>
```

7. Validate with project check:
```bash
cat Makefile package.json README.md 2>/dev/null | grep -i -A2 check
make check
# or project-defined: pytest / npm test - run as documented, must pass
```

8. Commit on `task/adapter`:
```bash
git branch --show-current
git add <adapter file>
git commit -m "Finish encode_record: normalize name, bool enabled, schema version"
git status
git log --oneline -2
```

9. Leave ready for review, no integration/publishing:
```bash
pwd
git branch --show-current
git status --short
# stay in adapter-current on task/adapter
# do not: merge/rebase, switch branch, push, PR, publish, integrate schema/prep
```

