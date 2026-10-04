## Safety Constraints

- DON'T discard work or bypass safeguards without user instructions covering the target and consequence; tool access and agent-written plans grant no permission.
- DON'T remove or relocate a worktree, run `git reset --hard`, or delete files with `git clean` before verifying the target repository, absolute worktree path, branch name (or detached state), and HEAD commit. Scripts must use `git worktree list --porcelain -z` for worktree inventory.
- DON'T bypass worktree safeguards with `--force`, `git worktree unlock`, or filesystem operations without authorization, including on the first attempt. Read the lock reason; an absent reason is not permission.
- DON'T use `git worktree add -B` unless resetting the named branch to the selected commit is authorized; use `-b` for a new branch.
- DON'T remove a worktree before inspecting and preserving needed changes and untracked/ignored files outside it, and anchoring needed detached commits with a branch or tag. A clean status does not establish preservation; authorized discards are exempt.
- DON'T delete worktree directories with filesystem commands or a file manager for routine cleanup; use `git worktree remove`. The main worktree is not a removable linked worktree.
- DON'T treat a `git worktree move` refusal as permission for filesystem relocation; the command excludes main worktrees and worktrees containing submodules. For authorized filesystem moves, preserve `.git` and other contents. Run `git worktree repair` from the main worktree's current location, passing relocated linked worktrees' new absolute paths; verify reconnection.
- DON'T create, relocate, or remove worktrees in repositories with submodules without checking submodule-specific constraints and preserving affected submodule work. Git discourages multiple worktrees of a superproject.
- DON'T prune missing worktree entries without establishing removal; repair relocated worktrees and lock temporarily offline ones instead. Review `git worktree prune -n` with the intended expiry options. Lock worktrees on removable/network storage before it goes offline.
- DON'T assume worktree isolation covers shared branch refs or repository configuration; `HEAD` is worktree-specific. Without `extensions.worktreeConfig`, `git config --worktree` writes shared configuration.
- DON'T enable `extensions.worktreeConfig` without migrating existing `core.worktree` and `core.bare` settings from common configuration to the main worktree's `config.worktree`. With the extension enabled, do not share `core.worktree` or `core.bare=true`; share `core.sparseCheckout` only if every worktree uses sparse checkout.
- DON'T enable `extensions.worktreeConfig` or relative worktree paths unless all Git installations required to access the repository support the resulting extensions.
- DON'T edit Git ref files or worktree administrative files directly; use Git commands. Resolve internal paths with `git rev-parse --git-path` from the verified target worktree.
