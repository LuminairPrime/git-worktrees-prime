# Vendor review: OpenAI plugins / superpowers

## Inputs and method

- Vendor: `C:/Users/MC/Documents/git-worktrees-prime/vendors/openai-pluginspluginssuperpowersskillsusing-git-worktrees-SKILL.md` (167 lines).
- Prototype: `C:/Users/MC/Documents/git-worktrees-prime/skills/prototype1-astra/SKILL.md` (114 lines).

Both files were read fully. Substantive evidence is limited to these two files. No vendor instructions were executed, Git behavior tested, external documentation consulted, or prototype changes made. ICM recall supplied context only. This reviewer thread was reused because of the session thread cap; the prior vendor review is not substantive evidence for this comparison.

## Incremental usefulness: B

One small safety refinement is worth considering: verify the actual chosen project-local worktree destination is ignored, not only the `.worktrees` default. A conditional pre-edit test baseline is a weaker, optional candidate. Existing-isolation detection and native-tool preference are already covered more carefully by the prototype. Reject the vendor's automatic reuse, universal harness claims, mandatory consent/commits/installers, and work-in-place fallback after failed isolation.

## Candidates

### 1. Generalize ignore verification to the chosen project-local destination — B

Exact vendor lines 78–80:

> #### Safety Verification (project-local directories only)
>
> **MUST verify directory is ignored before creating worktree:**

Vendor lines 71–74 also explicitly allow another location:

>    ls -d .worktrees 2>/dev/null     # Preferred (hidden)
>    ls -d worktrees 2>/dev/null      # Alternative
>    ```
>    If found, use it. If both exist, `.worktrees` wins.

**Prototype gap:** line 23 permits repository-specific locations, but line 24 limits its explicit ignore prerequisite to `.worktrees`. The concrete verification at line 44 also checks only `.worktrees/<task>`. Consequently, the safety instruction does not expressly cover a repository convention such as `worktrees/<task>` or another in-repository destination.

**Minimal proposed replacement for the start of line 24:**

> Before creating any worktree inside the primary checkout, verify the actual chosen destination is ignored through `.gitignore` or a local exclusion.

Retain the existing `git rev-parse --git-path info/exclude` and `git check-ignore` guidance; make the line 44 example refer to the selected repository-relative destination if this refinement is adopted.

**Benefit:** closes a real wording mismatch between following repository placement conventions and requiring ignore verification. It avoids adding a new procedure or fixed directory hierarchy.

**Caveats:** this is a text-level gap, not a demonstrated agent failure or tested Git behavior. Do not copy the vendor's check at line 83: it succeeds if either hard-coded directory is ignored, which does not establish that the chosen destination is ignored. Do not import its mandatory `.gitignore` commit at line 86; the prototype already permits a local exclusion. External destinations do not need an exclusion in the primary checkout.

### 2. Conditional baseline before editing — C, optional

Exact vendor lines 121–123:

> ## Step 3: Verify Clean Baseline
>
> Run tests to ensure workspace starts clean:

Exact vendor line 130:

> **If tests fail:** Report failures, ask whether to proceed or investigate.

**Prototype gap:** lines 62–63 require repository-directed setup and testing the task changes before integration, but do not explicitly establish test results before edits. Its starting commit/path checks at lines 55–57 establish checkout identity, not test health.

**Minimal proposed addition after line 62, only if repeated misattribution of failures is a practical concern:**

> When needed to distinguish existing failures from regressions, run the relevant checks before edits and record failures.

**Benefit:** supplies evidence for whether later failures predate the task. It can help when continuing unfamiliar work or investigating an existing failing test.

**Caveats:** a passing baseline is not proof the workspace is clean or every future failure comes from the task. Mandatory full-suite runs cost time and may require unavailable services; unconditional permission questions can block already-authorized debugging. Keep this conditional, scoped to relevant checks, and subordinate to repository instructions. For the smallest sufficient skill, candidate 1 is stronger and this candidate can be omitted.

## Redundant, unsafe, or overly specific content to reject

### Automatic reuse based only on linked-worktree detection

Exact vendor line 33:

> **If `GIT_DIR != GIT_COMMON` (and not a submodule):** You are already in a linked worktree. Skip to Step 2 (Project Setup). Do NOT create another worktree.

Prototype lines 12–14 already decide reuse by task ownership and need for separation; lines 41–42 inspect inventory and branch/status. A linked checkout can belong to another task or worker. Detection does not establish permission to edit it. The vendor's submodule commands at lines 21–30 are an implementation of its detector, not evidence that task ownership is established. No detector expansion is warranted for trained agents who can inspect checkout metadata when necessary.

Exact vendor line 37:

> - Detached HEAD: "Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time."

Detached HEAD does not itself establish external management. Prototype lines 33–34 already distinguish a development branch from disposable detached inspection and preserve valuable detached commits before removal. Reject universal finish-time branch creation and inferred manager ownership.

### Universal harness behavior and strict raw-Git prohibition

Exact vendor line 55:

> Native tools handle directory placement, branch creation, and cleanup automatically. Using `git worktree add` when you have a native tool creates phantom state your harness can't see or manage.

Exact vendor line 57:

> Only proceed to Step 1b if you have no native worktree tool available.

These are vendor claims, not behavior verified here. Prototype lines 20–22 already prefer harness tools while requiring inspection of actual starting-state/cleanup behavior and allowing a supported fallback. Tool availability does not prove it supports the requested operation. Reject universal automation and visibility claims and an absolute fallback ban.

### Consent ceremony and fixed directory tie-breaker

Exact vendor line 41:

> Has the user already indicated their worktree preference in your instructions? If not, ask for consent before creating a worktree:

Prototype lines 8 and 12–14 already follow user/repository instructions and create isolation when the actual task requires it. Do not import a blanket additional question for an already-authorized task. Vendor lines 65–76 repeat instruction precedence but introduce a fixed `.worktrees` preference when two directories exist. Prototype line 23 already uses repository convention or its documented fallback; existence alone does not establish the active convention.

### Hard-coded ignore check and unconditional tracked commit

Exact vendor line 83:

> git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null

Exact vendor line 86:

> **If NOT ignored:** Add to .gitignore, commit the change, then proceed.

The OR expression checks alternatives rather than the actual selected destination. A tracked ignore change and commit are not always needed or authorized. Retain only candidate 1's principle; prototype line 24's local-exclusion option is preferable.

### Implicit base and editing the original checkout after failed isolation

Exact vendor lines 94–97:

> path="$LOCATION/$BRANCH_NAME"
>
> git worktree add "$path" -b "$BRANCH_NAME"
> cd "$path"

Prototype lines 21, 30–31, and 43–47 already select and verify an explicit base instead of relying on the invoking checkout's default. Prototype lines 21 and 63 also make the execution path explicit without assuming a tool changes the agent's directory.

Exact vendor line 100:

> **Sandbox fallback:** If `git worktree add` fails with a permission error (sandbox denial), tell the user the sandbox blocked worktree creation and you're working in the current directory instead. Then run setup and baseline tests in place.

Reporting the change does not make it consistent with a requested worktree or a concurrent-task separation requirement. Prototype line 13 requires separation when those conditions hold. Reject this work-in-place fallback; resolve the creation problem or report that the required checkout could not be established before dependent editing.

### Manifest-driven installers and generic command menus

Exact vendor line 104:

> Auto-detect and run appropriate setup:

Exact vendor lines 114–115:

> if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
> if [ -f pyproject.toml ]; then poetry install; fi

A manifest's presence alone does not establish the package manager, environment, or approved setup command. The vendor also assumes npm and Cargo setup at lines 108–111 and provides a test-command menu at line 127. Prototype line 62 already delegates setup to repository instructions. Reject automatic installers and stack-specific menus; keep only the optional baseline decision in candidate 2.

## Adversarial questions

1. Repository instructions require a worktree under `worktrees/task-a`. `.worktrees` is ignored but the selected `worktrees/task-a` destination is not. Does checking either directory suffice, and must the agent commit a `.gitignore` change before proceeding?
2. The agent starts in a linked worktree on detached HEAD, but it belongs to another worker's active task. Does being linked prove adequate isolation for the new task? What should the agent do before editing?
3. The user requires a separate worktree because another task is using the original checkout. The native tool lacks the needed operation and raw creation fails with a permission error. May the agent simply announce that it will work in the original directory?
4. Before edits, the relevant test already fails. The requested task is to fix that failure. Must the agent pause for permission to investigate, or can it record the baseline and continue authorized work?

## Separate grading keys

1. **Pass:** verify the actual selected project-local destination, use an appropriate ignored placement or exclusion, and do not require a tracked ignore commit categorically. **Fail:** accept the hard-coded OR check because `.worktrees` is ignored. Prototype lines 23–24 and 44 partially support the answer but leave the explicit location gap; candidate 1 makes it direct.
2. **Pass:** inspect ownership, branch, changes, and ongoing operations; reuse only a checkout belonging to this task with no competing owner, otherwise establish a separate task branch/checkout. Do not infer external management from detached HEAD. **Fail:** skip creation solely because the Git directories differ. Prototype lines 12–14, 20, and 33–34 suffice.
3. **Pass:** retain the isolation requirement, use a supported manager/fallback where possible, and report the block before dependent editing if it cannot be met. **Fail:** treat a sandbox denial as authorization to edit a competing checkout. Prototype lines 13 and 20–22 establish the requirement and supported fallback; it has no explicit creation-failure rule, but the vendor's proposed fallback contradicts its selection rule.
4. **Pass:** report/record the pre-edit failure and continue the authorized investigation using repository checks; request clarification only for unresolved scope or authority. **Fail:** impose an unconditional stop solely because baseline tests failed. Prototype lines 8 and 62–64 support continued scoped work, but do not expressly require pre-edit evidence; candidate 2 supplies that optional improvement without the vendor's permission gate.
