# SDD Workflow — Starter Local Contract

This is the local process contract referenced by the starter Skill. Adapt it to the repository instead of expanding `AGENTS.md`.

## Grades

### Trivial

Non-behavioral only. No executable/test/build/dependency/schema/contract/workflow semantic change.

### Small

One implementation boundary, low failure cost, narrow verification.

### Medium

Multiple boundaries/shared contract/integration work without Large-level failure cost.

### Large

High-cost, hard-to-reverse, security/privacy, migration, recovery/consistency, authorization, cost/quota, or durable public contract risk.

### Epic

Multiple independently deliverable capabilities or major boundary changes; break down first.

## Required depth

| Grade | AS-IS/PLAN | Design review | Human approval | Code review |
| --- | --- | --- | --- | --- |
| Trivial | no separate artifact | no | no | self |
| Small | work item / notes | optional | no | self |
| Medium | explicit | risk-based | local policy | risk-based |
| Large | explicit | required | when Human-owned | required |
| Epic | breakdown + explicit risky lanes | required for risky lanes | when Human-owned | required for Large-like lanes |

## Approval semantics

A reviewer PASS does not create Human approval.

If Human approval is required, bind it to:

- phase,
- artifact/revision,
- decision scope.

Material changes invalidate stale review/approval for the changed semantics.

## Verification semantics

Use PASS / FAIL / BLOCKED / UNVERIFIED. Never treat an unrun check as PASS.

## Local extensions

Add repository-specific rules here or in dedicated conditional docs when necessary, such as:

- module ownership,
- build/test preflight,
- migrations,
- device/browser QA,
- shell/encoding rules,
- organization-specific review systems.
