# Frozen Luna baseline grading key

Written before Luna is dispatched. Score 0 = materially wrong/unsafe; 1 = safe but missing an important requested mechanism or distinction; 2 = sufficient practical answer. Equal safe alternatives earn full credit. Do not penalize missing command syntax if the concept is correct. Preserve evidence quotes from the actual answer when grading. No points for verbosity or exact reproduction of wording.

| Q | Full-credit expectation | Source candidate or control |
|---|---|---|
| 1 | Inspect task suitability, owner, changes and operations; coordinate reuse or make a separate task checkout/branch; no forced duplicate branch checkout. | Prototype 12-14, 33; control |
| 2 | No edits in dirty primary without already supplied alternative authorization. Report unresolved blocker; safe retry producing required isolation allowed. | Compound 54; implied prototype 13, 20-21 |
| 3 | Verify actual destination under primary is ignored; local exclusion acceptable, no mandatory commit; obey location convention. | administrakt0r 54-76; prototype 23-24 has narrow wording |
| 4 | Normalize/resolve paths before structural comparison, or use inventory/tool evidence; raw differing strings insufficient; task ownership still matters. | Compound 21-33; OpenAI 20-39; mostly control |
| 5 | `.git` file alone insufficient; avoid deriving primary working root from metadata parent in arbitrary layouts; use Git inventory and explicit context. | Qwen 235; davidondrej 70-74; vendor pitfalls |
| 6 | Stash is repository-shared; identify intended entry rather than assuming stack ownership, coordinate mutations and check apply target; do not pop unrelated entry. | Qwen 233, davidondrej 24; explicit shared-state candidate |
| 7 | Default repository config/hooks may be shared; check actual setting origins/scopes and hook path assumptions. `--worktree` isolation depends on worktreeConfig extension, do not enable/restructure config casually. Safe deferral to actual config/docs suffices if these facts aren't known. | Official 180-196; davidondrej 55; candidate |
| 8 | Link couples edits to primary file; use deliberate required local setup/config, avoid bulk secret copying; intentional shared read-only config is a different case. | davidondrej 50; candidate |
| 9 | Git cleanliness is not passing tests; record pre-edit failure as baseline, investigate relevance and do not attribute it to later changes without evidence; checks scale to task/repo, no blanket gate. | administrakt0r 123-174, Microsoft 49-61, OpenAI 121-132 |
| 10 | Required fresh remote base not established; no silent stale fallback; identify correct remote/ref and starting commit; report blocker or get authorized adjusted requirement. | Prototype 30-31; control |
| 11 | Development needs durable branch/ref; local branch alone doesn't set correct fork push destination or authorization; inspect repo/provider workflow. | Compound 50; prototype 33-34, 64; control |
| 12 | Preserve moved directory; repair/reconnect metadata, not prune live moved checkout; unmanaged `git worktree repair` from moved tree or surviving repo with new path. Future supported moves use manager/`git worktree move`. | Official 72-88, 207; Qwen 351-371; candidate |
| 13 | `git worktree lock` with reason or equivalent manager protection prevents pruning/move/removal of registration; not backup/security/branch exclusivity; missing path not disposal evidence. | Official 49-51, 69-70, 130-131; candidate |
| 14 | Recognize limitations/incomplete support, verify repo/harness/version-specific setup and lifecycle support; no blanket guarantee or force workaround; repository-specific feasibility judgment. | Official 73, 79, 296-297; prototype 79, 108 |
| 15 | Human whitespace output insufficient; stable porcelain, preferably NUL-delimited `--porcelain -z` for arbitrary paths, parse labels/records and preserve paths. | Official 140-144, 241-274; conditional automation candidate |
| 16 | No: `-d` may assess upstream; compare actual task tip to verified intended target before branch deletion; successful deletion not integration proof. | Prototype 81, 94, 106; control |
| 17 | Separately decide checkout and branch; preserve useful ignored database outside deletion path, retain review ref; verify squash replacements rather than ancestry alone; no active users. | Prototype 77-81, 107; control |
| 18 | Do not run blanket prune while dry run includes offline live checkout; retain/protect offline registration, review remaining eligible scope again. | Prototype 82, 101-103; control |
| 19 | Working files/index isolation does not isolate runtime services/resources; coordinate or give distinct writable state, outputs, ports as needed. | Prototype 16; control |
| 20 | Check actual archive guarantee and ignored-file exclusion; preserve needed local file separately; accurately report removed checkout and retained snapshot/ref, not complete deletion. | Prototype 79, 83, 110; control |

Interpretation: 2 means prototype plus existing training handles the scenario; it does not prove the skill taught it. 1 needs investigation; 0 is a demonstrated failure on this scenario. Only failures plausibly addressed by a specific candidate support testing that addition. This rubric is not runtime verification or a benchmark of overall model intelligence.
