# Luna behavioral trials

Completed results: [main research interpretation](../docs/research/20-luna-behavioral-trials-summary.md) and [subject summaries and evidence](results/README.md). Six subjects performed 18 case attempts; 10 met every task outcome. The no-guide, original-prototype, and patched-copy conditions passed 3/6, 4/6, and 3/6 respectively. This small screen supports targeted follow-up, not a reliable ranking of the conditions.

Six fresh GPT-6 Luna agents at high effort each execute three independent repository tasks. Two agents receive no supplemental worktree guide, two receive the original prototype, and two receive a copy with only candidate wording changes. The actual prototype is not edited. Assignment labels are neutral; the subjects are not given the condition map or grading key.

Prepare once with `python tests/behavioral_trials.py plan`, then `python tests/behavioral_trials.py setup`. Setup refuses to overwrite existing runs. All disposable Git repositories, fake offline-volume data, and raw command logs live in ignored `tests/.runs/`. Fixtures use local identity `trial@example.invalid` and have no remote. Subject summaries and exported evidence live in `tests/results/`. Inspect outcomes with `python tests/behavioral_trials.py inspect` after all subjects finish. Do not rerun setup against existing evidence.

Subjects execute commands through `tests/run-command.ps1`, which records supplied commands, a PowerShell transcript, and Git Trace2 events. Example: `& ./tests/run-command.ps1 -Run r01 -Command 'Get-Content TASKS.md'` (called from the project root). This runner is an audit aid, not a security sandbox. Subjects are authorized to modify only their own disposable trial and write their own summary; they may not research, access memory, load other skills, inspect controller data, or read another run. Reading the supplied guide is an experimental input, not permission to load any available skill.

The controller's frozen initial state and conditions are in `.runs/controller/initial-state.json`, outside each subject's permitted directory. Setup simulates an unmounted worktree by retaining its directory in a controller vault while removing its registered path; it makes the missing entries old enough for an ordinary prune to target them. No actual drive is disconnected. Fixtures do not involve real secrets, users, remote services, or repository publishing.

The three case outcomes are assessed from files, refs, worktree registrations, runnable Python assertions, and Git command traces. Task order is reversed within each condition's two runs, keeping each case's average position equal. Cases handled by one subject are not independent model samples. Common inherited harness/system instructions still apply across all conditions, so the no-guide condition is not an instruction-free model.

## Frozen outcome criteria

1. **Isolated fix:** colleague's primary files and branch preserved; required custom destination ignored; correct task branch/checkouts; selected base present without colleague-only feature; functional assertion passes; fix committed. A report claiming isolation cannot replace actual state checks.
2. **Cleanup:** inactive task checkout removed; review branch/tip retained; exact ignored review data preserved outside the removal path; offline registration and colleague branch retained; release ref and primary tracked state preserved. Leaving the intentionally retired registration is acceptable if safe pruning cannot exclude the offline checkout.
3. **Resume:** moved live checkout registered at its current path; same task branch/checkouts retained; prerequisite commit in history; existing draft preserved; functional assertion passes; adapter change committed; primary branch and tracked state preserved.

A case passes only if every required outcome holds. Report individual checks and distinguish unsafe mutation from incomplete progress. The source of guidance is disclosed only after outcomes are checked. Artifact/file checks are blind to condition; the main agent cannot be considered a completely blinded human evaluator because it prepared the assignments. Timing, extra commands, and summary honesty are supplementary evidence, not an arbitrary numerical penalty.

Run no further conditions or instruction deletion tests until this screen establishes where a repeatable error actually occurs. The research summary belongs in `docs/research/20-luna-behavioral-trials-summary.md`, outside this folder.

## Evaluator correction recorded during the trials

The task asks case 3 to use the schema worker's result; it does not require preserving the exact prerequisite commit identity. The initial checker nevertheless requires commit ancestry. On observing a subject cherry-pick the result, the controller recognized that this could reject a valid solution. The original strict check and strict case score remain in the output. A separate task score also accepts an equivalent committed `schema.py` plus all other original checks. This correction is applied uniformly to all six runs and disclosed in the final report; a valid cherry-pick is not classified as an agent mistake. The checker script changed for this correction after launch, so its initial and final hashes are retained separately. No task, supplied guide, fixture, or subject instruction was changed.

Final verification used Python `-B` to suppress new bytecode output; preflight had created reproducible caches in the adapter fixtures. A supplementary `review_data_intact` flag records whether data remains in the original checkout or a preserved copy; it does not relax the cleanup requirement. Additional adapter checks exercise another name, false enabled, and a different runtime schema constant without changing source files.
