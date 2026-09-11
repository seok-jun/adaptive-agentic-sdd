---
name: implementing-issue
description: Implement an approved work item with bounded analysis, risk-adaptive review, AC-linked evidence, and explicit integration authorization.
---

# Implementing Issue — Starter

## Required inputs and preflight

Read the current work item/snapshot and `docs/sdd-workflow.md`, then target code/direct contracts and linked domain docs only when relevant.

Resolve goal, user/business impact, ACs, scope/non-scope, allowed/forbidden modifications, fixed decisions, dependencies, grade, requested action, and current permissions. Identify important AC proof methods. Stop edits when required information or authority cannot be resolved safely.

## Grade route

Use the local matrix without redefining it:

- Trivial: direct non-behavioral change, targeted validation, self-review; no SDD package.
- Small: bounded analysis and plan in the work item/notes; targeted verification and self-review.
- Medium: explicit AS-IS, TO-BE/change plan, and risk-based independent review.
- Large: AS-IS -> independent AS-IS review -> PLAN -> independent PLAN review -> applicable design approval -> implementation. Independent CODE review follows final verification.
- Epic: breakdown/integration ownership first; apply Large gates to risky lanes.

Promote grade when new risk appears. Separate phases need distinct verdicts, not necessarily separate files. Required independent review must be another invocation/session or person; do not count the author's self-review.

## Bounded analysis and PLAN

Explore direct path, symbol, public contract, callers/callees, relevant durable docs, then broader sources only for concrete uncertainty. Record observations, evidence, unknowns, and drift. Direct-dependency reads do not widen write permission.

Define desired/preserved behavior, failure handling, relevant state transitions, change order, AC-to-evidence mapping, and genuine trade-offs only. Bind required review/approval to phase and target revision. Pass bounded packets; do not preload entire parent transcripts. Blind Audit, when justified, follows the local separation contract.

## Implement and verify

Edit only authorized scope; preserve fixed contracts and unrelated work. Add useful direct regression coverage. Run targeted checks before broader relevant checks.

For important ACs record method/expected result, actual observation, target revision/environment, PASS / FAIL / BLOCKED / UNVERIFIED, and evidence/reason. Never infer runtime PASS from generated commands or intended behavior.

Self-review the final diff against ACs, boundaries, decisions, and unintended effects. Sync durable docs from observed final behavior when relevant. Run final checks and obtain required independent CODE review and runtime evidence. Material candidate changes require affected checks/review again.

## Finish boundary

Report final candidate, AC evidence, required review results, documentation sync, remaining limitations, and requested integration action. Missing required evidence or review blocks readiness; self-review is not a fallback certification.

Wait for explicit final Human authorization of the candidate/action, unless a documented applicable low-risk delegation is recorded. Approval to implement or commit is not approval to merge/close/release. Approval does not make missing evidence PASS.

Until authorized, report ready for Human Review, not fully integrated/complete. After authorization, perform only allowed integration and cleanup, retaining required evidence and unrelated changes. State what actually ran and what remains unverified.
