## Safety Constraints

- DON'T remove, move, or reset a checkout before verifying its exact path and branch/HEAD. Scripts must use `git worktree list --porcelain -z` for inventory.
- DON'T bypass a Git refusal with `--force`, `unlock`, or filesystem operations unless the user authorized the specific override and its consequences.
- DON'T use `git worktree add -B` unless the user authorized resetting that branch; use `-b` for a new branch.
- DON'T remove a checkout until needed changes and untracked/ignored files are preserved outside it, and needed detached commits have a branch or tag. Discard only work the user authorized discarding.
- DON'T use filesystem deletion for worktree cleanup; use `git worktree remove`. Use `git worktree move` where supported; an authorized filesystem relocation requires moving the checkout intact and reconnecting it with `git worktree repair`.
- DON'T prune registrations merely because paths are missing. Confirm permanent removal, check `git worktree prune -n`, and repair relocated checkouts instead. Lock worktrees on removable/network storage before it goes offline.
- DON'T assume worktrees isolate branches or repository configuration; branches are shared, and repository configuration is shared by default.
- DON'T edit Git ref or worktree registration files directly; use Git commands. Resolve internal paths with `git rev-parse --git-path` from the intended checkout.