No — do not assume `main` is the integration target.

Per worktree rules:

1. **Base:** use requested base. If none, inspect repo conventions — `CONTRIBUTING`, PR template, default branch, open PRs — not `main`/`master`/`origin`/`HEAD`. If current remote base required:
   ```sh
   git -C "<repo>" worktree list --porcelain -z
   git -C "<repo>" rev-parse --verify "<base-ref>^{commit}"
   ```
   Keep base vs integration target distinct — they may differ.

2. **Task branch for feature X:** for development, create/reuse a branch:
   ```sh
   git -C "<repo>" worktree add -b "<task-branch>" "<worktree>" "<base-ref>"
   ```
   Never override checkout protection; don't use `-B` unless reset authorized. Location default: `<primary-root>/.worktrees/<task>` unless repo convention says otherwise.

3. **Disposable inspection:** detached HEAD only:
   ```sh
   git -C "<repo>" worktree add --detach "<worktree>" "<commit>"
   ```
   Anchor valuable commits to a branch before removal.

No repo found in `/tmp/skill-up-2800533418` to verify target. Provide `<repo>` path, desired `base-ref`, and `task-branch` name to proceed.
