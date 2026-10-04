# Five independent skill-enhancement investigations

These are copy-ready research prompts, not implementation instructions. Give each agent the full contents of its assigned file. Each prompt repeats the essential context so it works in a fresh conversation without loading the others.

| Agent | Prompt | Primary question |
|---|---|---|
| 1 | [Glossary and shared vocabulary](01-glossary-and-shared-vocabulary.md) | Which definitions change decisions or prevent communication errors? |
| 2 | [Activation and boundaries](02-skill-activation-and-boundaries.md) | Can routing become more distinctive without missing relevant tasks? |
| 3 | [Progressive disclosure and packaging](03-progressive-disclosure-and-packaging.md) | Which conditional split, if any, reduces useful task-path context? |
| 4 | [Task phases and execution discipline](04-task-phases-and-execution-discipline.md) | Does the workflow cause unrequested or redundant execution? |
| 5 | [Token attribution and efficiency](05-token-attribution-and-efficiency.md) | What explains the reported token overhead, and which change is justified? |

## Starting state

Prepared against commit 73d21c776ab51515ad3fb434292b22bec93823e0. The safety patch is already implemented in the live skill, its terminology heading is now Glossary, and historical research lives under docs/research/1.0-development/. Prior evaluation numbers must be matched to their actual skill version. Each agent must verify the current baseline again.

The latest user instructions allow reference files and glossary changes. Earlier single-file and glossary-freeze assumptions are not binding on these investigations. Critical terminology, safety, and task completeness must remain covered.

The [Agent Skills specification](https://agentskills.io/specification) is the format reference for SKILL.md and included resources; AGENTS.md is a different kind of repository instruction file. Investigator 3 should verify current format guidance and actual packaging behavior.

## Dispatch and outputs

- No agents have been launched by preparing these prompts.
- Each agent writes one independently named report under docs/research/skill-enhancement-investigations/ and returns a decision summary of at most 300 words.
- Run agents sequentially for desktop stability. Each may use one child at a time for research or peer review, with no nested delegation.
- Do not give an investigator another investigator's draft conclusions before its initial report. Cross-review can follow once independent reports exist.
- No model is forced by these prompts. Use your chosen capable model and record its identity for any empirical comparisons.
- Research permission does not authorize implementation, new evaluation runs, lifecycle operations, or publication. Only the assigned report may be written.
- Review the five recommendations separately. Accepting one does not require accepting the others; integrated changes will need a consistency check.
- These prompts were checked for scope, independent usability, unique outputs, and coverage. They have not been behaviorally tested or scored by Tessl.
