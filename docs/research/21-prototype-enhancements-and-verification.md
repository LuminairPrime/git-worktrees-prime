# Prototype enhancements and verification

Verified and applied on 2026-10-03. The original trial guide remains in `tests/inputs/prototype.md`; historical reports, results, and manifests describe that version. The current skill now includes the changes below.

## Claims checked

Read-only checks against all six preserved trial repositories confirmed the saved outcomes:

- Custom destinations remained unignored in r01, r03, r04, and r05.
- The moved adapter checkouts in r03, r04, and r06 still registered `adapter-old`, although the actual checkout was `adapter-current`.
- r02's report records an unnecessary cleanup refusal while preserving the database and branch. The prototype already permits preserving review state outside a removed checkout.
- The earlier patched guide broadened the ignore instruction and corrected the prune comment, but contained no positive repair instruction. Its results therefore do not test the new repair guidance.

These observations support narrow corrections. They do not establish that the revised skill improves Luna's success rate; no new model trial was run for this patch.

## Changes applied

1. Verify a reused checkout's current absolute path and branch against inventory. Give the raw Git repair command for relocated live checkouts, followed by inventory verification.
2. Require ignore coverage for the actual nested destination before and after creation. Use a directory path ending in `/` and require `check-ignore -q` to return 0. Resolve the local exclude file to an absolute path.
3. Verify retained checkout path, branch or detached commit, registration, and required ignore coverage before reporting readiness.
4. Correct the prune comment and make the protected parent-directory rule apply to custom locations too. Remove the elementary merge-command example; integration authority, ownership, and validation guidance remain.

Shared-stash wording and failed-isolation wording were optional proposals, not demonstrated gaps in these trials, and were not added.

## Command verification

The [Git worktree reference](https://git-scm.com/docs/git-worktree) distinguishes repair of relocated live checkouts from pruning stale registrations. [gitignore](https://git-scm.com/docs/gitignore) defines directory-only patterns; [check-ignore](https://git-scm.com/docs/git-check-ignore) documents the check and its exit status. Context7 was unavailable, so verification used these official pages and the installed Git.

A fresh disposable repository under `tests/.runs/patch-verification-20261003/` exercised the commands with Git 2.53.0.windows.1:

| Check | Observed result |
|---|---|
| Rule `/scratch-checkouts/task/`, nonexistent bare path `scratch-checkouts/task` | Exit 1: the directory-only rule did not match this probe |
| Same rule, nonexistent `scratch-checkouts/task/` | Exit 0 |
| Same rule, prospective child `scratch-checkouts/task/.git` | Exit 0 |
| Different destination `different-checkouts/task/` | Exit 1 |
| Selected directory after worktree creation | Exit 0 |
| Manually move this fixture's checkout | Git still operated inside it; inventory retained the old path |
| Repair using the new absolute path | Inventory listed the new path and omitted the old one; task branch retained |
| Untracked draft before and after repair | Identical SHA-256: `BDB3A3E9345375C112B8AE6A93D935F501CC70D50571B98FA65E9D27F7DAD7A5` |

The skill validator and `git diff --check` passed. The original guide SHA-256 is `0159CB4E95DCAE9463A4A2394081BEBBDB4B1E83EDD301E32B8AE7CD42CC47E2`; after these command-guidance changes it was `2E46F222E5EDFD532AEF56C0293AE4F1B9FEE13A1870FF74DC45C270133A1CB6`.

Future behavioral experiments must record their actual guide input. The existing setup script reads the current skill, so a new setup would no longer reproduce the original guide treatment automatically.

## Terminology added before sharing

At the user's request, a short glossary now defines repository, worktree/checkout, branch, HEAD/detached HEAD, main/linked worktree, base/integration target, and registration. It explains the branch/worktree relationship and asks readers to name paths and branches separately. Definitions were checked against the [Git glossary](https://git-scm.com/docs/gitglossary) and worktree reference. The branch-retention sentence was moved from cleanup into the glossary to avoid duplication.

Skill validation and whitespace checks passed again. The skill SHA-256 after this terminology edit is `2F7F933A25D980234221344BA9C1ED4E5C76CE2984DCB89D8A48983426EF51BA`. This addition supports a shared vocabulary for people and agents; it has not undergone a new model trial.
