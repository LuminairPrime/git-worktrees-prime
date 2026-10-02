# administrakt0r vendor review

## Inputs and scope

- Vendor: `C:/Users/MC/Documents/git-worktrees-prime/vendors/administrakt0r-AI-Agents-Safe-Coding-Skillsskillsusing-git-worktrees-SKILL.md` (223 lines).
- Prototype: `C:/Users/MC/Documents/git-worktrees-prime/skills/prototype1-astra/SKILL.md` (114 lines).

Both files were read fully. This is a source comparison, not a Git behavior test. Quoted commands and their claimed effects were not executed. Line ranges below are inclusive and refer to these input files. No prototype changes are part of this review.

## Incremental usefulness: B — two small, useful clarifications

Scale: **S** indispensable correction; **A** substantial improvement; **B** useful narrow addition; **C** marginal or situational addition; **D** no worthwhile addition.

The vendor contributes an explicit pre-edit test baseline and a reminder that ignore protection applies to a second project-local directory convention. The prototype already provides substantially more complete worktree guidance, including ownership, explicit bases, harness behavior, integration, and safe cleanup. Importing the vendor workflow wholesale would reduce quality. At most two short additions merit consideration.

## 1. Generalize ignore verification to every location inside the primary checkout

**Finding tier: B.**

Vendor evidence, lines 54–58:

> ## Safety Verification
>
> ### For Project-Local Directories (.worktrees or worktrees)
>
> **MUST verify directory is ignored before creating worktree:**

Vendor lines 72–76 distinguish the reason and the external-location exception:

> **Why critical:** Prevents accidentally committing worktree contents to repository.
>
> ### For Global Directory (~/.config/superpowers/worktrees)
>
> No .gitignore verification needed - outside project entirely.

**Prototype comparison:** Line 23 permits the repository's location convention, but line 24 explicitly conditions ignore protection on creation under `.worktrees`. The example at line 44 also checks only `.worktrees/<task>`. A repository convention using `worktrees/` or another directory beneath the primary checkout is therefore less explicitly protected. A trained agent can infer the principle; the wording need not depend on that inference.

**Minimal proposed addition:** Generalize the first sentence of prototype line 24 instead of adding a new section:

> Before creating a worktree inside the primary checkout, ensure its actual destination is ignored through `.gitignore` or a local exclusion; verify that destination with `git check-ignore`.

Retain the existing `git rev-parse --git-path info/exclude` guidance. Generalize the example at line 44 only if changing that example is useful; a new location-selection workflow is unnecessary.

**Realistic benefit:** Prevents a location-convention exception from escaping the existing guard. The text can become more general without becoming longer.

**Caveats:** Ignore protection addresses accidental tracking and status noise, not worktree isolation or security. The vendor's command at line 62 uses an OR between two directory checks. Its syntax can accept one ignored directory even when the selected destination is the other directory; this is an inference from the command, not a reproduced failure. Adopt the principle, not that command.

## 2. Record a relevant pre-edit test baseline when regression attribution needs it

**Finding tier: C.**

Vendor evidence, lines 123–125:

> ### 4. Verify Clean Baseline
>
> Run tests to ensure worktree starts clean:

Vendor lines 171–174:

> ### Proceeding with failing tests
>
> - **Problem:** Can't distinguish new bugs from pre-existing issues
> - **Fix:** Report failures, get explicit permission to proceed

**Prototype comparison:** Lines 55–57 verify the checkout identity, status, and commit. Line 62 requires setup from repository instructions; line 63 requires review and tests before integration. None explicitly records test failures before edits. The vendor supplies a distinct timing requirement, though its mandatory full baseline and permission gate are excessive for a general worktree skill.

**Minimal proposed addition:** Add one sentence near prototype lines 62–63:

> When needed to distinguish new failures from existing ones, run the relevant checks before editing and record any baseline failures.

**Realistic benefit:** Helps attribute failures in a new checkout, especially when setup, environment, or the starting commit already has problems. Uses existing task context rather than introducing a new baseline artifact.

**Caveats:** This is general development guidance rather than a Git worktree invariant. Trained agents and repository instructions may already cover it. Skip the addition if minimizing duplicated development guidance is the priority. “Starts clean” conflates test success with Git cleanliness; passing tests do not establish a clean working directory. Neither blanket permission requests for failures nor a complete suite on every worktree creation should be imported.

## Content to reject or leave redundant

| Vendor evidence | Why it adds little or should be rejected | Prototype coverage |
|---|---|---|
| Lines 13–17: overview, “Systematic directory selection + safety verification,” and required announcement | Overview is redundant. The slogan and ritual announcement do not improve a trained agent's decisions. | Lines 8–24 already give concrete selection and verification rules. |
| Lines 21–51: existing `.worktrees` wins, then `CLAUDE.md`, then ask | Repository instructions should govern before an incidental directory wins. Hard-coding one instruction filename misses other instruction sources. Asking for a location has an existing safe default in the prototype. | Lines 8, 20, and 23 prioritize instructions, manager, convention, then default. |
| Lines 65–70: “Per Jesse's rule \"Fix broken things immediately\"” followed by “1. Add appropriate line to .gitignore”, “2. Commit the change”, “3. Proceed with worktree creation” | Personal/project-specific rule. Unconditional tracked-file edits and a commit are unnecessary when a local exclusion suffices. Do not expand task scope just to create a checkout. | Line 24 supports a local exclusion and handles a `.git` file. |
| Lines 82–101: basename-derived project name, branch-derived directory, `git worktree add "$path" -b "$BRANCH_NAME"` | No explicit base, ownership check, continuation alternative, or unused-path validation. Line 95 places `~` inside a quoted assignment; that is not a reliable home-directory construction. These are source-level limitations, not tested behavior. | Lines 12, 21, 23, 28–57 address these decisions with explicit placeholders and alternatives. |
| Lines 104–121: automatically run `npm install`, `cargo build`, `pip install`, `poetry install`, or `go mod download` | A manifest alone does not establish the repository's package manager, environment, or setup command. “Auto-detect” can conflict with repository instructions and needlessly build or install dependencies. | Line 62 directs setup through repository instructions. |
| Lines 135–145, 171–174, 199–210: mandatory tests and permission to proceed after failures | Preserve the useful baseline idea only if needed. Test failures call for judgment about their relevance and cause, not an unconditional pause. Mandatory readiness prose and test-count formatting are ceremony. | Lines 63 and 114 require checks and honest reporting without a new gate. |
| Lines 147–195: quick reference, mistakes, and example workflow | Mostly repeats earlier material. The example's setup commands are not portable repository instructions. No new worktree-specific decision emerges. | The prototype's compact rules and command examples already serve trained agents. |
| Lines 214–220: “brainstorming” required when design is approved; “finishing-a-development-branch” required for cleanup; other paired skills | These are dependencies of the vendor's surrounding workflow, not universal worktree practices. Do not import another skill ecosystem or require isolation for every approved implementation. | Lines 12–14 allow the current checkout; lines 73–110 provide self-contained cleanup. |

The vendor also lacks the prototype's explicit shared-state warning (line 16), harness safeguards (lines 20–22), deliberate dirty-state transfer (line 32), branch checkout protection (line 33), and cleanup preservation checks (lines 75–110). These are reasons to retain the prototype, not proposed additions from this vendor.

## Adversarial questions

Give an agent only the prototype and ask these questions. Score its answers before adding text; an adequate answer is evidence that no addition is necessary for that tested case.

1. The repository convention uses `<primary-root>/worktrees/<task>`, not `.worktrees`. `.worktrees` is ignored, but `worktrees` is not. What must you check or change before creating the task checkout?
2. A new task checkout is at the correct base, has a clean Git status, and has completed the repository's setup. After your first edit, a relevant test fails. What missing evidence would help establish whether your edit caused the failure, and should every task require the complete suite before editing?
3. Both `.worktrees/` and `worktrees/` exist, but repository instructions require an external directory. Where should the checkout go? Must you edit `.gitignore`, commit it, or ask for a new location?
4. The new checkout contains `package.json`, `Cargo.toml`, and `pyproject.toml`; repository instructions provide a setup task. Which setup commands should you run, and does worktree creation itself require all detected ecosystem installers?

## Separate grading keys

1. **Pass:** Use the repository convention, but verify the actual destination is ignored before creating inside the primary checkout. Checking the other directory does not suffice. Use an appropriate ignore rule or local exclusion; no mandatory commit. **Prototype evidence:** lines 23–24, 44. This is the strongest test of the proposed wording generalization because line 24 names only `.worktrees`.
2. **Pass:** A pre-edit run of the relevant check at the starting state can establish a baseline; Git cleanliness cannot establish test success. Scale checks to the task and repository instructions, record existing failures, and assess cause and relevance. Do not demand every full suite or unconditional user permission. **Prototype evidence:** lines 55–57, 62–63, 114. The prototype does not explicitly require pre-edit timing; a passing answer demonstrates agent inference rather than literal coverage.
3. **Pass:** Follow repository instructions and any applicable harness contract. Existing directories do not override them. An external destination needs no ignore change merely for worktree creation, and a clear convention removes the location ambiguity. **Prototype evidence:** lines 8, 20–24. No proposed addition is needed.
4. **Pass:** Follow the repository setup task in the selected checkout, obtaining necessary local configuration deliberately. Manifest presence does not justify running all installers or copying the other checkout's ignored files wholesale. **Prototype evidence:** lines 62–63. No proposed addition is needed.

## Recommendation

Generalize the existing ignore sentence. Consider the conditional baseline sentence only if this skill should remind agents about regression attribution. Reject the vendor's fixed directory hierarchy, automatic setup commands, extra permission gates, automatic commit, and paired-skill requirements. No broader rewrite is justified by these two sources.
