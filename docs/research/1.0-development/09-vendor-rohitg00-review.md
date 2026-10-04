# Vendor review 09: rohitg00 parallel-worktrees

## Inputs and scope

- Vendor: `C:/Users/MC/Documents/git-worktrees-prime/vendors/rohitg00-pro-workflowskillsparallel-worktrees-SKILL.md` (90 lines).
- Prototype: `C:/Users/MC/Documents/git-worktrees-prime/skills/prototype1-astra/SKILL.md` (114 lines).

Both files were read fully. Substantive evidence is limited to these two files. This reviewer thread was reused because of the session cap; earlier vendor findings were not used as evidence. ICM recall was context only. No skills were loaded, no external documentation was consulted, no vendor instructions were executed, and the prototype was not edited. Tool and Git behavior described by the vendor is not independently verified here.

## Incremental usefulness: D

No addition recommended. The vendor is a brief introduction to parallel sessions rather than a source of missing worktree best practices. The prototype already handles separate checkouts and branches, harness preference, explicit paths, starting state, shared resources, integration, preservation, and cleanup with more precise conditions.

S means essential missing protection; A means a substantial general improvement; B means a useful general addition; C means an optional clarification or narrow benefit; D means no useful addition. This grade measures incremental value for trained programming agents, not readability for a Git beginner.

## Potential gaps considered

### Parallel review and approach exploration — covered; no addition

Exact vendor quotes, lines 75–76:

> | Exploring approaches | Compare 2-3 simultaneously |
> | Review + new work | Reviewer in one, dev in other |

Prototype coverage: lines 13–13 already require separate branches and checkouts for parallel tasks; lines 34–34 and 52–53 offer detached inspection/testing; lines 77–78 retain checkouts while used or needed for review. The vendor provides examples of why to parallelize, not a missing lifecycle rule.

Minimal proposed wording: none. An optional example such as “Use a detached worktree for concurrent review” would restate existing capability without resolving an actual gap.

Realistic benefit of the vendor text: discoverability for a beginner who has not considered concurrent review. Caveat: the intended audience is trained agents; examples do not authorize additional tasks or agents, establish resource availability, or decide whether parallel work is beneficial.

### Overlapping-file work — not a missing isolation rule

Exact vendor quote, lines 84–84:

> - Avoid editing the same files in multiple worktrees simultaneously.

Prototype coverage: lines 13 and 16 explain separate working files/branches and shared state; lines 64–65 require the repository integration workflow, owner coordination, and validation after conflict resolution. Separate checkouts make concurrent file edits physically distinct; integrating divergent edits still requires coordination.

Minimal proposed wording: none. If a particular project needs ownership partitioning, put that in its task plan rather than impose a generic ban.

Realistic benefit: can reduce integration conflicts between related tasks. Caveat: multiple approaches, review fixes, or intentionally overlapping changes may legitimately touch the same repository-relative file in separate checkouts. The vendor's blanket advice conflicts with some of its own exploration use cases and supplies no integration procedure. The prototype's existing coordination and validation rules are enough for a trained agent.

## Redundant, unsafe, or project-specific material to reject

| Exact vendor quote and lines | Prototype comparison | Decision |
| --- | --- | --- |
| “Zero dead time. While one session runs tests, work on something else.” (9–9) | Lines 8 and 12–14 keep work tied to user instructions, repository conventions, ownership, and need for separation. | Reject productivity rhetoric as worktree policy. A pending test is not authorization to begin unrelated work or evidence of spare resources. |
| “Use when waiting on tests, long builds, exploring approaches, or needing to review and develop simultaneously.” (13–13) | Lines 13–14 already select worktrees when concurrent tasks require separation. | Covered. Waiting alone need not trigger checkout creation. |
| “claude --worktree    # or claude -w (auto-creates isolated worktree)” (19–19) | Lines 20–22 prefer actual available harness tools and require checking their starting-state and cleanup behavior. | Do not import provider-specific CLI syntax into generic guidance; the claim was not verified. |
| “Both approaches create an isolated working copy where changes don't interfere with your main session.” (28–28) | Line 16 explicitly names shared Git state, no security boundary, and possible shared ports/databases/output locations. | Reject unqualified non-interference. Working-file isolation is narrower than complete session isolation. |
| “- `claude -w` auto-creates and cleans up worktrees” (34–34) | Lines 20–22 and 110 require checking actual harness creation/cleanup/archive behavior. | Reject a universal lifecycle assumption. Keep harness-specific documentation separate and current. |
| “- Subagents support `isolation: worktree` in agent frontmatter” (35–35) | Lines 13 and 20 cover parallel separation and available harness capabilities without assuming a provider. | Provider-specific, unverified claim; no addition. |
| “- `Ctrl+F` kills all background agents (two-press confirmation)” (36–36) | Line 77 permits stopping only task-owned processes. | Reject a blanket agent-kill shortcut; it may affect unrelated work and belongs in product documentation. No shortcut behavior was tested. |
| “- `Ctrl+B` sends a task to background” (37–37) | Lines 20–22 defer to actual harness features. | Provider-specific UI control, not worktree best practice. |
| “1. Show current worktrees: `git worktree list`” (41–41) and “4. When done, clean up the worktree.” (44–44) | Lines 41–57 provide inventory, branch/base checks, and returned-path verification; lines 75–83 decide what can be cleaned. | Useful intent already covered. Do not replace explicit state and ownership checks with a four-step overview. |
| “git worktree add ../project-feat feature-branch” (51–51) and “git worktree add ../project-exp -b experiment” (53–53) | Lines 23–24 choose safe placement; lines 30–34 require the intended base and branch handling; lines 38–57 use exact paths and selected alternatives. | Redundant examples with weaker context. The new-branch example has no explicit base; neither example verifies the resulting checkout or branch occupancy. |
| “git worktree remove ../project-feat” (55–55) and “git worktree prune” (56–56) | Lines 75–83 and 88–110 distinguish preserved state, exact checkout removal, branch deletion, and reviewed stale metadata repair. | Reject copying unconditional cleanup commands. The prototype already offers the commands with necessary conditions. |
| “Each worktree runs its own AI session independently.” (67–67) | Lines 13 and 16 distinguish separate checkout ownership from shared Git/service resources. | Reject as a universal statement. Worktrees do not require AI sessions, and sessions may affect shared resources. |
| “| Tests running (2+ min) | Start new feature in worktree |” (73–73) and “| Waiting on CI | Start next task in worktree |” (77–77) | Lines 8 and 12–14 select a checkout for authorized tasks. | Reject arbitrary timing and automatic scope expansion. CI/test waiting can justify concurrent authorized work, not create authorization. |
| “- Each worktree is a full working copy — changes are isolated.” (81–81) | Lines 16 and 62 describe shared resources and possibly absent ignored setup files. | Overbroad shorthand. Keep the prototype's qualified isolation statement. |
| “- Before removing a worktree, verify changes are committed: `git -C ../project-feat status`” (82–82) | Lines 34, 79, 81, and 88–91 include detached commits, ignored/untracked state, incomplete operations, and durable preservation. | Reject committed/clean status as a complete preservation check. It neither establishes integration nor covers every valuable file/reference. |
| “- Don't forget to clean up worktrees when done (`git worktree prune`).” (83–83) | Lines 82 and 101–109 explain reviewed pruning and distinguish metadata from checkout/branch deletion. | Reject conflating pruning with removing worktrees. This is a substantive weakness in the written guidance; no command was run to test it here. |
| “- Current worktree list” (88–88), “- Created worktree path and branch” (89–89), and “- Instructions for opening a new session” (90–90) | Lines 28 and 114 keep relevant paths/refs in task context and report work, checks, integration, and retained/removed state. | Path and branch reporting are covered. A full inventory and new-session instructions need not appear after every lifecycle task. |

## Adversarial questions

1. Tests have been running for three minutes. The user authorized one bug fix, and the agent sees an unrelated feature to implement. Does the vendor's timing table authorize creating another task checkout and starting that feature?
2. Two authorized tasks use separate worktrees and branches. Both start a development server that writes to the same database and port; both modify the same repository-relative source file. Which effects are isolated, and what needs coordination?
3. A task checkout reports clean ordinary `git status`, but it contains an ignored local database needed for review and a valuable detached commit. Another registered worktree lives on an offline volume. Is committing changes followed by `git worktree prune` a sufficient cleanup procedure?
4. A harness can create a worktree but its default base, whether it moves the agent's working directory, and cleanup behavior are unknown. Can the agent rely on the vendor's auto-create/cleanup claims and begin editing immediately?

## Separate grading keys

1. **Prototype alone suffices.** Cite 8 and 12–14. Follow the authorized task scope; a long-running test does not itself justify unrelated feature work. A worktree separates approved concurrent work when needed, not a new feature mandate. The prototype is not a scheduling skill and need not add a timing threshold.
2. **Prototype alone suffices.** Cite 13, 16, 63–65. Separate files/indexes and branches isolate direct working-file edits; shared services and Git state can still interfere. Configure or coordinate database/port/output use, and integrate divergent source edits with the selected workflow and validation. Do not assume identical filenames in different checkouts mean physical concurrent writes to one file, or impose a blanket prohibition on legitimate overlapping work.
3. **Prototype alone suffices and is stronger.** Cite 34, 77–83, 88–91, and 109. Preserve review state and anchor valuable detached commits to a durable ref; keep needed checkout/resources; remove only an eligible exact checkout through its manager. Pruning concerns stale registrations, not active checkout or branch removal, and unavailable volumes must not be treated as intentional deletions. Ordinary clean status is insufficient evidence.
4. **Prototype alone suffices.** Cite 20–22, 28–34, and 55–57. Inspect actual harness semantics, supply the intended base, wait for completion, verify returned path/commit, and run subsequent operations in that path. Use the manager for managed cleanup. The vendor's Claude Code claims are source statements, not verified behavior of the current harness.

## Recommendation

Keep the prototype unchanged. Do not add parallel-session scheduling, provider shortcuts, extra examples, or an overlapping-files prohibition. The useful worktree lifecycle guidance is already present, and the vendor's cleanup/isolation shorthand would weaken it.
