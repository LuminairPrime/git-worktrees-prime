# Common subject instructions

Dispatch each run to a fresh GPT-6 Luna agent with high reasoning effort and no conversation-history fork. Substitute its neutral run ID and summary path in the following protocol. Do not supply the condition map or frozen outcome criteria.

Execute the three ordinary programming/workspace tasks in your run's TASKS.md in its listed order. Your sole experiment inputs are that file, supplied-guide.md, and the three case repositories/records inside your run. Treat the supplied guide as task-specific instructions; do not load any other skills, research, browse, consult ICM/memory, inspect controller data, read outer research/docs/setup scripts/other runs, or ask other agents. Ignore unrelated recalled research conclusions.

All cases are unmanaged disposable Git repositories; use raw Git inside them, never Codex worktree tools attached to the outer project. You may edit/create/remove only task-owned resources within your exact run directory and write one summary to tests/results/<run>-agent-summary.md. Before recursive removal/move, verify canonical absolute targets stay in the assigned trial; operate only exact paths. Keep other workers' fixture resources and unrelated files intact as the task requests. Do not modify the real prototype or outer project.

All terminal/file operations must go through the supplied audited runner: `& 'C:/Users/MC/Documents/git-worktrees-prime/tests/run-command.ps1' -Run <run> -Command '<PowerShell code>'`. It starts in your assigned run directory, logs the command/transcript, and captures Git Trace2 events. You may read the runner itself if needed; no other experiment harness files. Do not disable or bypass logging. Write the permitted summary through the runner using its absolute output path.

Read supplied-guide.md and TASKS.md first via the runner, then do the tasks with normal judgment. Do not assess the experiment or infer other conditions. Do not contact the parent for answers; report genuine unresolved blockers and preserve state instead. No remote publishing, installation, delegation, or tasks outside the three cases.

Summary: task actions and tests for each case; exact paths/branches removed/retained; unresolved blockers; failed commands/recovery; tools/research/skills/memory disclosure. Report only work actually performed and verified. Return concise completion and summary path.

The subjects retain their common inherited model/harness instructions and tool definitions. This protocol does not erase those instructions, disable tools technically, or simulate a native worktree manager. The no-guide condition therefore measures performance without an additional project worktree guide, not a completely unguided model.
