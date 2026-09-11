# Review Gates

Review depth follows the [grade matrix](risk-grades.md). This document defines review and approval semantics.

## Independence

Self-review compares the author's own work against the request; it never counts as independent review.

An independent reviewer is a separate agent invocation/session or a separate person who was not the author of the target artifact. A different model is not required. Renaming the author's role inside the same continuing context does not establish independence. Record reviewer role/session identity according to local policy.

The same independent reviewer may review AS-IS and PLAN in sequence. If an agent cannot provide independent review, use another authorized reviewer or report the required gate as unmet. Do not relabel self-review as completion.

## Bounded phase packet

Give the reviewer:

- work-item identity/revision, ACs, and fixed requirements;
- phase (`AS-IS`, `PLAN`, or `CODE`) and exact target revision;
- approved upstream decisions and direct contracts/invariants;
- allowed/forbidden modification boundaries;
- relevant evidence, known unknowns, and a concrete review question.

The packet is an entry point, not a ban on reading direct callers/callees or evidence needed to test a claim. Expand reads for a concrete reason; do not authorize out-of-scope edits or repository-wide rediscovery.

Review should falsify, not redesign. A PASS applies only to the reviewed candidate and is not Human approval.

## Large phase gates

1. **AS-IS review:** verify observed behavior, evidence, direct dependencies, unknowns, and significant drift. Do not substitute an unapproved future design for current observations. Resolve blocking findings before depending on the analysis for PLAN.
2. **PLAN review:** examine TO-BE, change plan, AC coverage, preserved behavior, failure behavior, scope, ownership, and verification feasibility. Resolve contract blockers and obtain required design approval before implementation.
3. **CODE review:** compare the final candidate with the approved contract, AC evidence, regression risks, and modification boundaries. Complete before integration.

Keep separate phase verdicts even when the documents or report share a file. A combined artifact still needs AS-IS reviewed before its conclusions are treated as a settled planning baseline. Not every phase needs a new model or a large document.

Medium review is risk-based. Small/Trivial keep the lean path unless concrete risk requires escalation. Epic first reviews breakdown/integration ownership and applies Large gates to risky lanes.

## Requirements-based review and optional Blind Audit

Requirements-based review checks the supplied ACs and approved phase contract. Blind Audit adds an independent initial assessment when omission, hidden assumptions, or reviewer anchoring is material.

When used:

- use a reviewer/session independent of the author and primary reviewer;
- provide the same ACs, phase contract, safety boundaries, and target revision;
- withhold the primary verdict/findings and persuasive author review summaries until the auditor fixes its initial verdict;
- preserve that initial result, then reconcile findings with the primary review.

Blind does **not** mean hiding requirements or known safety constraints. It does not invite unconstrained product redesign. Record why the audit is needed; do not require it for every task merely because tooling supports it.

## Review result

A compact record is sufficient:

```text
Phase / target revision:
Reviewer role or session:
Verdict: PASS | CHANGES_REQUIRED | BLOCKED
Findings: class, location, evidence, violated AC/contract, required correction
Unknowns / unreviewed surface:
Blind initial verdict and reconciliation: only when used
```

These are review verdicts, distinct from [verification statuses](verification.md).

Classify findings by what they block:

- **Human Decision blocker:** competing product/architecture meanings require Human choice.
- **Execution-contract blocker:** technically plausible directions change contract, persistence, recovery, or scope meaning; fix one direction before implementation.
- **Implementation finding:** the contract is clear; correct code, fixture, or mechanics without reopening product decisions.
- **Non-blocking observation:** an improvement outside the current acceptance/decision boundary.

## Design approval

When local policy makes a decision Human-owned, record phase, artifact revision, decision scope, approver, and time according to local needs. Obtain approval after relevant review blockers are resolved.

Do not infer approval from reviewer PASS, vague assent, silence, or an older candidate. Planning authorization, implementation authorization, and integration authorization are different scopes.

## Final integration authorization

After required evidence and review are complete, present:

- final candidate revision and work-item identity;
- scope and material decisions;
- AC results, evidence, and unresolved/non-required limitations;
- required review results and applicable documentation sync;
- requested action: merge, close, release, or another explicitly bounded operation.

Default: wait for explicit Human approval of this candidate and action. Approval to implement or commit is not permission to merge or release. A policy explicitly delegating low-risk integration may substitute for per-task approval only within its recorded scope and conditions; missing or ambiguous policy means stop.

Approval does not turn FAIL, BLOCKED, or UNVERIFIED evidence into PASS. Unmet required ACs/reviews still block completion. Any scope/AC change must be explicit and re-reviewed as needed, not a silent waiver.

## Revision changes

Use an immutable or unambiguous target (commit, versioned document, or identifiable snapshot). Material changes to scope, contracts, decisions, acceptance semantics, or implementation invalidate the affected verdict/approval. Re-verify and re-review affected evidence and present the new candidate for required approval. Unchanged evidence may be reused only when its relevance remains demonstrable.
