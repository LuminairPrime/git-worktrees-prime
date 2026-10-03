# Restore a Broken Worktree Registration

## Background

The data engineering team at FinStream maintains a feature branch for an ongoing data pipeline project. The branch is developed in a dedicated Git worktree so it can run alongside the stable main codebase without interference.

During last week's workspace reorganization, a team member renamed the worktree directory using the operating system's file manager rather than Git. The directory moved to a new location, but Git's internal records still point to the original path. As a result, anyone running `git worktree list` from the repository sees the wrong location — the feature branch is effectively invisible to Git's worktree tracking until the registration is corrected.

You've been handed this repository to investigate and fix. A reproduction script is provided at `inputs/setup.sh` that recreates the broken state exactly as the team left it. Run the script first, then work inside the `repo/` directory it creates.

```bash
bash inputs/setup.sh
```

The `repo/` directory will contain a Git repository where a linked worktree has been relocated without Git's knowledge. The physical checkout exists at its new location and the feature branch's work is intact — only Git's registration is out of date.

## What to Produce

Correct the worktree registration so Git accurately reflects the checkout's current location. Then write a file named `repair-report.md` in your working directory that documents:

- What Git reported about the repository's worktrees before you made any changes
- The steps and commands you ran to restore the registration, including the exact paths involved
- What Git reports about the repository's worktrees after your changes
- Confirmation that the feature branch checkout is properly registered and at the expected location
