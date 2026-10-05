# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T05:31:42Z
**Evals**: Cleanup keeps review data and offline checkout, prunes only retired, Lock intermittently mounted worktrees before storage goes offline, Refuse worktree move of main or submodule-containing checkouts, Script worktree cleanup with NUL-safe listing, no filesystem deletion (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|--------------|-------|
| Pass Rate | 88% ± 22% | 75% ± 25% | +0.12 |

## Per-Case Results

### Cleanup keeps review data and offline checkout, prunes only retired (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]} | ✅ | output satisfies all regex checks (all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]) |
| output_contains{any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]} | ✅ | output satisfies all contains checks (any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]) |

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

### Script worktree cleanup with NUL-safe listing, no filesystem deletion (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_contains.all: missing [porcelain -z] | ❌ | output does not contain required keywords: [porcelain -z] |
| output_contains{any:[worktree remove dry-run dry run]} | ✅ | output satisfies all contains checks (any:[worktree remove dry-run dry run]) |

### Cleanup keeps review data and offline checkout, prunes only retired (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "prune -" |
| expect.must_not_contain | ✅ | all checks passed |

### Lock intermittently mounted worktrees before storage goes offline (without_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[lock], any:[worktree lock intermittent offline gc.worktreePruneExpire expire]} | ✅ | output satisfies all contains checks (all:[lock], any:[worktree lock intermittent offline gc.worktreePruneExpire expire]) |
| output_contains{any:[repair do not prune unavailable missing directory unlock]} | ✅ | output satisfies all contains checks (any:[repair do not prune unavailable missing directory unlock]) |

### Refuse worktree move of main or submodule-containing checkouts (without_skill)

- **Pass Rate**: 100% (2/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_matches{all:[(?i)main (?i)submodule], any:[cannot move refuse do not move never move must not move not support repair]} | ✅ | output satisfies all regex checks (all:[(?i)main (?i)submodule], any:[cannot move refuse do not move never move must not move not support repair]) |
| output_contains{any:[worktree move worktree list repair relocate]} | ✅ | output satisfies all contains checks (any:[worktree move worktree list repair relocate]) |

### Script worktree cleanup with NUL-safe listing, no filesystem deletion (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_contains.all: missing [porcelain -z] | ❌ | output does not contain required keywords: [porcelain -z] |
| output_contains{any:[worktree remove dry-run dry run]} | ✅ | output satisfies all contains checks (any:[worktree remove dry-run dry run]) |

