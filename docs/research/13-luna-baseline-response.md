# Luna baseline response

Input: skills/prototype1-astra/SKILL.md and docs/research/11-luna-baseline-questions.md.
Requested model/effort: GPT-6 Luna, high. Restrictions: use only those two inputs and pre-existing knowledge; no research, skills, memory/ICM, Git commands, other files, or agents.

1. First establish who owns the checkout and branch, and inspect its current state before editing; do not overwrite or reuse the colleague's checked-out branch. A suitable checkout is the one assigned to this task, based on the intended ref, with an understood state and no conflicting owner—not merely any directory registered as a worktree.

2. Keep source edits out of the dirty primary checkout. If the harness fails, use a documented generic Git worktree fallback only if it can safely satisfy the isolation requirement and repository conventions; otherwise stop before editing and report the blocker. Do the requested edits only in the isolated task checkout.

3. Verify that the exact scratch-checkouts/<task> path is ignored before creating it, so Git will not treat the checkout as untracked repository content. A tracked .gitignore change and commit are not automatically required; use the repository's accepted ignore mechanism, and make a tracked change only if its conventions require a shared rule.

4. Unequal strings are not proof: one path may be relative and the other absolute while resolving to the same directory. Normalize/resolve the paths and identify the checkout from its top-level path, worktree inventory, and task ownership; confirm its branch or detached commit against the requested starting state.

5. No. A .git file can occur in linked worktrees and submodules, while a bare repository has no ordinary checkout .git entry; the common Git directory's parent is not reliably the primary root. Use Git's worktree inventory and resolved Git paths, then confirm the actual checkout root and ownership rather than inferring them from one path shape.

6. Stashes belong to the shared repository stash list, not to a particular worktree, so “latest” may be the other agent's entry. Identify the intended stash by its recorded work and inspect it before applying the explicit entry; drop it only after confirming the recovered changes.

7. Check the configuration scope and origin: ordinary local config may be shared by worktrees, while per-worktree config depends on Git's worktree-config support and opt-in configuration. A worktree-local setting is not automatically isolated in every repository, so verify how core.hooksPath resolves before changing it.

8. Do not link the primary .env.local; that would share settings and possibly credentials and could point this task at the wrong database. Set up an explicit task-specific environment file or variables, with a distinct database and appropriate secret handling, and verify the target before running the app or checks.

9. A relevant check failing before edits establishes a baseline failure for that checkout and environment, not a regression caused by later changes. Record the base commit, command, environment details that matter, and failure output so a later comparison can attribute new failures; a full suite in every worktree is not mandatory if a narrower relevant check is appropriate.

10. Do not silently treat the old tracking ref as the current remote company/release; the failed fetch leaves freshness unverified. Resolve the intended ref and commit explicitly, retry or establish an approved fallback, and record the exact commit and fetch limitation; if only the stale commit is available, disclose that and get agreement before treating it as the requested current base.

11. No. A local branch at the PR head is only a local ref and does not by itself update the PR. Establish the PR's source repository and branch, the intended target, and the remote/push route; make commits on the correct source branch and publish only with the required authorization.

12. Preserve the valuable directory and do not prune the stale registration just because its recorded path is missing. From a surviving checkout, use git worktree repair with the new path to reconnect Git's administration data, then verify the inventory and the moved checkout's status and commit.

13. Lock the checkout before disconnecting, with a reason, so Git's prune flow protects its registration. A lock protects the registration from pruning; it does not back up or preserve the checkout's contents. Later, inspect every prune dry-run entry and leave the offline-drive checkout registered until that volume is available and its state is known.

14. That assurance is too broad: initialized submodules can change what worktree creation, moving, archiving, or removal supports. Check the chosen manager's documented behavior, keep the submodule checkout intact, and use its supported path; do not force removal or bypass a refusal.

15. No. Paths can contain whitespace, so parse a NUL-delimited porcelain format such as git worktree list --porcelain -z, respecting record boundaries and optional fields instead of splitting human-readable output on spaces or lines. Handle detached, locked, prunable, and bare entries as well as ordinary branches.

16. No. branch -d can use the configured upstream, which is not the intended integration target here. Before cleanup, verify the task tip or its replacement changes against the actual target, account for squash/rebase integration, inspect remaining working and ignored state, and retain the branch if it is still needed.

17. A clean tracked status does not cover the ignored review database; preserve it separately if it matters before removing the checkout. The open-review branch should remain, and squash integration should be checked by comparing the resulting changes rather than relying on ancestry. Remove the checkout only when its remaining state is accounted for and the review can continue without it.

18. Do not run the repository-wide prune while one listed path may merely be offline. Keep the dry-run evidence, reconnect the drive or otherwise establish that entry's status, then prune only when every entry affected by the operation is intentionally stale.

19. No. Worktree separation isolates checkout files and indexes, not shared databases, ports, services, or output directories. Give each task a distinct writable database and output path, and separate any shared services or ports that could conflict.

20. Confirm exactly what the harness snapshot includes; the prototype says ignored files may be omitted. Preserve the ignored credential through an appropriate secure mechanism before archiving, and report the checkout removal and recoverable snapshot accurately while noting any retained branch/archive or separately preserved credential; do not claim all state was deleted.

Tools used: PowerShell Get-Content to read the two supplied inputs and Set-Content to save this response. No outside research, skills, memory/ICM, other files, Git commands, or agents were used.
