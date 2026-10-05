**Short answer: not yet — but you don't need to avoid `-D` forever.** `-d` refuses only because a squash merge breaks *ancestry*, not because the work is missing. Run these checks in order, then `-D` is a perfectly safe, normal deletion.

## The verification sequence

**1. Refresh refs so you're judging against the real remote state**
```bash
git fetch origin --prune
git rev-parse --abbrev-ref HEAD
```

**2. Confirm the branch is already gone upstream** (the PR/merge flow deleted it)
```bash
git ls-remote --heads origin task/export
```
Empty output = remote branch deleted. If a SHA comes back, someone (or you) still has it out there — stop and reconcile first.

**3. Make sure `main` is the right target and is current**
```bash
git remote show origin | sed -n '/HEAD branch/p'
git switch main
git pull --ff-only
```

**4. Prove *why* `-d` refused** (expected exit code `1`)
```bash
git merge-base --is-ancestor task/export main; echo "exit=$?"
```
`1` means "not an ancestor" — which is exactly what a squash merge produces: main got one *new* commit containing the combined diff, so your branch tip commit is orphaned by design.

**5. The decisive check — compare the actual content (trees), not commits**
```bash
git diff --exit-code main task/export; echo "exit=$?"
```
* **`exit=0` / no output** → main's tree is byte-for-byte identical to the branch tip. Everything the branch had is on main. This is the proof `-d` wanted and couldn't record.
* **`exit=1`** → something differs. Do **not** delete yet; go to step 6.

**6. See what differs and list the commits you're about to orphan**
```bash
git diff --stat main task/export
git log --oneline main..task/export
git log --oneline $(git merge-base main task/export)..main | head -20
```
If the `main..task/export` commits' *content* shows up in the diff, they're not integrated. If the diff is empty apart from things you intentionally dropped (formatting churn, review fixes applied by hand on main), you're fine.

**7. Locate the squash commit on main for a human-readable confirmation**
```bash
git log --oneline -i --grep='task/export' main
git log --oneline -1 main -- path/that/changed
git show --stat $(git log -1 --format=%H -i --grep='task/export' main)
```

**8. Optional: check it wasn't actually merged somewhere else** (e.g. `develop`)
```bash
git for-each-ref --format='%(refname:short)' refs/remotes/origin |
while read r; do
  git diff --quiet "origin/$r" task/export && echo "IDENTICAL: $r"
done
```

**9. Take out insurance, then delete**
```bash
git rev-parse task/export | tee /tmp/task-export.sha
git tag backup/task-export task/export      # optional, cheap
git branch -D task/export
```

**10. Verify and note the recovery path**
```bash
git branch --list task/export                # empty = gone
git branch task/export "$(cat /tmp/task-export.sha)"   # exact restore
```
The tip SHA lives in your reflog for the usual retention window (~90 days by default), so `-D` is reversible even without the tag.

## When `-D` is acceptable

- `git diff --exit-code main task/export` returns **0** (identical trees), **or** the only differences are changes you deliberately did not carry over.
- The equivalent content shows up as a real commit on main (`git show --stat` on the squash commit).
- The remote branch is already deleted (`ls-remote` empty), so no collaborator is sitting on it.
- You've recorded the tip SHA or made a tag, so the delete is trivially undoable.
- `git log --oneline main..task/export` contains nothing whose content is absent from main.

## When `-D` is *not* acceptable

- The tree diff is non-empty and the missing content is still wanted.
- The branch has follow-up commits made **after** the squash merge (common: you kept pushing to it). Those are not on main — cherry-pick or re-merge them first: `git cherry-pick <sha>...` or `git diff main task/export | git apply`.
- You haven't confirmed which branch it landed in.
- The branch still exists on the remote, or is the only copy of work someone else needs.

## One caveat worth knowing

Don't use `git cherry main task/export` or `git log --cherry-mark` as your evidence here. They compare **patch-ids per commit**, and a squash merge collapses N commits into 1 whose patch-id matches none of them — so they'll report every branch commit as unmerged (`+`) even when all the content is on main. `git diff` on the trees (step 5) is the check that actually answers the question.

For the future: if you want `-d` to work after a squash merge, either keep the branch until you've verified (as above), or avoid squash merges when the branch is disposable — a real merge or a rebase-based merge records the ancestry `-d` looks for.
