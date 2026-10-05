Your working directory (`/tmp/skill-up-2302634821`) is empty and isn't a git repo, so there's no project here to inspect — below is the general policy. If you point me at the actual repo, I'll check its real default branch and set this up.

## 1. What base to use

Base your feature worktree on the **current tip of the branch the repo actually integrates into**, fetched fresh:

```bash
git fetch origin
git worktree add ../proj-feature-x -b feature/x origin/<integration-branch>
```

Freshness matters more than branch choice: branch from `origin/<integration>` (or `origin/main`), not from a local checkout that may be days stale.

Special cases:
- **X depends on an open PR** — base on that PR's branch, or base on integration and rebase after it merges. Pick one deliberately; don't let it happen by accident.
- **X is a large/risky change** — consider a short-lived spike branch off integration first, then the real branch.
- **Repo with no commits yet** (like this directory) — there's nothing to base on; `git init`, commit a root, then branch.

## 2. Should you assume `main`?

**No — verify it.** `main` is the common default but the real integration target is wherever PRs actually merge:

```bash
git remote show origin | grep -i 'head branch'   # default branch
git branch -r                                    # look for develop, trunk, master, release/*
```

If the repo uses `develop`, `trunk`, `master`, or a `release/*` line, branching off `main` means your feature is based on the wrong code. Also confirm the project's rebase-vs-merge policy before you start, since that changes how you keep the branch current.

## 3. Task branch vs. disposable inspection checkout

They're different jobs, so give them different worktrees:

**Task branch** — carries your work, keeps state, gets a named branch:
```bash
git worktree add ../proj-x -b feature/x origin/main
```

**Inspection checkout** — read-only peek at someone else's branch, a tag, or a bisect target. Use a **detached HEAD** so no branch is created and nothing can accidentally be committed into your branch namespace:
```bash
git worktree add --detach ../proj-inspect origin/some-other-branch
# ...read, build, test...
git worktree remove ../proj-inspect
```

Rules that prevent most worktree pain:

| Rule | Why |
|---|---|
| Never two worktrees on the same branch | git refuses this outright |
| Keep your primary checkout on integration, clean | it's your anchor for fetching and rebasing |
| Commit only in the task worktree | commits in a detached inspection worktree are unreferenced and easy to lose |
| Name worktrees by purpose (`proj-x`, `proj-inspect`) | `git worktree list` stays readable |
| Use `--lock` for long-lived shared worktrees | protects against accidental `prune` |

Housekeeping: `git worktree list` to see them all, `git worktree prune` to clear stale entries after a manual delete.

Want me to run this against a specific repo? Tell me the path or clone URL and I'll confirm the integration branch and create the worktrees.
