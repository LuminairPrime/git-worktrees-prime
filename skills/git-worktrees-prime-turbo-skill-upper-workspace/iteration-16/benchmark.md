# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:39:21Z
**Evals**: Verify squash integration before deleting the task branch (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Verify squash integration before deleting the task branch (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[branch -D], any:[retain verify squash ancestry authorized replacement]} | ✅ | output satisfies all contains checks (all:[branch -D], any:[retain verify squash ancestry authorized replacement]) |
| output_contains{any:[merge-base ancestor ancestry cherry diff replacement commits resulting changes verify the replacement]} | ✅ | output satisfies all contains checks (any:[merge-base ancestor ancestry cherry diff replacement commits resulting changes verify the replacement]) |

