Place sibling to bare repo, not inside it:

* Path: `/srv/repos/api-rate-limit` — sibling of `/srv/repos/api.git`.
* Why not inside: `api.git` is bare — no worktree, only objects/refs/metadata. Placing inside pollutes bare storage and breaks bare assumption. Per convention: bare repo -> sibling directory.

Checks/creation in order, raw Git:

1. `git -C "/srv/repos/api.git" worktree list --porcelain -z` — confirm unused path/branch.
2. `git -C "/srv/repos/api.git" rev-parse --verify "<base>^{commit}"` — verify base.
3. Skip `status` and `check-ignore` — source is bare, destination is not inside another checkout.
4. Create: `git -C "/srv/repos/api.git" worktree add -b "rate-limit" "/srv/repos/api-rate-limit" "<base>"`
5. Verify:
   * `git -C "/srv/repos/api-rate-limit" rev-parse --show-toplevel`
   * `git -C "/srv/repos/api-rate-limit" status --short --branch`
   * `git -C "/srv/repos/api-rate-limit" rev-parse HEAD`

