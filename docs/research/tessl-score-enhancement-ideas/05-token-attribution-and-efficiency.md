# Investigation 5: token accounting, causal attribution, and efficient completion

Date: 2026-10-04. Investigator: subagent session. Status: read-only investigation; no skill or config edits.

## 1. Decision summary

**Recommendation: defer any skill edit. The honest reading of the available evidence is that the reported ~26% token overhead has no established cause, and no change to `SKILL.md` can be defended as a token saving until the raw Tessl usage records are recovered. Make "capture and attribute the overhead" the next piece of work, not a glossary shrink, not a safety-section trim, and not a phase-skip clause.**

Why: after inventorying the repository, the reported 26% / ~200,000 tokens / 15–20 points are user-reported observations only. I could not match them to any stored artifact. `vendors/tessl_evals/` contains five scenario directories with `with-skill` / `without-skill` fixture snapshots (`.agents`, `.claude`, `.tessl`, fixture repos, criterion files) but no usage JSON, message logs, tool-call traces, or scores. ripgrep over `vendors/tessl_evals`, `skills/git-worktrees-prime/evals`, and `tests` finds no token or usage fields except an unrelated Git Trace2 error mentioning `usage.c`. Local trials (`tests/results/`, `experiments/`) record commands, transcripts, wall-clock minutes, and state-based pass/fail — never model token counts. With zero denominator and zero numerator, every candidate explanation (glossary, safety block, document length, extra turns, larger tool outputs, repeated verification) is currently unfalsifiable.

Expected impact if the recommendation is followed: no quality regression and no fake saving; the first future edit can be aimed at the measured cost driver instead of the most visible one. Principal risk of the alternative (editing on vibes): the skill's reported 5/5 actionability and the 15–20 point quality gap are the only measured advantages it has; conciseness edits could trade them away while buying nothing, because the overhead may live outside the skill bytes (extra turns, tool-output volume, retries) entirely.

Confidence: high that the overhead is unattributed; moderate that a measurement-first step is the right next action. Decision: **test first / defer** — do not implement a prose patch now. If the user wants forward motion regardless, the lowest-risk conditional option (B, moving the two generic command blocks into `references/`) is the only one I would call prospectively safe, and only after the usage artifact shows prompt-size share of the overhead. I attempted one peer-review subagent; the environment rejected it with a depth-limit error (`experimental.subagent_depth`), so no independent review is recorded.

## 2. Baseline and evidence

### Verified live state (checked 2026-10-04)

- HEAD: `f088f99` ("Add five skill-enhancement investigation reports") at re-verification. At first verification HEAD was `a2117395` ("before research starts"); the handoff commit `73d21c7` is two commits behind `f088f99` (one behind `a2117395`). The skill bytes are unchanged across all three.
- `skills/git-worktrees-prime/SKILL.md`: SHA-256 `01D156FD90C69091875E4311CB2EF89D34D5E362C0B71A014E3D34440D451744` — matches the handoff identifier exactly, so the structural claims below apply to the evaluated bytes.
- Size: 140 lines, 12,802 bytes, 1,863 non-empty whitespace-delimited "words" (PowerShell `(Get-Content -Raw) -split '\s+'` yields 1,864 elements including one empty string from the trailing newline; non-empty count is 1,863; method limitation: whitespace-delimited words, not tokenizer output; markdown table cells, placeholders, and code tokens each count differently across tokenizers, so 1,863 words is not a token count).
- Structure (line citations to the live file): frontmatter (1–4), `# Git worktrees` (6), Glossary table (10–22), Choose the checkout (24–30), Choose the manager and location (32–39), Establish the starting state (41–49), Generic Git commands block (51–75), Develop and integrate (77–83), Cleanup decision tree (85–95), Inspect and remove with Git block (97–122), Completion report (124–128), Safety constraints (130–140).
- `tessl.json`: `{ "name": "luminair/git-worktrees-prime", "mode": "vendored", "dependencies": {} }`.
- `SAFETY.md`: 15 lines, 13 `DON'T` constraints (lines 3–15). Line 133's "scripts must use `git worktree list --porcelain -z`" appears in the skill as "Scripts must parse `git worktree list --porcelain -z`" (line 133) — the skill states the requirement, not the exact same flag form as the source line (`-z` present in both); no contradiction established.

### Evidence inventory and provenance

| Source | What it contains | Comparable to the reported run? |
|---|---|---|
| `vendors/tessl_evals/scenario-{0..4}/{with-skill,without-skill}/` | Fixture repos, `AGENTS.md`/`CLAUDE.md`/`.tessl/RULES.md` copies, setup scripts, outcome files (`cleanup-report.md`, `repair-report.md`) | No: no usage, messages, model, settings, or scores |
| `skills/git-worktrees-prime/evals/scenario-{0..4}/` | `task.md`, `scenario.json`, `criteria.json`, setup scripts | Definitions only; schools/fixtures, not results |
| `tests/results/`, `tests/.runs/`, `tests/README.md` | Luna behavioral trials: command logs, transcripts, verified outcomes, agent summaries | Local GPT-6 screen; no token fields; not the Tessl run |
| `experiments/` (rounds 1–4), `experiments/analysis/command-efficiency.md`, `experiments/analysis/quality-report.md` | ours-vs-prp command counts and minutes; no token data | Separate local trials; do not merge numerically with Tessl claims |
| `docs/research/1.0-development/21-prototype-enhancements-and-verification.md`, `22-publication-review.md`, `docs/plans/integrate-safety-constraints.md` | Earlier decisions and rationale; Tessl docs reviewed but no measured score stored | Context only |
| User-reported observations | ~15–20 points above control; ~26% more tokens (~200k extra); 5/5 on five dimensions; 4/5 conciseness, progressive disclosure, distinctiveness | Unverifiable against any stored artifact |

### Missing evidence, stated exactly

Not present anywhere in the repo: (a) per-case token usage for with-skill and without-skill conditions; (b) the definition of the reported token metric (input vs output vs cached vs reasoning vs tool-output); (c) model name, temperature/max-token settings, evaluator version; (d) raw message histories or tool-call lists from the evaluated runs; (e) the aggregation method behind "26%"; (f) the 0–100 subscores behind "15–20 points"; (g) whether numerator and denominator cases, tasks, and settings matched. Absent these, I do not attribute any part of the 26% to the skill's bytes, and I do not divide extra tokens by score.

## 3. Options

No-change is the comparison baseline, listed first.

**Option 0 — No-change (baseline).** Keep `SKILL.md` at the verified 1,863-word/140-line state. Rubric effect: none, preserves the reported 5/5 clarity dimensions and the only measured quality advantage. Cost effect: keeps the unexplained ~26% overhead in place. Risk: none new. Effort: zero. This is the correct choice while the overhead's denominator is unknown.

**Option A — Measurement-first (no prose change).** Change only process: recover the raw Tessl usage fields (Section 6 names them) and build the provenance table. If, as expected, the artifact exists on the Tessl side, rerun analysis offline. Likely rubric effect: none. Cost effect: none directly; it is the prerequisite that makes any later saving claimable rather than speculative. Regression risk: none to the skill. Effort: one data pull plus a small join. This option is mandatory regardless of which skill option is chosen later.

**Option B — Move generic command blocks and generic glossary rows into `references/` (low-change, conditional).** Candidate move: the two shell blocks at lines 55–75 and 99–116 into `references/commands.md` with conditional links at lines 51–53 and 97–99 (e.g., "Run the matching block from `references/commands.md`; substitute all placeholders"), and the glossary rows that restate already-known Git basics (lines 14–17: Repository, Branch, `HEAD`/detached) into `references/glossary-basics.md`, keeping the skill-specific rows (`<primary-root>`, Base vs integration target, Registration, checkout-as-noun) inline (note: the "the noun **checkout** means this workspace" sentence inside the line-15 Worktree/checkout row would stay inline even as that row's generic portion moves). SKILL.md would shrink by roughly 320 words (counted: 109 + 108 in the two shell blocks, 105 in glossary rows 14–17); total bundle size is unchanged. Mechanism: pure prompt-size reduction on the loaded path. Rubric risk: the reviewer praised navigation of the single file; splitting could cost the progressive-disclosure 4/5 if links are not clearly conditional, or gain it if blocks are the only thing moved. Cost risk: zero behavioral change expected, but a more complete run can also mean more tokens — B does not fix turns, tool outputs, or retries. Safety check: all command semantics and all 13 SAFETY.md constraints stay reachable; only layout moves. Effort: one restructure pass plus link-text discipline. **This is the only prose-change option I consider prospectively safe before usage data, and even it should wait for Option A.**

**Option C — Phase-gating / conditional execution (rejected as proposed).** Add explicit skip conditions so small creation-only tasks skip parts of the cleanup decision tree or the starting-state checks. Mechanism: cuts repeated verification tokens. Rubric/safety risk: high. The cleanup tree is where instruction-following failures would pay off in the evaluation's safety dimensions; the local Luna protocol treats those checks as the task. C converts a rubric strength into a token saving by deleting safety work — exactly the trade the assignment forbids treating as efficiency. Reclassified as "do not propose without evidence that those phases are currently over-executed on creation-only tasks," which does not exist (local command logs show 0 retries and task-appropriate `check-ignore`/`prune` counts; ours ran `check-ignore` 30× over 6 runs because the guide demands proof, not because agents dawdle).

**Option D — De-duplicate overlapping statements across body and bottom safety section.** Some statements repeat: absolute-path repair (lines 37 vs 132–133 coverage), `check-ignore` gating (lines 39, 60), prune-dry-run-first (lines 94, 113–115). Keep the operational statement at first use and the short invariant in the bottom section; do not delete any constraint. Mechanism: small prompt-size saving (tens of words). Risk: repetition between body and bottom section is deliberate safety redundancy per the assignment; deduplicating could weaken exactly the invariant-carrying statements. Rubric effect: negligible. Effort: small. Verdict: not worth the safety-review surface for its expected saving.

For attribution clarity, the three genuinely different directions were B (size of loaded prompt), C (volume of executed phases), D (textual redundancy); A is the process gate that must precede all of them; 0 is the baseline. I did not manufacture a safety weakening, a glossary deletion, or a "shorter is better" rewrite to fill the quota.

## 4. Recommended option: A — measurement-first, with B held in reserve

I recommend **Option A now; Option B only if the recovered usage data shows the loaded skill bytes are a material share of the overhead; Option 0 otherwise.** Recommendation mechanics:

- **Exact next artifact:** the Tessl run's per-case usage export for with-skill and without-skill (input_tokens, cached_input_tokens, output_tokens, reasoning/thinking tokens if exposed, tool-output/context size, message count, tool-call count, per-case duration, pass/fail, and the evaluated `SKILL.md` SHA for each run).
- **Smallest justifying evaluation:** a paired rerun of the existing five `evals/scenario-*` fixtures, with-skill vs without-skill, fixed model and settings, recording the fields above plus both safety failures and outcome checks. Fixed task set, fixed model, fixed max-tokens; report totals and per-case ratios; pre-register the comparison.
- **Reverse condition:** if the usage data shows the overhead is concentrated in turns/tool outputs rather than prompt size, B loses and 0 holds; if it shows the skill prompt is loaded many times but nearly all of it goes unused per task, a references split (B) becomes implementable with a candidate patch.
- **Candidate minimal diff for B (proposal only, no files created):**

```diff
@@ line 51 @@
-### Generic Git commands
-
-Substitute all placeholders. Run only the selected alternative. ...
-
-```sh
-... (full block at lines 55–75)
-```
+### Generic Git commands
+
+Substitute all placeholders. Run only the selected alternative. `<repo>` is an
+existing checkout; `<worktree>` is the task's exact absolute path. Run the
+matching block from `references/commands-generic.md` — load it only when a
+raw-Git command is actually needed.
```

```diff
@@ line 97 @@
-### Inspect and remove with Git
+### Inspect and remove with Git
 
 ```sh
-(lines 99–116)
+... (moved to references/commands-cleanup.md)
 ```
```

Plus `references/glossary-basics.md` holding lines 14–17. The `## Safety constraints` section and every decision-tree invariant stay byte-identical. Expected saving: roughly 320 whitespace-delimited words of the 1,863-word body come off the always-loaded path; total repo size unchanged; behavior expected unchanged. I claim no token reduction from this — a word cut is not a measured token cut, and this agent has no applicable tokenizer dependency available (no transformers/tiktoken install is permitted here).

- **Why A beats B now:** B's mechanism is speculative until the denominator is known; the 26% might dwarf anything a ~320-word move can explain. Scale check: 322 words is ~17% of the 1,863-word skill body, and the skill body is only one component of total run tokens (turns, tool outputs, retries — all unmeasured), so B's ceiling sits far below a 26%-of-total-run saving unless the skill is re-loaded per turn many times, which is itself unmeasured. A costs little and, if the records exist only on the Tessl side, converts an unfalsifiable complaint into an attributable one.

## 5. Safety and semantic coverage check

All thirteen SAFETY.md constraints, and where the live skill or my proposals touch them:

| # | SAFETY.md constraint (condensed) | Live skill coverage | Affected by my recommendation? |
|---|---|---|---|
| 1 | No discarding/bypassing without explicit authorization | lines 132, 87–88, 93 | No |
| 2 | Verify repo, abs path, branch, HEAD before destructive ops; parse `porcelain -z` | lines 26, 37, 92, 94, 133 | No |
| 3 | No `--force`/unlock/fs ops without authorization; read lock reason | lines 132, 94 | No |
| 4 | No `add -B`; use `-b` | line 134 | No |
| 5 | Preserve changes/untracked/ignored files before removal; anchor detached commits | lines 49, 91–93, 100–102, 119 | No (B moves the verifying command block's location, not its semantics; the decision-tree requirement to inspect before removing remains inline at lines 91–94) |
| 6 | Use `git worktree remove`, not fs delete; main worktree not removable | lines 92, 109, 120, 122 | No (script move leaves the command and the invariant text intact) |
| 7 | No `git worktree move` refusal ⇒ fs relocation; repair with absolute paths | lines 37, 135 | No |
| 8 | Submodule constraints for create/relocate/remove; avoid superproject multi-checkout | lines 94 (nested repos), 136, 120 | No |
| 9 | No pruning without establishing removal; review dry-run with same expiry; lock offline/removable storage | lines 94, 113–115, 137 | No |
| 10 | No assumption of config isolation without `extensions.worktreeConfig` | line 138 | No |
| 11 | Migrate `core.worktree`/`core.bare` before enabling the extension; never share them | lines 138–139 | No |
| 12 | Only enable worktree extensions when all needed Git installs support them | lines 139, 136 (submodule case) | No |
| 13 | Edit refs via Git commands; resolve paths with `git rev-parse --git-path` | lines 110, 140, plus `.git` file note at line 39 | No |

Confirmed: no constraint is removed, reworded, or silently weakened by any option I recommend. A removes nothing. B relocates the two command blocks and four glossary rows; every imperative sentence around them stays in the skill body, and the moved rows remain reachable via the inline pointer. Options C and D were rejected partly because they would touch constraints 2, 3, 5, 9, 13.

Deliberate repetitions I identified and will NOT deduplicate: absolute-path repair appears in both the manager-selection section (line 37) and the safety section (line 133); prune-dry-run-first appears in the decision tree (line 94) and in the cleanup script comment (line 113); `check-ignore` gating appears inline (line 39) and as a command comment (line 60). These are the safety-invariant repeats the brief explicitly preserves.

## 6. Validation

Checks already performed (this session):

- Verified live HEAD `a2117395` and recomputed the skill SHA-256 — matches the handoff identifier `01D156FD…451744`; no stale-version risk in the analysis above. Re-verified during peer review (2026-10-04): HEAD is now `f088f99`, which contains this report; the SKILL.md SHA-256 recomputes identically, so all line citations still hold.
- Word count: 1,863 non-empty whitespace-delimited words via PowerShell `-split` (1,864 elements including the trailing-newline empty string); recorded method and limitation inline (not a tokenizer count). No tokenizer dependency was available or installed.
- Exhaustive-ish search for token/usage artifacts: ripgrep across the repo for `token|usage|tokens` (excluding `vendors/**` noise) and inside `vendors/tessl_evals`, `skills/git-worktrees-prime/evals`, `tests` — only Git Trace2 error text and prose mentions; no usage JSON or run metrics exist locally.
- Read `tessl.json`, `SAFETY.md` (13 constraints), the live `SKILL.md` in full, `experiments/README.md`, `experiments/analysis/command-efficiency.md`, `tests/README.md`, and skimmed `docs/research/1.0-development/22-publication-review.md` for stored Tessl results (none — it states no score was predicted or stored).
- Attempted one peer-review subagent; environment returned `tool.execution ... Subagent depth limit reached (1)`. No peer review was performed. My self-challenge of the causal claims is recorded in Section 3 (0/A/B/C/D challenged against the artifact inventory).
- Second independent review pass (2026-10-04, HEAD still `f088f99`, SKILL.md SHA-256 recomputed identical): confirmed zero usage/token artifacts across `vendors/tessl_evals`, `skills/git-worktrees-prime/evals`, `tests`, and `experiments` (only unrelated hits: Git Trace2 `usage.c` error text in `tests/results/*/git-events.jsonl` and CLI-count prose using "tokens" for `uv run` invocations in `experiments/analysis/command-efficiency.md`); confirmed SKILL.md byte-identical across `73d21c7`/`a211739`/`f088f99`; recomputed Option B at 109 + 108 + 105 = 322 words and fixed the one stale "600-word" remnant in Section 4; verified the `check-ignore` 30× and zero-retry citations against `command-efficiency.md` rounds 1–2. Conclusion unchanged.

Not performed (by design): no Tessl runs, no fixture resets, no evaluator edits, no dependency installs, no worktree/branch/commit changes.

Proposed future comparison that isolates the change, if a change is later adopted (B):

- Fixed: model, temperature, max-tokens, the five `evals/scenario-*` tasks, with-skill vs without-skill.
- Variables: one skill variant (B-restructure) vs the current bytes, same frontmatter/name/description.
- Report per case: pass/fail on the state-based criteria, any safety failure, wall-clock, command count, and the usage fields in Section 4.
- Success criterion: outcome parity (no lost task, no new safety failure) and a measurable reduction in the loaded-prompt share of total tokens. Not a promise of a Tessl score or zero regression.
- Stop/revert criterion: any lost scenario outcome, any new unsafe shortcut, or no perceptible reduction in prompt-size share across the paired cases reverts B to 0.

## 7. Dependencies and boundaries

- **Other investigators.** A Glossary/shared-vocabulary revision (01) overlaps B's glossary rows; a progressive-disclosure/packaging revision (03) overlaps B's references move; an activation-boundary revision (02) owns description-text changes; a task-phases/execution-discipline revision (04) owns any phase-gating (C). My recommendation does not depend on their adopting or rejecting anything; B explicitly defers to whoever owns packaging.
- **Assumptions.** The user-reported 26%/~200k/15–20-points stand as approximate claims; I treated them as unverified because no artifact stores them. The Luna trials and command-efficiency tables are local, non-Tessl evidence and were not numerically merged with the reported run.
- **Subagents.** Requested but blocked by the depth limit; no nested delegation occurred. Disagreement between my conclusion and a hypothetical peer verdict: unresolved, since the tool error prevented the exchange.
- **Boundary respected.** Report-only write to `docs/research/tessl-score-enhancement-ideas/05-token-attribution-and-efficiency.md` (parent created); no edits to the skill, metadata, references, SAFETY.md, plans, inputs, results, or config; no paid or remote evaluations launched; no worktrees, branches, or commits touched.
