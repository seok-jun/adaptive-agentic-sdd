# Large Example

**Fictional change:** enforce a retry budget before an external paid operation.

Why Large: retry semantics, cost exposure, and expensive failure. The example contains no real provider, endpoint, schema, customer, or operational result.

## Ordered gates

1. Define ACs, preserved behavior, allowed/forbidden modifications, and fixed decisions.
2. Write AS-IS from current code/evidence: identify retry ownership and the external-call boundary; label unknowns.
3. Obtain an **independent AS-IS verdict** for that revision. Resolve observation/contract blockers before relying on the analysis as the PLAN baseline.
4. Write TO-BE/change plan: define retry ordinal input, accumulated-cost input, allow/block decision, failure handling, and enforcement ordering. Record real trade-offs only when present.
5. Obtain a separate **independent PLAN verdict** for the TO-BE/change-plan revision. Obtain required Human approval for Human-owned decisions. Neither AS-IS PASS nor review PASS is that approval.
6. Implement the authorized scope; collect targeted and final evidence and synchronize relevant durable docs.
7. Obtain independent **CODE review** for the final candidate. Add a Blind Audit only for a stated omission/anchoring risk, preserving its initial verdict before reconciliation.
8. Gather required integration/runtime observations. Any required missing or failing evidence blocks readiness.
9. Present the final candidate and requested action for Human authorization; only then perform authorized merge/close/cleanup. Release requires its own authority if not included.

The same independent reviewer can cover AS-IS and PLAN; the verdicts remain distinct. Direct caller/contract reads are allowed, but out-of-scope edits are not.

## Illustrative verification plan — not executed

| AC ID | Expected evidence | Status in this example |
| --- | --- | --- |
| AC-01 | just-below, at-limit, and over-limit decisions match the approved budget contract | UNVERIFIED |
| AC-02 | retry accumulation follows the approved contract | UNVERIFIED |
| AC-03 | denial prevents the paid operation from occurring | UNVERIFIED |
| AC-04 | approved failure behavior is preserved when required input is unavailable | UNVERIFIED |

These are proposed checks, not proof. If a required runtime environment or independent reviewer is unavailable, report the blocker rather than simulating a PASS. Material candidate changes require affected verification/review/approval again.
