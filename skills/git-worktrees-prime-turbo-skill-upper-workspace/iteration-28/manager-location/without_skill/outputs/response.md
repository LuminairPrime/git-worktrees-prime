Checked in this environment:

* `/repo` does not exist - `ls: cannot access '/repo'`.
* Current workspace `/tmp/skill-up-718424562` is empty, not a git repo.
* No `opencode.json(c)` found, no repo location convention in OpenCode V2 docs index.

### Where to place `checkout-api`

Do not nest by default. Use a sibling of the main checkout, not a subdirectory:

* If `/repo` existed: `/repo-checkout-api` or `/checkout-api`, e.g. `git -C /repo worktree add -b checkout-api ../repo-checkout-api`
* In this environment, per approved temp dir: `/tmp/opencode/checkout-api`

Reason: avoids nested working trees, avoids OpenCode ancestor config merging (`opencode.json(c)` is discovered from current dir to `/`), and avoids `git worktree list/prune/remove` confusion.

### Must verify before creating inside another checkout

1. Is the parent actually inside a checkout: `git rev-parse --show-toplevel` + `git worktree list` from that directory.
2. Is target path free and not already registered: `test -e <path>` + not in `git worktree list --porcelain`.
3. Branch collision: `checkout-api` not already checked out in another worktree - `git worktree list -v` / `git branch --list checkout-api`.
4. Intent for nesting: `.git` file/dir handling, ignore rules, tooling, and outer `opencode.json(c)` will apply to inner checkout.
5. Parent is writable and main checkout exists - currently fails here since `/repo` is missing.

Provide the real `/repo` path if different, and I can give the exact `git worktree add` command.

