# Vendor review 03: davidondrej git-worktree

## Inputs and scope

- Vendor: `C:/Users/MC/Documents/git-worktrees-prime/vendors/davidondrej-skillsskillsagent-orchestrationgit-worktree-SKILL.md` (89 lines).
- Prototype: `C:/Users/MC/Documents/git-worktrees-prime/skills/prototype1-astra/SKILL.md` (114 lines).

Both files were read fully. This is a comparison of their written instructions, not verification of Git, Cursor, package-manager, Docker Compose, or bundler behavior. No lifecycle commands or vendor instructions were executed. ICM recall supplied context only and did not determine the findings.

## Incremental usefulness: C

The vendor offers one small optional clarification: writable local configuration linked to another checkout can couple edits. Its setup checklist also makes shared hooks more concrete, but the prototype already covers shared configuration and coordination. The remaining guidance is redundant, more prescriptive than necessary, or tied to Cursor and particular application stacks. No workflow expansion is justified.

For this report, S means essential missing protection; A means a substantial general improvement; B means a useful general addition; C means an optional clarification or narrow benefit; D means no useful addition. The grade measures value beyond this prototype, not the vendor in isolation.

## Candidate additions

### 1. Optional warning about writable configuration symlinks — C

Exact vendor quote, lines 50–50:

> 1. **Env/secret files** — copy `.env`, `.env.local`, and similar files from the primary checkout. Never symlink them: edits would change the originals.

Prototype coverage: lines 16–16 explain that worktrees provide no security boundary and share configuration; lines 32–32 require deliberate transfer instead of silent copying; lines 62–62 require repository-directed setup and prohibit bulk copying ignored dependencies, secrets, and outputs. Those instructions do not explicitly say that a symlink to writable local configuration lets edits affect another checkout.

Minimal proposed addition to prototype line 62, if this failure mode merits spelling out:

> Do not symlink writable local configuration from another checkout unless sharing those edits is intentional.

Realistic benefit: prevents an agent from substituting a seemingly convenient link for a local configuration file and unintentionally changing another task's environment. It expresses the risk without mandating that secrets be copied.

Caveats: a trained agent may already infer this from isolation and repository setup instructions. Intentional sharing can be valid. The vendor's absolute prohibition and automatic secret-copy instruction should not be imported. This is optional, not evidence that the prototype is generally insufficient.

### 2. Shared hooks as a concrete example — C individually; omit from minimal patch

Exact vendor quote, lines 55–55:

> 6. **Git hooks** — `core.hooksPath` and `.git/config` are shared; verify hook scripts don't assume the primary checkout's path.

Prototype coverage: lines 16–16 already say that much Git configuration is shared and require coordinating shared mutations; lines 20–22 defer to harness behavior; lines 62–63 require repository setup and execution in the selected path. The gap is an explicit example of a shared setting or path-sensitive script, rather than a missing general rule.

Minimal possible addition to prototype line 16:

> Treat hook configuration as potentially shared, and check checkout-specific path assumptions when hooks fail.

Realistic benefit: helps diagnose a hook resolving files against a different checkout, and discourages treating a task-local hook-setting change as isolated.

Caveats: the vendor's categorical configuration claim is not verified here. The prototype deliberately says “much Git configuration,” which is safer than copying a universal statement. A generic skill need not enumerate every shared setting, and a speculative hook audit on every task would add ceremony. Do not add this sentence unless actual hook failures justify it.

## Content to reject or leave covered

| Exact vendor quote and lines | Prototype comparison | Decision |
| --- | --- | --- |
| “- **Primary checkout** → create a task-named worktree, complete the setup below, and `cd` into it before editing.” (19–19) | Lines 12–14 choose reuse, separation when required, or the current checkout; lines 21 and 63 keep operations in the selected path. | Reject mandatory worktree creation. It adds unnecessary checkout/setup work when isolation is not required. The detection command at 15–16 cannot establish task ownership or suitability. |
| “- **Worktree** (including one created by Cursor) → proceed with the task.” (20–20) | Lines 12–12 require inspecting ownership, changes, branch, and ongoing operations; lines 28–34 establish the intended start. | Reject this shortcut. Being in a linked checkout does not make it the correct task checkout. |
| “- **One task = one worktree = one agent session.** Never share a working directory between agents.” (26–26) | Lines 12–13 and 77–80 cover ownership and separate concurrent task checkouts. | Retain the isolation principle already present; reject a rigid session-to-worktree identity that prevents legitimate continuation. |
| “- Keep the primary checkout on main, only for review, merging, and pushing.” (27–27) | Lines 8 and 30 require repository conventions and an inspected integration target. | Reject a fixed branch name and exclusive checkout role. |
| “- Nothing auto-merges. The human reviews each diff before merging or discarding the worktree.” (28–28) | Lines 64–65 make integration depend on workflow and authority; lines 75–81 distinguish safe cleanup from unresolved authority or data loss. | Reject universal manual approval. Preserve the prototype's authority-sensitive rule. |
| “- Keep task branches local and short-lived. Push only main unless the user explicitly asks to push a task branch.” (29–29) | Lines 64–66 already limit publishing to authority and distinguish review preservation from integration. | Reject a main-only publishing policy incompatible with many PR workflows. |
| “- Merge one worktree at a time. If main moved, rebase the task branch before merging.” (30–30) | Lines 64–65 permit repository merge, rebase, squash, or PR workflows and validate integration. | Coordination is covered. Reject compulsory rebase and assumed main target. |
| “A branch can be checked out in only one worktree, including main.” (42–42) | Lines 33–33 explain how to handle an already checked-out branch and prohibit overriding protection. | Redundant; the prototype gives the actionable response. |
| “Cursor auto-deletes older worktrees, so preserve results promptly; pushing task branches still requires explicit approval.” (excerpt, 44–44) | Lines 20–22 require checking actual harness behavior; lines 79–80 and 110 cover preservation and managed cleanup. | Do not import unverified Cursor lifecycle behavior or tool names. Useful general lesson is already present. |
| “A fresh worktree contains tracked files only. Bootstrap it before task work:” (48–48) | Lines 32–32 and 62–62 already warn about absent local state and require repository setup. | Redundant source claim, not an independently verified guarantee of every harness creation path. |
| “Never symlink `node_modules` from the primary checkout: bundlers such as Next.js/Turbopack reject paths outside the worktree.” (excerpt, 51–51) | Lines 62–62 require repository-directed dependency setup. | Reject a universal stack-specific prohibition and the adjacent `rm -f node_modules` repair recipe. Dependency layout and removal should follow the actual repository and platform. No bundler claim was verified. |
| “For shared Docker Compose services, pin the project name, for example with a top-level `name:`; otherwise each worktree's folder name creates a separate project.” (excerpt, 52–52) | Lines 16–16 already mention service ports, databases, and output locations; line 62 delegates setup to the repository. | Useful for some Compose projects, but not generic worktree guidance. Shared service identity can also cause cross-task interference; choose it deliberately. |
| “4. **Ports** — run dev/test servers and debuggers one at a time, or configure separate ports per worktree.” (53–53) | Lines 16–16 cover distinct ports and service state; line 77 covers active processes during cleanup. | Redundant. |
| “5. **Generated files and caches** — rebuild gitignored output in the worktree (`npm run build`, codegen).” (54–54) | Lines 62–63 cover absent outputs and repository-directed builds/tests. | Redundant; always rebuilding outputs can waste work when the task does not need them. |
| “Otherwise, put the checklist in `scripts/setup-worktree.sh` and run it first in each new worktree.” (excerpt, 70–70) | Lines 62–62 already use existing repository instructions. | Reject mandatory new automation. Add a helper only for repeated, demonstrated setup work. Cursor JSON at 59–68 belongs in harness-specific documentation. |
| “- Rebase or restart worktrees that have stalled for days.” (88–88) | Lines 12, 30–34, and 64–65 inspect actual task and integration state. | Reject age as sufficient reason to rewrite or restart work. |
| “- Commit early and often. Deleting a worktree loses uncommitted work; commits remain in the shared repository.” (89–89) | Lines 34, 79, 81, and 110 require preserving valuable detached, local, or archived state and durable refs. | Preservation is covered more precisely. Commit frequency is project policy; a commit existing in the object store does not establish a durable reference after branch removal. |

The vendor's terse removal and prune commands (35–39 and 79–82) should not displace the prototype's separate checkout, branch, and metadata decisions (75–83), exact-path checks (80), integration verification (93–107), and refusal handling (108–110). The prototype is materially stronger here.

## Adversarial questions

1. You land in an existing linked checkout belonging to a different unfinished task. It has local modifications. The current request is a small unrelated fix. Does detecting “worktree” authorize immediate edits, and how do you choose the checkout?
2. The new checkout lacks `.env.local`. A symlink to another checkout would make setup quick, but this task must change one environment value. What should you do, and how much of that answer does the prototype state explicitly?
3. A hook fails after worktree creation because it refers to the primary checkout's absolute path. An agent proposes changing `core.hooksPath` and assumes that change affects this worktree alone. What must be checked before the change?
4. A task branch was squash-integrated into a release branch. The checkout contains an ignored SQLite file used for review, and a registered sibling worktree is on an unavailable disk. Can the agent run the vendor's merge/remove/branch-delete/prune sequence as routine cleanup?

## Separate grading keys

1. **Prototype alone suffices.** Cite 12–14, 28–33, and 63. Inspect ownership and state; reuse only a suitable task checkout, otherwise create separation when needed. Do not overwrite or commandeer another task's checkout. The vendor's line 20 is insufficient.
2. **Prototype gives the governing rule; optional symlink sentence gives explicit mechanism.** Cite 32 and 62. Follow repository setup, obtain only required local configuration deliberately, and avoid modifying another checkout's configuration accidentally. A full answer recognizes that editing a symlink target changes shared state. The prototype does not name symlinks; that is the narrow candidate addition, not a reason to mandate copying secrets.
3. **Prototype alone supplies the safety boundary, with ordinary Git knowledge needed for the specific setting.** Cite 16, 62–63. Determine configuration scope and hook path assumptions; coordinate effects on other tasks. Do not assume isolation merely because the command runs inside the task checkout. A correct answer need not reproduce the vendor's categorical configuration claim or audit every hook preemptively.
4. **Prototype alone suffices and is stronger.** Cite 75–83 and 106–110. Preserve the review database if still needed; verify squash replacement changes rather than relying on ancestry or branch deletion success; remove only the exact eligible checkout through its manager; inspect prune dry-run entries and retain unavailable-volume registrations. Cleanup must not force removal or conflate branch, checkout, and stale metadata deletion.

## Recommendation

Keep the prototype workflow. At most add the one sentence about intentionally sharing writable local configuration. Skip the setup checklist, Cursor commands, mandatory scripts, branch policy, and additional approval ceremony.
