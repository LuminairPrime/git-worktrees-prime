# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:33:26Z
**Evals**: Cleanup keeps review data and offline checkout, prunes only retired (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Cleanup keeps review data and offline checkout, prunes only retired (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]} | ✅ | output satisfies all regex checks (all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]) |
| output_contains{any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]} | ✅ | output satisfies all contains checks (any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]) |

