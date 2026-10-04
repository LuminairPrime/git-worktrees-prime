# Investigation 2: activation description, scope, and overlap

Path note: the orchestrator override redirects this report from
`docs/research/skill-enhancement-investigations/02-...` to
`docs/research/tessl-score-enhancement-ideas/02-...`. It is written there.

## 1. Decision summary

**Recommendation: adopt Candidate B (capability-anchored description with an explicit negative scope clause) as the SKILL.md `description` value, and align `.tessl-plugin/plugin.json`'s drifted description with it. Test first; do not ship untested.**

Why it matters: the current description (verified live) triggers on "isolated or parallel development" plus a long enumeration of worktree verbs. Its strongest false-positive hooks are (a) "isolated or parallel development", which matches container/port/database isolation and generic parallel-agent research, and (b) "integrating task branches", which matches any Git merge. Distinctiveness/conflict risk was already scored 4/5 for this reason. The fix is narrow: describe *what capability activates the skill* (a task needing its own working directory of the same repository), enumerate the true task lifecycle, and add one explicit "Not for…" clause naming the observed overlap neighbors. Explicit exclusions are worth their characters here because the neighbors (process isolation, containers, parallel read-only research, plain branch work, independent clones) are real and recurrent in agent prompts.

Expected impact: trigger-term quality (currently 5/5) should be preserved — every worktree verb stays; distinctiveness/conflict risk should move from 4/5 toward 5/5 by construction, not measurement. Token cost grows by ~95 words (~424 chars) in always-loaded metadata (Candidate B is 669 chars / 95 words vs 245 / 32 for the current one; both far under the 1024-char spec cap). Execution-token cost of the skill body is unchanged (zero body edits proposed).

Principal risk: false negatives for terse implicit requests ("hotfix while the other checkout has uncommitted changes", "review this branch without touching my files"). Candidate B mitigates this by naming those two implicit patterns verbatim while excluding only requests where no linked checkout of the same repository is relevant. Over-broad exclusion text could also teach agents to skip the skill for legitimate edge cases (e.g., parallel agents doing read-only research that later writes).

Confidence: medium-high on the failure-mode analysis, medium on rubric effect (no measured classifier exists; hand-scored matrix below is a design check, not an empirical precision/recall).

Action: **test first.** Add the description to a fixture set (Section 6) and compare activation decisions against the current description before replacing. No Tessl score is promised.

## 2. Baseline and evidence

Live state verified at investigation start (2026-10-04):

- HEAD: `a2117395a18fb0db7608796a65c514ee528eb426` ("before research starts"). The handoff baseline `73d21c7` moved only by adding the five investigation prompt files; `73d21c7` itself moved the pre-existing research into `docs/research/`.
- Primary skill: `skills/git-worktrees-prime/SKILL.md`, SHA-256 `01D156FD90C69091875E4311CB2EF89D34D5E362C0B71A014E3D34440D451744`, 140 lines, 1,863 whitespace-delimited words. Matches the handoff identifier exactly; no newer skill edit exists.
- Live frontmatter:

  ```yaml
  name: git-worktrees-prime
  description: Manage Git worktrees for isolated or parallel development. Use when creating, listing, reusing, or removing worktrees; working in a separate checkout; integrating task branches; repairing moved checkouts; or pruning stale worktree registrations.
  ```

  245 chars, 32 words. Under the Agent Skills spec cap of 1024 chars for `description` and 64 chars for `name` (checked against https://agentskills.io/specification on 2026-10-04).

- **Plugin metadata drift**: `skills/git-worktrees-prime/.tessl-plugin/plugin.json` carries a *different* description: "Manage Git worktrees for isolated or parallel software development. Use when creating, reusing, integrating, or cleaning up task checkouts and branches. Use when experimental or parallel agent work must be done without stepping on others' toes." If Tessl or a harness surfaces this string for routing, it currently wins or competes with the SKILL.md description. Any description fix must align both.
- `tessl.json`: `{ "name": "luminair/git-worktrees-prime", "mode": "vendored", "dependencies": {} }` — packaging context only, no trigger metadata.
- Glossary (SKILL.md lines 10–22) defines Worktree/checkout, Main/linked worktree, Base/integration target, Registration. The description's "separate checkout", "integrating task branches", and "pruning stale worktree registrations" lean on these terms; they remain understandable only because the glossary is loaded with the body — the routing metadata itself must therefore be self-contained enough to route correctly even before the glossary is read.
- `SAFETY.md` (13 constraints) and the skill's "Safety constraints" section: coverage confirmed intact; no proposal here touches them.
- `docs/plans/integrate-safety-constraints.md`: historical, not mandate; not re-implemented.
- `docs/research/1.0-development/21-prototype-enhancements-and-verification.md`: repair/ignore/readiness instructions were added only after observed failures in preserved trial repos; its claim that no new model trial validates changes applies to my proposal too.
- Vendor overlap sample (frontmatter only, `vendors/*SKILL.md`): `using-git-worktrees`, `ce-worktree`, `git-worktree`, `git-worktrees`, `parallel-worktrees` (two variants) all use near-identical "isolated/parallel worktrees" phrasing. This confirms the overlap surface is crowded; distinctiveness must come from scoping and exclusions, not from different synonyms. Not audited exhaustively by design.
- Evaluation report: user-reported (roughly +15–20/100 over control, ~26% more tokens ≈ +200k, rubric 5/5 on actionability/workflow clarity/specificity/completeness/trigger terms, 4/5 conciseness, 4/5 progressive disclosure, 4/5 distinctiveness/conflict). The 4/5 distinctiveness note matches the overlap analysis above. No evaluator artifact pins which description bytes were scored; the live 245-char string is the verified current one.
- Missing/mismatched evidence: no captured Tessl transcript for the reported score; `plugin.json` description ≠ SKILL.md description (drift, recorded above); `SAFETY0.md` is a second file whose relationship to SAFETY.md was not investigated here.

## 3. Options

All options keep `name: git-worktrees-prime`, the frontmatter shape, and all body bytes unchanged. Only the `description` value (and, for Option B/C, `plugin.json` alignment) changes.

**Option 0 — No change (baseline).** Description stays as verified. What stays: everything. Rubric effect: none; distinctiveness stays at the reported 4/5; the false-positive surface (containers, ports, databases, generic parallel agents, any merge) remains. Context cost: 245 chars always loaded. Effort: zero. Regression risk: none. This is the honest comparison baseline; it is not manufacturing a change.

**Option A — Minimal append: keep current text, add one explicit exclusion clause.** 386 chars / 50 words:
> Manage Git worktrees for isolated or parallel development. Use when creating, listing, reusing, or removing worktrees; working in a separate checkout; integrating task branches; repairing moved checkouts; or pruning stale worktree registrations. Not for ordinary single-checkout branch, merge, or commit workflows, container isolation, port or database isolation, or independent clones.

Keeps all current trigger terms (5/5 quality preserved trivially) and adds the exclusion the reviewer implicitly asked for. Likely rubric effect: distinctiveness 4/5 → plausibly 5/5 without restructuring; conciseness slightly lower (body unchanged, metadata +141 chars). Risk: the overbroad trigger prefix "isolated or parallel development" still actively invites false activation before the exclusion is weighed; implicit positives ("hotfix while a colleague has uncommitted changes", "review a branch without disturbing my files") remain without direct support. Effort: one YAML line plus plugin.json alignment.

**Option B — Capability-anchored description with explicit exclusions (recommended).** 669 chars / 95 words:
> Manage Git worktrees (linked checkouts of one shared repository). Use when a task needs its own working directory alongside other active work: creating or reusing a task worktree, continuing one owned by this task, repairing a moved linked worktree, integrating a task branch, or removing a disposable checkout while preserving its branch. Select this for parallel agent edits to conflicting branches or files, hotfixes while another checkout has uncommitted changes, or reviewing another branch without disturbing current files. Not for plain branch switches, merges or commits, read-only parallel research, container isolation, ports/databases, or independent clones.

What changes: the leading hook is now the *capability* (a task needs its own working directory of the same repository) rather than the adjectives "isolated or parallel development". The full lifecycle (create/reuse/continue/repair/integrate/remove) is enumerated, so coverage claims in the skill body stay truthful. Two implicit-but-legitimate triggers are named verbatim. Clear negatives are explicit. What stays: every current worktree trigger term ("worktrees", "checkout", "integrating task branches", "repairing moved checkouts"→"repairing a moved linked worktree", "pruning stale worktree registrations" is folded into "removing a disposable checkout" — see risk note). Rubric effects: trigger quality preserved; distinctiveness improved by construction; conciseness of *metadata* drops modestly (95 vs 32 words) but the skill body, which carries the 4/5 conciseness note, is untouched. Context/execution cost: +424 chars in always-loaded skill index; body tokens and task-path tool calls unchanged. Regression risks: (1) "prune stale registrations" disappears as a literal phrase — pruning is a rare, late-stage case and the body still teaches it; if activation is observed missed on prune requests, add the phrase back. (2) Exclusions create false negatives if a user describes a worktree task using only excluded-sounding words (e.g., "isolate my build in a separate checkout" — not excluded, fine; but "parallel agents editing one shared checkout" would now be a correct negative). (3) Longer description metadata costs a small always-on token tax across every session using this plugin. Effort: two-line YAML edit + plugin.json alignment + routing-set test run.

**Option C — Compressed middle ground.** 318 chars / 45 words:
> Manage Git worktrees. Create, reuse, repair, integrate, and clean up linked task checkouts when work must proceed in a separate directory of the same repository: parallel agents, hotfixes alongside other uncommitted changes, branch review without disturbing files. Do not use for normal single-checkout Git operations.

Keeps the capability anchor and implicit-trigger support of B but drops the negatives for containers/ports/clones and the explicit negation beyond ordinary Git ops. Cheaper metadata, weaker distinctiveness improvement than B, and it still says "parallel agents" broadly, so read-only parallel research remains an ambiguous case. Use only if B's length is rejected.

## 4. Recommended option

**Option B**, with `plugin.json`'s `description` replaced by the same string. Rationale: the reviewer's distinctiveness note is specifically about *broad parallelism/isolation triggers*; only B removes the overbroad lead-in instead of appending exceptions to it, while preserving the enumerated lifecycle that makes current coverage claims accurate. A and C leave the lead-in or the ambiguity in place. "Managing" and "separate checkout" from the current text are subsumed; no glossary term needs to change, but the description must keep the words "worktree", "checkout", and "linked" so that an agent that saw the glossary (or the body) can map cases consistently.

Exact proposed YAML (proposal, not applied):

```yaml
description: >-
  Manage Git worktrees (linked checkouts of one shared repository). Use when a task
  needs its own working directory alongside other active work: creating or reusing a
  task worktree, continuing one owned by this task, repairing a moved linked worktree,
  integrating a task branch, or removing a disposable checkout while preserving its
  branch. Select this for parallel agent edits to conflicting branches or files, hotfixes
  while another checkout has uncommitted changes, or reviewing another branch without
  disturbing current files. Not for plain branch switches, merges or commits, read-only
  parallel research, container isolation, ports/databases, or independent clones.
```

Scope of patch: one YAML value in `skills/git-worktrees-prime/SKILL.md` frontmatter, one matching string in `skills/git-worktrees-prime/.tessl-plugin/plugin.json`. No body, glossary, SAFETY, eval, or packaging changes.

Most dangerous edges: false negative — "prune stale worktree registrations" no longer a literal trigger phrase (mitigate: keep body; revisit if missed). False positive — "hotfixes while another checkout has uncommitted changes" could over-trigger if the real fix never needs a second directory, but that is exactly the case the skill's own safety section adjudicates, so a false *activation* is cheap; a false *negative* would skip the preservation checks.

Evidence that would reverse this recommendation: if the routing-set test (Section 6) shows Candidate B misses ≥2 legitimate implicit cases that the current description catches, revert to Option A; if metadata token growth measurably hurts a Tessl run (unlikely; +424 chars), fall back to Option C.

## 5. Safety and semantic coverage check

No structural reorganization is proposed. The only affected instructions are the two `description` strings. Coverage mapping:

- All 13 SAFETY.md constraints remain verbatim in the skill's "Safety constraints" section; none is removed, weakened, or reordered. The description change neither adds nor removes safety behavior.
- The description still truthfully enumerates the lifecycle the body governs: create ("Use the harness to finalize…" + `worktree add`), reuse/continue ("Choose the checkout" step 1), repair (step 4 repair path), integrate ("Develop and integrate"), remove ("Cleanup decision tree"). "Prune stale worktree registrations" is the one body capability not literally named in Option B's description — flagged above as the main regression watch item, mitigated by keeping the body section and by "Not for…" not excluding it.
- Deliberate redundancy preserved: worktree-vs-branch separation, checkout-protection, and porcelain-parsing warnings appear in both body and safety section by design; the description does not duplicate them and should not.
- Terms kept consistent: "checkout", "linked worktree", "integration target" (as "integrating a task branch"), "task worktree". No glossary edit required.

## 6. Validation

Checks performed (results):

1. Live revision pinned: HEAD `a2117395…`; SKILL.md SHA-256 `01D156FD…451744`, 1,863 words — matches handoff; no newer bytes exist. ✅
2. Spec constraints checked against agentskills.io: description ≤1024 chars (candidates: current 245, A 386, B 669, C 318); name unchanged and valid. ✅
3. `plugin.json` drift recorded (Section 2). ✅
4. Vendor frontmatter sample inspected (10 skills): overlap confirmed via near-identical isolation/parallel phrasing; diagnosed need for scoped exclusions. ✅
5. Routing design check (hand-scored, not empirical): matrix below. Rows = required cases; C = current description routed by a reasonable agent, B = Option B.

| Case | Desired | Current desc. | Option B |
|---|---|---|---|
| Explicit create/remove/list worktrees | activate | activate | activate |
| Continue existing task-owned worktree | activate | activate ("reusing") | activate ("continuing one owned by this task") |
| Repair moved linked worktree | activate | activate ("repairing moved checkouts") | activate ("repairing a moved linked worktree") |
| Hotfix while colleague has uncommitted changes | activate | implicit; uncertain | activate (named verbatim) |
| Review another branch without disturbing files | activate | implicit; uncertain | activate (named verbatim) |
| Parallel agents, independent read-only research | do not activate | likely misfire ("parallel development") | excluded ("read-only parallel research") |
| Parallel agents editing conflicting branches/files | activate | activate | activate (named) |
| Port/database/process isolation | do not activate | likely misfire ("isolated") | excluded |
| Normal single-checkout commit/merge/branch switch | do not activate | likely misfire ("integrating task branches") | excluded |
| Cleanup of one disposable worktree, keep review branch | activate | activate | activate ("preserving its branch") |
| Independent clone / security boundary request | do not activate | possible misfire ("separate checkout") | excluded explicitly |

Hand-scoring only; this is a design check, not measured precision/recall, and no Tessl score is claimed.

Proposed future test (not run): a two-column activation trial — for each matrix case, present the prompt with (a) current description and (b) Option B description to the same agent configuration, record activate/skip/decline-with-reason. Success criteria: all 6 activate cases still activate; read-only parallel research, port/db isolation, plain branch ops, and clone-as-security-boundary no longer activate; no new false negative on the hotfix and branch-review implicit cases. Stop/revert criteria: any loss on the 6 required activations, or >1 lost implicit case, reverts to Option A; two consecutive Tessl regressions against the current baseline also revert.

## 7. Dependencies and boundaries

- Interacts with Investigation 01 (glossary) only through the shared terms "checkout", "linked worktree", "integration target"; no glossary change required or proposed from this topic. Investigations 03–05 (disclosure/packaging, phases, token attribution): the +424-char always-loaded description slightly raises the metadata budget; body/token-execution questions are theirs, not mine.
- Assumptions: the reviewed rubric's 4/5 distinctiveness note refers to the live description; plugin.json drift is real, not a staging artifact (verified file bytes).
- Subagents: none used for this report (the orchestrator's single-child, read-only bound was respected by simply not delegating). No peer challenge was run; the matrix above is my own design check.
- Unresolved: whether Tessl scores plugin.json's description or SKILL.md's (evidence absent); whether "prune stale registrations" must remain literally in the description (flagged as the top watch item); `SAFETY0.md` provenance not investigated.
