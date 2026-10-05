# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T00:49:55Z
**Evals**: Repair moved checkout and finish on the same task branch (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[repair], any:[worktree repair current absolute path worktree list registration]} | ✅ | output satisfies all contains checks (all:[repair], any:[worktree repair current absolute path worktree list registration]) |
| output_contains{any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]} | ✅ | output satisfies all contains checks (any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]) |

