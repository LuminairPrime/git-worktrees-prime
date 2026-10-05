Short answer: **not yet.** `-d` refused because the branch tip is not an ancestor of the target — which is exactly what a squash merge produces. That refusal is not evidence the work is missing, but it's also not evidence it's present. Verify content, then decide.

## Why `-d` refuses (and why its success wouldn't prove anything either)

A squash merge writes a **new commit** whose patch equals the branch's combined changes but whose ancestry does **not** contain the branch. So `git merge-base --is-ancestor task/export main` is false, and `-d` blocks. Conversely, if `-d` had succeeded, that would only mean the branch tip is merged into its **upstream** — not necessarily your intended integration target. Do the checks below regardless.

## Checks, in order

Run from any surviving checkout (the branch's checkout is already gone; that's fine — you're only touching the branch ref).

**1. Confirm the branch still exists and nothing else holds it; capture the tip.**

```sh
git -C <repo> worktree list --porcelain -z
git -C <repo> show-ref --verify --quiet refs/heads/task/export && echo "branch present"
tip=$(git -C <repo> rev-parse refs/heads/task/export)
echo "$tip"
```

**2. Fetch and resolve the real integration target (don't assume `main`).**

```sh
git -C <repo> fetch <remote> --prune
target=$(git -C <repo> rev-parse --verify <remote>/main^{commit})
```

**3. Document the ancestry result (explains the refusal; nonzero is expected for a squash).**

```sh
git -C <repo> merge-base --is-ancestor "$tip" "$target"; echo "exit=$?"
```

**4. Locate the squash commit that landed this task.**

```sh
git -C <repo> log --oneline --decorate --grep='task/export' "$target"
git -C <repo> log --oneline -20 "$target"        # if the message isn't named after the branch
```

**5. See what the branch actually introduced, relative to its merge base.**

```sh
base=$(git -C <repo> merge-base "$target" "$tip")
git -C <repo> diff --stat "$base" "$tip"
paths=$(git -C <repo> diff --name-only "$base" "$tip")
```

**6. Prove the squash captured that content — compare the branch tip against the squash commit, scoped to the touched paths.**

```sh
git -C <repo> diff "$tip" <squash-sha> -- $paths
```

Empty output means the integrated tree matches the branch exactly for everything the branch touched. Then confirm the changes are really on the target:

```sh
git -C <repo> diff "$target" "$tip" -- $paths   # inspect any remaining delta
```

Non-empty output is the moment to stop: it means either conflict resolution diverged, or part of the branch never landed. Investigate before deleting.

**7. (Only if you can't identify one squash commit.)** Inspect the full delta and reconcile each hunk by hand; do not treat "main looks like it has it" as proof:

```sh
git -C <repo> diff "$target" "$tip"
```

## When `-D` is acceptable

Use `-D` only when at least one is true, and you own the branch / no review still needs it:

- **Verified integration:** step 6 shows the branch's changes are all present in the target (possibly plus unrelated main-side drift). The obsolete history is confirmed safe to drop.
- **Preserved elsewhere:** the tip is anchored under another durable ref before deletion, e.g.
  ```sh
  git -C <repo> tag archive/task/export "$tip"
  # or push to a backup ref
  git -C <repo> push <remote> "refs/heads/task/export:refs/heads/archive/task-export"
  ```
- **Explicitly authorized abandonment:** the user accepts losing the un-integrated work.

If none hold, keep the branch. Removing the branch is a separate decision from removing the checkout (already done).

## Then, and after

```sh
git -C <repo> branch -D task/export
git -C <repo> worktree prune --dry-run --verbose   # only if stale registrations from the removed checkout exist
git -C <repo> worktree list --porcelain -z
```

Before pruning, review every dry-run entry and require that each one is the checkout you intentionally removed — a missing directory may just be offline storage, not a deletion.

**Bottom line:** `-D` is fine here *only* after step 6 (or a preserved backup tag/ref, or explicit permission). `-d` refusing by itself tells you nothing about the squash; verify by comparing the branch tip to the squash commit over the touched paths.
