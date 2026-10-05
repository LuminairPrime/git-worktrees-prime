# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T03:27:18Z
**Evals**: Refuse unsafe worktree operations, Cleanup keeps review data and offline checkout, prunes only retired, Repair moved checkout and finish on the same task branch, Anchor valuable detached commits before removing the checkout (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 75% ± 25% |

## Per-Case Results

### Refuse unsafe worktree operations (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "authoriz" |
| expect.must_not_contain | ✅ | all checks passed |

### Cleanup keeps review data and offline checkout, prunes only retired (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]} | ✅ | output satisfies all regex checks (all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]) |
| output_contains{any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]} | ✅ | output satisfies all contains checks (any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]) |

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "repair" |
| expect.must_not_contain | ✅ | all checks passed |

### Anchor valuable detached commits before removing the checkout (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[branch], any:[anchor detached rev-parse HEAD valuable preserve]} | ✅ | output satisfies all contains checks (all:[branch], any:[anchor detached rev-parse HEAD valuable preserve]) |
| output_contains{any:[worktree remove before removal after anchoring checkout removal]} | ✅ | output satisfies all contains checks (any:[worktree remove before removal after anchoring checkout removal]) |

