In this env `/repo` does not exist and `/tmp/skill-up-1886892014` is empty, non-git.

Do not nest:

* Place: `/tmp/opencode/checkout-api` — sibling/outside, not ` /repo/checkout-api` or `/repo/.worktrees/*`. `/tmp/opencode` is pre-created/approved vs generic `/tmp`.
* Raw Git: `git -C /repo worktree add /tmp/opencode/checkout-api -b checkout-api` (or detached/existing branch).

Before creating *inside* another checkout, verify:

1. Parent is actually a git top-level: `git -C /repo rev-parse --show-toplevel; git -C /repo worktree list`
2. Target path does not exist and is not already registered.
3. Nesting is ignored (`git status --ignored`, `.gitignore`) to avoid polluting outer checkout + opencode config discovery merging.

