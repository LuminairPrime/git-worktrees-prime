# Vendor review: heyitsnoah / claudesidian

## Inputs and scope

- Vendor: `C:/Users/MC/Documents/git-worktrees-prime/vendors/heyitsnoah-claudesidian-.agentsskillsgit-worktrees-SKILL.md` (187 lines).
- Prototype: `C:/Users/MC/Documents/git-worktrees-prime/skills/prototype1-astra/SKILL.md` (114 lines).

Both files were read fully. This is a source comparison, not a Git behavior test: no vendor commands were executed, no external documentation was consulted, and the prototype was not edited. ICM recall supplied task context only; it is not evidence for the findings.

## Incremental usefulness: D

No substantive addition recommended. The vendor provides a short introductory tutorial and concrete examples, but the prototype already covers its useful worktree lifecycle guidance with fewer unsafe assumptions. For trained programming agents, importing the tutorial, troubleshooting recipes, or PR-specific cleanup gate would add repetition or weaken existing safeguards.

## Candidate guidance and prototype coverage

### Setup in the new checkout: already covered

Vendor lines 67–80:

> After creating a worktree, you typically need to:
>
> ```bash
> cd .worktrees/my-feature
>
> # Install dependencies
> npm install  # or pnpm install, yarn, etc.
>
> # Copy any required env files
> cp ../.env .env.local
>
> # Verify setup
> npm test
> ```

Prototype lines 62–63 already require repository-directed dependency/configuration setup and keeping builds/tests in the selected path. Prototype line 62 explicitly handles missing ignored dependencies, secrets, and outputs without bulk copying. No gap supports an addition.

Minimal proposed addition: none. The realistic benefit of the vendor example is reminding a novice that checkout creation is not environment setup. That benefit is already present in the prototype. The Node commands and environment-copy path depend on a particular project layout; the file does not establish that the example's source path or destination configuration name is correct.

### Separate branch cleanup: already covered more precisely

Vendor lines 90–94:

> # If empty, safe to remove
> git worktree remove .worktrees/my-feature
>
> # Delete the branch after merge (-d is safe, fails if not merged)
> git branch -d feat/my-feature

Prototype lines 75–83 distinguish checkout removal, branch deletion, and stale metadata. Lines 79 and 88–90 account for ignored state as well as ordinary status; lines 81 and 106–107 require evidence against the intended integration target and handle rewritten history. No gap supports an addition.

Minimal proposed addition: none. The benefit of deleting an obsolete task branch is already covered. The vendor's claim that empty status establishes safe removal overlooks state and ongoing use that the prototype explicitly checks. Its parenthetical description of `-d` is a source claim, not verified here; the prototype already warns against treating command success as integration evidence.

### Branch occupancy troubleshooting: already covered without displacement

Vendor lines 161–168:

> A branch can only be checked out in one worktree at a time:
>
> ```bash
> # Find where branch is checked out
> git worktree list
>
> # Remove that worktree first, or use different branch
> ```

Prototype line 33 already gives the useful response: reuse the occupied checkout through its owner or create another branch from the required commit, and never override checkout protection. Lines 12 and 77 protect another worker's checkout. The inventory command is already at line 41.

Minimal proposed addition: none. Finding the occupied checkout is useful, but adding a troubleshooting heading offers no new decision guidance. The vendor's removal option needs ownership and preservation qualifications and could displace active work.

## Content to reject

- **PR merge as a mandatory checkout-retention gate.** Vendor lines 99–104 say:

  > | PR Merged? | Uncommitted Changes? | Action |
  > |------------|---------------------|--------|
  > | Yes | No | Safe to remove |
  > | Yes | Yes | Ask user - changes will be lost |
  > | No | No | Do NOT remove - work not preserved |
  > | No | Yes | Do NOT remove - active work |

  An unmerged PR is not itself evidence that committed work disappears with checkout removal. Prototype lines 78 and 81 already distinguish local review needs from durable refs, and lines 79–80 handle preservation and ownership. The matrix also overstates safe removal after merge and clean status. Reject rather than add a permission gate or require every task to use a PR.

- **Force as the default response to a nonempty directory.** Vendor lines 173–174 say:

  > # Force add if directory exists but isn't a worktree
  > git worktree add --force <path> <branch>

  This source provides no explanation of the refusal or proof that this command solves that condition safely. Prototype line 23 selects an unused path, line 33 forbids overriding checkout protection, and line 108 requires resolving refusals rather than forcing them. Reject the recipe; its operational validity was not tested.

- **Unlock and remove without investigating the lock.** Vendor lines 179–187 say:

  > If a worktree is locked (prevents accidental removal):
  >
  > ```bash
  > # Unlock it
  > git worktree unlock <path>
  >
  > # Then remove
  > git worktree remove <path>

  Prototype lines 82 and 108 already protect unavailable or deliberately locked worktrees and require resolving the cause. Reject routine unlocking as cleanup.

- **Review cleanup with unconditional forced branch deletion.** Vendor lines 141–143 say:

  > # Review, test, then clean up
  > git worktree remove .worktrees/pr-123
  > git branch -D pr-123

  The example omits state/ownership checks and proof that any review changes remain preserved. Prototype lines 34, 79–81, and 107 cover this directly. Reject the shortcut.

- **Automatic prune after a manually missing directory.** Vendor lines 126–130 say:

  > If a worktree directory was deleted manually:
  >
  > ```bash
  > git worktree prune

  Prototype lines 82 and 101–103 already require reviewing all dry-run entries before a prune. A justified cleanup of one missing registration does not justify silently affecting other entries. Reject the unconditional command.

- **Assumed base, remote, location, editor, and stack.** Vendor examples use `main` (line 41), `origin` (lines 48 and 138), `.worktrees` (lines 38–41), Node setup (lines 73–79), and `code` (line 154). Prototype lines 20–24, 30–31, and 62 already leave these choices to the harness, repository, and task. Examples are not evidence of a universally correct default. Reject their promotion into requirements.

- **Generic Git explanation and repeated command tables.** Vendor lines 10–20 and 24–30 introduce use cases and common commands. Prototype lines 12–16 and 36–58 already convey the decisions and selected commands an agent needs. No additional tutorial is warranted.

## Adversarial questions

1. A reviewed PR is still open. Its branch is pushed, the task checkout has no valuable local state, no worker uses it, and review can continue remotely. Must the agent retain the checkout until merge? Which resources may be removed or retained, and why?
2. A task PR was merged and ordinary status is empty, but the checkout contains an ignored private configuration file. Another terminal still uses the directory. Can the agent remove it immediately and call the task cleaned up?
3. Worktree creation refuses because the desired branch is already checked out elsewhere. That other checkout is locked and presently unavailable. Should the agent remove/unlock it, force creation, or choose another approach?

## Separate grading keys

1. **Pass:** distinguish checkout removal from branch deletion; permit removal once actual preservation, ownership, and use checks pass; retain the necessary branch/ref for pending review. Cite prototype lines 75–81. **Fail:** require PR merge categorically, or delete the review branch merely because it is pushed. This tests whether the vendor matrix adds value; prototype alone suffices.
2. **Pass:** stop task-owned use, leave the directory, preserve valuable ignored configuration outside the removal path or obtain discard authorization, then remove the exact verified checkout through its manager. Report any retained resource. Cite prototype lines 77, 79–80, 83, and 88–90. **Fail:** treat empty ordinary status and merged PR as enough. Prototype alone suffices.
3. **Pass:** inspect ownership/inventory; reuse the occupied checkout through its owner when available or create another task branch from the required commit. Do not remove another worker's checkout or bypass the lock/protection to clear a refusal. Cite prototype lines 12, 33, 77, 82, and 108. **Fail:** follow the vendor's remove-first, unlock-first, or force recipe. Prototype alone suffices.
