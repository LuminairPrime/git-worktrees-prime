# WSL handoff: skill-upper evolve loop for git-worktrees-prime-turbo-skill-upper

## Goal
Iterate on this skill until significantly improved and ready for the user to submit
to external evaluators. Target: higher eval scores from online evaluators.

## Skill under test
- Root: `skills/git-worktrees-prime-turbo-skill-upper/` (`SKILL.md` + `references/raw-git-commands.md`)
- Do NOT edit the skill until you have a failing eval report. Diagnose first.

## Eval suite (ready, validated: 8 cases)
- Config: `skills/git-worktrees-prime-turbo-skill-upper/evals/eval.yaml`
- Engine: `opencode` (default model; uses existing opencode login, no API key needed)
- Cases 1-5 (generic, rule_based): choose-checkout, manager-location, starting-state,
  cleanup-decision, safety-constraints
- Cases 6-8 (distilled from `tests/behavioral_trials.py` frozen outcomes + `tests/README.md`):
  - `isolated-fix-custom-location` <- trials case01 (custom ignored path, required base,
    preserve colleague checkout, commit, no merge/publish)
  - `cleanup-offline-prune` <- trials case02 (preserve ignored review.db outside removal
    path, retain review branch + offline registration, prune only retired after dry run)
  - `resume-repair-reorganized` <- trials case03 (repair moved checkout, same task branch,
    preserve draft, incorporate schema worker result, commit, no integration)
- All judges are `rule_based` (cheap, deterministic). Do not add `agent_judge` without need.
- Validation: `skill-up validate skills/git-worktrees-prime-turbo-skill-upper/evals/eval.yaml`
  must print `eval.yaml is valid (loaded 8 case(s))`. This already passes.

## Why WSL (Windows blocker)
On native Windows every case ERRORs before grading:
`opencode run failed (exit 1): Failed to change directory to /tmp/skill-up-*`.
skill-up builds Unix-style `/tmp/...` workspace paths that opencode on Windows cannot
`chdir` into. `result.json` shows `grading: null`, 0 turns, 0 tokens. This is a harness
incompatibility, not a skill failure. Evidence:
`skills/git-worktrees-prime-turbo-skill-upper-workspace/iteration-1/result.json`.
Delete or ignore that directory; it is stale Windows output.

## Your loop (skill-upper Steps 6-8)
1. Prerequisites in WSL: `skill-up --version` (or `go install github.com/alibaba/skill-up/cmd/skill-up@main`),
   `opencode --version` + working login.
2. `skill-up run skills/git-worktrees-prime-turbo-skill-upper/evals/eval.yaml`
3. Read `skills/git-worktrees-prime-turbo-skill-upper-workspace/iteration-N/result.json`
   and per-case `grading.json` + outputs. Summarize: pass rate, per-failure case id,
   failed assertion text, evidence.
4. For each failure decide: **skill wrong** (fix `SKILL.md` / references) or **eval wrong**
   (fix case prompt/judge). NEVER weaken a valid assertion to make it pass.
5. Rerun failures first: `skill-up run <eval.yaml> --include-case-name "<pattern>"`,
   then the full suite.
6. Optional: `skill-up run <eval.yaml> --baseline` to prove the skill adds value
   (with-skill vs without-skill pass-rate/token delta).
7. Stop when the suite passes or report exactly what remains blocked.

## Reference material
- skill-upper skill: `.agents/skills/skill-upper/` (SKILL.md, references/, assets/*.tmpl)
- Old behavioral evidence: `tests/README.md`, `tests/behavioral_trials.py`,
  `tests/results/`, `tests/subject-instructions.md`
- skill-up manual: https://alibaba.github.io/skill-up/

## Constraints
- Use only the skill-upper skill and the skill-up app. No tessl.
- Report in English. Keep technical identifiers (eval.yaml fields, judge types) in English.
- Before finishing, CJK self-check generated YAML: no CJK characters anywhere.
