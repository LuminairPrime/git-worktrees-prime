# Investigation 3: progressive disclosure and skill packaging

## 1. Decision summary

**Recommendation: adopt Option B — a minimal two-reference split — after an offline vendoring/dry-run check, not as an immediate edit.**

Keep in `SKILL.md` everything that acts as a decision gate: the Glossary, the checkout/manager/starting-state gates, the ignore-coverage check (`check-ignore -q`, exit 0, trailing `/`, exclude-file resolution, re-verify after creation), the repair trigger and `git worktree repair` line for relocated live checkouts, the cleanup decision tree, the squash/rebase branch-deletion caveats, the completion report, and the entire "Safety constraints" bottom section verbatim. Move only (a) the two raw-Git command blocks ("Generic Git commands", "Inspect and remove with Git") into `references/raw-git-commands.md`, and (b) rarely conditioned advanced-operation detail (submodule constraints, filesystem-relocation mechanics, offline-storage lock/prune nuances, harness-archive caveats, `git config --worktree` migration and extension-compatibility details) into `references/advanced-operations.md`. Replace each moved block with an exact conditional read-trigger naming the file.

Why it matters: the live `SKILL.md` is 140 lines / 1,863 words and already fits the Agent Skills guideline (<500 lines, <5000-token body), so the benefit is not raw size — it is expected loaded context on the most common paths. Creation-with-harness-tools and listing-only drop from ~1,863 to ~1,450 words (~22%) because the raw-Git command prose and exceptions are read on demand. Safety routing improves because every prerequisite gate stays at its decision point; the bottom safety section stays inline as the non-circular backstop.

Expected impact: modeled, not measured — routine harness-managed paths save roughly 390 words of entrypoint context; a raw-Git path pays one extra tool call (~420 words) to read `references/raw-git-commands.md`; advanced paths pay one more read (~300 words). Total bundle grows ~18% due to trigger paragraphs and anchors. Distinctiveness/conciseness rubric items (4/5 findings) should hold or improve modestly; no score is promised.

Principal risk: a conditional-link trigger that an agent cannot recognize without having read the target file (circular routing), or a packaged evaluation copy that omits `references/`. Both are checkable before implementation by dry-walking the routing table below against a vendored copy.

Confidence: medium-high on structure, low on runtime token savings. **Defer implementation; run the validation in §6 first.** Retain-the-status-quo (Option A) remains the fallback if routing dry-runs show a missed gate.

## 2. Baseline and evidence

**Live revision (verified 2026-10-04):**

- HEAD: `f088f99862f0a1fbebe6953c4bc6c4e5c1c4d251` ("Add five skill-enhancement investigation reports"). At investigation time HEAD was `a2117395a18fb0db7608796a65c514ee528eb426` ("before research starts"); the handoff expected `73d21c77…`. `git log` shows `d839d62 changed terms to glossary`, `73d21c7 moving docs around`, `a211739 before research starts`, `f088f99 Add five skill-enhancement investigation reports`. Both newer commits touched only research reports, not the skill file, so the handoff's skill facts still hold.
- `skills/git-worktrees-prime/SKILL.md` SHA-256: `01d156fd90c69091875e4311cb2ef89d34d5e362c0b71a014e3d34440d451744` — matches the handoff value. 140 lines, 1,863 whitespace-delimited words (Python `str.split()`; matches handoff).
- `SAFETY.md` exists at repository root (15 lines, 13 constraints, lines 3–15), not inside the skill directory. `SAFETY0.md` is an older draft.

**Files examined:**

- `SAFETY.md` (root): thirteen constraints; wording differs slightly from the skill's bottom section.
- `docs/plans/integrate-safety-constraints.md` (verified present, 18,994 bytes) — earlier patch and coverage reasoning; treated as evidence, not a mandate.
- `docs/research/1.0-development/21-prototype-enhancements-and-verification.md`: path/ignore/repair instructions were added after observed failures in preserved trial repos (custom destinations unignored in r01/r03/r04/r05; moved adapter checkouts still registered at old paths in r03/r04/r06). This is why those gates must remain visible at the decision point.
- `skills/git-worktrees-prime/evals/scenario-0..4/` and `vendors/tessl_evals/scenario-{0,1,3,4}/with-skill/`: captured Tessl artifacts. The vendored `SKILL.md` copies there are 128 lines, 0 occurrences of "Safety constraints" — i.e., the **pre-safety skill version**. Therefore the user-reported review ratings (conciseness 4/5, progressive disclosure 4/5, the under-50-line top-score mention) characterize an older revision, not the live bytes. The ~26% token increase is unattributed to any specific section; no causal explanation exists in the artifacts.
- `tessl.json`: `{"name": "luminair/git-worktrees-prime", "mode": "vendored", "dependencies": {}}`. Vendored skill copies live only under `vendors/tessl_evals/scenario-{0,1,3,4}/with-skill/.tessl/plugins/luminair/git-worktrees-prime/` (scenario-2 has no `with-skill` copy — `vendors/tessl_evals/scenario-2/` exists but is an empty directory: no inputs, no artifacts, no `.tessl/` tree; no `.tessl/` tree exists at the repo root). Each contains `SKILL.md`, `.tessl-plugin/plugin.json`, `tessl-package.json`, and `tile.json`; `tile.json` names only `"git-worktrees-prime": {"path": "SKILL.md"}` under its `skills` key, but the whole plugin directory is copied. Highest-probability interpretation: a `references/` directory inside the skill directory is vendored alongside `SKILL.md`, so relative one-level-deep links resolve. This is not verified by a fixture containing `references/` — it is the first thing to falsify.
- Agent Rules files (`AGENTS.md`, `.tessl/RULES.md`, `CLAUDE.md`) — present only inside the vendored scenario `with-skill/` copies, not at the repo root — contain only generic "follow instructions" pointers; they do not inline the skill body, so activation loads `SKILL.md` in full.
- `tests/README.md`, `tests/results/`, `experiments/`, `tests/behavioral_trials.py`: historical GPT-6 Luna trials with frozen outcome criteria; `setup()` in `tests/behavioral_trials.py` (line ~158) hardcodes a read of `skills/prototype1-astra/SKILL.md`, a path that no longer exists (`skills/` contains only `git-worktrees-prime`), so re-running would fail outright with `FileNotFoundError` rather than reproduce any guide treatment. Not used for scoring.

**Specification facts (https://agentskills.io/specification, fetched 2026-10-04):**

- `SKILL.md` needs YAML frontmatter (`name`, `description`); body has no format restrictions; recommended <500 lines; body loaded in full on activation; `references/` is an optional conventional directory for on-demand files; keep file references one level deep; the "progressive disclosure" tiers are metadata → full SKILL.md → resources as needed. The 50-line top-score example from the Tessl review is a scoring anchor, **not** a spec requirement.

**Measurement method and honesty note:** word counts are whitespace-delimited; tokenizer counts differ (code fences tokenize denser than prose) and no tokenizer was run. No runtime data exists for the live skill. Nothing below converts a word reduction into a proven execution-token saving.

**Section-level live skill composition (words):** frontmatter+title 53; Glossary 226; Choose the checkout 110; Choose the manager and location 214; Establish the starting state 149; Generic Git commands 133; Develop and integrate 125; Cleanup decision tree 301; Inspect and remove with Git 254; Completion report 48; Safety constraints 250.

## 3. Options

### Option A — No change (baseline)

Everything stays in one 140-line file. Raw-Git blocks and advanced exceptions remain loaded by every activation. Zero implementation risk, zero packaging risk. Reviewer already rated conciseness 4/5 and progressive disclosure 4/5 with specific, actionable complaints: generic command blocks and some cleanup exceptions "might suit included reference files." Expected value: the classic determinism-versus-context trade — maximal determinism, maximal standing context cost.

### Option B — Minimal two-reference split (recommended)

- `SKILL.md` (~105–115 lines, ~1,450 words): all gates and decision procedures inline; safety section verbatim; glossary unchanged (terminology redesign is investigation 01's dependency; duplicating or redefining terms here would fork it).
- `references/raw-git-commands.md` (~420 words): the two command blocks, verbatim except adding file headers and the "substitute placeholders; run only the selected alternative" line.
- `references/advanced-operations.md` (~300 words): submodule limitations, relocation mechanics (`.git` preservation, `worktree repair`, inventory verification), offline-storage lock/prune, harness-archive semantics, `git config --worktree` migration, relative-path/extension compatibility, submodule-specific creation checks.
- No other new files. No per-edge-case files.

Trigger wording (exact candidates, §4). Rubric effects: conciseness likely holds or improves (body less dense on generic blocks); progressive disclosure should move toward 5/5 because there are two real conditional references instead of none; distinctiveness unaffected. Regression risks: trigger misrecognition, packaging omission, safety-gate loss if an editor trims inline duplication by accident. Effort: ~2–4 hours of careful rewriting plus one vendored dry-run.

### Option C — Phase/task-specific split

`references/create.md`, `references/integrate.md`, `references/cleanup.md`, `references/config.md`, `references/submodules.md`, maybe `references/archives.md`. Each phase file holds its gates + commands. Expected loaded context per task is slightly lower than B for narrow tasks (e.g., config change loads only config.md), but a routine creation+integration+cleanup lifecycle reads three files instead of two, and each file repeats anchor definitions (repository, checkout, registration, integration target) or links back — partial-glossary duplication either grows every file or forces circular cross-links. Trigger paragraphs multiply (one per operation instead of one per condition family). More files also mean more chances that a vendored copy, symlink, or UI truncates the bundle incompletely. Rubric upside is small because SKILL.md must still summarize all routes. Rejected except as a fallback if B's two files prove too coarse in dry-runs.

### Option D — Single merged `references/REFERENCE.md`

Moves the same content as B into one file. Fewer files, simpler trigger ("read references/REFERENCE.md before any raw-Git command or advanced operation"), but every raw-Git command now pays for the advanced-config text and vice versa. This is B with worse marginal cost on the common path. Not recommended; kept only to bound the comparison.

## 4. Recommended option (B) — exact routing

**Proposed tree:**

```
skills/git-worktrees-prime/
├── SKILL.md
├── .tessl-plugin/plugin.json
├── evals/…                          (unchanged)
└── references/
    ├── raw-git-commands.md
    └── advanced-operations.md
```

**Routing paragraph candidates (to be inserted in place of the moved sections):**

- After "Choose the manager and location", replace "### Generic Git commands" with:

  > **Raw Git commands.** If you are about to run any `git worktree …`, `git check-ignore`, `git merge-base`, or `git worktree prune` command yourself (no harness worktree tool applies, or as a supported fallback), read `references/raw-git-commands.md` first and run exactly one selected alternative. Substitute all placeholders. Do this before the first mutating command, not after an error. The in-line gates in the rest of this document still apply when you use the raw-Git path.

- Replace "### Inspect and remove with Git" with:

  > **Raw Git inspection/removal.** Before running `git worktree remove`, `branch -d`, or `worktree prune`, apply cleanup-decision-tree steps 1–6 above. For the exact commands (including the required dry-run prune and ancestry check), read `references/raw-git-commands.md`.

- Add one advanced-operations paragraph near the end of the manager/location section:

  > **Advanced or offline paths.** Read `references/advanced-operations.md` before acting when any of these holds: the repository has submodules or is a superproject; a live checkout was moved on disk; storage hosting a worktree is removable/network-mounted or may go offline; `git config --worktree` or `extensions.worktreeConfig` is involved; relative worktree paths are requested; a harness archive is the only preservation copy. The matching `DON'T` lines in "Safety constraints" below remain in force either way.

**What stays inline and why:** the check-ignore gate (it fires before creation, a recognizable condition), `git worktree repair` one-liner (fire it on the "moved checkout" trigger alongside the advanced-operations link; the one-liner stays visible so the trigger is never empty), prune dry-run discipline (in the cleanup tree), squash/rebase ancestry caveat (branch deletion), archive caveat (one sentence), completion-report requirements, and all thirteen safety lines verbatim.

**What intentionally disappears as content (moved, not deleted):** the two raw command blocks and the expanded config-migration prose. Nothing is deleted outright except possibly the duplicated "Substitute all placeholders. Run only the selected alternative." sentence, which now lives once at the top of `raw-git-commands.md` and once in the routing paragraph (deliberate, because each file is read through a different entry point).

**Deliberate duplication:** every advanced-operations reference carries a header naming the controlling `DON'T` bullets because a model that opens the reference directly still sees the constraint anchors; the full glossary stays only in SKILL.md, and references use — not redefine — its terms.

**Estimated costs:** main file ~1,450 words (−22%); bundle ~2,190 words (+18%) counting the two reference files plus new trigger paragraphs; routine harness creation/listing/integration paths read ~1,450; raw-Git creation/removal paths read ~1,870 (+1 tool call); moved-checkout repair / offline storage / config changes read ~1,750–2,170 depending on whether the raw-Git file is also needed; worst-case full read ≈ bundle size. These are size estimates, not token-consumption forecasts.

**Why B beats the alternatives:** A pays the exception cost on every activation and does not address the reviewer's specific note; C multiplies triggers and glossary maintenance for negligible additional specialization; D collapses both read triggers into one coarse file. B's two triggers are families with recognizable entry conditions, and both reference files are one level deep per the spec.

**Evidence that would reverse the recommendation:** a packaged Tessl run omitting `references/` (fix: vendoring doc update or fall back to A); dry-run routing failures where an agent skips the raw-Git file before mutating (fix: keep a 3-line minimal command excerpt inline, shrinking the split); or tokenizer measurements showing a harness-managed run with no word-count reduction (fix: accept A and document the no-change decision).

## 5. Safety and semantic coverage check

Mapping of the 13 constraints in `SAFETY.md` to the proposed bundle. Status key: **INLINE** = remains verbatim or substantively present in SKILL.md; **EXPANDED** = mechanics elaborated in a reference while the constraint statement stays inline in "Safety constraints".

| # | SAFETY.md constraint | Proposed location |
|---|---|---|
| 1 | No discard/bypass without user authorization for target and consequence | SKILL.md "Safety constraints" bullet (unchanged) + cleanup tree steps 3–5 (unchanged) |
| 2 | Verify repo, absolute path, branch/detached state, HEAD before remove/relocate/reset/clean; porcelain `-z` for scripts | Safety bullet unchanged; decision-tree step 4 unchanged |
| 3 | No `--force`, `worktree unlock`, filesystem ops without authorization, first attempt included; read lock reasons | Safety bullet unchanged; prune step 6 unchanged |
| 4 | No `worktree add -B` without authorization; use `-b` for creation | Safety bullet unchanged; raw-Git creation alternatives in `raw-git-commands.md` retain `-b` vs `-B` distinction |
| 5 | Preserve needed changes/untracked/ignored outside the worktree; anchor detached commits; clean status is not preservation | Cleanup step 3 unchanged; "Inspect and remove" prose moves with the block but keeps the preservation pointer; header repeats anchor terms |
| 6 | No filesystem deletion for routine cleanup; use `worktree remove`; main worktree not removable | Cleanup step 4 unchanged; `worktree remove` remains the documented path in the raw-Git reference |
| 7 | `worktree move` refusal is not permission for filesystem relocation; preserve `.git`; repair from main with new absolute paths; verify | Inline repair trigger + one-line repair command stays in SKILL.md; full mechanics EXPANDED in `advanced-operations.md` |
| 8 | Submodule constraints before create/relocate/remove; Git discourages multiple superproject worktrees | Inline manager bullet keeps the "check before assuming" pointer; EXPANDED in `advanced-operations.md` |
| 9 | Prune only reviewed dry-run entries; same expiry options; lock before offline | Cleanup step 6 unchanged; dry-run command text moves to `raw-git-commands.md` with the instruction intact; offline lock EXPANDED in `advanced-operations.md` |
| 10 | No assuming `git config --worktree` isolation without `extensions.worktreeConfig`; shared-vs-worktree config fields | Safety bullets unchanged; EXPANDED in `advanced-operations.md` |
| 11 | Migrate `core.worktree`/`core.bare` before enabling; never share them; share `core.sparseCheckout` only when uniform | Safety bullets unchanged; migration procedure EXPANDED in `advanced-operations.md` |
| 12 | No enabling `extensions.worktreeConfig`/relative paths without Git-version support across installations | Safety bullet unchanged |
| 13 | No editing refs/worktree metadata as files; use Git commands; `git rev-parse --git-path` | Safety bullet unchanged |

The bottom "Safety constraints" section of SKILL.md stays **verbatim**; no constraint text moves. The inline prose-redundancy between those bullets and the decision tree is deliberate in the source and remains deliberate — it is the backstop that makes the advanced-operations link non-circular (an agent can act safely even if it never reads the references).

Semantic anchors preserved across file boundaries: "checkout", "registration", "base / integration target", "main (primary) / linked worktree", and "detached HEAD" definitions remain only in SKILL.md's Glossary; references use these terms without redefining them. Critical distinctions that must survive the split: branch vs worktree path are named separately (glossary + completion report); prune ≠ remove ≠ branch deletion; archive ≠ deletion; repair ≠ prune. A relative-path check from a reference header back to SKILL.md terms is included in both reference files.

Dependencies on investigation 01 (glossary/shared vocabulary): if it trims the Glossary, the references' anchor line must be re-pointed to the trimmed definitions; no text is added here that would conflict.

## 6. Validation

**Already performed:**

- Verified live HEAD, git blob hash, SHA-256, line count, word count of SKILL.md against the handoff: all match except HEAD, which has since the handoff advanced by two docs-only commits (`a211739`, `f088f99`, both touching only research reports).
- Confirmed the captured Tessl artifacts contain a pre-safety skill copy (128 lines, no safety section) — used to qualify which revision the reported rubric scores describe.
- Confirmed vendored packaging layout, `tile.json`/`tessl-package.json`/`plugin.json` contents, and that `references/` would travel with the vendored plugin directory copy.
- Fetched the current Agent Skills spec; confirmed `references/` one level deep and <500-line guidance.
- Counted per-section words to size the split.
- Peer-review subagents attempted twice and failed (depth-limit errors); no reviewer output was produced, so this report carries no peer-review section content. Recorded here for honesty.

**Proposed, not performed (do not run as part of this investigation):**

1. **Packaging check:** copy `skills/git-worktrees-prime` to a scratch dir, add the two reference files, and inspect a vendored install layout to confirm `references/…` survives. (No skill-validator script exists in the repo as of this HEAD, so validate frontmatter and relative-link resolution manually.) Success: files present and links resolve from a fresh-clone-equivalent path.
2. **Routing dry-run (no model):** tabulate the mandated task paths — listing-only; creation with harness tools; creation with raw Git; detached inspection; reuse of existing checkout; ordinary removal; squash/rebase cleanup; harness archive; moved-checkout repair; offline storage; `git config --worktree` change — and for each, mark the last inline gate and exactly one read-trigger before any mutation. Success: every path has a trigger that fires before mutation; no trigger requires text from the reference to be recognized.
3. **Behavioral A/B (separate task, paid evals not authorized here):** vendor the restructured bundle into a *copy* of one Tessl scenario workspace (do not modify `vendors/` or `skills/`), run one model, count tool calls and input-token totals; success criterion: raw-Git and repair/config paths show identical safety checks with no missed gate; stop/revert criterion: any missed ignore/repair/prune gate, or creation path with zero word-count reduction, or token use ≥ baseline on all paths → revert to Option A.

No Tessl score or zero-regression claim is made. The 15–20-point delta and 26% token increase remain unattributed observations about a different skill revision.

## 7. Dependencies and boundaries

- **Investigation 01 (glossary/shared vocabulary):** strong dependency. If it shortens or restructures the Glossary, only SKILL.md's inline glossary changes; references consume its terms, so no edit to the references is needed unless terms are removed entirely.
- **Investigation on activation wording/trigger terms:** the description frontmatter and opening lines are untouched by this proposal; the broader distinctiveness (4/5) finding about broad parallelism triggers is out of scope here.
- **Investigation on concision:** B reduces density but does not rewrite prose; do not duplicate its work.
- **No implementation performed.** No files created except this report. Candidate layouts, link wording, and diffs live only in this document. Subagent delegation was attempted for peer review and failed twice; no nested delegation occurred.
- **Assumptions:** vendored Tessl installs copy the whole plugin directory (strong but unverified for a `references/` addition); harness tools remain unavailable in some environments, so raw-Git routing must keep working; models that read only entrypoint-named files are handled by naming both reference files explicitly in the routing paragraphs.
- **Open question for the user:** whether investigation 01's likely glossary trimming should land first, letting B's routing paragraphs reference the final term inventory. Recommendation: B is safe to implement without waiting, because it adds no new terms.
