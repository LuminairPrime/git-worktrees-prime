# Plan: integrate worktree safety constraints with bounded edits

## Status and boundaries

- Status: reviewed; author and GPT-6.1 Sol medium endorse the exact textual patch. Ready for the user's implementation decision, not yet implemented.
- Planned at: `9d4be20e52fa30b5d32e9b3cbf6ef8129cc539e8`, 2026-10-04.
- Repository: `C:/Users/MC/Documents/git-worktrees-prime`.
- Implementation target: `skills/git-worktrees-prime/SKILL.md` only.
- Preserve `SAFETY.md` and `SAFETY0.md` as development evidence; neither becomes a runtime dependency or linked reference.
- Keep frontmatter, glossary definitions, command examples, workflow order, and cleanup decision tree. Do not create a second safety reference, change packaging, rerun evaluation fixtures, commit, or publish.
- The user reports the current skill ranked highest among 30+ Tessl evaluations. That ranking was not independently reproduced here. Existing success is a reason for narrow edits, not proof that new edits are harmless.

## Objective and confidence rule

Append a compact `## Safety constraints` section after Completion report. Cover every fact in the 13 SAFETY.md constraints, either there or in the existing body. Preserve routine task-owned cleanup authority and the stronger existing prohibition against overriding branch checkout protection.

Only execute edits endorsed by both the author and reviewer after checking exact wording and coverage. Do not equate agreement, a valid skill file, or word counts with proven behavioral improvement or zero regression risk. If certainty means demonstrated unchanged model behavior, this plan alone cannot meet it; keep the current skill until a separately scoped behavioral evaluation is accepted.

## Baseline and drift

- Skill SHA-256: `DF4BD253AE6160981DBAAE77A45151521209D6BB9F182CD15AD47F7D011A6DCF`.
- SAFETY.md SHA-256: `A1938D2BEE998CE1F3BA9F233722C1AE5161CC75D61B176ED034AEF37CDA8B06`.
- Skill: 1,667 whitespace-delimited words. Safety source: 411 words.
- Worktree was clean at planning start. The native skill validator passed on the unchanged skill.

Before execution, run from the repository root:

```powershell
git diff 9d4be20e52fa30b5d32e9b3cbf6ef8129cc539e8 -- skills/git-worktrees-prime/SKILL.md SAFETY.md
Get-FileHash -LiteralPath 'skills/git-worktrees-prime/SKILL.md','SAFETY.md' -Algorithm SHA256
```

Expected: no source diff and the hashes above. If either source drifted, reconcile it before applying these anchors; do not overwrite newer edits.

## Constraint-by-constraint decisions

Numbers below match SAFETY.md's 13 bullets. S1-S9 refer to the proposed bottom section in order. Original line numbers are navigation aids; exact text anchors govern edits.

1. **Authorization — trim and retain in S1.** Existing body lines 81 and 87 already distinguish integration authority and routine disposable-resource cleanup. Keep both unchanged. S1 adds the missing distinction between user authorization and tool access or an agent's plan. It must not impose a new approval round on already-authorized work.
2. **Target verification and parsing — retain a compact S2.** Path and ownership checks at lines 26, 92, and 126 remain. S2 adds explicit hard-reset/clean coverage, branch-versus-detached state, HEAD commit, and NUL-delimited inventory for scripts. Existing `--porcelain` commands remain human/agent inspection examples; do not change them to NUL output indiscriminately.
3. **Safeguard overrides and locks — relocate the existing prohibition into S1.** Replace the paragraph at line 120 using B3 below. S1 applies to safeguard bypasses regardless of whether an earlier command refused; read the lock reason. Absence of a reason supplies no authorization. Preserve the supported-removal-method sentence in the body and the absolute branch-checkout guard at line 48. S1 repeats that stronger guard intentionally so its general authorization exception cannot weaken it.
4. **`-B` branch reset — add S3.** The existing `-b` example stays unchanged. The warning is valuable because `-B` can reset an existing branch without a preceding refusal. Name the branch and selected commit in the authorization condition.
5. **Preservation — omit a separate bottom bullet; keep detailed body coverage.** Lines 49, 91, 100-103 already require anchoring valuable detached commits, inspecting tracked/untracked/ignored state and unfinished operations, handling submodules/nested repositories, preserving outside the deletion path, or obtaining discard authority. They also distinguish reproducible build products. Do not shorten any of these instructions or add an obligation to preserve attached commits when their existing branch is retained.
6. **Filesystem deletion and primary protection — omit a separate bottom bullet.** Lines 36 and 92 already require the manager or raw Git, exclude the primary checkout and neighboring paths, and protect managed lifecycle behavior. S1 retains the prohibition on using filesystem operations to bypass guards. No blanket rule may displace a supported harness cleanup tool.
7. **Filesystem relocation and repair — retain the exceptional details in S4.** Keep the evidence-backed positive repair command and re-list check at line 37 intact. S4 adds complete-content preservation and the main/submodule move limitations, plus the repair execution location when the main/bare repository itself moved. The existing manager-first rule still applies; this does not authorize a filesystem move or assert that repair solves submodule-specific layout problems.
8. **Submodules — add S5; retain cleanup coverage.** The existing body covers submodule state before deletion and potentially different removal methods. S5 fills the creation/relocation gap and preserves Git's recommendation against multiple superproject worktrees. It is a limitation check, not an invented absolute Git prohibition or new blanket approval gate.
9. **Prune and offline storage — trim to S6.** Keep the stronger existing requirement that every dry-run entry is intentionally removed, the ban on pruning/unlocking unavailable storage, and repair-versus-prune separation (lines 37, 94, 113-115). Add only matching expiry options and locking intermittently mounted worktrees before disconnection. Do not propose routine pruning.
10. **Shared state and configuration — retain only the configuration trap in S7.** The glossary establishes per-worktree HEAD/index, and line 30 explains shared refs/configuration. A branch reset affecting a shared branch follows from those definitions; do not repeat the explanation. Add the non-obvious `git config --worktree` fallback to shared configuration without the extension.
11. **Configuration migration — add the rest of S7.** Preserve the supplied documentation's instruction to migrate existing `core.worktree` and `core.bare` settings; do not silently narrow it to only `core.bare=true`. Keep the distinct prohibition on shared `core.worktree`/`core.bare=true` and the all-worktrees condition for shared sparse checkout. This is a guard for a requested configuration change, not a suggestion to enable the extension.
12. **Compatibility — add S8.** Keep the condition on all Git installations that must access this repository; do not require auditing unrelated Git installations. Cover both the worktree configuration extension and relative worktree paths.
13. **Git internals — add S9.** Keep existing `rev-parse --git-path` use at line 39. S9 generalizes it and prohibits raw ref/metadata edits. Do not prohibit legitimate Git configuration commands or treat resolved paths as permission to edit metadata directly.

## Exact body edits and space trade

Apply only B1-B4, followed by the bottom section. Exact prose is specified because wording and reviewability are the deliverable; do not regenerate the skill.

### B1

Replace this exact text:

```text
Create, choose, use, integrate, and retire task worktrees.
```

With an empty string; remove the following space and retain the rest of that paragraph.

B1 justification: the lifecycle inventory repeats the frontmatter and section headings. Retain the following user-instructions/conventions/ownership sentence verbatim.

### B2

Replace this exact text:

```text
One repository can have several worktrees on different branches or detached commits.
```

With an empty string; remove the following space and retain the rest of that paragraph.

B2 justification: multiple worktrees and branch/detached alternatives remain explicit in the glossary, selection workflow, and commands. Preserve the following branch-retention and naming sentences verbatim.

### B3

Replace this exact text:

```text
- Do not add `--force`, reset changes, unlock a worktree, or recursively delete its directory merely to overcome a refusal. Resolve the cause; submodules and managed checkouts may require another supported removal method.
```

With:

```text
- Submodules and managed checkouts may require another supported removal method.
```

B3 justification: move the guard to S1 while retaining its supported-method caveat here. This is relocation and clarification, not removal of the protection.

### B4

Replace this exact text:

```text
State the work and checks completed, the integration or review status, and which checkout, branches, or archives were removed or retained. Include paths or refs only where they help locate remaining work.
```

With:

```text
Report completed work and checks, integration/review status, and removed or retained checkouts, branches, or archives. Include paths/refs useful for locating remaining work.
```

B4 justification: shorten the report wording without dropping completed work/checks, integration/review state, resource disposition, or locatable remaining work. The existing cleanup verification still requires reasons for retention.

## Exact proposed bottom section

Append the following after the final Completion report paragraph. Do not insert per-rule rationale or links to SAFETY.md into the skill.

```markdown
## Safety constraints

- DON'T discard work or bypass safeguards without user authorization for the target and consequence; tool access and agent-written plans confer none. Resolve safeguard causes before using force flags, resets, unlocking, or filesystem operations. Read lock reasons. Never override branch checkout protection.
- DON'T remove or relocate worktrees, hard-reset, or clean files without verifying the repository, absolute path, branch name (or detached state), and HEAD commit. Scripts must parse `git worktree list --porcelain -z`.
- DON'T use `git worktree add -B` unless resetting the named branch to the selected commit is authorized; use `-b` for creation.
- DON'T relocate through filesystem tools without preserving `.git` and contents, repairing from the current main/bare repository with new absolute linked-worktree paths, and verifying inventory. `git worktree move` cannot move main or submodule-containing worktrees.
- DON'T create or relocate superproject worktrees without checking submodule limitations; multiple superproject checkouts are discouraged.
- DON'T prune with different expiry options from the reviewed dry run. Lock worktrees on intermittently mounted storage before it goes offline.
- DON'T expect `git config --worktree` isolation unless `extensions.worktreeConfig` is enabled. Before enabling it, migrate existing `core.worktree` and `core.bare` to the main worktree's `config.worktree`; never share `core.worktree` or `core.bare=true`, and share `core.sparseCheckout` only when all worktrees use sparse checkout.
- DON'T enable `extensions.worktreeConfig` or relative worktree paths unless all required Git installations support the resulting extensions.
- DON'T edit refs or worktree metadata as files; use Git commands and resolve paths with `git rev-parse --git-path` from the target worktree.
```

## Size and preserved content

- B1-B4 recover 52 words: body 1,667 -> 1,615.
- New section including its heading adds 250 words: projected total 1,865, a net increase of 198 words (11.9%).
- This is a bounded increase, not a claim of size neutrality. If that cost is unacceptable, defer the change rather than remove unique safeguards to hit a number.
- Do not add other trims or additions during execution. Reviewer-backed revisions must amend this plan and recount the projection before implementation.
- Do not alter the seven glossary entries, task-owned cleanup authority, exact-path/ownership exclusions, review-before-merge retention rules, separate branch deletion checks, archive caveats, manager selection, integration checks, or any command example.
- Specifically protect the inventory/path check, actual destination ignore probe with trailing slash and exit 0, before/after ignore verification, positive repair command and re-listing, and final readiness checks. These were added following observed failures; see `docs/research/21-prototype-enhancements-and-verification.md`.

## Execution and verification

1. Confirm implementation authorization and baseline hashes. Check the recorded reviewer verdict and any amendments. If disputed wording remains, do not execute that edit.
2. Apply B1-B4 by exact matches and append the reviewed section once. Review `git diff -- skills/git-worktrees-prime/SKILL.md`; changes must be limited to those hunks.
3. Run the checks below, then perform the constraint coverage review against items 1-13. A text validator cannot establish semantic coverage or safety.

```powershell
python 'C:\Users\MC\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'skills\git-worktrees-prime'
git diff --check
$taskSkillText = Get-Content -LiteralPath 'skills\git-worktrees-prime\SKILL.md' -Raw
([regex]::Matches($taskSkillText, '\S+')).Count
git diff --stat -- skills/git-worktrees-prime/SKILL.md
git status --short
```

Expected: validator prints `Skill is valid!`; whitespace check exits 0; count equals the reviewed projection (currently 1,865); source changes are limited to the skill. The plan file may already be untracked from planning. The interpreter and validator command were verified on the baseline.

4. Have the reviewer inspect the actual diff against this plan before treating implementation as accepted. Report the exact word delta, unchanged command examples, coverage, and any remaining concern. Stop on a substantive disagreement instead of claiming consensus.

### Semantic checks

- Ordinary authorized cleanup stays executable without redundant permission requests; uncertain authority or loss still blocks the destructive step.
- No first-attempt force flag, unlock, filesystem deletion, or relocation evades the guard; general override authorization never permits duplicate branch checkout.
- Needed ignored data and detached work survive removal; generated outputs do not require needless preservation; an open review can retain its branch without retaining an unnecessary checkout.
- A relocated live tree is repaired and re-listed, not pruned; offline entries survive; custom prune expiry is previewed consistently.
- Main/bare relocation, submodules, metadata edits, configuration scope/migration, and compatibility have explicit constraints without becoming mandatory setup work.
- Commands intended for inspection remain usable; machine parsing is explicitly NUL-safe.

No new automated tests or model trials are required for drafting this plan. Do not run `tests/behavioral_trials.py setup` or repurpose existing preserved trials: their instructions and results are historical evidence, not tests of this candidate. `tests/README.md` and research21 explicitly limit what they establish. Fresh model trials or Tessl evaluation require a separately scoped run; if improved scores or zero behavioral regression must be demonstrated before adoption, keep implementation provisional until that evidence exists.

## Evidence

- Live sources: `skills/git-worktrees-prime/SKILL.md` and `SAFETY.md` at the hashes above.
- Git facts: `vendors/official-git-worktree-doc.md`, especially lines 73-88 (moves/repair), 180-196 (configuration migration), 294-297 (compatibility/submodules). These agree with the official documentation already checked during SAFETY.md development.
- `git config --worktree` fallback: https://git-scm.com/docs/git-config#Documentation/git-config.txt---worktree (verified during the preceding review; not inferred from the option's name).
- Historical preservation/behavior evidence: `tests/README.md` and `docs/research/21-prototype-enhancements-and-verification.md`. Do not claim this plan has repeated or improved the user's reported Tessl ranking.

## Stop conditions and handback

Stop if source hashes/anchors differ, a proposed deletion loses a unique constraint, authority rules conflict, a Git claim cannot be substantiated, reviewer and author disagree, or the diff exceeds the reviewed edits/word budget. Leave unrelated files untouched. Write a short `memo-safety-constraints.md` beside this plan describing current state, disputed point, and evidence needed; do not invent a broader rewrite.

## Independent review record

The fresh GPT-6.1 Sol medium reviewer read this plan, the skill, SAFETY.md, and the cited vendored Git documentation. No files were modified and no lifecycle commands or model trials were run.

- Initial verdict: changes required. S1 covered authorization for safeguard bypasses but omitted authorization for ordinary discards such as a hard reset or clean with no safeguard. The author verified and accepted this finding; S1 now explicitly covers both discard and bypass authorization, using the reviewer's proposed wording.
- The reviewer endorsed the other twelve coverage decisions and B1, B2, and B4; B3 was conditional on the S1 correction. It independently reproduced the initial 1,864-word projection.
- Optional suggestion to repeat that an absent lock reason is not permission was not added: the corrected authorization condition already supplies that constraint, and no reason cannot satisfy it.
- Confidence: high in the identified defect and counts, moderate-high in the remaining textual assessment. Neither reviewer nor author claims that static review proves unchanged model behavior or evaluation scores.
- Follow-up verdict: accept for textual implementation. The reviewer explicitly endorsed revised S1-S9 and B1-B4, found no remaining verified concern, and confirmed the 250-word section and 1,865-word projection. Confidence remains high in the correction/counts and moderate-high in the overall textual assessment; actual diff review is still required after implementation.
- Author verification: reconstructed the candidate in memory from the plan's four unique anchors and appended section. Confirmed 1,865 words, identical shell command blocks and glossary definitions, one bottom safety section, and no trailing whitespace in this plan. The live skill SHA-256 still matches the baseline. No candidate file, skill edit, lifecycle operation, or behavioral test was performed.
