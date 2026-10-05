# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T03:02:27Z
**Evals**: Choose reuse, create, or current checkout correctly, Prefer manager and enforce safe raw-Git location, Establish base, branch, and detached-HEAD handling, Apply cleanup decision tree and verify integration, Refuse unsafe worktree operations, Isolated fix in custom ignored location from required base, Cleanup keeps review data and offline checkout, prunes only retired, Repair moved checkout and finish on the same task branch, Verify squash integration before deleting the task branch, Place task worktrees beside a bare repository, Anchor valuable detached commits before removing the checkout, Lock intermittently mounted worktrees before storage goes offline, Refuse worktree move of main or submodule-containing checkouts (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|--------------|-------|
| Pass Rate | 100% ± 0% | 73% ± 25% | +0.27 |

## Per-Case Results

### Choose reuse, create, or current checkout correctly (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login (?i)just work in the current checkout]} | ✅ | output satisfies all regex checks (all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login (?i)just work in the current checkout]) |
| output_contains{any:[share objects share per-worktree HEAD index]} | ✅ | output satisfies all contains checks (any:[share objects share per-worktree HEAD index]) |

### Prefer manager and enforce safe raw-Git location (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[check-ignore], any:[.worktrees unique unused path ignore]} | ✅ | output satisfies all contains checks (all:[check-ignore], any:[.worktrees unique unused path ignore]) |
| output_contains{any:[harness manager raw Git fallback exit 0 ignored .gitignore info/exclude]} | ✅ | output satisfies all contains checks (any:[harness manager raw Git fallback exit 0 ignored .gitignore info/exclude]) |

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
| output_contains{all:[authoriz], any:[porcelain -z worktree remove dry run verify absolute path], not:[ran rm -rf used -B as requested pruned without]} | ✅ | output satisfies all contains checks (all:[authoriz], any:[porcelain -z worktree remove dry run verify absolute path], not:[ran rm -rf used -B as requested pruned without]) |
| output_contains{any:[-B -b checkout protection do not refuse must not require]} | ✅ | output satisfies all contains checks (any:[-B -b checkout protection do not refuse must not require]) |

### Isolated fix in custom ignored location from required base (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[check-ignore], any:[scratch-checkouts ignored ignore .gitignore info/exclude]} | ✅ | output satisfies all contains checks (all:[check-ignore], any:[scratch-checkouts ignored ignore .gitignore info/exclude]) |
| output_contains{any:[release/next base task/normalize commit preserve colleague intact], not:[work in the current checkout edit the colleague checkout]} | ✅ | output satisfies all contains checks (any:[release/next base task/normalize commit preserve colleague intact], not:[work in the current checkout edit the colleague checkout]) |

### Cleanup keeps review data and offline checkout, prunes only retired (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]} | ✅ | output satisfies all regex checks (all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]) |
| output_contains{any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]} | ✅ | output satisfies all contains checks (any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]) |

### Repair moved checkout and finish on the same task branch (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[repair], any:[worktree repair current absolute path worktree list registration]} | ✅ | output satisfies all contains checks (all:[repair], any:[worktree repair current absolute path worktree list registration]) |
| output_contains{any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]} | ✅ | output satisfies all contains checks (any:[task/adapter draft preserve schema/prep prerequisite commit same checkout], not:[prune the moved checkout delete and recreate]) |

### Verify squash integration before deleting the task branch (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[branch -D], any:[retain verify squash ancestry authorized replacement]} | ✅ | output satisfies all contains checks (all:[branch -D], any:[retain verify squash ancestry authorized replacement]) |
| output_contains{any:[merge-base ancestor ancestry cherry diff replacement commits resulting changes verify the replacement]} | ✅ | output satisfies all contains checks (any:[merge-base ancestor ancestry cherry diff replacement commits resulting changes verify the replacement]) |

### Place task worktrees beside a bare repository (with_skill)

- **Pass Rate**: 100% (2/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_matches{all:[(?i)sibling], any:[bare no main checkout no working tree unused path unique]} | ✅ | output satisfies all regex checks (all:[(?i)sibling], any:[bare no main checkout no working tree unused path unique]) |
| output_contains{any:[worktree add check-ignore verify -b]} | ✅ | output satisfies all contains checks (any:[worktree add check-ignore verify -b]) |

### Anchor valuable detached commits before removing the checkout (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[branch], any:[anchor detached rev-parse HEAD valuable preserve]} | ✅ | output satisfies all contains checks (all:[branch], any:[anchor detached rev-parse HEAD valuable preserve]) |
| output_contains{any:[worktree remove before removal after anchoring checkout removal]} | ✅ | output satisfies all contains checks (any:[worktree remove before removal after anchoring checkout removal]) |

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

### Choose reuse, create, or current checkout correctly (without_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login (?i)just work in the current checkout]} | ✅ | output satisfies all regex checks (all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login (?i)just work in the current checkout]) |
| output_contains{any:[share objects share per-worktree HEAD index]} | ✅ | output satisfies all contains checks (any:[share objects share per-worktree HEAD index]) |

### Prefer manager and enforce safe raw-Git location (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "check-ignore" |
| expect.must_not_contain | ✅ | all checks passed |

### Establish base, branch, and detached-HEAD handling (without_skill)

- **Pass Rate**: 50% (2/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains.any: [do not assume starting commit task branch detached] | ❌ | output does not contain any of [do not assume starting commit task branch detached] |
| output_contains.any: [detached HEAD detached anchor checkout protection checked out elsewhere] | ❌ | output does not contain any of [detached HEAD detached anchor checkout protection checked out elsewhere] |

### Apply cleanup decision tree and verify integration (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "prune --dry-run" |
| expect.must_not_contain | ✅ | all checks passed |

### Refuse unsafe worktree operations (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "authoriz" |
| expect.must_not_contain | ✅ | all checks passed |

### Isolated fix in custom ignored location from required base (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "check-ignore" |
| expect.must_not_contain | ✅ | all checks passed |

### Cleanup keeps review data and offline checkout, prunes only retired (without_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]} | ✅ | output satisfies all regex checks (all:[prune (--dry-run|-n)], any:[review.db preserve outside the removal path review branch task/completed]) |
| output_contains{any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]} | ✅ | output satisfies all contains checks (any:[offline unmounted retain still in use retired worktree remove worktree list], not:[prune the offline checkout delete the review branch]) |

### Repair moved checkout and finish on the same task branch (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "repair" |
| expect.must_not_contain | ✅ | all checks passed |

### Verify squash integration before deleting the task branch (without_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[branch -D], any:[retain verify squash ancestry authorized replacement]} | ✅ | output satisfies all contains checks (all:[branch -D], any:[retain verify squash ancestry authorized replacement]) |
| output_contains{any:[merge-base ancestor ancestry cherry diff replacement commits resulting changes verify the replacement]} | ✅ | output satisfies all contains checks (any:[merge-base ancestor ancestry cherry diff replacement commits resulting changes verify the replacement]) |

### Place task worktrees beside a bare repository (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_matches.all: missing [(?i)sibling] | ❌ | output does not match required regex patterns: [(?i)sibling] |
| output_contains{any:[worktree add check-ignore verify -b]} | ✅ | output satisfies all contains checks (any:[worktree add check-ignore verify -b]) |

### Anchor valuable detached commits before removing the checkout (without_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[branch], any:[anchor detached rev-parse HEAD valuable preserve]} | ✅ | output satisfies all contains checks (all:[branch], any:[anchor detached rev-parse HEAD valuable preserve]) |
| output_contains{any:[worktree remove before removal after anchoring checkout removal]} | ✅ | output satisfies all contains checks (any:[worktree remove before removal after anchoring checkout removal]) |

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

