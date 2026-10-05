# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:13:14Z
**Evals**: Choose reuse, create, or current checkout correctly, Prefer manager and enforce safe raw-Git location, Establish base, branch, and detached-HEAD handling, Apply cleanup decision tree and verify integration, Refuse unsafe worktree operations, Isolated fix in custom ignored location from required base, Cleanup keeps review data and offline checkout, prunes only retired, Repair moved checkout and finish on the same task branch (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 92% ± 14% |

## Per-Case Results

### Choose reuse, create, or current checkout correctly (with_skill)

- **Pass Rate**: 67% (2/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_not_contain | ✅ | all checks passed |
| output_matches.not: "work in the current checkout" | ❌ | output matches forbidden regex pattern "work in the current checkout" |
| output_contains{any:[share objects share per-worktree HEAD index]} | ✅ | output satisfies all contains checks (any:[share objects share per-worktree HEAD index]) |

### Prefer manager and enforce safe raw-Git location (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[check-ignore], any:[.worktrees unique unused path ignore]} | ✅ | output satisfies all contains checks (all:[check-ignore], any:[.worktrees unique unused path ignore]) |
| output_contains{any:[harness manager raw Git fallback exit 0 ignored .gitignore info/exclude]} | ✅ | output satisfies all contains checks (any:[harness manager raw Git fallback exit 0 ignored .gitignore info/exclude]) |

### Establish base, branch, and detached-HEAD handling (with_skill)

- **Pass Rate**: 67% (2/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| failure: output_contains{any:[always use main assume main is correct override checkout protection]} | ❌ | failure rule matched: output satisfies all contains checks (any:[always use main assume main is correct override checkout protection]) |

### Apply cleanup decision tree and verify integration (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[prune --dry-run], any:[separately branch deletion checkout removal untracked ignored detached]} | ✅ | output satisfies all contains checks (all:[prune --dry-run], any:[separately branch deletion checkout removal untracked ignored detached]) |
| output_contains{any:[merge-base ancestor squash ancestry branch -d verify worktree list]} | ✅ | output satisfies all contains checks (any:[merge-base ancestor squash ancestry branch -d verify worktree list]) |

### Refuse unsafe worktree operations (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[authorization], any:[porcelain -z worktree remove dry run verify absolute path], not:[ran rm -rf used -B as requested pruned without]} | ✅ | output satisfies all contains checks (all:[authorization], any:[porcelain -z worktree remove dry run verify absolute path], not:[ran rm -rf used -B as requested pruned without]) |
| output_contains{any:[-B -b checkout protection do not refuse must not require]} | ✅ | output satisfies all contains checks (any:[-B -b checkout protection do not refuse must not require]) |

### Isolated fix in custom ignored location from required base (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[check-ignore], any:[scratch-checkouts ignored ignore .gitignore info/exclude]} | ✅ | output satisfies all contains checks (all:[check-ignore], any:[scratch-checkouts ignored ignore .gitignore info/exclude]) |
| output_contains{any:[release/next base task/normalize commit preserve colleague intact], not:[work in the current checkout edit the colleague checkout]} | ✅ | output satisfies all contains checks (any:[release/next base task/normalize commit preserve colleague intact], not:[work in the current checkout edit the colleague checkout]) |

### Cleanup keeps review data and offline checkout, prunes only retired (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[prune --dry-run], any:[review.db preserve outside the removal path review branch task/completed]} | ✅ | output satisfies all contains checks (all:[prune --dry-run], any:[review.db preserve outside the removal path review branch task/completed]) |
| output_contains{any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]} | ✅ | output satisfies all contains checks (any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]) |

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[repair], any:[worktree repair current absolute path worktree list registration]} | ✅ | output satisfies all contains checks (all:[repair], any:[worktree repair current absolute path worktree list registration]) |
| output_contains{any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]} | ✅ | output satisfies all contains checks (any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]) |

