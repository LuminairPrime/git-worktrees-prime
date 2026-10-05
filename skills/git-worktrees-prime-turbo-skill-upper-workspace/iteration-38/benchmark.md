# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T03:45:44Z
**Evals**: Repair moved checkout and finish on the same task branch (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 50% ± 0% |

## Per-Case Results

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "repair" |
| expect.must_not_contain | ✅ | all checks passed |

