# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:09:56Z
**Evals**: Isolated fix in custom ignored location from required base, Cleanup keeps review data and offline checkout, prunes only retired, Repair moved checkout and finish on the same task branch (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 89% ± 16% |

## Per-Case Results

### Isolated fix in custom ignored location from required base (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[check-ignore], any:[scratch-checkouts ignored ignore .gitignore info/exclude]} | ✅ | output satisfies all contains checks (all:[check-ignore], any:[scratch-checkouts ignored ignore .gitignore info/exclude]) |
| output_contains{any:[release/next base task/normalize commit preserve colleague intact], not:[work in the current checkout edit the colleague checkout]} | ✅ | output satisfies all contains checks (any:[release/next base task/normalize commit preserve colleague intact], not:[work in the current checkout edit the colleague checkout]) |

### Cleanup keeps review data and offline checkout, prunes only retired (with_skill)

- **Pass Rate**: 67% (2/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| failure: output_contains{any:[prune the offline checkout delete the review branch rm -rf prune without review data needs no backup]} | ❌ | failure rule matched: output satisfies all contains checks (any:[prune the offline checkout delete the review branch rm -rf prune without review data needs no backup]) |

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[repair], any:[worktree repair current absolute path worktree list registration]} | ✅ | output satisfies all contains checks (all:[repair], any:[worktree repair current absolute path worktree list registration]) |
| output_contains{any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]} | ✅ | output satisfies all contains checks (any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]) |

