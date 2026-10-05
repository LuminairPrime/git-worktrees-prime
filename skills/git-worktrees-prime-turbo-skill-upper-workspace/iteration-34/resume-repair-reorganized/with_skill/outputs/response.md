Repair the moved checkout first, then read the worker result, finish the code, validate, and commit. All commands run against the existing checkout — no new worktree, no merge, no push.

## 0. Identify the repository and repair the moved registration

The checkout physically moved from `adapter-old` to `adapter-current`, but Git's registration still points at the old path, so **`git worktree repair` must run before any development**.

```sh
# Inventory: see the stale adapter-old registration and the actual branch/paths.
git -C "case03" worktree list --porcelain -z

# Reconnect the live checkout at its current absolute path (run from the primary repo/bare repo).
git -C "case03" worktree repair "$PWD/case03/checkouts/adapter-current"

# Re-list to verify adapter-current is now the registered path and adapter-old is gone.
git -C "case03" worktree list --porcelain -z
```

Check: `adapter-current` appears with branch `task/adapter` and the correct HEAD; the old `adapter-old` entry is no longer the live path. Do **not** prune, move, delete, or recreate the checkout to fix this.

## 1. Confirm the checkout, branch, and current state

```sh
git -C "case03/checkouts/adapter-current" rev-parse --show-toplevel
git -C "case03/checkouts/adapter-current" status --short --branch
git -C "case03/checkouts/adapter-current" rev-parse HEAD
```

Check: top-level is the adapter-current path; branch is `task/adapter` (not detached); the existing draft notes are present and uncommitted/committed as expected; no unfinished Git operation is in progress (no `MERGE_HEAD`, `rebase-merge`/`rebase-apply`, or `CHERRY_PICK_HEAD`). Do not stash, reset, or copy in changes from elsewhere.

## 2. Read the completed schema worker result

Use the manager inventory for the worker's checkout; if `worker-status.json` is tracked on `schema/prep`, read it without needing the checkout path:

```sh
git -C "case03" show schema/prep:worker-status.json
# or, from the worker checkout named in the inventory:
cat "case03/checkouts/<schema-prep-checkout>/worker-status.json"
```

Extract: confirmation the worker is complete, the `SCHEMA_VERSION` value, and any schema artifact/path it produced. This is the source for `schema` in `encode_record` — do not hard-code or guess a version.

## 3. Finish `encode_record` in the adapter checkout

Locate the function in the adapter checkout (e.g. `git -C "case03/checkouts/adapter-current" grep -n "encode_record"`), then apply exactly:

- `name`: `strip()` and lowercase it.
- `enabled`: emit as a boolean (not string/int).
- `schema`: set from `SCHEMA_VERSION` obtained in step 2.
- Preserve the existing draft notes unchanged.

## 4. Validate with the project check

Use the repository's documented check command (from `README`, `Makefile`, `justfile`, `package.json` scripts, etc.), run **inside the task checkout**:

```sh
git -C "case03/checkouts/adapter-current" status --short   # confirm only intended files changed
<project-check-command>                                    # e.g. make check / npm test
```

Check: the project check passes, and only the intended files (the `encode_record` implementation and its test/validation file if any) are modified. Do not proceed if it fails.

## 5. Commit on `task/adapter`

```sh
git -C "case03/checkouts/adapter-current" add <changed-files>
git -C "case03/checkouts/adapter-current" commit -m "Finish encode_record: normalize name, include enabled boolean and schema version"
git -C "case03/checkouts/adapter-current" status --short --branch
git -C "case03/checkouts/adapter-current" rev-parse HEAD
```

Check: commit lands on `task/adapter`, working tree is clean, and draft notes remain intact in the tree. No amend that would drop the draft notes.

## 6. Leave ready for review — no integration or publishing

```sh
git -C "case03/checkouts/adapter-current" status --short --branch
git -C "case03" worktree list --porcelain -z
```

Do **not** run merge/rebase, push, open a PR, or touch the integration target. The checkout `case03/checkouts/adapter-current` stays in place on `task/adapter` at the new commit, registered under its new path, clean and ready for a reviewer.

## Reporting

Report: repaired path and verified registration, branch `task/adapter`, the commit SHA, the `SCHEMA_VERSION` used from `worker-status.json`, the project check command and its result, and that no integration/publishing occurred. Note anything retained (checkout and branch kept for review) and why.

One caveat: I don't know your project's actual check command or the exact primary repo root, so substitute the real `<project-check-command>` and the repo path from the `worktree list` inventory. If the primary repo is bare or lives elsewhere, adapt the `-C "case03"` argument accordingly — the repair step itself is unchanged.
