Place at `/srv/repos/api-rate-limit`:

* Bare repository: no `<primary-root>`, so `<primary-root>/.worktrees/<task>` does not apply.
* No location convention, raw Git -> sibling of repository directory `/srv/repos/api.git`.
* Do not place inside `/srv/repos/api.git/`: it is bare Git metadata, not a checkout; nesting pollutes the bare repo.

Checks in order, from `references/raw-git-commands.md#creation`:

1. `git -C "/srv/repos/api.git" worktree list --porcelain -z` — confirm no existing `rate-limit` checkout/branch collision.
2. Skip `status --short --branch`: `<repo>` is bare, not a checkout.
3. `git -C "/srv/repos/api.git" rev-parse --verify "<base-ref>^{commit}"` — resolve base; fetch first if remote base required.
4. Skip `check-ignore -q`: destination is sibling, not inside another checkout.
5. Create: `git -C "/srv/repos/api.git" worktree add -b "rate-limit" "/srv/repos/api-rate-limit" "<base-ref>"`
6. Verify:
   * `git -C "/srv/repos/api-rate-limit" rev-parse --show-toplevel`
   * `git -C "/srv/repos/api-rate-limit" status --short --branch`
   * `git -C "/srv/repos/api-rate-limit" rev-parse HEAD`

