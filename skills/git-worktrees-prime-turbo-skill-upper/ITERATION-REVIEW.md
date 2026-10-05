# Iteration review: 2026-10-05

This iteration improves instructions and grading, but has no new model pass rate:
the configured free provider returned HTTP 429 quota errors for every fresh trial.
The instruction fixes and both test passes are committed together for review.

## Evidence and comparison

Report iteration numbers are individual runner invocations, not skill generations.
The comparison below separates the original skill, the previous revision, and this
revision. Different case sets and models prevent a controlled score comparison.

| Revision | Recorded evidence | Assessment |
|---|---|---|
| Original skill (`0a11162`) and initial eval loop | iteration-1: 8 infrastructure errors on Windows; iteration-10: 8/8 PASS with muse-spark | Established a working WSL runner and basic planning coverage; the Windows errors are not a 0% skill score. |
| Earlier expansion | iteration-23: 12/12 PASS; iteration-31: 14/14 with skill versus 7/14 without, with muse-spark | Useful new coverage and registration examples. Baseline compares skill presence, not two document layouts or two revisions. |
| Previous revision (`7241a4b`) | fledge's iteration-35: 13/14 PASS, repair FAIL; iteration-44: mimo 14/14 PASS; latest iteration-47: longcat 3/4 PASS with skill versus 2/4 without | Cross-model failures persist. More repeated repair wording did not establish reliable compliance. Latest suite result is a subset, not a full-suite score. |
| This revision | iteration-51: 15 provider-quota errors; configuration validates 15 cases; 3 offline judge tests pass, including several negative mutations | More discriminating tests and narrow instruction fixes; behavioral improvement remains unverified. |

## Changes and validation

- Reconciled the registration reference: repair now precedes inventory in the
  moved-checkout example, matching the main skill.
- Replaced duplicated absolute repair-first language with a conditional rule.
  Establish unknown paths first; reorganization alone is not evidence that a
  checkout moved, and an offline mount must not trigger invented-path repair.
- Added batch-cleanup guidance: directory existence/prefix is insufficient;
  inspect complete records, ownership, locks, detached state and preservation;
  stop on removal refusal; inspect the whole prune dry run.
- Strengthened the cleanup judge to require removal, prune dry run, ownership,
  preservation and review, and reject command-line force removal. Existing
  requirements were retained. This remains a text judge, not a shell safety proof.
- Added `repair-command-order`, with a script judge for a constrained JSON plan.
  It requires the repair command first and read-only inventory/status/HEAD checks
  afterward. It deliberately accepts a narrow output contract; equivalent
  unconstrained shell workflows are not what this case measures.
- Offline tests accept a valid recovery plan and reject wrong order, stale path,
  missing verification, pruning, shell chaining and prose-only answers. They
  also reject keyword stuffing, force removal and absent prune dry runs.
- Replayed the unsafe iteration-47 cleanup output with the missing `porcelain -z`
  keyword appended: the stronger judge still rejects it. The former success
  checks would accept those keywords despite the unsafe force/prune commands.
- `skill-up validate`, `git diff --check`, and the required YAML CJK scan pass.
  Offline checks: `python3 evals/fixtures/test-judges.py` in WSL, with PyYAML.

Fresh runs: iteration-48 exposed missing opencode in WSL PATH; after supplying
the existing `/home/mc/.opencode/bin`, iteration-49 hit provider quota. A targeted
retry with the historically successful muse-spark model (iteration-50), followed
by the required full-suite rerun (iteration-51), also hit quota. No credentials,
provider settings or paid-model configuration were changed.

## Length and progressive disclosure

PowerShell word counts (not tokenizer measurements): original main skill 1,672
words; previous main skill 1,866; current main skill 1,916; current command
reference 441. The two operational files total 2,357 words. These figures exclude
evals and this report; the report is not linked as runtime skill guidance.

This is a substantial but plausible instruction budget. The additional cost is
not automatically lost information: it consumes context and competes for
attention, especially alongside long task histories. Repetition and conflicting
examples are clearer observed concerns here than a demonstrated context limit.

Keep core decisions, preservation and safety in SKILL.md; keep operation-specific
command examples in the reference. That split has practical value if the engine
loads references only when needed. The saved evals do not establish that behavior
or prove the split outperforms a single file. They do not measure long-context
retention, skill activation, reference-loading fidelity or filesystem outcomes.

To test those claims, freeze model/cases and compare the same content in split,
combined and shortened forms, with repeated trials and long task histories.
Include actual disposable Git fixtures and data-preservation assertions. Do not
interpret changing-model keyword scores as evidence that document structure is
optimal. No such layout experiment was run in this iteration.

## Judgment

The skill covers valuable operational hazards and is broadly useful. This pass
is modest, meaningful hardening, chiefly of evaluation quality. It is worth doing
once to remove a real contradiction and expose false confidence. Further rounds
of keyword additions or repeated prose have diminishing value. The next useful
investment is stronger behavioral fixtures or a controlled layout comparison,
not making the document longer to chase every model omission.

## Additional iteration and commit

The follow-up adds two actual Git fixture tests without adding more runtime skill
prose. One externally relocates a disposable checkout, repairs it, and verifies
registration, branch, HEAD, staged diff and draft contents. The other demonstrates
that clean status can conceal valuable ignored data, preserves that data outside
the deletion path, removes the exact fixture checkout, and checks that the task
branch remains. These verify documented Git behavior, not agent compliance.

The ordering judge now rejects malformed JSON shapes and non-string commands
without crashing. Its offline suite no longer depends on untracked iteration-47
output files: the unsafe force/prune pattern is distilled into a local regression.
Four judge tests and two Git behavior tests pass in WSL. All 15 eval cases validate;
whitespace and YAML CJK checks pass. The full model rerun, iteration-52, again
produced 15 HTTP 429 quota errors and no graded results. Runtime instructions are
unchanged from the preceding pass; this iteration strengthens verification rather
than claiming a measured model improvement. Existing report directories are left
outside the commit.
