# Luna follow-up questions and frozen grading key

Purpose: distinguish concise omissions from missing knowledge. No vendor text, corrective notes, research, skills, or memory are supplied. This follow-up reuses the baseline subject and is not a fresh independent sample.

## Questions supplied to Luna

21. What operations does Git's worktree lock actually block, and does it prevent another agent from committing in that checkout? Answer from your existing knowledge; do not inspect further material.
22. Can ordinary `git worktree move` relocate a linked checkout containing initialized submodules? If you do not know the documented limitation, say so and explain the safe next action rather than guessing.

## Frozen expectations (not supplied to Luna)

21. The provided Git snapshot documents protection against pruning, normal moving and removal (51, 69-70, 98-100). A worktree retention lock is not a worker mutex preventing edits or commits. Accurate conceptual coverage passes; no command spelling required. Do not recommend bypassing it.
22. The snapshot explicitly says worktrees containing submodules cannot be moved with this command (73), and warns incomplete submodule support (297). Exact knowledge passes. Safe deferral is acceptable task behavior but is not proof of knowing that specific limitation. A confident guarantee that move is supported fails.

These questions receive qualitative judgments rather than retroactively changing the baseline's frozen 40-point score. A correct answer without new information weakens the claim that the corresponding vendor fact teaches something missing.
