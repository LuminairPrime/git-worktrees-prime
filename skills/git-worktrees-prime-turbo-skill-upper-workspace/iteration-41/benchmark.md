# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T03:56:29Z
**Evals**: Repair moved checkout and finish on the same task branch, Lock intermittently mounted worktrees before storage goes offline, Refuse worktree move of main or submodule-containing checkouts (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 83% ± 24% |

## Per-Case Results

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "repair" |
| expect.must_not_contain | ✅ | all checks passed |

### Lock intermittently mounted worktrees before storage goes offline (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[lock], any:[worktree lock intermittent offline gc.worktreePruneExpire expire]} | ✅ | output satisfies all contains checks (all:[lock], any:[worktree lock intermittent offline gc.worktreePruneExpire expire]) |
| output_contains{any:[repair do not prune unavailable missing directory unlock]} | ✅ | output satisfies all contains checks (any:[repair do not prune unavailable missing directory unlock]) |

### Refuse worktree move of main or submodule-containing checkouts (with_skill)

- **Pass Rate**: 100% (2/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_matches{all:[(?i)main (?i)submodule], any:[cannot move refuse do not move never move must not move not support repair]} | ✅ | output satisfies all regex checks (all:[(?i)main (?i)submodule], any:[cannot move refuse do not move never move must not move not support repair]) |
| output_contains{any:[worktree move worktree list repair relocate]} | ✅ | output satisfies all contains checks (any:[worktree move worktree list repair relocate]) |

