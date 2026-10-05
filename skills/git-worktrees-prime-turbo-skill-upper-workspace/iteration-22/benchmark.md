# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T01:12:48Z
**Evals**: Place task worktrees beside a bare repository (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Place task worktrees beside a bare repository (with_skill)

- **Pass Rate**: 100% (2/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_matches{all:[(?i)sibling], any:[bare no main checkout no working tree unused path unique]} | ✅ | output satisfies all regex checks (all:[(?i)sibling], any:[bare no main checkout no working tree unused path unique]) |
| output_contains{any:[worktree add check-ignore verify -b]} | ✅ | output satisfies all contains checks (any:[worktree add check-ignore verify -b]) |

