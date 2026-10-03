# Prepare Development Worktree for Code Audit Feature

## Problem/Feature Description

Your team maintains the **atlas-runner** project and has recently adopted a multi-worktree Git workflow so developers can keep multiple tasks in flight simultaneously without context-switching overhead. Each active task gets its own isolated checkout under a shared directory at the repository root, keeping the main working tree clean.

An upcoming code audit sprint needs an isolated checkout called `audit-pass` set up for a new team member. Before any nested checkout can live inside the main repository tree, the team's workflow requires that the destination path be explicitly excluded from Git tracking in the enclosing repository — otherwise the worktree's contents show up as untracked files in the main checkout and cause confusion. This exclusion must be confirmed to be in effect before the checkout is created, and then verified once more after creation to ensure nothing changed during setup.

The new team member will need a clear record of every step taken so they can reproduce the setup on their own machine if needed.

## Output Specification

1. Initialize a Git repository for the **atlas-runner** project in your working directory. Add a few starter files (for example, a `README.md` and a basic source file) and make an initial commit so the repository has history to branch from.

2. Create a dedicated development worktree for the audit task at `.worktrees/audit-pass`. The worktree should be on its own branch for this task.

3. Before creating the worktree, ensure the `.worktrees/audit-pass` destination is excluded from Git tracking in the enclosing repository. The exclusion must be verifiably in effect prior to running the worktree creation command.

4. After the worktree is created, confirm that:
   - The ignore coverage for the worktree path is still correct
   - The new worktree appears in the repository's registered worktree list
   - The checkout's absolute path and branch are as expected

5. Write a step-by-step log to `nested-worktree-setup.md` that records:
   - Every command run and its output
   - How you established and verified the ignore exclusion before creation
   - The worktree registration details after creation
   - A summary of the final state, including the worktree's absolute path and branch name
