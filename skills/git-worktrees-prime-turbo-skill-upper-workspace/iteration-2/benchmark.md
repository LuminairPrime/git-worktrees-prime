# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:05:27Z
**Evals**: Choose reuse, create, or current checkout correctly, Prefer manager and enforce safe raw-Git location, Establish base, branch, and detached-HEAD handling, Apply cleanup decision tree and verify integration, Refuse unsafe worktree operations, Isolated fix in custom ignored location from required base, Cleanup keeps review data and offline checkout, prunes only retired, Repair moved checkout and finish on the same task branch (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 50% ± 43% |

## Per-Case Results

### Choose reuse, create, or current checkout correctly (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "create" |
| expect.must_not_contain | ✅ | all checks passed |

### Prefer manager and enforce safe raw-Git location (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ❌ | output contains forbidden keyword "inside another disposable worktree" |

### Establish base, branch, and detached-HEAD handling (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[integration target], any:[do not assume starting commit task branch detached]} | ✅ | output satisfies all contains checks (all:[integration target], any:[do not assume starting commit task branch detached]) |
| output_contains{any:[detached HEAD detached anchor checkout protection checked out elsewhere]} | ✅ | output satisfies all contains checks (any:[detached HEAD detached anchor checkout protection checked out elsewhere]) |

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

- **Pass Rate**: 0% (0/0)

### Cleanup keeps review data and offline checkout, prunes only retired (with_skill)

- **Pass Rate**: 0% (0/0)

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 0% (0/0)

