# SDD Workflow — Starter Local Contract

This self-contained adoption snapshot defines local semantics referenced by the starter Skill. Adapt it deliberately; public methodology updates do not automatically change an adopted repository.

## Grade matrix

| Grade | Analysis / plan | Independent review | Verification | Design approval |
| --- | --- | --- | --- | --- |
| Trivial | direct target; no SDD package | self only by default | targeted static/path/format | none by default |
| Small | bounded inspection; work item/notes | self; independent only for concrete risk | targeted AC evidence | local policy |
| Medium | explicit AS-IS / TO-BE / change plan | risk-based design/code review | mapped AC evidence and relevant integration | local policy |
| Large | AS-IS, then PLAN | separate independent AS-IS, PLAN, and CODE verdicts | evidence covering expensive failure modes | when Human-owned |
| Epic | breakdown and integration ownership | breakdown; Large gates on risky child/integration lanes | child and integration evidence | when Human-owned |

Trivial means no runtime/product, test expectation, build, dependency, schema, API/contract, or workflow-execution meaning change. Small stays in one boundary with low failure cost. Medium crosses boundaries/shared contracts without Large failure cost. Large includes security/privacy, authorization, destructive migration, recovery/consistency, retry/scheduling, cost/quota, or durable public-contract risk. Epic contains separately deliverable capabilities or major boundary changes. Promote when new risk appears; never downgrade to avoid gates.

## Scope and phases

Resolve current work-item revision, ACs, fixed decisions, allowed/forbidden modifications, blockers, and requested action before edits. Read direct dependencies when necessary; stop before out-of-scope modifications.

For Large: independently review observed AS-IS before using it as the settled planning baseline; then independently review TO-BE/change plan before implementation. Separate phase verdicts are required, not separate files or models. Resolve blockers and obtain applicable design approval. Review final CODE before integration.

## Reviewer independence and Blind Audit

An independent reviewer is a separate invocation/session or person, not the author of the target artifact. Changing the author's role name in the same context is self-review. The same independent reviewer may cover AS-IS and PLAN. If unavailable, leave required review unmet.

Provide phase, target revision, ACs, fixed contracts, edit boundaries, direct evidence, and unknowns. Return a verdict (PASS / CHANGES_REQUIRED / BLOCKED), concrete findings, evidence, and unreviewed surface. Review falsifies rather than redesigns; direct evidence reads remain allowed.

Optional Blind Audit uses a reviewer independent of both author and primary reviewer. Supply ACs and safety constraints but withhold primary verdict/findings until the initial result is fixed; then reconcile. Use only for material omission/anchoring risk.

## Verification

Map important ACs to method/expected result, target revision/environment, actual observation, status, and evidence/reason. A work-item or PR row is enough for small tasks.

PASS = executed/observed and satisfies expectation. FAIL = observed contradiction. UNVERIFIED = unrun or insufficient evidence. BLOCKED = named obstacle prevents execution/judgment. Generated commands/queries are not runtime evidence; a build alone does not prove behavior. Required non-PASS evidence blocks integration. Omit non-applicable methods with a reason, never a fabricated PASS.

## Approval and completion

Design approval binds phase, target revision, decision scope, approver, and time according to local policy. Reviewer PASS is not approval.

After final evidence, documentation sync, and required CODE/runtime review, present the candidate and exact integration action for explicit Human approval. Planning/implementation/commit permission does not authorize merge/close/release. An explicitly documented low-risk delegation may substitute only within its recorded eligibility; missing policy means stop. Approval cannot override unmet required ACs/reviews.

Material changes invalidate affected evidence, review, and approval. Recheck/review affected parts and request applicable approval for the new candidate. Report ready for Human Review while waiting; perform cleanup/close/release only within actual authority and preserve required evidence/unrelated changes.

## Local extensions

Keep actual commands, module ownership, environment constraints, approval systems, device/browser QA, and model routing in conditional local docs. Do not silently assume capabilities exist. Restrict handoffs to relevant phase context and return evidence references rather than whole transcripts.
