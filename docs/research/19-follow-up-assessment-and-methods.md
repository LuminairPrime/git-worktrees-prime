# Follow-up assessment and proposed research methods

Date: 2026-10-02. This assessment supplements the completed vendor comparison and Luna questioning. It proposes further work; none of the experiments below has been run. The prototype remains unchanged.

## What was missed or remains unproven

The largest missing evidence is ordinary task behavior. The questions direct attention to the relevant trap, so a good answer shows accessible knowledge rather than reliable action without prompting. We did not observe creation, setup, integration, recovery, or cleanup in a real or disposable repository. The correct follow-up answers show that Luna knew the facts, but not that it would notice when those facts matter.

We also lack a no-skill control. The result cannot show whether the prototype contributed beyond training or whether a shorter skill would work equally well. There was one Luna sample at high effort, some reviewer threads were reused, and the main author performed the grading. Those limits are disclosed in the packet. Calling Q22 independent recall means no new facts were supplied, not that its answer was an independent statistical sample.

Git and harness behavior were not verified during the first research round. A setup check for this commit reports installed Git `2.53.0.windows.1`; the vendor reference labels itself `2.56.0`. That difference is a reason to check relevant commands against the target installation, rather than assume every snapshot detail applies. Exact source URLs/revisions and retrieval dates are also not recorded consistently for all vendor snapshots. Add those when revisiting a source; do not invent missing provenance.

Some operational situations deserve later task coverage: a dependent worker whose checkout lacks the prerequisite commit despite a completion signal; stale task context after resuming a chat; a harness that transfers dirty files or archives only selected state; and a refusal requiring recovery rather than force. These are test candidates, not evidence that the skill needs new paragraphs.

## Highest-value next experiment: tasks, not questions

Use a small set of disposable Git repositories and ordinary task requests that do not name the trap. Keep fixture state and expected outcomes private. Examples:

- Ask for an isolated fix with a custom in-repository checkout location. Inspect whether the exact location is ignored and the intended starting commit is used.
- Make requested isolation fail while the primary checkout contains unrelated changes. Check that no code edits reach the primary checkout and that the failure is reported accurately.
- Ask to finish a task with ignored review data, a still-needed branch, rewritten integration history, and an offline sibling registration. Check retained data/refs and actual deletion scope.
- Rename a live task checkout and ask the agent to resume it. Check that recovery preserves the checkout and reconnects its registration.
- Start a dependent task from an old commit after its prerequisite worker finishes. Check that the dependent checkout receives the required changes before work begins.

Begin with three fixtures, not a general evaluation framework. Save prompts, starting state, command transcripts, and resulting file/ref inventories. Grade completed outcomes and inappropriate mutations, not merely whether the answer mentions a keyword. Include unnecessary questions, extra setup, and instruction length as secondary costs.

## Controlled comparison

Run matched fixtures in three conditions: no worktree skill, the unchanged prototype, and the prototype with only the small candidate wording changes. Use fresh subjects and reset fixture state for each run. Hold model, effort, harness instructions, tool availability, and permitted research constant. Start with two or three repetitions per condition as a practical screen; treat small differences as inconclusive rather than a robust estimate.

Give the evaluator an anonymized transcript/result and the frozen outcome key, without identifying the condition. Prevent the test subject from receiving answer keys or other subjects' outputs. Keep memory and research disabled consistently; for execution tests, permit only the repository and operational tools needed for the task. Record actual tool use rather than relying solely on self-report.

This comparison answers whether extra wording improves decisions. A failure that repeats with the prototype and disappears with a tiny patch is more useful evidence than a vendor document containing another rule.

## Test what can be removed

After a few representative fixtures work, remove one instruction group at a time and rerun the affected tasks. This tests the user's minimality goal directly: which instructions actually help beyond training and the surrounding harness? Keep a clause when deleting it creates a repeatable failure or removes a necessary authority/data-preservation boundary. Avoid equating a small number of passing samples with proof that a safeguard is never needed.

Keep default guidance short. Move rare recovery or parser specifics into a small optional reference only if real tasks repeatedly need them. Broadening the actual-destination ignore wording and correcting the prune comment remain reasonable clarity changes, but this round has not demonstrated a behavioral gain from either.

## Recommendation

Do not collect more generic vendor skills now. Next, run a small blind task comparison of no skill versus prototype versus a tiny patch. Then use targeted deletion experiments to identify redundant guidance. Validate specific Git/harness behavior only for failures or candidate instructions that affect those fixtures. This directly tests both sufficiency and minimality without turning the project into an evaluation platform.
