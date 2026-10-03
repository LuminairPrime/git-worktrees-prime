# Worktree Cleanup Assessment

## Background

Your team has been running a data pipeline project that uses Git worktrees to isolate feature work. A parser improvement sprint was recently completed on the `feature/improve-parser` branch. The work has been integrated into `develop`, and the team repository manager has asked you to clean up the worktree and feature branch as part of regular housekeeping.

The worktree for `feature/improve-parser` is checked out at `project-repo/.worktrees/improve-parser`. The team uses a squash-merge workflow, meaning pull requests are squash-merged rather than merged with full history.

Your organization's repository hygiene policy requires that any cleanup be fully documented. No branch or worktree may be deleted without a written record showing that the work was verified safe to remove.

First, run the provided setup script to initialize the repository in its current state:

    bash inputs/setup-repo.sh

This creates the `project-repo/` directory with the repository and worktree configured as described above.

## Output Specification

Investigate the repository state and worktree, carry out appropriate cleanup, and write a file named `cleanup-report.md` in your working directory (not inside `project-repo/`). The report must include:

- The commands you ran during your investigation and their output
- Your interpretation of what you found at each step
- Your decision about whether to remove the worktree and delete the branch, with justification
- The cleanup steps you performed (or chose not to perform) and why
- The verified final state of the repository after cleanup
