# Development Environment Setup — `add-config-validation`

**Status:** ✅ Ready for development
**Prepared:** 2026-10-03
**Feature:** Validate application configuration files against a known schema at startup.

This document records the isolated development environment prepared for the
`add-config-validation` feature and the evidence that it is correctly set up.
No feature code was written — this is environment preparation only.

---

## 1. Repository initialization

The repository was brought to its expected state by running the provided script:

```bash
bash setup/setup.sh
```

> **Note on the initial run:** the script's final step is `git checkout main`,
> but the environment's git defaulted new repositories to the branch name
> `master`, so the first run failed with
> `error: pathspec 'main' did not match any file(s) known to git`.
> The repository's own `README.md` names the production branch `main`, so the
> default was corrected and the script re-run from a clean directory:
>
> ```bash
> git config --global init.defaultBranch main
> rm -rf myproject && bash setup/setup.sh
> ```
>
> The second run completed successfully and produced the expected history.

The repository lives at `/workspace/solution/myproject`.

## 2. Branching conventions (from the repository)

`README.md` defines the team's integration workflow:

- **`main`** — production-ready releases only. *Do not develop directly on this branch.*
- **`develop`** — integration branch for all feature work. Pull requests are opened against `develop`.
- **All new features branch from `develop`.**

Current refs:

```
  add-config-validation 833ced7 (/workspace/solution/add-config-validation) Add config loader tests
  develop               833ced7 Add config loader tests
* main                  a94f781 Initial project setup
```

Commit graph:

```
* 833ced7 (add-config-validation, develop) Add config loader tests
* fe94603 Add config loader module
* a94f781 (main) Initial project setup
```

## 3. Isolated workspace (git worktree)

Because `main` and `develop` must not be disrupted, the feature is developed in a
dedicated **git worktree** — a separate working directory backed by the same
repository, with its own checked-out branch. This keeps the feature's files,
dependencies, and commits fully isolated from the main working tree.

```bash
# run from /workspace/solution/myproject
git worktree add -b add-config-validation ../add-config-validation develop
```

| Property | Value |
| --- | --- |
| Worktree path | `/workspace/solution/add-config-validation` |
| Feature branch | `add-config-validation` |
| Branched from | `develop` (integration branch, per README) |
| Base commit | `833ced7` — *Add config loader tests* (= `develop` tip) |
| Main working tree | `/workspace/solution/myproject` (left on `main`, untouched) |

The worktree is a **sibling** of the repository, so it does not appear inside or
disturb the repository's working directory. Its `.git` is a pointer file:

```
gitdir: /workspace/solution/myproject/.git/worktrees/add-config-validation
```

`git worktree list`:

```
/workspace/solution/myproject             a94f781 [main]
/workspace/solution/add-config-validation 833ced7 [add-config-validation]
```

## 4. Python environment

The worktree contains an isolated virtual environment (PEP 668 — the system
Python is externally managed, so a venv is required to install test tooling):

| Tool | Version |
| --- | --- |
| Python | 3.14.4 |
| pytest | 9.1.1 |
| venv path | `/workspace/solution/add-config-validation/.venv` |

Activate with:

```bash
cd /workspace/solution/add-config-validation
source .venv/bin/activate
```

`venv` and `.pytest_cache` ship their own `.gitignore` (`*`), so they are
automatically ignored by git and do not dirty the branch.

## 5. Verification

All checks below were run and passed.

### 5.1 Correct base branch
```
$ git rev-parse HEAD            # in worktree
833ced757f45314ea8267236b90298323ff261d4
$ git rev-parse develop         # in main repo
833ced757f45314ea8267236b90298323ff261d4
$ git merge-base --is-ancestor develop HEAD && echo ok
ok   # develop is an ancestor of the feature branch → branched from develop
```

### 5.2 Working tree contents match `develop`
```
$ diff <(git ls-tree -r develop --name-only) <(git ls-files)
# (no output — identical)
```
The worktree contains `README.md`, `src/__init__.py`, `src/config.py`,
`tests/__init__.py`, `tests/test_config.py` — i.e. the integration branch, not
the production `main` branch (which holds only `README.md`).

### 5.3 Test suite runs and passes
```
$ .venv/bin/python -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /workspace/solution/add-config-validation
collected 1 item

tests/test_config.py::test_load_simple_config PASSED                     [100%]

============================== 1 passed in 0.01s ==============================
```

### 5.4 Isolation from the main working tree
```
$ git -C /workspace/solution/add-config-validation status --short
# (clean)
$ git -C /workspace/solution/myproject branch --show-current
main
$ git -C /workspace/solution/myproject status --short
# (clean)
```
A temporary file created in the worktree was **not** visible in
`/workspace/solution/myproject`, confirming the two working directories are
independent. The main repository remains on `main` at `a94f781` with a clean
working tree.

## 6. Ready for development

The isolated workspace is in place and verified:

- ✅ Repository initialized at `/workspace/solution/myproject` with `main` + `develop`.
- ✅ Feature worktree created at `/workspace/solution/add-config-validation` on branch `add-config-validation`, branched from `develop` (the team's required integration branch).
- ✅ Main working tree left on `main`, clean and undisturbed.
- ✅ Isolated Python 3.14.4 + pytest 9.1.1 environment installed in the worktree.
- ✅ Existing test suite passes; worktree is clean and matches `develop`'s tip.

Development of the configuration-validation feature can now begin inside the
worktree. When complete, open a pull request from `add-config-validation` into
`develop` (per `README.md`). The worktree can be removed afterwards with:

```bash
git -C /workspace/solution/myproject worktree remove /workspace/solution/add-config-validation
```
