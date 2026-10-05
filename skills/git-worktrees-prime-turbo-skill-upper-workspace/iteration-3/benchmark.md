# Skill Benchmark: git-worktrees-prime-turbo-skill-upper

**Date**: 2026-10-04T09:07:44Z
**Evals**: Choose reuse, create, or current checkout correctly, Prefer manager and enforce safe raw-Git location (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Choose reuse, create, or current checkout correctly (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_not_contain | ✅ | all checks passed |
| output_matches{all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login work in the current checkout]} | ✅ | output satisfies all regex checks (all:[(?i)create], any:[owned by another another worker ownership concurrent separation isolation], not:[reuse the worktree at /repo/.worktrees/login work in the current checkout]) |
| output_contains{any:[share objects share per-worktree HEAD index]} | ✅ | output satisfies all contains checks (any:[share objects share per-worktree HEAD index]) |

### Prefer manager and enforce safe raw-Git location (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| output_contains{all:[check-ignore], any:[.worktrees unique unused path ignore]} | ✅ | output satisfies all contains checks (all:[check-ignore], any:[.worktrees unique unused path ignore]) |
| output_contains{any:[harness manager raw Git fallback exit 0 ignored .gitignore info/exclude]} | ✅ | output satisfies all contains checks (any:[harness manager raw Git fallback exit 0 ignored .gitignore info/exclude]) |

