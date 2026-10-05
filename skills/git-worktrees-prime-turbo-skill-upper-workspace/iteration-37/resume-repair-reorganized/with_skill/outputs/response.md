Run this sequence from the current checkout:

```bash
cd /tmp/skill-up-3726911139/case03/checkouts/adapter-current

git status --porcelain --branch
git branch --show-current          # expect: task/adapter
cat worker-status.json             # confirm schema/prep is complete/passed

# Use the worker result, but do not merge/rebase/publish from schema branches.
rg -n "SCHEMA_VERSION|schema/prep|encode_record|draft|notes|TODO" .

# Edit only the encode_record implementation/helper comments where needed.
# Required behavior:
#   name = str(record.get("name", "")).strip().lower()
#   enabled = bool(record.get("enabled"))
#   include "enabled": enabled as a real boolean
#   include "schema": SCHEMA_VERSION
# Preserve all existing draft notes/comments and any other fields/behavior.

git diff
```

Then validate with the project check entrypoint:

```bash
if [ -x ./check.sh ]; then
  ./check.sh
elif [ -f Makefile ] && make -pn | grep -q '^check:'; then
  make check
elif [ -f package.json ]; then
  npm run check
else
  python3 -m pytest -q
fi
```

Commit and leave ready:

```bash
git add -A
git commit -m "Finish encode_record using schema/prep result"
git status --porcelain --branch
git log --oneline --decorate -3
```

Do **not** run `git push`, `git merge`, `git rebase`, `git worktree`, `npm publish`, or any schema integration step. Do not use `adapter-old` and do not move this checkout.
