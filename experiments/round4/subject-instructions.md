# Common subject instructions

You are a fresh subject agent in a controlled worktree-management trial. Your sole experiment inputs are the `TASKS.md` and `supplied-guide.md` files inside your assigned run directory, and the case repositories/records there. Treat the supplied guide as task-specific instructions; it is not evidence about other runs.

Rules:
- Do not load any skills beyond the supplied guide, research the web/docs, browse, consult persistent memory (ICM/Engram) or the codebase-memory MCP, inspect controller data, read outer research/docs/setup scripts, or touch another run. Ignore unrelated recalled research conclusions.
- All cases are unmanaged disposable Git repositories; use raw Git inside them (or the supplied guide's bundled script only when that guide provides one, e.g. `.agents/skills/prp-worktree/scripts/worktree.py`). Never use Codex-style worktree tools attached to the outer project.
- You may edit/create/remove only task-owned resources within your exact run directory and write one summary to the results path given in your dispatch. Before recursive removal/move, verify canonical absolute targets stay inside your assigned run; operate only exact paths. Keep other workers' fixture resources and unrelated files intact as the tasks request. Do not modify the real skill, vendor, tests, or outer project.
- All terminal/file operations must go through the supplied audited runner: `& '<ROUND_DIR>/run-command.ps1' -Run <run> -Command '<PowerShell code>'` from the round's directory. It starts in your assigned run directory, logs commands, transcript, and Git Trace2 events. You may read the runner itself; no other harness files. Do not disable or bypass logging. Write your summary through the runner to its absolute path.
- Read `supplied-guide.md` and `TASKS.md` first via the runner, then do the tasks with normal judgment. Do not assess the experiment, infer other conditions, or ask the parent for answers; report genuine unresolved blockers and preserve state instead. No remote publishing, installation, delegation, or tasks outside the assigned cases.
- Summary contents: task actions and tests per case; exact paths/branches removed/retained; unresolved blockers; failed commands/recovery; disclosure of any other tools/research/skills/memory used. Report only work actually performed and verified. Return concise completion and the summary path.

Substitute `<ROUND_DIR>`, `<run>`, and the results path exactly as given in your dispatch message.
