# Investigation 4: task phases, command selection, and unnecessary work

## 1. Decision summary

**Recommendation: adopt Option B (a small, additive phase-selection rule plus conditional command-block headings), but treat it as a hypothesis to test first — do not implement untested.** Option A (no change) is a defensible fallback; Option C (full reorganization) is not justified by the current evidence.

**Why it matters.** The live skill is laid out as one continuous lifecycle — Choose → Create → Establish → Develop/Integrate → Cleanup → Report — and no sentence tells the agent which of those phases the current request actually activates. The one scope limiter that does exist ("Run only the selected alternative", SKILL.md:53) applies to command lines inside a block, not to sections. An agent asked to *list*, *inspect*, or *reuse* a worktree has no textual anchor stating it may stop after verification and a completion report. Likewise, "Routine cleanup of this task's disposable resources is part of finishing" (SKILL.md:87) could be read as an obligation to run the cleanup decision tree even when the task never created anything. Both gaps are wording-level, so a wording-level fix suffices.

**Expected impact.** Plausibly fewer unrequested sub-phases per run (no cleanup walk for a list-only request, no develop/integrate framing for a repair), which should reduce executed tool calls and generated prose on the cheap task types. It will not, by itself, explain the reported ~26% token increase, and it is not expected to change the rubric dimensions that were already 5/5. No score is promised.

**Principal risk.** A blunt scope-limiter makes the agent skip prerequisite checks it still needs (pre/post `check-ignore`, path/branch/HEAD verification before `worktree remove`, integration verification before branch deletion) or leave genuinely required cleanup unfinished. The proposed wording is designed to route, not truncate: it names which phases activate per task type and explicitly preserves all checks within an activated phase.

**Confidence: medium-low.** Captured with-skill traces (scenario-1 cleanup, scenario-4 repair) show task-appropriate scope already, so the suspected over-execution is a layout hypothesis, not an observed failure. A peer-review subagent was unavailable (depth limit), so this recommendation rests on static obligation mapping plus two trace samples, not behavioral comparison.

**User decision: test first.** Run the small comparison in §6 with the paired task suite before editing the live skill. Defer or fall back to Option A if the patched skill does not reduce unrequested-phase tool calls, or if any required check disappears.

## 2. Baseline and evidence

- Live revision verified 2026-10-04: HEAD `a2117395a18fb0db7608796a65c514ee528eb426`; `skills/git-worktrees-prime/SKILL.md` SHA-256 `01D156FD90C69091875E4311CB2EF89D34D5E362C0B71A014E3D34440D451744`; 140 lines, ~1,864 whitespace-delimited words (matches the handoff identifiers; word count method: `Get-Content -Raw` split on `\s+`).
- Eval artifact copies of the skill used by the captured Tessl runs (`vendors/tessl_evals/scenario-1/with-skill/.tessl/plugins/luminair/git-worktrees-prime/SKILL.md`, same for scenario-3 and scenario-4) hash to `2A9FA731...` and **differ from the live file**. The live file added the bottom "Safety constraints" section and a Glossary heading after those runs. Attributing the reported scores to the live bytes is therefore unsafe; they exercised the pre-safety-section revision.
- Older full-hash of the post-prototype, pre-safety skill: `2F7F933A...` (from `docs/research/1.0-development/21-...`). Pre-safety word count 1,667.
- Files examined: `skills/git-worktrees-prime/SKILL.md` (full); `SAFETY.md` (13 constraints, all quoted above); `docs/plans/integrate-safety-constraints.md` (status of the earlier safety patch); `docs/research/1.0-development/21-prototype-enhancements-and-verification.md`; `docs/research/1.0-development/README.md` (toc only); `experiments/README.md` (rounds 1–3 methodology and outcomes); `tessl.json`; `skills/git-worktrees-prime/evals/scenario-{0..4}/{scenario,criteria,task}.json|md`; captured artifacts under `vendors/tessl_evals/scenario-{0,1,3,4}/{with-skill,without-skill}/`.
- Concrete trace evidence (bounded sample, two runs):
  - `vendors/tessl_evals/scenario-1/with-skill/cleanup-report.md` (dated 2026-10-03, task: cleanup of a squash-merged feature worktree). The agent ran a full but task-appropriate cleanup: inventory, dirty/ignored/stash inspection, ancestry check (expected fail under squash-merge), content-equivalence proof (empty `git diff`, identical blob SHAs), `worktree remove`, refused plain `branch -d`, recorded tip, `branch -D`, dry-run prune, post-state verification. Command count is high but every group maps to a checklist item in that scenario's `criteria.json` — i.e., the work is explained by the task spec, not by the skill's lifecycle layout.
  - `vendors/tessl_evals/scenario-4/with-skill/repair-report.md` (relocated-checkout repair). The agent ran `worktree list` before, `git worktree repair <abs path>`, `worktree list` after, plus a log check of the repaired branch. It did **not** run develop/integrate/cleanup. Positive evidence that the live-era skill (the eval copy) does not force phases the task omits.
- Missing / unmatched evidence: no with-skill trace for scenario-0 (only a without-skill tree), no with-skill working tree for scenario-3 (only inputs and a without-skill tree), no transcripts or tool-call counts alongside the reports, and no causal decomposition of the user-reported ~200k extra tokens. `tests/results/` and `experiments/round*/results` hold local Luna-style trials under different subjects and fixtures; they cannot establish the cause of the Tessl aggregate and were used only for provenance context.
- A peer subagent was requested to challenge the proposal but the spawn failed with a depth-limit error ("Subagent depth limit reached (1)"), so no peer contribution exists; this is recorded rather than silently dropped.

### Obligation map (static, from the live SKILL.md)

| Instruction group | Lines | Activated by | Required or conditional? |
|---|---|---|---|
| Glossary | 10–22 | any task | contextual reference |
| Choose the checkout | 24–30 | any task (decides reuse vs create vs current) | always consulted |
| Choose the manager and location | 32–39 | create / repair / manager-specific | conditional on create/repair/managed |
| Establish the starting state | 41–49 | create / reuse | conditional, but text does not say so |
| Generic Git commands ("Run only the selected alternative") | 51–75 | create/inspect | conditional; scoped to lines, not sections |
| Develop and integrate | 77–83 | develop / hotfix / integration tasks | conditional, not flagged as such |
| Cleanup decision tree | 85–95 | finishing with created disposable resources | conditional, sentence 87 reads as routine obligation |
| Inspect and remove with Git | 97–122 | cleanup | conditional, scoped to lines |
| Completion report | 124–128 | any task reporting readiness | scoped to "retained task checkout ready" and reporting |

The map shows the skill's obligations are mostly conditional in effect but unconditional in presentation order. That is the core ambiguity Option B addresses.

## 3. Options

### Option A — No change (comparison baseline)

- **What changes:** nothing. **What stays:** everything.
- **Why it is credible:** The two captured with-skill traces show correct phase selection already; cleanup was task-relevant in scenario-1 and absent in scenario-4. The only scope statement that might over-trigger ("routine cleanup is part of finishing") is wrapped in retain-if-needed conditions (SKILL.md:89–94) and asks-only-when-unresolved (SKILL.md:87). Under this reading the 26% token increase is better explained by task specs demanding verbose documented reports, by the general harness, or by the token-attribution work, not by this file.
- **Rubric effects:** none expected; distinctiveness 4/5 and conciseness 4/5 comments were about glossary mix and density, not lifecycle routing.
- **Cost effects:** none. **Regression risks:** none. **Effort:** zero.
- **Weakness:** it leaves the identified ambiguity in place; a less literal model could still traverse the whole file for a list-only request, and the ambiguity is exactly the kind the reviewer flagged as dense-but-navigable.

### Option B — Compact phase-selection rule + conditional command headings (recommended)

- **What changes:** (1) one short paragraph near the top stating that only request-activated phases run, with explicit stop points per task type; (2) two retitled command-block headers making clear each block is a menu, not a script. No sections removed, no checks removed.
- **What stays:** every existing check, including pre/post `check-ignore`, path/branch/HEAD verification before removal, ancestry-plus-content integration checks, dry-run prune, and the completion-report requirements (SKILL.md:126–128).
- **Rubric effects:** neutral on the 5/5 dimensions; may help conciseness slightly (~+30–60 words for less per-run prose) and give trigger-distinctiveness no new surface.
- **Cost effects:** goal is fewer executed unrequested phases on list/inspect/reuse/repair tasks; no promised runtime savings — measure with the §6 comparison.
- **Regression risks:** the phase rule must preserve prerequisite checks; mitigated by wording that routes phases rather than relaxing any check inside a phase.
- **Effort:** one small edit pass; trivially reviewable and revertible.

### Option C — Reorganize into explicit task-type entries

- **What changes:** restructure SKILL.md from lifecycle order into task-type sections (List/Inspect, Create, Reuse, Develop, Integrate, Repair, Remove, Prune, Full lifecycle), each enumerating its obligations, with shared checks factored into one "checks referenced by several tasks" block.
- **What stays:** same obligations, reattributed. **Likely rubric effects:** clearer routing, but reviewers may see it as a density trade and it collides with the separate progressive-disclosure proposal (conditional links into `references/`).
- **Cost effects:** possibly the largest reduction in unrequested work, but also the largest authoring and review surface; any wording drift can silently drop a SAFETY.md-derived check.
- **Regression risks:** highest — safety constraints currently flow through the lifecycle sections; a restructure must re-prove all thirteen.
- **Effort:** full rewrite plus re-validation against all 13 constraints and the eval criteria; not justified while Option B is untested.

## 4. Recommended option (B): exact candidate wording

Insert immediately after SKILL.md:8 (the line "Follow user instructions and repository conventions; keep ownership and the integration target explicit."), as a new subsection heading `## Scope of a task`:

> ## Scope of a task
>
> Perform only the phases the request activates; a phase's checks still apply in full once its phase is active.
>
> - **List or inspect only:** inventory and report; do not create, develop, integrate, clean up, or prune.
> - **Create (or reuse) for later work:** creation/reuse and verification, then report a ready checkout. Do not develop, integrate, or clean up unless asked.
> - **Develop or integrate:** the selected checkout plus the Develop and integrate section; cleanup applies only to resources this task created.
> - **Repair a relocated checkout:** reconnect and verify registration; do not prune, recreate, or run unrelated phases.
> - **Remove or prune:** the cleanup decision tree and its checks, exactly as written.
> - **Entire lifecycle authorized:** all sections, in order.
>
> Finishing with "routine cleanup" (below) covers only this task's disposable resources; it never authorizes touching another worker's checkout, the primary checkout, or the current working directory.

Replace the two command-block lead-ins:

- Line 53: "Substitute all placeholders. Run only the selected alternative." → "Substitute all placeholders. This is a menu, not a script: run only the lines for the single operation you selected."
- Line 99 area (under `### Inspect and remove with Git`): add the same "menu, not a script" sentence once, before the fenced block.

And adjust the cleanup gate sentence (SKILL.md:87) minimally, keeping its existing conditions:

> "Routine cleanup of **resources this task created** is part of finishing; ask only when authority, ownership, or possible data loss is unresolved. Routine cleanup never expands a list/inspect/reuse/repair request into removal, integration, or publishing."

**What it should eliminate:** cleanup-tree traversal and any removal/prune commands on list-only, inspect-only, reuse, and repair requests; develop/integrate framing on create-only and repair requests; any read of the sections below as a mandatory sequential script.

**What it must retain:** every check inside an activated phase — ignore-file location and `check-ignore -q` with trailing slash before **and after** creation (SKILL.md:39, 60–61), starting-state capture (43–48), ownership/branch/cleanliness verification before local integration (82), inspection of tracked/untracked/ignored/detached state before removal (91), canonical path/ownership confirmation before `worktree remove` (92), integration evidence beyond `branch -d`'s ancestry check (105–106, 118–119), dry-run review before prune (94, 114), post-mutation re-listing (95, 111), and readiness verification before reporting (126).

**Why it beats the alternatives:** A risks leaving a real ambiguity; C buys routing at the cost of a full safety re-audit and a fight with the progressive-disclosure proposal for little demonstrated gain. B directly names the suspected over-execution trigger (sections read as phases-by-default) with ~120 added words and no check removal, and it is byte-revertible.

**Evidence that would reverse the recommendation:** the §6 comparison shows no reduction in unrequested-phase tool calls, or any required check disappears under B, or traces demonstrate the live file already routes phases correctly in the model families used (then A wins).

### Walkthrough of representative tasks (Option B)

- **List-only / inspection-only:** stop after inventory and report; no create/develop/cleanup. Counterexample check: none of the prerequisite checks belong to this phase, so nothing required is lost.
- **Create then leave ready:** create, verify path/branch/registration/ignore, report ready; no develop, no cleanup, no branch deletion. The "Do not claim complete deletion" and retry semantics are untouched.
- **Reuse with existing uncommitted work:** Establish phase applies (43–48): confirm ownership, path, branch, ongoing operations; transfer changes deliberately (47); no stash/reset (47); cleanup does not run because the checkout is not disposable to this task.
- **Hotfix requiring develop + integration:** Develop and integrate section activates fully (79–83); Develop section's working-directory discipline applies; cleanup limited to resources this hotfix created.
- **Review of a branch without publication authority:** review section's integration guidance applies as "report pending review location" (83); no merge/publish. The B wording keeps 'record the integration commit or pending review location' — review is recorded, not performed.
- **Removal of a disposable checkout while retaining its review branch:** cleanup tree 2 and 5 both trigger: checkout removed, branch retained with reason (90, 93); "removed checkouts' branches may be retained" is preserved (90).
- **Repair of a relocated live checkout:** repair instruction (37) runs; re-list verification runs; explicitly no prune (37, 94), no recreate. Counterexample check: `git worktree move` caveats and the live-checkout protection remain (37, 135).
- **Cleanup with ignored data, offline entry, or concurrent ownership:** items 1, 3, 6 of the tree still gate: ignored files inspected (91, 101–102), offline volume not pruned (94), another worker's checkout untouched (89). B adds nothing here; the conditions already carry the load.
- **Explicitly authorized entire lifecycle:** all sections run in order; B explicitly preserves this.

## 5. Safety and semantic coverage check

No structural reorganization is proposed, so the affected SAFETY.md subset is the constraints whose host sentences B touches. All thirteen SAFETY.md constraints were re-read against the proposed wording; coverage is unchanged:

1. **Authorization for discards (SAFETY.md:3):** preserved — B does not weaken any "don't" and its cleanup-gate edit *adds* non-expansion language. The "ask only when authority... unresolved" gate stays.
2. **Verify repo/path/branch/HEAD before destructive ops (:4):** preserved at SKILL.md:92, 133.
3. **No `--force`/unlock/filesystem bypasses (:5):** untouched.
4. **No `-B` unless authorized (:6):** untouched (SKILL.md:134).
5. **Preserve changes/untracked/ignored files before removal (:7):** preserved at SKILL.md:91, 100–102.
6. **No filesystem deletion for routine cleanup (:8):** untouched (SKILL.md:92, 109).
7. **`move` refusal ≠ filesystem relocation permission; repair from current main path (:9):** preserved at SKILL.md:37, 135.
8. **Submodule constraints (:10):** untouched (SKILL.md:91 third bullet, 136).
9. **Prune only established removals; dry-run first; lock offline storage (:11):** preserved at SKILL.md:94, 114–115, 137.
10. **Shared refs/config isolation limits (:12):** untouched (SKILL.md:138).
11. **`extensions.worktreeConfig` migration (:13):** untouched (SKILL.md:138).
12. **Extension support across Git installs (:14):** untouched (SKILL.md:139).
13. **No direct ref/metadata file edits (:15):** untouched (SKILL.md:140).

Deliberately *repeated* statements that B does not consolidate (redundancy is functional): (a) the pre/post-creation `check-ignore` at SKILL.md:39 and scenario-2's criteria both require it — it is a post-mutation revalidation, not caching; (b) `worktree list` at establish (after 37/95) and at completion (126) revalidates registration after creation/repair; (c) `status --short --branch` and `rev-parse HEAD` recur across Establish, Cleanup inspection, and removal verification because each follows a mutation boundary. Consolidating these into one "check once" instruction would invalidate them at exactly the points where shared state may have changed. B's phase rule is written so it cannot be read as "do each check once per session."

## 6. Validation

**Already performed (static):** obligation map of all 21 instruction/command groups (§2); SHA-256 and word-count verification of the live skill; hash comparison proving eval artifacts used an older revision; trace sampling of two with-skill runs showing task-appropriate phase scope; re-read of all 13 SAFETY.md constraints against the proposed edit; walkthrough of nine task archetypes against the proposed wording (§4). No runtime test was executed, so no runtime claim is made.

**Proposed future comparison (not run):** build a paired harness that runs the same five fresh-agent subjects against (i) the live SKILL.md and (ii) the Option-B patched SKILL.md, on a fixed task set deliberately skewed to cheap phases: one list-only, one inspect-only, one create-only (leave ready), one reuse-with-dirty-tree, one repair. Fixtures: fresh disposable repos per run (the `tests/.runs` pattern). Metrics to record per run: tool-call count and categories, commands that fall outside the activated phase (the key signal), generated tokens, wall time, checklist score on scenario-equivalent criteria, and a safety-checklist audit (did `check-ignore` pre+post, path/branch verify before remove, integration evidence, dry-run prune all still appear where required?). **Success criterion:** fewer out-of-phase commands and fewer generated tokens on list/inspect/create/repair tasks with zero checklist-score loss and zero missing safety checks. **Stop/revert criterion:** any missing required check, any task failure attributable to phase-routing, or no measurable reduction in out-of-phase commands after two subject runs → revert to Option A and close the hypothesis. Do not claim a Tessl score change from this; it isolates instruction-to-action links only.

## 7. Dependencies and boundaries

- The progressive-disclosure investigation (references/ layout) overlaps with B's "menu, not a script" fix only superficially: both reduce visible bulk, but B changes no file layout. If both land, apply B's wording edits first, then move the command blocks behind conditional links, re-checking that the "menu" sentence survives the move.
- The token-attribution investigation owns the ~26%/~200k-token reconciliation; this report deliberately does not explain it. The observed eval traces point at task-spec-driven verbose reporting as a stronger candidate than lifecycle over-execution, but that is their lead to test, not a conclusion.
- The safety-constraint integration plan (`docs/plans/integrate-safety-constraints.md`) is evidence of the earlier patch; it is not reimplemented here.
- No subagent contribution: the single permitted peer spawn failed with a depth-limit error; no nested delegation was attempted. Unresolved disagreement: none recorded, since the peer could not run.
- Assumptions: the two captured traces are representative of the with-skill condition; the eval-copy skill revision is older than live, so live-skill behavior on the same scenarios is extrapolated, not measured. Fixtures under `vendors/tessl_evals` were not modified; no worktrees, branches, or files were created, moved, or removed during this investigation.
