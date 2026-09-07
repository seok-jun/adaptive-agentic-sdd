---
name: implementing-issue
description: Implement an approved repository work item using bounded analysis, risk-adaptive SDD gates, scoped edits, verification, and review.
---

# Implementing Issue — Starter

## Inputs

Required:

1. current work-item identity and current body/snapshot,
2. `docs/sdd-workflow.md`,
3. target code and direct contracts,
4. linked architecture/product docs only when relevant.

Do not read unrelated domains for general project understanding.

## Preflight

Before product edits:

1. confirm goal, scope/non-scope, acceptance criteria, dependencies/blockers,
2. resolve grade,
3. confirm allowed/forbidden boundaries when path ownership matters,
4. confirm required approvals are present for the current phase,
5. identify a verification strategy for important acceptance criteria.

If required information cannot be resolved safely, stop edits and report the blocker.

## Grade gate

- **Trivial**: no separate SDD artifact; targeted change + targeted validation + self-review.
- **Small**: work item can serve as plan; bounded inspection + targeted verification + self-review.
- **Medium**: explicit AS-IS / TO-BE / change plan; bounded review when contract/integration risk warrants it.
- **Large**: explicit AS-IS + PLAN, independent design/contract review, Human approval when local policy requires it, independent code review before merge.
- **Epic**: break down first; define integration ownership; do not create one giant implementation lane.

Promote the grade if analysis reveals higher risk.

## Bounded AS-IS

Explore in this order:

1. direct target path,
2. target symbol,
3. direct public contract,
4. direct callers/callees,
5. relevant durable docs,
6. broader search only when concrete evidence requires it.

Record observed behavior and unknowns. Do not treat stale planning documents as current runtime truth.

## TO-BE + verification

For Medium+ work, define:

- desired behavior,
- preserved behavior,
- failure behavior,
- ordered change plan,
- acceptance-criterion-to-evidence mapping,
- real trade-offs only when competing options exist.

## Review / approval

When design review is required, provide a bounded phase-aware packet. If the environment supports immutable/revisioned artifacts, bind review to the exact revision.

Review PASS is not Human approval.

When Human approval is required, it applies only to the phase, artifact revision, and decision scope actually presented. Material revision changes require fresh review/approval.

## Implementation

- modify only in scope,
- preserve approved decisions/contracts,
- avoid unrelated cleanup,
- add direct regression coverage where useful.

## Verification

Run targeted checks first, then broader checks only when the change surface warrants them.

Report every required check as PASS, FAIL, BLOCKED, or UNVERIFIED. Never infer PASS from intention.

## Self review

Compare the final diff against:

- work-item scope,
- acceptance criteria,
- boundaries,
- approved decisions,
- unintended changes.

## Finish

Before calling the work complete:

- update durable docs when runtime/product behavior changed,
- complete required independent review,
- state verification evidence and unverified items,
- create/update the PR according to repository policy,
- clean temporary artifacts/workspaces when applicable.
