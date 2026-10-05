Neither `/repo` nor any `.worktrees` directory exists in this environment, and the working directory isn't a git repo — so I can't run these checks against your actual worktree. Below is the ordered walkthrough to run yourself in `/repo`.

## Check 1 — Confirm the worktree is registered

```bash
git -C /repo worktree list
```

Look for `/repo/.worktrees/old-task`. This tells you the branch checked out there too. If it's missing from the list but the directory exists, the admin files are stale — skip to step 6.

## Check 2 — Is there any uncommitted or unpushed work?

```bash
git -C /repo/.worktrees/old-task status
git -C /repo/.worktrees/old-task log --oneline main..HEAD
git -C /repo/.worktrees/old-task log --oneline origin/main..HEAD
```

- A dirty tree blocks `git worktree remove` unless you pass `--force`.
- The second and third commands will show commits **even after a squash merge** — that's expected, because squash creates a *new* commit rather than moving your branch. Don't treat this as proof of unmerged work.

## Check 3 — Verify the squash actually landed (the important one)

Because it was squash-merged, the usual signals lie:

```bash
git -C /repo branch --merged main          # will NOT list old-task
git -C /repo merge-base --is-ancestor old-task main   # exits 1
```

Both fail *by design* here. Use tree equality instead — your branch's final tree should match a commit on `main`:

```bash
T=$(git -C /repo rev-parse old-task^{tree})
git -C /repo log --pretty=%T main | grep -qx "$T" && echo "LANDED" || echo "NOT FOUND"
```

Or, if the squash was a PR, just confirm the PR shows merged. Also check nothing is sitting unpushed that you'd lose:

```bash
git -C /repo ls-remote origin old-task
```

## Check 4 — Remove the checkout

```bash
git -C /repo worktree remove /repo/.worktrees/old-task
```

Add `--force` only if check 2 showed modified or ignored-but-tracked files you've confirmed disposable. This deletes the directory but leaves the branch and the admin files.

## Check 5 — Delete the branch

```bash
git -C /repo branch -d old-task
```

**This will refuse** with "not fully merged" — that's the squash, not a mistake. Once check 3 confirmed the tree landed:

```bash
git -C /repo branch -D old-task
```

If the branch is pushed, also delete the remote ref:

```bash
git -C /repo push origin --delete old-task
```

## Check 6 — Prune

```bash
git -C /repo worktree prune -v
```

Prune only clears stale administrative files for worktrees whose directories are *already* gone — it does not delete a live checkout. So it's a no-op if step 4 succeeded, and a fix if the directory was deleted manually. Verify at the end:

```bash
git -C /repo worktree list
git -C /repo branch --list old-task
```

---

**Order matters:** verify (1–3) → remove checkout (4) → delete branch (5) → prune (6). The trap is that `branch -d` refusing after a squash looks like a safety warning but is just ancestry math; the tree check in step 3 is what actually tells you it's safe.
