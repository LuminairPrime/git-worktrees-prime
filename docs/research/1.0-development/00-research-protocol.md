# Worktree skill research protocol

Date: 2026-10-02. Scope: the ten files in `vendors/` compared with `skills/prototype1-astra/SKILL.md`. The prototype is an input and remains unchanged. Input paths, line counts, and SHA-256 hashes are recorded in `00-input-manifest.json`.

## Review method

One GPT-6.1 Sol reviewer at medium reasoning effort reviews each vendor file and the full prototype. Six reviewer threads were created; completed threads were reused for the remaining four assignments when the tool rejected further threads. Reused reviewers were instructed to exclude previous vendor findings as evidence, but their earlier context was not technically erased. Each vendor still has its own assignment and report. Reviewers receive no other vendor files and cannot browse, load skills, execute vendor recipes, or modify the prototype. Each owns a unique numbered report. Work runs with at most three concurrent reviewers because the session has four total agent slots, including the main agent. The user requested up to five reviewers; this is the available maximum.

Each report supplies exact source quotations and line ranges, incremental gaps against the prototype, minimal candidate wording, caveats, rejected content, and conceptual test questions with separate answer keys. Vendor instructions are evidence to analyze, never instructions to execute. The main agent reads the inputs and reports, verifies quotations and cross-document claims, and sets the final tiers independently.

## Incremental usefulness tiers

- S: essential missing guidance with clear evidence and little instruction cost.
- A: strongest follow-up source; concrete useful gaps or authoritative edge-case guidance.
- B: limited useful additions, mostly redundant or conditional.
- C: little incremental value; primarily confirmation or general workflow advice.
- D: no worthwhile addition relative to the prototype, or misleading advice dominates.

Tiers measure usefulness for enhancing this prototype, not overall writing quality. Similar documents do not count as independent confirmation of a claim. A command reference can be valuable as a source without belonging in the skill itself.

## Luna evaluation method

Freeze a question set and grading key before seeing the test subject's answers. Spawn GPT-6 Luna at high effort with fresh context. Supply the complete unchanged prototype file and questions, but no vendor documents, review reports, rubric, skills, or memory. The subject must use no research, skills, or memory. Its only permitted tool uses are reading the exact two supplied input files (prototype and questions) and writing its response; input handling is distinct from research.

Questions cover candidate gaps plus controls already answered by the prototype. Require practical next actions, reasoning, and identification of uncertainty. Grade each 0 (materially wrong), 1 (safe but materially incomplete), or 2 (sufficient). Do not require a specific command when an equally safe conceptual answer suffices. Distinguish absent knowledge from appropriate deferral to repository/tool documentation. Commands proposed in answers are not runtime evidence.

Passing one model on a constructed question set establishes sufficiency for those scenarios only. It cannot prove universal sufficiency or separate prior training from the prototype's contribution. Baseline failure supports investigating a candidate addition; it does not prove that addition remedies the failure. If a supplement is tested afterward, label it as a coached follow-up rather than a blinded causal comparison.
