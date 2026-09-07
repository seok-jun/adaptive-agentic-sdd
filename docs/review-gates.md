# Review Gates

Review depth scales with risk and phase.

## Review principles

- Review should **falsify**, not redesign.
- Reviewer context should be bounded to the current phase and direct contracts.
- A review PASS is evidence, not Human approval.
- When a reviewed artifact is revision-addressed, findings and PASS apply to that revision only.
- Material changes to decision/scope/contract semantics require fresh review.

## Phase-aware Review Packet

A design review packet should normally include only:

- work-item identity and acceptance criteria,
- current phase (`AS-IS`, `PLAN`, or `CODE`),
- exact target artifact/revision when available,
- approved upstream decisions,
- direct callers/callees, public contracts, and invariants,
- allowed/forbidden boundaries,
- relevant evidence.

Do not hand a reviewer the whole repository and ask for a new design unless the explicit task is architecture discovery.

## Small

Default:

- implementation-agent self-review.

Independent review is optional when there is a concrete reason.

## Medium

Default:

- bounded independent review when shared contracts, ambiguity, or integration risk justify it.

The reviewer should stay within the phase packet.

## Large

Require by default:

1. independent design/contract review before implementation,
2. independent code review before merge.

Design review should check:

- architecture/boundary violations,
- acceptance criteria that cannot be satisfied,
- unsafe failure behavior,
- missing integration ownership,
- unresolved contract choices,
- hidden assumptions that materially affect implementation.

Code review should check:

- diff vs work item and approved plan,
- verification evidence,
- regressions,
- scope creep,
- unsafe implementation details.

## Epic

Require:

- breakdown/integration-ownership review,
- design review for risky child/integration work,
- independent code review for Large-like lanes.

## Blind Audit escalation

A Blind Audit is useful when the main risk is omission, hidden assumptions, or reviewer anchoring.

When used:

- use a reviewer/session independent from the author and primary contract reviewer,
- do not preload the primary review verdict/findings before the auditor's initial verdict,
- give the same bounded phase contract and target revision,
- reconcile prior findings only after the initial blind verdict is fixed.

Do not make Blind Audit universal merely because the tooling can support it.

## Finding classes

Classify findings by what they actually block:

- **Human Decision blocker** — competing product/architecture meanings require Human choice.
- **Execution-contract blocker** — multiple technically reasonable implementations would change contract/persistence/recovery/scope meaning and must be fixed to one direction before implementation.
- **Implementation finding** — the approved contract is clear; code/fixture/mechanical correction is needed.
- **Non-blocking observation** — useful improvement outside the current acceptance/decision boundary.

This prevents implementation defects from unnecessarily reopening product decisions.

## Human approval provenance

When Human approval is required, record enough provenance to know what was approved:

- phase,
- target artifact/revision,
- decision scope,
- approver identity according to local policy,
- approval time according to local policy.

Approval must not be inferred from reviewer PASS, generic conversation assent, or an older artifact revision.
