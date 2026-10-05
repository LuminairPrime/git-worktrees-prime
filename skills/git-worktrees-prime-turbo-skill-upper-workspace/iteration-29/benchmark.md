# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-05T03:08:29Z
**Evals**: Script worktree cleanup with NUL-safe listing, no filesystem deletion (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|--------------|-------|
| Pass Rate | 100% ± 0% | 50% ± 0% | +0.50 |

## Per-Case Results

### Script worktree cleanup with NUL-safe listing, no filesystem deletion (with_skill)

- **Pass Rate**: 100% (2/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_contains{all:[porcelain -z], any:[NUL null -z spaces]} | ✅ | output satisfies all contains checks (all:[porcelain -z], any:[NUL null -z spaces]) |
| output_contains{any:[worktree remove dry-run dry run]} | ✅ | output satisfies all contains checks (any:[worktree remove dry-run dry run]) |

### Script worktree cleanup with NUL-safe listing, no filesystem deletion (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| output_contains.all: missing [porcelain -z] | ❌ | output does not contain required keywords: [porcelain -z] |
| output_contains{any:[worktree remove dry-run dry run]} | ✅ | output satisfies all contains checks (any:[worktree remove dry-run dry run]) |

