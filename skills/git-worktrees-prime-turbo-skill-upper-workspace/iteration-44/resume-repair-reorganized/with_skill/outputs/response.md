Here is the exact sequence I would run, in order. Placeholders: `<primary-root>` = the main/bare repository, `<checkout>` = `/abs/path/case03/checkouts/adapter-current`.

## 1. Reconnect the moved checkout (first, before anything else)

```sh
git -C "<primary-root>" worktree repair "<checkout>"
git -C "<primary-root>" worktree list --porcelain -z
```

**Check:** the registration now names `adapter-current`, not `adapter-old`. No prune, no `worktree add`, no re-create — repair preserves branch, index, and state.

## 2. Establish the starting state in that same checkout

```sh
git -C "<checkout>" rev-parse --show-toplevel
git -C "<checkout>" status --short --branch
git -C "<checkout>" rev-parse HEAD
git -C "<checkout>" branch --show-current
```

**Check:** toplevel resolves to `adapter-current`; branch is `task/adapter`; record HEAD as the base commit; any existing draft notes/edits are present and **left untouched** (never stash/reset them away).

## 3. Read the schema worker's result (without touching its branch)

```sh
cat "<task-context-path>/worker-status.json"
git -C "<primary-root>" rev-parse --verify "schema/prep^{commit}"
git -C "<primary-root>" log -1 --oneline schema/prep
git -C "<primary-root>" worktree list --porcelain -z
```

**Checks:**
- `worker-status.json` says complete (no pending/failed state) and names `schema/prep`.
- `schema/prep` resolves to a real commit; its hash matches what `worker-status.json` records.
- The worktree list tells you which checkout holds `schema/prep` — **do not** check that branch out here; read its content with `git show` (step 4).

```sh
git -C "<checkout>" show "schema/prep:<schema-file-path>"
git -C "<checkout>" grep -n "SCHEMA_VERSION" -- .
```

**Check:** you have the authoritative schema value and the definition/location of `SCHEMA_VERSION` to use in `encode_record`.

## 4. Implement `encode_record`

Edit the existing draft file in `<checkout>` only:

- `name`: strip + lowercase (`name.strip().lower()` / `.trim().toLowerCase()`).
- `enabled`: explicit boolean (`bool(...)` / `=== true`), not a string/truthy passthrough.
- `schema`: taken from `SCHEMA_VERSION`.
- **Keep** the existing draft notes — additive edit only, no reverts of in-progress text.

## 5. Validate with the project check

```sh
git -C "<checkout>" diff --check
# then the project's documented check command (e.g. make check / pytest / npm test), run from <checkout>
```

**Check:** all pass. If it fails, fix and re-run — do not commit unvalidated work.

## 6. Review the change before committing

```sh
git -C "<checkout>" status --short
git -C "<checkout>" diff
```

**Check:** only `encode_record` files changed; draft notes still present; no stray or unrelated files staged.

## 7. Commit on `task/adapter`

```sh
git -C "<checkout>" add -- <changed-file(s)>
git -C "<checkout>" commit -m "encode_record: normalized name, boolean enabled, schema from SCHEMA_VERSION"
```

**Check:**

```sh
git -C "<checkout>" status --short --branch   # clean, still on task/adapter
git -C "<checkout>" log -1 --stat
git -C "<primary-root>" rev-parse "refs/heads/task/adapter"
git -C "<checkout>" rev-parse HEAD            # the two must match
```

## 8. Leave the checkout ready for review

```sh
git -C "<primary-root>" worktree list --porcelain -z
```

**Check:** `<checkout>` is still registered, on `task/adapter`, clean, at the new commit.

**Deliberately not run:** no merge/rebase into an integration target, no push, no `git worktree remove`, no `branch -d`, no `worktree prune`. The same checkout stays in place for review.

**Report:** repaired path (`case03/checkouts/adapter-current`), branch `task/adapter`, commit hash, validation result, schema source (`schema/prep` commit + `SCHEMA_VERSION`), and that no integration or publishing was performed.
