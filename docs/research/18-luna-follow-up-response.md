# Luna follow-up response

21. Locking a worktree protects its registration from automatic pruning and blocks the worktree management operations that would move or remove it while locked; those operations require it to be unlocked (or the documented force override). It does not lock the files or Git index, so another agent can still edit and commit in that checkout. Coordinate ownership and shared changes separately.

22. Git's ordinary worktree move does not support moving a linked checkout that contains submodules. Leave it in place, or use a manager-supported migration path that explicitly handles the submodules; do not force the move based on an assumption.

Tools used: PowerShell Set-Content to save this response. No files were read, and no new reference material, outside research, skills, memory/ICM, Git commands, or agents were consulted.
