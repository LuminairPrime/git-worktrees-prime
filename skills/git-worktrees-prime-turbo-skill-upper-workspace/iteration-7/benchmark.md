# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:15:56Z
**Evals**: Choose reuse, create, or current checkout correctly, Establish base, branch, and detached-HEAD handling (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Choose reuse, create, or current checkout correctly (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login (?i)just work in the current checkout]} | ✅ | output satisfies all regex checks (all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login (?i)just work in the current checkout]) |
| output_contains{any:[share objects share per-worktree HEAD index]} | ✅ | output satisfies all contains checks (any:[share objects share per-worktree HEAD index]) |

### Establish base, branch, and detached-HEAD handling (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[integration target], any:[do not assume starting commit task branch detached]} | ✅ | output satisfies all contains checks (all:[integration target], any:[do not assume starting commit task branch detached]) |
| output_contains{any:[detached HEAD detached anchor checkout protection checked out elsewhere]} | ✅ | output satisfies all contains checks (any:[detached HEAD detached anchor checkout protection checked out elsewhere]) |

