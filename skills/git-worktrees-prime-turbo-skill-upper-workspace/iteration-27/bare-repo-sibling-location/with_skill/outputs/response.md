In `/srv/repos/rate-limit` — sibling of `/srv/repos/api.git`:

* No location convention -> bare-repo fallback: sibling of repository directory.
* `rate-limit`: unique task name, unused path.
* Why not inside `/srv/repos/api.git/`: bare repo has no worktree, only `objects/refs/config`; checkout inside would mix work files with Git internals and break bare assumption. Do not place inside another disposable worktree.

Checks, in order, raw Git `Creation`:

1. `git -C "/srv/repos/api.git" worktree list --porcelain -z` — confirm no checkout owns `rate-limit`, path unused.
2. Resolve base: `git -C "/srv/repos/api.git" rev-parse --verify "<base-ref>^{commit}"` — fetch remote first if current remote base required. Skip source `status` — bare only.
3. Branch: new `git -C "<repo>" worktree add -b "<task-branch>" "/srv/repos/rate-limit" "<base-ref>"`, or for reuse: `show-ref --verify --quiet "refs/heads/<task-branch>"` then `worktree add`.
4. Verify: `git -C "/srv/repos/rate-limit" rev-parse --show-toplevel`, `status --short --branch`, `rev-parse HEAD`.

