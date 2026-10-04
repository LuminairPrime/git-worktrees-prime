# Investigation 1 — Glossary, shared vocabulary, and conciseness

Report path (override): `docs/research/tessl-score-enhancement-ideas/01-glossary-and-shared-vocabulary.md`

---

## 1. Decision summary (292 words)

**Recommendation: implement Option C — keep the `## Glossary` section in `SKILL.md` and keep all seven *topics* it covers, but delete the three rows that are ordinary Git reference material (Repository, Branch, `HEAD` / detached HEAD) and tighten the two loosest remaining rows (Main/linked, Base/integration target). The section drops from 226 to 132 whitespace-delimited words (−94 words, −5.0% of the skill's 1,863 words). No other line of the skill changes.**

Why it matters: the reviewer's only *named* conciseness defect is that the glossary "mixed already-known Git basics with valuable skill-specific conventions." Option C removes exactly that content while preserving every local convention this skill depends on — **checkout** as a noun meaning this workspace, `<primary-root>` regardless of branch name, bare repositories having no main worktree, base ≠ integration target, registration vs. directory vs. branch — plus the branch-retention/naming sentence. All seven required edge cases still resolve from retained wording.

Expected impact: addresses the named criticism; no expected change to actionability, workflow clarity, specificity, completeness, trigger-term quality, or distinctiveness — none depend on the deleted rows (verified below). Runtime effect is ~140 input tokens per skill read (4-chars/token estimate) — noise against the reported ~200,000-token overhead. **This is a clarity/rubric change, not an efficiency change.**

Principal risk: this partially reverses the user's own 2026-10-03 request for exactly seven entries (`docs/research/1.0-development/21-prototype-enhancements-and-verification.md:48`), and it removes the skill's only statement that a detached `HEAD` does not advance a branch.

Confidence: **moderate.** The content argument is well evidenced; the score effect is speculative.

Action: **test first.** Implement only after the user accepts reversing part of that request, then run the five local Tessl scenarios before keeping it. Revert on any lost checklist item or rubric dimension below baseline; the change is one section and trivially reversible.

---

## 2. Baseline and evidence

### 2.1 Live revision verified

| Item | Observed value |
|---|---|
| `git rev-parse HEAD` (first call) | `73d21c776ab51515ad3fb434292b22bec93823e0` (matches handoff) |
| `git rev-parse HEAD` (later in same investigation) | `a2117395a18fb0db7608796a65c514ee528eb426` — "before research starts" |
| `SKILL.md` SHA-256 | `01D156FD90C69091875E4311CB2EF89D34D5E362C0B71A014E3D34440D451744` |
| Bytes / lines / whitespace-delimited words | 12,802 / 140 / **1,863** |
| Glossary block (`SKILL.md` lines 10–22) | **226 words**, 1,368 characters |
| Rest of file | 1,637 words |
| Safety bullets in skill | 9 (SAFETY.md has 13 constraints) |

HEAD advanced during the investigation: a concurrent commit (`a211739`) added `docs/prompts/` only.
`git diff --stat 73d21c7 a211739` shows six files added under `docs/prompts/skill-enhancement-investigations/` and no skill change; `SKILL.md` hashes identically at `d839d62`, `73d21c7`, and `a211739`. Working tree was clean at both observations. No identifier was "reset to" — the handoff identifiers still match the live bytes.

### 2.2 Which skill the evaluation actually exercised — important attribution finding

`vendors/tessl_evals/` contains five scenarios with `with-skill` / `without-skill` artifacts. Every `with-skill/.tessl/plugins/luminair/git-worktrees-prime/SKILL.md` copy is **11,276 bytes**, SHA-256 `2A9FA731C0D01521A12901E80D3F00AC62EEDD044E8FF3BFE2978AECBC76BD68`.

A line-by-line comparison against `git show 9d4be20:skills/git-worktrees-prime/SKILL.md` (1,667 words, pre-safety) shows **exactly one differing line: the frontmatter `description`**. The body is byte-identical to `9d4be20`.

Consequences:

- The evaluated skill has heading **`## Terms used here`**, not `## Glossary` (the rename landed at `d839d62` "changed terms to glossary").
- The evaluated skill has **no `## Safety constraints` section** (its section list ends at `## Completion report`, line 124 of 128).
- **The seven-row terms table the reviewer commented on is identical in content to the live table.** Therefore the conciseness remark ("mixed already-known Git basics with valuable skill-specific conventions") transfers to the live skill, but **no captured run exercised the live 12,802-byte skill**. Any score quoted from these artifacts is a score for `9d4be20` + current description, not for `01D156…`.
- `tests/`, `experiments/` runs carry `supplied-guide.md` of 11,276 bytes (ours) and 3,090/3,309 bytes (the `prp-worktree` comparator) — same version family, same conclusion.

### 2.3 The glossary was a user request

`docs/research/1.0-development/21-prototype-enhancements-and-verification.md:48`:

> "At the user's request, a short glossary now defines repository, worktree/checkout, branch, HEAD/detached HEAD, main/linked worktree, base/integration target, and registration. … The branch-retention sentence was moved from cleanup into the glossary to avoid duplication."

Line 50 adds: "it has not undergone a new model trial."

`docs/plans/integrate-safety-constraints.md:10` and `:137` freeze "glossary definitions" / "the seven glossary entries." Per the assignment, those freezes are evidence of an earlier decision, not a constraint on this recommendation — but they are the reason Option B/C must be presented as a deliberate partial reversal rather than a cleanup.

### 2.4 Evaluation criteria do not depend on glossary text

Read all five `skills/git-worktrees-prime/evals/scenario-*/criteria.json` (weighted checklists, 8–10 items each). Every item is an observable artifact or command: `<primary-root>/.worktrees/<task>` path (scenario-0, 20 pts), base branch = `develop` not `main` (20), named task branch not detached HEAD (15), `git worktree list` before/after (15/10), `rev-parse HEAD` (10), `merge-base --is-ancestor` (scenario-1, 15), `check-ignore -q` with trailing `/` (scenario-2, 15), no bulk copy (scenario-3), `git worktree repair` with absolute path (scenario-4, 20), registration confirmed (scenarios 0/2/4). **No criterion credits the presence of a definition.** The words `registration`, `branch`, `HEAD`, `<primary-root>` appear in criteria as *outcomes*, and all remain instructed in the body.

### 2.5 Term usage map (glossary block excluded, lines 23–140)

| Glossary term | Body lines using it | Does the point of use carry its own meaning? |
|---|---|---|
| Repository | 8, 38, 45, 79, 81, 91, 122, 133, 135 | Yes — ordinary Git noun; shared-state meaning restated operationally at line 30 |
| Worktree / checkout | worktree 41 lines; checkout 29 lines (24, 26–28, 36–39, 43, 46–48, 53, 60–61, 79, 82, 87, 89–90, 92, 108, 120–121, 126, 128, 132, 136, 138) | **No** — "checkout" is used as a noun throughout and the skill contains **zero** `git checkout` / `git switch` / `git restore` commands (grep: no matches). The noun definition is load-bearing for user communication. |
| Branch | 3, 26–27, 43, 48–49, 57, 63–64, 66–67, 73, 82–83, 87, 90, 93, 95, 101, 110, 118–119, 121, 126, 128, 132–134 | Yes — "branch can exist without a checkout" is restated at line 22 and line 121 |
| `HEAD` / detached HEAD | `HEAD` 45, 49, 74, 103, 133; `detached` 49, 91, 126, 133 | Mostly — every use is a standard Git use; the actions (anchor, verify detached state) are imperative at 49/91/126/133 |
| Main (primary) / linked worktree | `primary-root` **once** (38); `primary` 38, 92; `linked` **once** (135); `main` 45, 135, 138; `bare` 135, 138 | **No** — three of these are unique symbols/placeholders that appear nowhere else; without the row they are undefined |
| Base / integration target | base 35, 45, 46, 58, 64, 106; "integration target" 8, 43, 45, 118 | **No** — line 118 (`branch -d` may check upstream, not the intended target) only makes sense with "they may differ" |
| Registration | 3, 37, 126 (+ `repair` 37, `prune` 37, 94, 114, 115, 137) | Partly — line 37 and line 94 state the operational distinction; the glossary supplies the noun-to-object mapping |
| Manager (not in glossary) | 26, 32, 37, 43, 92 | Defined by contrast at line 36 ("raw Git for **unmanaged** worktrees") and by the section heading; see §3 Option notes |

### 2.6 Missing / mismatched evidence

- No runtime, tokenizer, or model-call data anywhere for the current skill; all token figures here are labeled estimates with method.
- No behavioral trial of `01D156…`; doc21 line 50 says the glossary itself never had one.
- The reviewer's raw Tessl report is not in the repository; the conciseness/progressive-disclosure remarks are user-reported.
- **Peer review could not be run:** spawning one child agent returned `Subagent depth limit reached (1)`. I performed the interpretation exercise myself (§6.2). No nested delegation occurred.

---

## 3. Options

Word counts use one method throughout: `($text -split '\s+' | ? {$_ -ne ''}).Count` on the section block, same as the 1,863-word file count.

### Option A — No change (comparison baseline)

Keep lines 10–22 verbatim: seven rows, 226 words.

- **Changes:** nothing. **Stays:** everything.
- **Rubric:** conciseness stays at the reviewer's 4/5 with the named criticism intact; all other dimensions unchanged.
- **Context/execution cost:** 226 words ≈ 340 tokens per read (1,368 chars ÷ 4).
- **Regression risk:** zero.
- **Effort:** zero.
- **Honest weakness:** it leaves the single most concrete piece of reviewer feedback unaddressed, and two of the seven rows are pure Git glossary text ("A commit records a project snapshot and its history links" is 9 words of tutorial).

### Option B — Delete only the two wholly generic rows (low-change option)

Delete the **Repository** and **Branch** rows; keep the other five verbatim.

- **Changes:** −48 words (226 → 178; file 1,863 → 1,815). One hunk, no other edits.
- **Stays:** all local conventions and the HEAD row.
- **Rubric:** half-addresses the criticism; the HEAD row and the generic half of the Worktree row still read as Git reference material, so a re-review could repeat the same remark.
- **Context/execution cost:** −48 words ≈ −70 tokens. Immaterial.
- **Regression risk:** low. Retained wording: line 30 (shared objects/refs) for Repository; lines 22 and 121 for "a branch can exist without a checkout."
- **Effort:** minutes.
- **Versus C:** smaller and safer, but it reverses 2 of the user's 7 requested entries while still leaving generic content — you pay the political cost of reversing the request without fully fixing the criticism.

### Option C — Skill-specific only (RECOMMENDED)

Delete the **Repository**, **Branch**, and `HEAD` / detached HEAD rows; tighten **Main (primary) / linked worktree** and **Base / integration target**; keep **Worktree / checkout** and **Registration** verbatim; keep the heading, table structure, and the branch-retention sentence.

- **Changes:** −94 words (226 → 132; file 1,863 → 1,769). Glossary characters 1,368 → 810 (−558 ≈ −140 tokens by chars÷4). One hunk, no other line changes.
- **Stays:** every local name, alias, relationship, and safety-relevant distinction; the table the reviewer navigated well; the `## Glossary` heading that was deliberately chosen at `d839d62`.
- **Rubric:** removes the exact example the reviewer cited. Every remaining row states a fact *this skill* depends on, so "valuable skill-specific conventions" survives intact. Completeness/specificity risk is confined to the three deleted rows, whose actions are all retained elsewhere (§5).
- **Context/execution cost:** −94 words ≈ −140 tokens per skill read. **Not** an execution-cost fix.
- **Regression risk:** moderate-low; concentrated in the detached-HEAD deletion (§5.2).
- **Effort:** one small reviewed patch.

### Option D — Definitions at first use; delete the section

Remove `## Glossary` entirely; insert four short parentheticals at first use (checkout ≈ line 26, registration ≈ line 37, base/integration target ≈ line 43, `<primary-root>`/main/bare ≈ line 38) and keep the branch-retention sentence near the cleanup tree.

- **Changes:** ≈ −120 words net (remove 226, add back ≈ 105 spread over 4–5 insertion points). Requires rewriting two already list-heavy sentences (line 43, line 45).
- **Stays:** all semantic content, in principle.
- **Rubric:** could score well on conciseness (the "glossary" the reviewer disliked is gone) but risks the reviewer's praised *navigation*; a reader searching for `<primary-root>` no longer has a lookup point.
- **Context/execution cost:** similar to C, slightly better.
- **Regression risk:** higher — definitions land mid-procedure, first-use ordering is scattered (line 37 before line 43), and it becomes a hidden multi-site rewrite, which the assignment explicitly warns against.
- **Effort:** moderate; 4–5 hunks plus two reworded sentences.
- **Verdict:** not preferred. It buys ~25 more words than C and pays for them with spread-out edits and worse lookup.

### Rejected: move the glossary to `references/`

Would remove 226 words from active context, but those terms are needed from the first workflow section (line 24) onward, so it forces an extra read for foundational vocabulary and degrades lookup of `<primary-root>`. This is investigation 3's territory; flagged as a **dependency, not proposed here**.

---

## 4. Recommended option — exact candidate wording

**This is a proposal, not authorization.** Replace `SKILL.md` lines 10–22 (the whole `## Glossary` section) with:

```markdown
## Glossary

| Term | Meaning |
|---|---|
| Worktree / checkout | A directory of checked-out files with its own `HEAD` and index (staging area). Here the noun **checkout** means this workspace. |
| Main (primary) / linked worktree | The repository's original checkout; every other worktree is a linked worktree. `<primary-root>` is that directory regardless of its branch name. A bare repository has none. |
| Base / integration target | The commit or ref a task starts from, versus the branch meant to receive it; they may differ. |
| Registration | Git's record linking a linked worktree's path to the repository. Repair reconnects a live checkout; prune removes obsolete registrations. |

Removing a worktree leaves its branch. Name the checkout path and branch/ref separately when communicating about them.
```

### Entry-by-entry disposition

| Current entry | Words (incl. pipes) | Disposition | Retained wording that carries the safety-relevant part |
|---|---:|---|---|
| Repository | 15 | **Removed** | Line 30: "Worktrees separate working files and indexes, but share objects, refs, remotes, and much Git configuration. Coordinate shared mutations." |
| Worktree / checkout | 26 | **Kept verbatim** (keeps "(staging area)" for human readers) | — |
| Branch | 33 | **Removed** | Line 22 (kept): "Removing a worktree leaves its branch."; line 121: "Pruning removes stale worktree metadata, not branches…"; lines 90, 93 |
| `HEAD` / detached HEAD | 31 | **Removed** | Line 49: "Use detached HEAD … Anchor valuable detached commits to a branch before removal."; lines 91, 126, 133 |
| Main (primary) / linked worktree | 39 | **Shortened** (39 → 33) | All three clauses preserved: linked, `<primary-root>` regardless of branch, bare has none |
| Base / integration target | 33 | **Shortened** (33 → 25) | "they may differ" preserved; lines 45, 118 unchanged |
| Registration | 24 | **Kept verbatim** | — |
| Branch-retention sentence | 17 | **Kept verbatim** | Single-sourced here by deliberate earlier move (doc21:48) |

### Downstream wording changes required: **none**

- No other line cross-references a glossary row, and no line says "see Glossary."
- The removed labels (`Repository`, `Branch`, `HEAD` / detached HEAD) never reappear as glossary pointers; each remaining use is a plain Git word whose meaning is unchanged.
- Placeholders `<repo>`, `<worktree>`, `<base-ref>`, `<task-branch>` are defined at line 53, independent of the glossary.
- No safety bullet, command block, decision-tree step, or completion-report instruction changes. This is one contiguous hunk — there is no hidden whole-file terminology rewrite.

### Why it beats the alternatives

- Versus **A**: it is the only option that removes the reviewer's named example without touching behavior.
- Versus **B**: it finishes the job — after B, two of five rows are still generic; after C, every row carries a skill-specific fact — at the cost of one extra row deletion and two short rewrites.
- Versus **D**: same order of savings with one hunk instead of five, no reworded list-sentences, and a preserved lookup point for `<primary-root>`.

### What would reverse this recommendation

1. The user re-affirms that all seven entries must exist verbatim (doc21:48) → fall back to **Option A**, or accept only Option B.
2. A behavioral run shows any scenario-0/1/2/3/4 checklist item lost after the trim → revert.
3. A reviewer still names the glossary after C → the criticism is not about these rows, and the correct target is body density (investigations 3/4), not vocabulary.
4. Evidence that model agents actually consult the Repository/Branch/HEAD rows at decision time (e.g. transcripts in `tests/results/` or `experiments/` showing a glossary-dependent correction) — I found none, but I did not audit every transcript.

**Fallback if the user wants the detached-HEAD rationale kept:** re-add one row, `| \`HEAD\` / detached HEAD | A worktree's \`HEAD\` names its checked-out branch; detached, it points at a commit, so new commits do not advance a branch. |` (≈ 27 words), giving a 159-word section (−67). This is the single highest-risk deletion in Option C and is cheap to keep.

---

## 5. Safety and semantic coverage check

The proposal is a localized content edit to one section, **not** a structural reorganization, so the affected subset of the thirteen `SAFETY.md` constraints is identified rather than all thirteen. No safety bullet, and no other section, is edited — so no unrelated coverage can be silently removed.

### 5.1 Affected constraints and where their vocabulary now lives

| SAFETY.md constraint (line) | Glossary term it leans on | Status after Option C |
|---|---|---|
| 2 — verify repository, absolute path, branch (or detached state), HEAD commit; `-z` (line 4) | detached / HEAD | **Self-contained**: the constraint itself says "(or detached state)" and "HEAD commit"; body keeps `rev-parse HEAD` (74, 103) and "branch (or intended detached commit)" (126) |
| 5 — inspect/preserve changes, anchor detached commits (line 7) | detached | **Retained at line 91** ("detached commits") and **line 49** ("Anchor valuable detached commits to a branch before removal") |
| 6 — use `git worktree remove`; main is not a removable linked worktree (line 8) | main / linked | **Retained**: Main row kept, including linked-worktree sense (used at line 135) |
| 7 — repair from main/bare repository, new absolute linked paths (line 9) | main / bare / linked / registration | **Retained**: Main row keeps "A bare repository has none"; Registration row kept; line 37 unchanged |
| 9 — prune only with reviewed dry run; lock offline worktrees (line 11) | registration / prune | **Retained**: Registration row keeps "prune removes obsolete registrations"; lines 94/114/115/137 unchanged |
| 10 — shared branch refs/config; `HEAD` worktree-specific (line 12) | HEAD / repository | **Partial but sufficient**: shared-state claim lives at line 30 (unchanged); `HEAD` remains at 45/49/74/103/133. The glossary's "each worktree's HEAD normally names its branch" is the only removed statement of worktree-specific `HEAD` — flagging it as the one genuine semantic loss of the proposal |
| 11 — migrate `core.worktree`/`core.bare` to the **main** worktree's `config.worktree` (line 13) | main | **Retained**: Main row kept; line 138 unchanged |
| 13 — don't edit refs/metadata files; resolve with `rev-parse --git-path` (line 15) | registration | **Retained**: Registration row keeps "Git's record linking … Repair reconnects … prune removes obsolete registrations" |

Unaffected (no glossary dependency): constraints 1, 3, 4, 8, 12 — authorization, `--force`/unlock, `add -B`, submodules, extension support.

### 5.2 The one real semantic loss

Removing the `HEAD` / detached HEAD row deletes the skill's only explanation that **new commits on a detached `HEAD` do not advance a branch**. Every *action* it motivates is retained (lines 49, 91, 126, 133), and no instruction in the skill depends on that explanation. The rationale is textbook Git, which is precisely what the reviewer called "already-known Git basics." If the user prefers to keep the rationale, use the fallback row in §4 (−67 instead of −94 words).

### 5.3 Deliberate repetitions (unchanged, not duplicated by this patch)

- **Branch/path separation** is stated once, in the glossary's final sentence, by deliberate earlier move (doc21:48). Option C keeps it — it is not repeated in the cleanup tree.
- **Path/branch/HEAD verification** appears in the safety section *and* at lines 92/126. That redundancy is deliberate (safety), and is untouched.
- **Registration vs. directory** appears in the Registration row *and* line 94 ("A missing directory may be an offline volume; do not prune…"). Line 94 is the operative check; the glossary supplies only the noun mapping. The proposal adds **no new procedural rule** to compensate for anything removed.
- **`manager`** is *not* added as a new entry: it is defined by contrast at line 36 ("raw Git for unmanaged worktrees") and by the section heading at line 32. Adding it would cost ≈15 words to duplicate what line 36 already establishes. If the user disagrees, the cheapest fix is a 4-word clause at line 26 ("against the manager's (harness tool's) inventory"), not a new row.

### 5.4 Required edge cases under the proposed wording

| Case | Resolves via |
|---|---|
| Main worktree is on `develop`, not `main` | Kept row: "`<primary-root>` is that directory regardless of its branch name" + line 38 usage + line 45 "Do not assume `main`… is correct" |
| Bare repository, no main worktree | Kept row: "A bare repository has none" + line 135 "repairing from the current main/bare repository" |
| Worktree removed, branch remains | Kept sentence: "Removing a worktree leaves its branch" + lines 90, 93, 95, 121 |
| Detached commits must survive cleanup | Lines 49, 91, 126, 133 (all unchanged). Lost: only the explanatory clause — see §5.2 |
| Starting base differs from integration target | Kept row: "they may differ" + lines 45, 118 |
| Unavailable/relocated path vs. stale registration | Kept row: "Repair reconnects a live checkout; prune removes obsolete registrations" + line 37 ("Do not prune the live checkout's registration") + line 94 |
| "checkout" as noun vs. `git checkout` action | Kept row: "Here the noun **checkout** means this workspace". Verified: the skill contains **no** `git checkout`/`switch`/`restore` command, so the noun sense is the only sense used |

---

## 6. Validation

### 6.1 Checks already performed (results)

| Check | Result |
|---|---|
| Live `SKILL.md` SHA-256 / words / lines vs handoff | `01D156FD…D451744` / 1,863 / 140 — matches handoff exactly |
| HEAD at start vs handoff | `73d21c7…` matches; later advanced to `a211739` by a concurrent `docs/prompts/` commit; skill bytes identical across `d839d62`, `73d21c7`, `a211739` |
| Glossary block word count (same method as file) | 226 of 1,863 (12.1%); per-row counts recorded |
| Term→line map for every glossary term | Computed (§2.5), glossary block excluded |
| Vendored Tessl skill vs git history | Body identical to `9d4be20` (1,667-word pre-safety version); only frontmatter `description` differs; heading is `## Terms used here`; no safety section |
| All five `with-skill` plugin copies byte size | 11,276 each (same version) |
| Eval criteria read (5 scenarios, 46 checklist items) | No item depends on glossary presence; all items map to retained body instructions |
| `git checkout` / `switch` / `restore` occurrences in skill | **0** — "checkout" is exclusively a noun here |
| Safety bullet count in skill vs SAFETY.md | 9 bullets vs 13 constraints; §5.1 accounts for the 8 affected/unaffected split |
| Candidate wording word counts | 132 (Option C), 178 (Option B), computed with the identical split method |
| Peer subagent for neutral variant interpretation | **Attempted, blocked**: `Subagent depth limit reached (1)`. No child ran; no nested delegation |

### 6.2 Self-run static interpretation (no peer available)

Applying the three variant blocks to the seven required cases produced identical object/action conclusions for every case under all three variants, with one difference: **the variant lacking the `HEAD`/detached row required general Git knowledge** to explain why a detached commit must be anchored (the *action* — anchor before removal — was still given by line 49 in every variant). No variant caused a wrong prune/repair decision: the Registration row and lines 37/94 are present in all three. No variant conflated path with branch, because the kept trailing sentence ("Name the checkout path and branch/ref separately") is present in all three.

*Static interpretation identifies ambiguity; it is not evidence of better model behavior.* No peer agreement claim is made, because no peer ran.

### 6.3 Proposed future comparison (not run here)

**Design:** one-factor A/B — same harness, same five scenarios in `skills/git-worktrees-prime/evals/`, same model; treatment = `SKILL.md` with only the §4 hunk applied; control = current `01D156…`. Record the SHA-256 of the guide actually supplied to the agent (doc21:44 warns the setup script reads the *current* skill, so a stale run would silently mix versions).

**Success criteria (all required):**
1. Every checklist item that scored with the control still scores with the treatment, in all five scenarios (primary gate — 46 items).
2. Re-review shows the glossary criticism gone and conciseness ≥ 4/5, with completeness and specificity still 5/5.
3. In any completion report, path, branch, and registration remain stated separately (the one communication behavior the glossary directly enforces).

**Stop / revert criteria (any one):**
1. Any previously-passing checklist item fails under treatment.
2. Any rubric dimension falls below its control value.
3. A run conflates a checkout path with a branch/ref, or treats a missing directory as proof of a stale registration.
4. The guide hash recorded for a run does not match the intended candidate.

**Explicit non-promise:** no Tessl score is forecast, and no zero-regression guarantee. Expected token delta from this change alone is ≈140 input tokens per skill read (1,368 → 810 characters ÷ 4, labeled estimate) — it cannot be credited with any change in the reported ~26% overhead.

---

## 7. Dependencies, boundaries, and limitations

**Interactions with the other investigations**
- **02 (activation/description):** the evaluated skill already carried the *current* frontmatter description with an older body (§2.2). If investigation 02 changes `description`, that change and this one must be attributed separately in any future score comparison.
- **03 (progressive disclosure/references):** **dependency, not redesigned here.** My recommendation assumes the glossary stays inside `SKILL.md`. If investigation 03 moves it to `references/`, the lookup argument in §3 Option D changes and Option C's advantage shrinks — please treat "glossary stays inline" as my stated boundary.
- **04 (phases/execution):** cleanup-tree and develop/integrate wording are untouched; if investigation 04 restructures those sections, re-check that lines 22, 49, 91, 94, 118, 121 still exist somewhere, since Option C relies on them as the retained carriers.
- **05 (token attribution):** **flagged explicitly.** A 94-word glossary trim cannot explain or offset a ~200,000-token (26%) overhead. Do not cite this proposal as an efficiency fix.

**Assumptions**
- The reviewer's word "glossary" refers to the seven-row terms table. Verified as safe: the evaluated version has that identical table under the heading `## Terms used here`.
- "Highly capable model agents" know standard Git (detached HEAD, repository, branch), which is the basis for classifying three rows as reference material.

**Boundaries respected**
- Investigation only: no skill, metadata, reference, SAFETY.md, plan, eval, fixture, result, or config file was modified. The only file written is this report.
- No worktree created/moved/removed, no branch change, no commit, no dependency installed, no evaluation run. All git usage was read-only (`rev-parse`, `log`, `show`, `diff`, `status`, `diff --no-index` against `%TEMP%` scratch copies).
- The other four investigators' reports were not read.

**Limitations / unresolved**
- Peer subagent blocked by `experimental.subagent_depth`; §6.2 is self-review only.
- No tokenizer-accurate counts; all token figures are chars÷4 estimates, labeled.
- I did not audit `tests/results/**/transcript.txt` or `experiments/**` for evidence that an agent actually relied on a glossary row; absence of such evidence is unverified rather than disproven.
