# Official Git worktree documentation versus prototype1-astra

## Inputs and scope

- Vendor: `C:/Users/MC/Documents/git-worktrees-prime/vendors/official-git-worktree-doc.md` (303 lines).
- Prototype: `C:/Users/MC/Documents/git-worktrees-prime/skills/prototype1-astra/SKILL.md` (114 lines).

Both files were read fully. This is a source comparison only: no Git behavior was tested, no vendor instructions were executed, and the prototype was not modified. The vendor snapshot labels itself Git 2.56.0 at line 26; that version and its applicability to an installed Git were not independently verified. ICM recall supplied prior review context, not evidence for findings.

## Incremental usefulness: B

The official reference offers two small, conditional additions: distinguish relocation repair from deletion pruning, and flag submodule limitations before creation. Most normal task worktree guidance is already present. This is useful edge-case coverage, not a reason to turn the prototype into a Git manual. Tier scale: S = indispensable, A = substantial, B = useful narrow additions, C = marginal, D = no useful addition.

## 1. A moved live checkout needs repair, not prune

Exact vendor quotes:

> “Also, if you moved a working tree elsewhere causing the worktree information to become dangling, see "git worktree repair" to reconnect the worktree to the new working tree location.” (line 76)

> “Similarly, if the working tree for a linked worktree is moved without using git worktree move, the main worktree (or bare repository) will be unable to locate it. Running repair within the recently-moved worktree will reestablish the connection.” (line 86)

> “For instance, if the main worktree (or bare repository) is moved, linked worktrees will be unable to locate it. Running repair in the main worktree will reestablish the connection from linked worktrees back to the main worktree.” (line 84)

Prototype comparison: lines 82 and 101–103 correctly restrict pruning to intentionally removed worktrees, but provide no positive recovery route when a missing registration represents a relocated live checkout. Line 101 calls its prune example “stale registrations need repair,” which blurs the two operations. Line 108 tells the agent to resolve the cause of a refusal, so a trained agent might recover without more guidance; the specific repair command remains absent.

Minimal proposed addition, beside cleanup step 6:

> If a live checkout or its main repository was moved, use `git worktree repair` from the appropriate surviving location; pruning is for intentionally removed checkouts.

Also change the line 101 comment to “Only if intentionally removed worktrees left stale registrations; review the dry run before pruning.” No new command block or relocation workflow is necessary.

Realistic benefit: an agent encountering stale paths after a directory rename gets the correct recovery operation immediately and avoids treating a still-needed checkout as deleted. Caveat: this is the documented recovery route, not a guarantee that every damaged registration can be repaired. The vendor's lines 84–88 describe different invocation locations and path arguments for different moves; consult those details when an actual relocation occurs. Do not automate repair merely because a directory is unavailable.

## 2. Submodule caution belongs before creation as well as cleanup

Exact vendor quotes:

> “Note that the main worktree or linked worktrees containing submodules cannot be moved with this command.” (line 73)

> “Multiple checkout in general is still experimental, and the support for submodules is incomplete. It is NOT recommended to make multiple checkouts of a superproject.” (line 297)

Prototype comparison: line 79 requires separate inspection of submodules and nested repositories before removal, and line 108 acknowledges that submodules may require another removal method. Lines 12–24 and 30–34 have no submodule caveat when selecting or creating a checkout. The vendor therefore adds an earlier decision point rather than another cleanup warning.

Minimal proposed addition, in checkout selection or manager choice:

> If the repository uses submodules, check its worktree instructions first; Git documents incomplete submodule support, so do not assume the ordinary lifecycle applies.

Realistic benefit: prevents an agent from promising routine move/cleanup behavior for a submodule checkout before checking project support. Caveats: line 297 is the snapshot's broad warning, not a tested failure in this repository or proof that every superproject workflow fails. Do not turn it into a universal prohibition, mandatory user approval, or a custom submodule-management procedure. For agents that already know the limitation, this addition has little value.

## Optional details that do not earn more default guidance

- **Machine parsing:** vendor line 141 says porcelain output is stable across versions/configuration and recommends `-z`; line 144 explains newline-containing paths. Prototype lines 41 and 99 already use `--porcelain`. If a parser is actually implemented, use `--porcelain -z` with a NUL-aware parser. A task instruction that only inspects output needs neither parsing machinery nor another mandatory command.
- **Repository configuration:** vendor line 181 says repository config is shared by default, and lines 183–196 describe the opt-in worktree configuration extension and compatibility consequences. Prototype line 16 already warns that much configuration is shared and requires coordination. A more concrete `git config --local` warning is possible, but it repeats that principle; do not enable the extension preemptively.
- **Locks on intermittent storage:** vendor lines 51 and 69–70 explain preventive locking. Prototype line 82 already prevents destructive pruning/unlocking of an offline volume. Mention locking only if the task actually creates a checkout on intermittently mounted storage; ordinary local task worktrees do not need another lifecycle step.

## Redundant, unsafe, or context-specific content to reject

- Vendor lines 43–55, 102–108, and 277–284 largely repeat the prototype's isolation model, explicit branch/detached creation, and removal examples (prototype lines 13–16, 33–34, 46–53, 97–99). The emergency-fix narrative adds no agent instruction.
- Do not adopt implicit path-derived branches or implicit `HEAD` bases from vendor lines 47, 62, 104, and 288–289. Prototype lines 21, 30, and 46–53 deliberately keep base and branch explicit. Do not import the example's `master` as an integration policy.
- Reject routine `--force`, double-force, or `-B` recovery recipes from vendor lines 96–104. They describe bypassing safeguards, not appropriate authority. Prototype lines 33 and 108 already protect other checkouts and valuable state.
- Reject direct editing of administrative files from vendor line 207. Its own safer recommendation is `git worktree repair`; the prototype need not teach Git internals to fix relocation.
- Do not reproduce ref exceptions, internal directory layouts, or cross-worktree ref addressing (vendor lines 169–178 and 198–211). Prototype line 24 already uses `git rev-parse --git-path` for its concrete filesystem need. The remainder is reference material for an actual specialist task.
- Do not adopt `--guess-remote`, `--orphan`, sparse checkout, or relative-path configuration as standard setup (vendor lines 112–138 and 288–294). Each solves a separate need and some configuration changes affect compatibility. None is needed for the prototype's explicit task checkout flow.
- Do not treat “clean” removal from vendor line 79 as sufficient preservation evidence. Prototype lines 79 and 88–90 correctly include ignored local state, detached commits, and unfinished operations. The vendor's terse cleanup example should not weaken those checks.

## Adversarial questions

These are evaluation prompts, separate from the grading keys below. Give an evaluator the prototype alone and compare its answers with the keys; the vendor adds value only where it changes a consequential decision.

1. A task checkout was renamed with a file manager. The old path appears missing in `worktree list`, but all task files still exist at the new path. How should you recover it, and should you prune first?
2. The main repository directory was moved; its linked task checkout still exists but cannot locate its Git metadata. Where should recovery start, and is recreating the task branch necessary?
3. You are asked to create and later relocate a task checkout in a repository with submodules. Is the prototype's ordinary create/move/remove lifecycle enough to promise success?
4. A script must inventory worktrees whose paths may contain newlines. Is parsing `worktree list --porcelain` by newline sufficient? What should it use instead?

## Grading keys

1. **Pass:** preserve the relocated checkout, do not prune it as intentionally removed, and use `git worktree repair` within the moved checkout (vendor line 86). **Partial:** correctly refuses pruning and investigates without naming repair. **Fail:** prune, force-add, or delete/recreate the live checkout without preserving it. Prototype lines 82 and 108 supply restraint; vendor supplies the direct recovery command.
2. **Pass:** run repair in the relocated main worktree to restore links (vendor line 84), retaining existing work; no branch recreation is implied. **Partial:** preserves both paths and investigates safely. **Fail:** assumes branches vanished or prunes linked registrations merely because their connections broke. Prototype alone has no relocation instructions.
3. **Pass:** check repository support/instructions, acknowledge incomplete documented submodule support, and do not promise `git worktree move` for a linked checkout containing submodules (vendor lines 73 and 297). **Partial:** recognizes the prototype's submodule cleanup caveats but misses the move limitation. **Fail:** promises the normal lifecycle without qualification, or prescribes force-removal as its fallback. Prototype lines 79 and 108 are relevant but late.
4. **Pass:** use `git worktree list --porcelain -z` and parse NUL-terminated output (vendor lines 140–144). **Partial:** recognizes escaping or unusual paths and consults the reference. **Fail:** assumes every newline is a record/attribute delimiter. This is parser-specific; a correct answer does not justify adding parser guidance to every task workflow.

## Recommendation

Consider only the relocation/prune distinction and a one-sentence submodule caveat. Keep the rest as reference knowledge. The prototype already covers normal worktree use, ownership, starting-state selection, integration, and preservation more completely than the vendor's usage examples.
