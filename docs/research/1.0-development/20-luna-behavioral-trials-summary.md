# Luna behavioral worktree trials

## Finding

The prototype's strong conceptual test result did not establish reliable execution. Fresh Luna high subjects completed ordinary programming tasks while missing worktree lifecycle conditions: ignoring a custom nested destination and reconnecting a moved live checkout. Broader ignore wording helped one patched-guide subject but did not reliably prevent the omission. Preserve the compact skill; target the demonstrated decisions instead of importing whole vendor workflows.

## Method and evidence

Six fresh GPT-6 Luna subjects at high reasoning effort each received three independent disposable Git tasks, without a conversation-history fork. Two received no supplemental guide, two the original prototype, and two a tiny patched copy. Each condition's two task orders were reversed. The tool limit allowed two active subjects at a time. Subjects could use raw Git, PowerShell, and local Python checks; research, browsing, memory, other skills, other agents, and other runs were forbidden. Reading their assigned prototype copy was the treatment.

All repositories and operations were inside [tests](../../tests/README.md). Each subject wrote its own summary. [Results and evidence](../../tests/results/README.md) include assigned tasks/guides, command logs, transcripts, selected native Git events, initial commits/hashes, preflight, and final repository-state checks. Local fixture repositories had no remote. The actual prototype and vendor inputs were preserved.

The cases were:

1. Fix a small function in a custom nested worktree from a specified release branch while preserving a colleague's dirty primary checkout.
2. Reclaim a squash-integrated task checkout, preserving an ignored review database and review branch, while leaving a colleague's unavailable worktree registration intact.
3. Resume a manually relocated live checkout, incorporate a completed schema worker result, preserve draft notes, implement and commit the adapter.

Subjects were not given the outcome key or condition map. State checks used actual refs, protected-file hashes, worktree inventory, ignore behavior, preserved data, and runnable assertions. A case passes only when every required lifecycle and programming outcome holds. The main evaluator prepared the assignments and was therefore not fully blinded.

## Results

See [verified-outcomes.json](../../tests/results/verified-outcomes.json) for complete boolean checks. Task scores accept a valid cherry-pick of the schema result; strict launch-time scores remain separately available.

| Subject | Guide | Isolated fix | Cleanup | Moved checkout | Task score | Remaining failure |
|---|---|---|---|---|---|---|
| [r01](../../tests/results/r01-agent-summary.md) | prototype | Fail | Pass | Pass | 2/3 | checkout_ignored |
| [r02](../../tests/results/r02-agent-summary.md) | patched | Pass | Fail | Pass | 2/3 | task_checkout_removed, review_data_preserved |
| [r03](../../tests/results/r03-agent-summary.md) | none | Fail | Pass | Fail | 1/3 | checkout_ignored, live_registration_reconnected |
| [r04](../../tests/results/r04-agent-summary.md) | patched | Fail | Pass | Fail | 1/3 | checkout_ignored, live_registration_reconnected |
| [r05](../../tests/results/r05-agent-summary.md) | none | Fail | Pass | Pass | 2/3 | checkout_ignored |
| [r06](../../tests/results/r06-agent-summary.md) | prototype | Pass | Pass | Fail | 2/3 | live_registration_reconnected |

| Guide | Cases passing all required task outcomes | Original strict score |
|---|---|---|
| none | 3/6 | 2/6 |
| prototype | 4/6 | 3/6 |
| patched | 3/6 | 3/6 |

All functional checks and requested task commits passed. All subjects preserved the colleague's files/branch, review branch and database, offline-worker registration/branch, primary release state, and adapter draft. Failed cases therefore reflect incomplete lifecycle work or cleanup, rather than observed data loss. This small screen does not establish comparative model or skill performance statistically.

## What the execution revealed

**Custom destination:** The original prototype permits repository location conventions but applies its explicit ignore instruction only to `.worktrees`. The tested task used `scratch-checkouts/normalize`. Subjects could produce correct code and a clean task checkout while leaving a nested repository exposed as untracked content in the colleague's checkout. The patched copy broadened the wording to the actual selected destination, but one subject still missed it. This supports repairing the instruction's scope; it does not prove that wording alone is sufficient. Relevant vendor evidence remains in [candidate instructions](15-candidate-instructions.md): administrakt0r and OpenAI's project-local ignore guidance.

**Moved checkout:** Some subjects could operate and commit in the relocated checkout without noticing that the surviving repository still registered its old path. Functional validation could not detect this. The official Git reference's positive repair route is useful here. The tested patch corrected the prune comment but did **not** add the proposed `worktree repair` instruction, so this experiment has not tested whether that candidate remedies the error. A concise repair-and-inventory cue deserves the next isolated test.

**Cleanup judgment:** r02 preserved all resources but stopped because it inferred the open review needed the existing checkout. The records said the branch and ignored database were needed, and the request explicitly authorized reclaiming the checkout. The other subjects demonstrated successful preservation outside the removal path. This is a safe but incomplete result, accurately reported by r02 as blocked. The prototype already permits removal when review can continue from preserved commits; no large new cleanup section is justified from this one refusal.

**Report reliability:** Agents' statements that tasks were complete did not establish ignore coverage or correct registration. Preserve subject summaries as evidence, but grade independently. Some subjects acknowledged the untracked nested checkout without treating it as a failure. r04 also described the task tip as a squash commit, although the release contained the squash replacement. Neither that label nor ancestry alone was used as integration proof by the evaluator.

## Corrections and limits

The launch checker incorrectly demanded exact prerequisite ancestry although the task allowed using the worker result through cherry-pick. After observing that mismatch, the evaluator retained the original check and added a uniformly applied task score accepting an identical committed `schema.py` plus all remaining checks. [The original checker](../../tests/results/checker-at-launch.py) and launch/final hashes are retained. This was an evaluator correction, not an agent failure. Verification later used Python `-B` to avoid producing bytecode; preflight had already created reproducible cache files in the adapter fixtures. A supplementary `review_data_intact` flag distinguishes r02's retained database from actual loss without changing the removal requirement.

The logger audits commands and native Git execution; it is not a technical sandbox. Subjects retained common system/harness instructions, including inherited project guidance, so no-guide means no additional worktree guide. They reported no research, skills, or memory use. r02 listed the shared results directory when checking its summary path, exceeding the sole-output-path boundary, but no other report content was observed being read. Subjects were not given controller records or grading keys. A missing/offline checkout was simulated by moving its files into a controller vault; no physical drive was disconnected.

Two subjects per condition are too few for statistical claims, and three cases handled by one subject are correlated. The patch bundles several concepts rather than isolating a single clause. Shared-stash mutation, failed creation, actual harness archival, submodules, secret/config setup, detached commits, remote publication, and difficult integration conflicts were not exercised. Correct behavior in these fixtures does not prove those areas covered. Transient shell quoting, CRLF, relative-path, and unsupported-command errors were recorded; final outcomes were checked after recovery.

## Next research and skill decision

1. Repair the actual-destination wording as a narrow editorial candidate. Test an executable ignore gate against wording alone in fresh tasks with another custom location; do not mandate a broad setup framework.
2. Test the positive moved-live-checkout repair cue against the original in fresh, matched trials. Require current-path registration verification; a passing programming test is insufficient.
3. If a candidate fixes repeatable mistakes, remove that candidate in an ablation trial to check whether it earns its tokens. Keep the final skill short and retain clauses that change decisions.
4. Use a failed-creation/isolation fixture and a shared-stash fixture only if assessing those candidate additions. Use an actual native harness case before claiming its archive/ignored-file behavior validated.

No production skill patch was made. The behavioral evidence strengthens the priority of actual-path isolation checks and moved-checkout recovery, while leaving most vendor additions unproven or redundant. The conceptual score remains useful evidence of knowledge, but it is insufficient evidence of dependable task completion.
