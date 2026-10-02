# Main research summary: minimal Git worktree skill

Date: 2026-10-02. All ten vendor files received a GPT-6.1 Sol review at medium effort; Luna at high effort answered twenty baseline scenarios and two diagnostic follow-ups without vendor material, research, skills, or memory. Reports, questions, keys, source quotations and responses are indexed in [README.md](README.md). The prototype and all ten vendor files remain unchanged and match their initial hashes.

The prototype is already a strong minimal lifecycle guide. Most vendor content adds generic Git tutorials, rigid workflow policy, provider commands, or weaker cleanup shortcuts. The few useful concepts concern narrower wording and unusual recovery situations. This research found no essential missing concept demonstrated to cause a mistake in the Luna test.

## Final tier list

These tiers measure incremental usefulness for improving this particular prototype, not general document quality or how much text can be copied. S is essential missing guidance; A is a strongest follow-up source with concrete gaps/reference value; B is limited useful guidance; C is marginal or mostly redundant; D supplies no worthwhile addition. Similar documents are not independent evidence. The main agent sets final tiers after reviewing both sources and reports.

| Tier | Vendor file | Most useful contribution | Sol tier |
|---|---|---|---|
| A | `official-git-worktree-doc.md` | Precise relocation/repair distinction; submodule limits; conditional lock/config/parser reference. Best source to consult for uncommon cases, rather than importing its manual. | B |
| B | `compound-engineering-plugin-skills-ce-worktree-SKILL.md` | Failed requested isolation must not become permission to edit the original checkout. Explicitly counters an unsafe fallback in another source. | C |
| B | `administrakt0r-AI-Agents-Safe-Coding-Skillsskillsusing-git-worktrees-SKILL.md` | Applies ignore protection to project-local locations beyond `.worktrees`; conditional pre-edit baseline idea. | B |
| B | `openai-pluginspluginssuperpowersskillsusing-git-worktrees-SKILL.md` | Same actual-location ignore clarification and baseline reminder; otherwise largely covered. Reject its work-in-place fallback after isolation failure. | B |
| C | `qwen38-answer.md` | Naming stashes as shared needs only a few words. Its long tutorial and ambiguous cleanup rules do not justify expansion. | C |
| C | `davidondrej-skillsskillsagent-orchestrationgit-worktree-SKILL.md` | Writable config symlinks and hook-path scope are practical examples, but existing principles plus ordinary training handled them. | C |
| C | `microsoft-fluidframework-agencypluginsnoriskillsusing-git-worktrees-SKILL.md` | Conditional pre-edit baseline reminder; path discipline already handled more accurately by prototype. | C |
| D | `heyitsnoah-claudesidian-.agentsskillsgit-worktrees-SKILL.md` | Useful lifecycle content duplicated; force/unlock and PR cleanup recipes weaken safeguards. | D |
| D | `rohitg00-pro-workflowskillsparallel-worktrees-SKILL.md` | Parallel-session introduction and provider shortcuts; no missing lifecycle concept. | D |
| D | `spillwavesolutions-parallel-worktrees-SKILL.md` | Orchestration tutorial and status machinery, with unsafe force/publishing shortcuts; no useful minimal addition. | D |

**S tier is empty.** Official Git is promoted to A for its specific recovery guidance and reference value. Compound is promoted to B for its clear failure response and its usefulness in resolving contradictory advice. These promotions reflect source usefulness for follow-up, not a demonstrated need to add paragraphs to the skill.

## Sources to investigate further

1. **Official Git reference, especially lines 72-88, 140-144, 180-196 and 296-297.** Use it to tighten relocation-versus-prune wording and clarify uncommon submodule/configuration/parser cases when those cases arise. Its local snapshot identifies a version; this research does not establish the installed or current Git version.
2. **Compound Engineering, line 54.** Consider one explicit sentence preserving the user's isolation requirement after creation failure. Do not import question-tool instructions or prohibit safe creation retries.
3. **administrakt0r, lines 54-76**, with OpenAI lines 78-88 as a redundant comparison. Generalize the existing ignore sentence to the actual selected destination inside the primary checkout. The vendor's two-directory OR probe is not suitable evidence that the selected path is ignored.
4. **Qwen line 233, low priority.** At most add `(including stashes)` to the shared-refs sentence. Investigate the shared-state wording, not the whole tutorial.

No further broad investigation of heyitsnoah, rohitg00, or spillwavesolutions is justified for this goal. Davidondrej's config-link/hook examples and the three baseline-test variants can remain optional reference material unless real agent behavior demonstrates a gap.

## Candidate text and Luna findings

Exact vendor quotations, prototype line comparisons, minimal proposed wording, and rejection reasons are preserved in [15-candidate-instructions.md](15-candidate-instructions.md) and the individual reports. They are proposals only; nothing was patched.

| Concept | Luna evidence | Recommendation |
|---|---|---|
| Actual in-repository destination must be ignored | Q3 sufficient, including alternate directory and no mandatory commit. | Consider replacing the narrow `.worktrees` sentence; improves text coverage without teaching a new workflow. |
| Preserve requested isolation after failure | Q2 sufficient, including safe fallback and blocker response. | Optional one-sentence clarification; no demonstrated model ignorance. |
| Explicitly name shared stashes | Q6 sufficient; identifies specific stash before recovery. | Optional few-word insertion, not a stash procedure. |
| Repair relocated live checkout rather than prune | Q12 sufficient; names repair and verification. | Retain as recovery reference. Correct prototype line 101's comment, which calls pruning “repair,” if editing later. |
| Submodule support limits | Q14 sufficient; Q22 independently recalled the documented move limit without new facts. | Do not expand lifecycle recipes on this sample's evidence; consider an early caution only if needed. |
| Writable config links | Q8 sufficient. | Omit default symlink paragraph. |
| Relevant pre-edit baseline | Q9 sufficient. | Omit blanket setup/test gates; existing task validation guidance may suffice. |
| Shared hook/config scope | Q7 sufficient, including opt-in per-worktree config. | Omit extension enablement or migration instructions. |
| Proactive lock on intermittent storage | Q13 partial for scope; Q21 recalled move/removal protection and lack of edit/commit exclusion. | Baseline omission, not demonstrated missing knowledge; keep as conditional reference. |
| NUL-safe inventory parsing | Q15 sufficient. | Keep parser specifics out of ordinary lifecycle instructions unless writing a parser. |

The smallest plausible edit is to broaden the existing ignore wording and correct the prune comment. Explicit failure handling and shared-stash wording are optional clarity improvements. Keep the prototype's ownership checks, explicit base/path selection, manager-aware lifecycle, integration evidence, ignored-state preservation, and separate checkout/branch/metadata decisions. Add no new sections merely because the vendor documents have them.

## Luna test summary

**Baseline: 39/40; nineteen sufficient answers, one safe partial answer, zero unsafe answers.** Luna recognized all major candidate concepts and all cleanup controls. Q13 omitted lock effects on normal move/removal; the score remains partial under the frozen key.

**Follow-up: both answers correct without new material.** Q21 demonstrated that Luna already knew the omitted lock behavior and that it is not a worker mutex. Q22 demonstrated knowledge of the specific submodule move limitation. The follow-up therefore weakens the claim that including those facts would teach this subject something it did not know. No coached retest was needed and no vendor supplement was supplied.

The result supports sufficiency of the prototype plus this model's prior knowledge for the tested scenarios. It does not establish how much the prototype taught, prove universal sufficiency, or predict unprompted behavior during coding. The questions deliberately direct attention to possible mistakes. A future useful check would observe ordinary task decisions using the unchanged prototype, then compare against a tiny candidate edit if a reproducible mistake appears; further expansion is not justified by this test alone.

Detailed scoring and methodological limits are in [14-luna-baseline-evaluation.md](14-luna-baseline-evaluation.md); original subject outputs are preserved in [13](13-luna-baseline-response.md) and [18](18-luna-follow-up-response.md).

## Execution and validation

Six Sol medium reviewer threads handled ten file-specific assignments; four assignments reused completed threads because the tool rejected additional threads. Reused reviewers were explicitly restricted to their assigned vendor and prototype, with unique report paths. Their prior context was not technically erased, so these are ten reviews, not ten fully independent fresh contexts. Luna was spawned separately with fresh conversation context and high effort. At most three reviewers ran concurrently, reflecting the four-slot session limit including the main agent.

Reviewers analyzed source claims without executing vendor commands or changing inputs. Luna was allowed only the two supplied input reads and response writes; its recorded outputs declare no outside research, skills, memory, Git execution, or delegation. Tool restrictions were instructions rather than a separate sandbox audit. No actual Git or harness lifecycle operation was tested. All eleven input hashes were verified unchanged; output-file presence, UTF-8 readability, local links, and required response/question coverage were checked. ICM completion context was stored by the main agent, separately from the test subject.
