# Microsoft FluidFramework vendor review

## Inputs and verdict

- Vendor: `C:/Users/MC/Documents/git-worktrees-prime/vendors/microsoft-fluidframework-agencypluginsnoriskillsusing-git-worktrees-SKILL.md` (185 lines).
- Prototype: `C:/Users/MC/Documents/git-worktrees-prime/skills/prototype1-astra/SKILL.md` (114 lines).

**Tier C — small, optional incremental usefulness.** The vendor contributes one potentially useful clarification: record an appropriate test baseline before changing code when existing failures could otherwise be confused with the task's changes. Most of its worktree guidance is already covered more precisely in the prototype. Its mandatory setup, approval, and directory rituals should not be imported.

Both files were read fully. This is a source comparison, not verification of Git, package-manager, harness, or repository behavior. ICM recall supplied task context only; recalled conclusions from other reviews are not evidence here. No vendor workflow was executed and the prototype was not modified.

## Possible addition

### Conditional pre-change baseline

Vendor lines 49–59:

> 5. Run tests to ensure the worktree is clean.
>
> ```bash
> # Examples - use project-appropriate command
> npm test
> cargo test
> pytest
> go test ./...
> ```
>
> **If tests fail:** Report failures, ask whether to proceed or investigate.

Vendor lines 144–147:

> **Proceeding with failing tests**
>
> - **Problem:** Can't distinguish new bugs from pre-existing issues
> - **Fix:** Report failures, get explicit permission to proceed

The useful source claim is about attribution of failures, not worktree cleanliness. Prototype lines 62–63 already require repository-directed setup and testing task changes before integration; lines 55–57 inspect the initial checkout, branch, and commit. It does **not explicitly require a test result before edits**. Thus its ordinary validation requirement may still leave uncertainty about whether a failure predated the task.

Minimal optional addition after prototype line 62:

> When pre-existing failures could obscure the task's validation, run the relevant repository-prescribed checks before edits and record any failures as the baseline.

Benefit: a small explicit reminder can prevent attributing an existing failure to a new change. It is most useful for unfamiliar checkouts, bug fixes, or tasks whose final validation depends on a currently unreliable suite.

Caveats: running every suite for every worktree adds cost without improving simple inspection or documentation tasks. Existing trustworthy baseline evidence may suffice. A baseline failure is not automatically a reason to stop authorized work; report it and decide whether it actually blocks validation. Test success also does not establish a clean Git status or absence of local configuration differences. The vendor's unconditional user-permission gate and claim that tests ensure a clean worktree should be rejected. This addition is optional; general task-testing instructions may already cover it outside this skill.

## Already covered; no addition needed

### Keep operations in the selected checkout

Vendor lines 71–78:

> 7. Understand that you are now in a new working directory. Your Bash tool instructions from here on out should refer to the worktree directory, NOT your original directory. This is ABSOLUTELY CRITICAL.
>
> </required>
>
> # Maintaining Working Directory in Worktree
>
> CRITICAL: Once you create and enter a worktree, you must stay within
> it for the entire session.

Prototype line 21 explicitly handles the important failure case: creation may not change the agent's working directory, so subsequent commands must use the returned path. Lines 38 and 55–57 provide exact-path commands and verification; line 63 keeps edits, builds, tests, and commits there. The vendor adds emphasis, not a missing rule.

Do not add the session-wide restriction. Prototype lines 65 and 70 allow authorized integration in the target checkout, and lines 77 and 96–97 require leaving a checkout before removing it. Those operations need an explicit intended path, not permanent confinement to one directory.

### Follow repository placement and verify exclusion

Vendor lines 134–137:

> **Assuming directory location**
>
> - **Problem:** Creates inconsistency, violates project conventions
> - **Fix:** Follow priority: existing > CLAUDE.md > ask

Vendor lines 129–132:

> **Skipping .gitignore verification**
>
> - **Problem:** Worktree contents get tracked, pollute git status
> - **Fix:** Always grep .gitignore before creating project-local worktree

Prototype lines 8 and 23 already honor repository conventions, then supply a default. Line 24 permits tracked or local exclusion and asks Git to verify it; line 44 gives the verification command. The vendor's literal-file test does not improve this. Its claim about contents being tracked is source wording: the review did not test that behavior, and lack of an ignore entry is not itself proof that files are already tracked.

### Initialize the new checkout

Vendor lines 30–45 propose manifest-based automatic setup, and lines 139–152 require installing the project while warning against hardcoded setup commands. Prototype line 62 already directs setup using the task checkout's repository instructions and calls out absent ignored dependencies, secrets, and outputs. That is more applicable than assuming a manifest selects the project's package manager or safe install command.

## Content to reject

| Vendor evidence | Why not import it | Prototype comparison |
| --- | --- | --- |
| Lines 6–13: `*CRITICAL* Add the following steps to your Todo list using TodoWrite:` and `- If not found, ask me for permission to create a .worktrees directory` | Harness-specific task-list tool and unconditional permission ceremony. Directory creation can be ordinary authorized work. | Lines 20–24 support available harness tools, repository conventions, and a fallback without assuming a universal tool. |
| Lines 17–22: `grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore` and `- If not found, add the appropriate line to the .gitignore immediately.` | A literal-pattern presence check is not effective ignore verification. A `worktrees/` match does not establish exclusion of `.worktrees/`; other valid exclusions can exist. Mandatory tracked-file editing creates avoidable repository changes. These are limitations inferred from the text, not execution results. | Line 24 uses `git check-ignore` and permits local exclusion. |
| Line 27: `- Create the worktree with the Bash tool: \`git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"` | The source has an unclosed inline-code delimiter and does not supply an intended base. Its relative-path Bash recipe is narrower than the prototype. | Lines 21, 30–33, and 46–50 require an explicit base and account for continuation and checkout ownership. |
| Lines 33–44: `if [ -f package.json ]; then npm install; fi`, `if [ -f Cargo.toml ]; then cargo build; fi`, `if [ -f requirements.txt ]; then pip install -r requirements.txt; fi`, `if [ -f pyproject.toml ]; then poetry install; fi`, `if [ -f go.mod ]; then go mod download; fi` | Manifest presence alone does not justify those particular setup actions. Automatic installation/building can consume time or change environment and dependency state. Read actual repository instructions. | Line 62 already does this with less policy and no stack-specific recipes. |
| Line 47: `- If there is no obvious project setup, you _MUST_ ask me.` versus line 125: `| No package.json/Cargo.toml  | Skip dependency install    |` | Internal inconsistency and unnecessary questioning when the task needs no setup. | Lines 62–63 allow task-appropriate setup and validation. |
| Lines 82–85: `1. Never use cd .. from within a worktree - It will eventually take` / `   you outside the worktree boundary`; `2. Always use absolute paths for commands - Use npm run lint from` / `   within the worktree, not cd .. && npm run lint` | Blanket prohibition confuses a directory change with unsafe operation. The prose says absolute paths while its command example uses implicit current directory. Use explicit tool working directories or exact paths for the actual operation. | Lines 21, 38, and 63 already cover path discipline. |
| Lines 101–102: `pwd  # Should show .worktrees/branch-name in path` and `git branch  # Should show * on your feature branch, not main`; lines 113–115 flag main, absence of `.worktrees/`, and any `cd ..`. | Directory-name and branch-name heuristics reject valid external or harness-managed checkouts and disposable detached inspection. They can also falsely reassure an agent in the wrong similarly named path. | Lines 20–24, 28, 34, and 55–57 verify actual selected state and support detached inspection. |
| Lines 174–185 forbid skipping baseline tests and require asking for any failure. | Too broad for minimal guidance; testing scope and blockers depend on the task. | Lines 62–65 already prescribe task validation. The optional baseline sentence above captures the useful part. |

The vendor does not provide a reason to weaken or replace prototype ownership, shared-state, integration, preservation, or cleanup guidance (lines 12–16, 64–66, and 73–110).

## Adversarial questions

Use these as prompts without showing the grading keys. They probe whether the prototype alone suffices, not whether an agent repeats vendor slogans.

1. A harness creates `D:/task-checkouts/fix-42` at the requested commit, but your shell remains in the primary checkout. The path contains no `.worktrees` component. What do you verify and where do you run edits and checks?
2. An unfamiliar repository contains `pyproject.toml`, but its checkout instructions specify a different environment command and no Poetry. Must you run `poetry install` or ask the user before proceeding?
3. You are about to change a parser. There is no recent baseline evidence, and the suite has a reputation for intermittent failures. After your edit, one test fails. What could you have done before editing to make attribution easier, and does a baseline failure always require user permission to continue?
4. The task's changes are ready for authorized local integration. The integration checkout belongs to another active worker, and afterward your disposable task checkout needs removal. Must you remain in the task directory throughout the session?

## Separate grading keys

1. **Prototype sufficient.** Verify returned path and commit; inspect top-level, branch, and HEAD; use the selected exact path for task commands. Neither directory naming nor the original shell's current directory establishes the target. Supported by lines 20–21, 28, 38, 55–57, and 63.
2. **Prototype sufficient.** Follow checkout repository instructions; manifest-only inference does not override them. Ask only if necessary information is unresolved for the task. No automatic Poetry install is required. Supported by lines 8 and 62.
3. **Prototype partially sufficient; candidate gap.** A relevant pre-edit baseline can distinguish pre-existing failures from new ones, while recording uncertainty for intermittent failures. The prototype requires setup and final task validation at lines 62–63 but does not explicitly call for the pre-edit baseline. Accept a prototype-only agent that independently chooses one; do not claim the text guarantees that choice. A known failure warrants reporting and a blocker assessment, not an unconditional permission request. The proposed addition improves that explicit cue without importing the vendor's blanket test gate.
4. **Prototype sufficient.** Coordinate with the target's owner before integration; use its verified path for authorized integration, and leave the task directory before removal from a surviving checkout. Permanent confinement would obstruct the documented lifecycle. Supported by lines 65, 70, 75–80, and 96–97.

## Recommendation

Consider only the conditional baseline sentence, and omit even that if the agent's existing task-testing guidance already supplies it. Import no vendor commands, required TodoWrite steps, directory-name heuristics, automatic installers, or unconditional approval gates.
