## Why `-d` refuses

Squash-merging writes a **brand-new commit** on `main` whose *tree* equals your branch's tree, but whose *parentage* does not include your branch's commits. `git branch -d` checks ancestor relationships (via `--merged`), so it correctly sees `task/export` as "not merged." That's expected — it's not evidence your work is missing.

## Verification, in order

Run these from anywhere in the repo (you don't need the old checkout; the branch ref still exists):

```bash
# 1. Get an up-to-date main
git fetch origin --prune
git switch main
git pull --ff-only

# 2. Find the squash-merge commit on main
git log --oneline --grep="export" main
# or, better, by PR number:
gh pr list --state merged --head task/export
git log --oneline --grep="#<PR_NUMBER>" main

# 3. Inspect that commit — it should contain your changes
git show --stat <squash_sha>

# 4. Confirm your branch tip = the pre-squash commits (expected)
git rev-parse task/export
git log --oneline main..task/export        # pre-squash commits only
git merge-base main task/export            # where branch diverged

# 5. Cross-check that the branch's footprint matches the squash commit
git diff --stat $(git merge-base main task/export)..task/export
# ^ file list / line counts should match step 3's --stat

# 6. Content equivalence between branch tip and main
git diff main task/export --stat
# Empty = identical trees. If non-empty, it should only show main's
# *newer* commits since the merge — never files from your branch.
```

Optional modern helper:

```bash
git cherry -v main task/export
```

Caveat: `git cherry` matches by patch-id, so with a multi-commit branch squashed into one commit it will typically show `+` (looks unapplied) even when everything landed. Treat `+` as a prompt to do steps 3–6, not as proof of non-integration.

## When `-D` is acceptable

Run `git branch -D task/export` only after all of these hold:

1. The squash commit is reachable from `main` / `origin/main` (step 2).
2. Its stat matches your branch's diff stat (steps 3–5).
3. `git diff main task/export` shows nothing attributable to the branch (step 6).
4. `git log main..task/export` contains only the commits you recognize as the pre-squash ones (nothing unpushed that you'd lose).

If you want a safety net before deleting, record the tip:

```bash
git rev-parse task/export > /tmp/task-export-tip.txt
# or
git tag archive/task-export task/export
```

Then:

```bash
git branch -D task/export
git branch -a | grep export   # confirm gone locally and remotely
```

`-D` is **not** acceptable when steps 2–6 show gaps — e.g., the squash commit is missing (someone force-pushed `main` or merged a different branch), or `git diff main task/export` shows branch files as missing from `main`. In those cases investigate before force-deleting.

Note: even after `-D`, the commits survive in the reflog (~30–90 days) and can be recovered via `git fsck --lost-found`, so a mistake is recoverable — but verify first regardless.
