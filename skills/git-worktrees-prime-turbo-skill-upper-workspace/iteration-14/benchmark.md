# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:36:43Z
**Evals**: Place task worktrees beside a bare repository (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Place task worktrees beside a bare repository (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| output_contains{all:[sibling], any:[bare no main checkout no working tree unused path unique]} | ✅ | output satisfies all contains checks (all:[sibling], any:[bare no main checkout no working tree unused path unique]) |
| output_contains{any:[worktree add check-ignore verify -b]} | ✅ | output satisfies all contains checks (any:[worktree add check-ignore verify -b]) |

