In `case03/checkouts/adapter-current`, on `task/adapter`:

1. `cd case03/checkouts/adapter-current && pwd`
   - confirms moved checkout, not `adapter-old`.
2. `git status -sb`
3. `git branch --show-current`
   - must be `task/adapter`; if not: `git checkout task/adapter`
4. `cat worker-status.json`
   - confirm schema worker `schema/prep` complete.
5. `git log --oneline -3 schema/prep`
6. `git show schema/prep --stat` + read `SCHEMA_VERSION` result from that branch
7. Open file containing `encode_record`, keep existing draft notes untouched, finish implementation:
   - `name.strip().lower()`
   - `enabled` as `bool`
   - `schema` from `SCHEMA_VERSION`
8. Run project check, e.g. `make check` / repo check script - must pass.
9. `git status -sb`
10. `git add <adapter file only>`
11. `git commit -m "Finish encode_record"`
12. `git status -sb && git log --oneline -3 && git branch --show-current`
   - clean, on `task/adapter`, same checkout ready for review.
   - No merge, no checkout switch, no push/integration/publishing.

