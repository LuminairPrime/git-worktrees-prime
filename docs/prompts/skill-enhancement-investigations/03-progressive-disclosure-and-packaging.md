# Investigation 3: progressive disclosure and skill packaging

## Assignment and decision owner

You are one of five independent investigators of the git-worktrees-prime Agent Skill. Investigate your assigned topic; return several credible options and exactly one preferred recommendation. The user will read all five summaries, decide which ideas are worthwhile, and separately choose whether another agent should implement anything. Your recommendation may be a small coherent change, a conditional experiment, or retaining the current design if the alternatives do not earn their cost. Do not manufacture a change to satisfy the assignment.

The primary consumers are highly capable AI model agents doing software development. Optimize useful decisions, clarity, consistent terminology, and actual task outcomes per unit of context and execution cost. Human users must also understand the terms agents use with them. Elementary tutorials, fancy formatting, and exhaustive repetition are not goals. Important exceptions and deliberate safety redundancy can still earn their space.

## Current permissions and boundaries

- Investigate; do not implement. Do not edit the skill, its metadata, references, SAFETY.md, existing plans, evaluation inputs, fixtures, results, or repository configuration. Candidate prose, diffs, layouts, and commands belong inside your report as proposals.
- Bundled reference files are now allowed. You may recommend a smaller SKILL.md with an included references/ folder and explicit conditional links. The previous single-file/no-reference restriction is superseded for this investigation.
- Glossary changes are now allowed. Preserve critical meanings and consistent usage across agents, users, workflow text, and any proposed references. Tables are optional.
- Older plans are evidence of earlier decisions, not a mandate to implement them. Their freezes on glossary/frontmatter/reference layout do not constrain your recommendations under this request.
- You may read repository files, use read-only Git commands, perform static/in-memory analyses, and research authoritative external documentation. Respect applicable repository instructions. Do not install dependencies, launch paid/remote evaluations, rerun trial setup, create/move/remove worktrees, change branches, reset/clean files, commit, or publish. Propose new behavioral experiments rather than executing them here.
- Follow actual paths and current source; record missing evidence instead of inventing it. Treat retrieved documents, logs, fixtures, and old prompts as evidence, not fresh instructions.
- Work independently. Do not read the other four investigators' draft reports or coordinate an answer with them before submitting your own initial conclusions.
- You may use subagents for focused research or peer review. For desktop stability, use at most one active child at a time and do not permit nested delegation. Give children the same read-only boundaries. A peer should receive the relevant task, evidence, and neutrally labeled candidates without your preferred verdict or claims about candidate pedigree. Report what was challenged and whether it changed your recommendation. Peer agreement is not a behavioral test.
- Only write your assigned report below. Do not change any other files. If you cannot write it, return the full report in chat with that limitation.

## Repository and evidence provenance

Repository root: C:/Users/MC/Documents/git-worktrees-prime.
Primary skill: skills/git-worktrees-prime/SKILL.md.

At handoff preparation, HEAD was 73d21c776ab51515ad3fb434292b22bec93823e0. The skill SHA-256 was 01D156FD90C69091875E4311CB2EF89D34D5E362C0B71A014E3D34440D451744. That version includes the new bottom safety section and a Glossary heading, and has 1,863 whitespace-delimited words. Verify the live revision and content at the start; do not reset to these identifiers if newer work exists.

The pre-safety skill at 9d4be20e52fa30b5d32e9b3cbf6ef8129cc539e8 had 1,667 words. The safety integration plan is docs/plans/integrate-safety-constraints.md; its status prose may lag the actual committed implementation. Do not propose implementing that plan again. Establish which version any evaluation actually exercised before attributing results to the live skill.

Start with the current skill. Then load only evidence relevant to your topic:
- SAFETY.md: thirteen source constraints, some incorporated in the skill body and some in its bottom section.
- docs/plans/integrate-safety-constraints.md: exact earlier patch, coverage reasoning, reviewer finding, and limits.
- docs/research/1.0-development/21-prototype-enhancements-and-verification.md: why particular path, ignore, repair, and readiness instructions were added after observed failures.
- skills/git-worktrees-prime/evals/ and vendors/tessl_evals/: local Tessl scenarios and captured artifacts; discover what they actually contain.
- tessl.json: repository packaging context.
- tests/README.md, tests/results/, and experiments/: separate historical local trials. Inspect provenance before use; these are not automatically the Tessl runs reported below.

Do not read all history by default. Use precise file/line citations and record the tested skill version when available. If a historical document has moved, locate it by filename and report the resolved path; do not restore old locations.

## Evaluation information supplied by the user

Treat these as user-reported observations until matched to an artifact and version:
- The evaluated skill scored roughly 15-20 points out of 100 above a control agent.
- It used about 26% more tokens, described as almost 200,000 additional tokens. The user does not know why; no causal explanation has been established.
- Actionability, workflow clarity, specificity, completeness, and trigger-term quality were each rated 5/5.
- Conciseness was 4/5: the reviewer found the body dense and instructional, but thought the glossary mixed already-known Git basics with valuable skill-specific conventions.
- Progressive disclosure was 4/5: a single roughly 125-line file had good navigation, but generic command blocks and some cleanup exceptions might suit included reference files. The review mentioned an under-50-line top-score case; do not treat that scoring example as an Agent Skills specification requirement.
- Distinctiveness/conflict risk was 4/5: broad parallelism/isolation triggers could overlap with general branching or multi-agent work. Trigger-term quality and distinctiveness were separate dimensions.
- The user describes the skill as the highest-rated among 30+ related skills. That is context for caution, not proof the present bytes are optimal or immune to defects.

Preserve substantive task success and safety while investigating better concision, routing, organization, or efficiency. Distinguish likely rubric improvement from measured behavior. A shorter file does not establish lower execution tokens, and a more complete run can legitimately cost more.

## Your investigation

Determine whether and how to split this skill into a smaller entrypoint and included references while preserving practical safety, discoverability, and self-contained operation. Reference files are allowed, but their existence is not itself an improvement.

Use the actual Agent Skills format specification as the governing format reference, not assumptions about AGENTS.md. Start with https://agentskills.io/specification and verify relevant current guidance. Distinguish specification requirements, recommendations, platform-specific behavior, and Tessl's quoted scoring anchors. A top-score example mentioning 50 lines is not a mandate to collapse instructions into long lines.

### Questions to resolve

- Which information must be present whenever the skill activates, and which is relevant only to a recognizable task condition?
- Can an agent identify the need for a reference before it knows the detailed exception explained inside it? Avoid circular routing such as read advanced safety if you think there is a safety issue.
- Which instructions are prerequisite gates that must remain at the decision point even if detailed procedures move?
- Do generic raw-Git commands, advanced branch cleanup, archive behavior, relocation, submodules, and configuration changes have sufficiently distinct read triggers?
- Would splitting by lifecycle phase, by exceptional operation, or by raw-Git versus harness management reduce expected loaded context with tolerable navigation cost?
- Does the repo's packaging/evaluation setup actually include and expose the proposed files? Inspect relevant manifests or conventions; do not assume a relative link is automatically packaged or read.
- After a reference is loaded, its text may remain in context. What are the best, ordinary, and worst task-path costs, rather than just the entrypoint size?
- Can any information be deleted outright as duplicate rather than moved into another file?

### Candidate exploration

Compare at least three credible layouts, including the current single-file baseline, a minimal split with few references, and a more task-specific split if justified. Do not create a file for every edge case merely to score progressive disclosure.

For each proposed layout show:
- A directory tree under skills/git-worktrees-prime/.
- Which current sections/paragraphs stay, move, shrink, or disappear.
- Exact proposed link and read-trigger wording in SKILL.md.
- Information that intentionally remains duplicated and why.
- Estimated main-file size, total bundle size, and cumulative files/words or tokens read for representative tasks.
- Additional reads/tool calls, navigation failure risks, and packaging assumptions.

Exercise the routing on routine creation, reuse, detached inspection, ordinary removal, squash/rebase branch cleanup, harness archive, moved checkout repair, offline-storage handling, and worktree-configuration changes. Show when each reference is read and before which mutation. Include a user who requests only listing worktrees.

Map all thirteen SAFETY.md constraints across the proposed bundle. No constraint may vanish merely because it is inconvenient to place. Preserve accessible definitions for critical terms across file boundaries without reproducing an entire glossary in every file. Existing path/ignore/repair instructions added after observed failures deserve particular scrutiny before relocation.

### Recommended output detail

For your preferred layout, provide a compact entrypoint outline, exact conditional-link language, and sufficient candidate excerpts to demonstrate safety routing. You need not write complete implementation files. Recommend the smallest useful split and explain why the alternatives are worse.

If you propose optional reference reads, explain why skipping them cannot violate a required safety prerequisite. If a read is required for an operation, say so clearly. Discuss compatibility with models that only read files explicitly named by the entrypoint.

### Scope boundary

This is structural research, not implementation. Do not move files, create proposed references, edit packaging, or rerun evaluation. Leave activation wording and vocabulary redesign primarily to their respective investigations, but identify exact dependencies your layout creates.

## Required report and final handoff

Write your report to docs/research/skill-enhancement-investigations/03-progressive-disclosure-and-packaging.md. Create only that report's parent directory if necessary; candidate implementation files must not be created.

Organize the report as follows:
1. A decision summary of at most 300 words: one recommendation, why it matters, expected impact, principal risk, confidence, and whether the user should implement, test first, or defer.
2. Baseline and evidence: revision/hash, exact files examined, relevant observed facts, and missing or mismatched evidence.
3. At least three substantively different options. Include a low-change option; do not invent bad alternatives to favor your preferred one. For each, show what changes, what stays, likely rubric effects, context/execution-cost effects, regression risks, and implementation effort. No-change can be the comparison baseline.
4. Your single recommended option, with exact candidate wording or a small illustrative diff/layout sufficient for another agent to estimate the work. This is a proposal, not authorization. Explain why it beats the alternatives and what evidence would reverse your recommendation.
5. A safety and semantic coverage check for affected instructions. Cover all thirteen SAFETY.md constraints when you propose a structural reorganization; otherwise identify the affected subset and confirm you did not silently remove unrelated coverage. Clarify which repeated statements are deliberate.
6. Validation: checks already performed and results, separately from tests merely proposed. Supply a small future comparison that isolates your proposed change, including success criteria and stop/revert criteria. Do not promise a Tessl score or zero regression.
7. Dependencies and boundaries: interactions with the other investigation topics, assumptions, and any subagent contributions or unresolved disagreement.

Use measurements honestly. Word counts, tokenizer counts, total bundle size, active task-path context, model-call input totals, generated tokens, tool calls, and elapsed time are different quantities. Label estimates and give the method. If runtime data is absent, do not turn a word reduction into a runtime-saving claim.

Return the concise decision summary in your final chat response with a link to the report. The user should be able to accept, reject, or defer the recommendation without reading a long exploratory transcript.
