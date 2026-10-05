Don't run `-D` blind. `-d` refuses for a *structural* reason (squash merge records no ancestry), so its refusal proves nothing about your work — but that also means you need real evidence before forcing. Here's the exact sequence I'd run, in order.

## 1. Confirm nothing still holds the branch

```sh
git worktree list --porcelain -z
git branch --list task/export
git status --short --branch
```

You removed the checkout, but a stale registration can survive. Confirm `task/export` is not checked out anywhere and that you're not standing on it (Git refuses to delete the current branch regardless of flag).

## 2. Refresh refs so you compare against current `main`

```sh
git fetch origin --prune
git rev-parse --short HEAD origin/main task/export
```

Verifying against a stale local `main` is the most common way to get a false "not integrated" answer.

## 3. Reproduce and classify the refusal

```sh
git merge-base --is-ancestor task/export origin/main; echo "exit=$?"
```

`exit=1` is *expected* for squash/rebase merges: the branch tip commit was rewritten, so ancestry is gone. This tells you nothing about content.

## 4. Find the squash commit that replaced it

```sh
git log --oneline -20 origin/main
git log --oneline --grep='task/export' -20 origin/main
# If using GitHub/GitLab:
gh pr list --head task/export --state merged
```

Note its hash as `$SQUASH`.

## 5. Verify content, not ancestry (the real check)

```sh
# Strongest single check: branch tip tree vs. the squash commit's tree.
git diff --stat "$SQUASH" task/export        # must be empty

# Also compare against current main (empty unless main advanced after the squash).
git diff --stat origin/main task/export

# What's on the branch that isn't obviously on main:
git log --oneline origin/main..task/export

# Patch-equivalence sweep. Note: after a true squash, individual commit
# patch-ids often MISMATCH (they show '+'), so treat '+' here as "inspect",
# not as "unmerged" — the diff above is authoritative.
git cherry -v origin/main task/export
```

If `git diff "$SQUASH" task/export` is empty, every change on `task/export` is present in `main` at `$SQUASH`, and the leftover commits in `origin/main..task/export` are just the pre-squash originals.

## 6. Confirm the work is recoverable somewhere else

```sh
git ls-remote --heads origin task/export     # still on the remote?
git log -g --oneline task/export | head -20  # reflog as a local safety net (~90 days)
```

Optional belt-and-braces before deleting: `git tag archive/task-export task/export` or `git push origin refs/heads/task/export:refs/heads/archive/task-export`.

## 7. Delete, then verify

```sh
git branch -D task/export                    # -d will STILL refuse; that's normal
git rev-parse --verify refs/heads/task/export   # must fail now
git worktree prune --dry-run --verbose           # review every stale entry
git worktree prune --verbose                      # only if all entries are your removed checkout
git worktree list --porcelain -z
```

Remote branch deletion is a separate, separately-authorized step: `git push origin --delete task/export` — only if no collaborator still needs it.

## When `-D` is acceptable

- Squash, rebase, or cherry-pick integration into the target — ancestry *cannot* be recorded, so `-D` is the only flag that will ever work after verification (your case).
- The branch's tree is identical to the integrating commit (`git diff "$SQUASH" task/export` empty).
- The branch tip is reachable from another durable ref — remote branch, tag, archive, or reflog — so a mistake is still recoverable.
- The branch is task-owned, no review is pending on it, and deletion is within your authority.

## When `-D` is **not** acceptable yet

- `git diff` still shows changes, or `origin/main..task/export` lists commits you can't account for.
- You never located `$SQUASH` — "it looked merged" is not evidence.
- The branch is the *only* copy of the work (unpushed, no tag) — back it up first.
- Review or a pending PR depends on it: a closed/merged-looking PR alone doesn't establish integration.
- The branch is checked out elsewhere, or its owner is someone else.

Two cautions worth keeping: `branch -d` can pass by checking the branch's *upstream* rather than your intended integration target, so even a success isn't proof — and never treat a forced flag as permission. Run steps 1–6, and `-D` goes from "risky shortcut" to "correct tool for a squash merge."
