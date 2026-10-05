Short answer: don't reach for `-D` yet. `git branch -d` (and `-r` merged checks) rely on commit ancestry, and squash-merged commits are **not** ancestors of `main` — the patch landed as a new, different commit. So `-d` refusing is expected and tells you nothing about whether the work is integrated. Verify with patch-equivalence instead.

Run these, in order:

```bash
# 1. Get current state, including remote refs
git fetch origin --prune

# 2. Make sure main is what you think it is
git checkout main
git pull --ff-only origin main

# 3. Locate the squash commit that landed your work
git log --oneline --grep="export" origin/main
# or by PR number:
git log --oneline --grep="#1234" origin/main
```

Step 3 should show a commit on `main` whose message matches your PR/squash message. Note its SHA.

```bash
# 4. Patch-equivalence check: every commit on your branch should be marked '-'
git cherry origin/main task/export
```

- Lines starting with `-` = the same patch already exists on main.
- Any line starting with `+` = that commit's changes are **not** on main.

If any `+` lines appear, stop — the branch still holds unintegrated work.

```bash
# 5. Content sanity check: branch changes vs. the squash commit should match
git show <squash-sha> --format= --patch | git patch-id
git diff $(git merge-base origin/main task/export) task/export | git patch-id
# Same patch-id output (same left/right IDs) means the branch's net diff == the squash commit
```

Optional extras:

```bash
# Remote branch still around as a safety net?
git branch -r | grep export

# Worktree fully pruned (checkout was removed earlier)?
git worktree list
git worktree prune
```

When `-D` is acceptable:

1. `git cherry` shows only `-` lines and you've located the squash commit on main — integration is confirmed, so `git branch -D task/export` loses nothing. (At that point, plain `-d` may *still* refuse due to the ancestry issue — that's fine.)
2. The branch still exists on the remote (`origin/task/export`), so the work is recoverable even if you're wrong. In that case `git push origin --delete task/export` + local `-D` is fine.
3. You deliberately mean to discard the work (abandoned spike, superseded approach).

When it is **not** acceptable: `git cherry` shows `+` commits you don't recognize, you can't find the squash commit on main, or you haven't fetched recently (stale local refs can make a merged branch look unmerged and vice versa — always `fetch` first).

Typical cleanup sequence once verified:

```bash
git branch -D task/export
git push origin --delete task/export   # if the remote branch still exists
git worktree prune
```
