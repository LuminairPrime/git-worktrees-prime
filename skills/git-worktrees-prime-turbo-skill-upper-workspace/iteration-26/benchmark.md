# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T02:57:16Z
**Evals**: Refuse worktree move of main or submodule-containing checkouts (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|--------------|-------|
| Pass Rate | 100% ± 0% | 0% ± 0% | +1.00 |

## Per-Case Results

### Refuse worktree move of main or submodule-containing checkouts (with_skill)

- **Pass Rate**: 100% (2/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_matches{all:[(?i)main (?i)submodule], any:[cannot move refuse do not move never move must not move not support repair]} | ✅ | output satisfies all regex checks (all:[(?i)main (?i)submodule], any:[cannot move refuse do not move never move must not move not support repair]) |
| output_contains{any:[worktree move worktree list repair relocate]} | ✅ | output satisfies all contains checks (any:[worktree move worktree list repair relocate]) |

### Refuse worktree move of main or submodule-containing checkouts (without_skill)

- **Pass Rate**: 0% (0/0)

