# Workflow

This is the canonical lifecycle. [Risk Grades](risk-grades.md), [Review Gates](review-gates.md), and [Verification](verification.md) define their respective contracts. Diagrams, examples, and the developer guide explain them; they do not override them.

## 0. Bootstrap

Identify actual module boundaries, work-item system, build/test paths, and existing rules before adopting a small root contract and task Skill. Keep environment-specific safeguards local. See [Bootstrap](bootstrap.md).

## 1. Work item and preflight

Before edits, resolve:

- current work-item identity/revision or trustworthy snapshot;
- goal, user/business impact, priority, grade, and fixed decisions;
- scope/non-scope, allowed/forbidden modification boundaries;
- ACs, proof methods, dependencies/blockers, and authoritative references;
- requested action and available capabilities: plan, implement, verify, review, commit, or integrate.

Missing required boundaries, conflicting authoritative requirements, unresolved dependencies, or missing phase permission block edits. Grade follows risk, not file type or implementation time.

Read scope and write scope differ: inspect direct dependencies needed to understand a change, but do not modify outside authorized boundaries. Stop and obtain a scope update if such edits become necessary.

## 2. Claim / isolation when needed

Parallel work may require lane ownership, overlap checks, and an isolated branch/worktree/sandbox. These are local operational extensions, not mandatory ceremony for every repository. Preserve unrelated user/team changes.

## 3. Bounded AS-IS

Start from current mainline code and direct runtime evidence. Prefer direct target path, symbols, public contracts, callers/callees, then relevant durable docs. Broaden only for concrete uncertainty.

Record observed behavior, evidence, unknowns, boundaries, and meaningful drift. Trivial skips a separate artifact; Small can use the work item or notes.

**Large gate:** independent AS-IS review must resolve blocking observation/contract gaps before its conclusions are used as the settled PLAN baseline. Record the AS-IS target revision and verdict.

## 4. TO-BE + change plan + verification strategy

Define desired and preserved behavior, failure behavior, relevant state transitions, ordered changes, AC-to-evidence mapping, and rollback inspection. Capture trade-offs only when real competing options exist.

Medium+ uses explicit sections; separate files are optional. Epic first breaks down independently verifiable children and assigns integration ownership.

**Large gate:** independently review PLAN (TO-BE and change plan) at its own target revision. Resolve blockers and obtain design approval when the decision is Human-owned. An AS-IS PASS is not a PLAN PASS or implementation authorization.

## 5. Implementation

Implement only the authorized work. Preserve approved decisions/contracts; avoid unrelated refactors, features, renames, and dependency changes. Add direct regression coverage where useful. Escalate grade or stop for approval when new risk or scope changes appear.

## 6. Verification and self-review

Run targeted checks first, then broader checks warranted by the changed surface. Connect each important AC to expected behavior, actual observation, target revision/environment, status, and evidence.

Compare the diff against ACs, scope, allowed/forbidden boundaries, fixed decisions, and unintended changes. Self-review is not independent review. Unrun checks are never PASS.

## 7. Durable documentation and final candidate

When product/runtime behavior changes, synchronize durable docs from final observed code behavior, not copied planning prose. Run final required checks against the candidate. If documentation changes execution/contract meaning, include that change in verification and review scope.

## 8. Independent CODE review when required

Large and Large-like Epic lanes require independent code review. Medium uses bounded independent review when contract/integration risk warrants it. Apply [Review Gates](review-gates.md); do not ask the author to certify independence.

Material changes after review require fresh affected checks/review. Optional Blind Audit has a separate initial verdict before findings are reconciled.

## 9. Required runtime evidence and readiness

Collect device/browser/integration/runtime observations whenever ACs require them. This can happen during verification; it must finish before final authorization. See [Device QA](device-qa.md).

Prepare the PR or equivalent candidate report with scope, AC results, review evidence, meaningful decisions, documentation sync, and limitations. Required FAIL, BLOCKED, UNVERIFIED, missing review, or unresolved contract findings block readiness. Commands generated for someone else to execute are not execution evidence.

## 10. Final Human Review / authorization

Submit the final target revision and requested integration action for explicit Human approval. Design approval and reviewer PASS do not authorize merge/close/release. A documented, applicable low-risk delegation is the only policy alternative; record its reference and eligibility.

Approval cannot replace required evidence. If the candidate changes materially, revisit affected verification, review, and approval. Until authorized, report **ready for Human Review**, not merged or fully complete.

## 11. Authorized integration / cleanup

Only within the actual authorization: merge, update/close the work item, clean disposable SDD artifacts and isolated workspaces, and release the lane. Preserve evidence required by local retention policy; never remove unrelated changes. Release/deployment needs its own authority when not covered.

Report what actually happened. Approved implementation work can be delivered as a candidate without claiming the entire integration lifecycle is complete.
