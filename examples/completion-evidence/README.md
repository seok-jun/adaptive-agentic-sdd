# Preserving completion evidence

**OPTIONAL / FICTIONAL — a retention walkthrough, not completed work or an executed validation.** All identifiers below are placeholders. [Workflow](../../docs/workflow.md) owns lifecycle and authorization; local policy chooses the retention system and duration.

Suppose a Large change rejects invalid input while preserving valid-input behavior. The fictional work item has AC-01 (rejection) and AC-02 (preserved behavior). Its disposable planning notes will be removed after authorized integration.

## 1. Preserve the approved design checkpoint

Retain an immutable `<design-checkpoint>` containing or referencing the authoritative work-item contract, AS-IS and PLAN artifacts, their separate independent review records, resolved findings, and required design approval. Record reviewer/approver identity, target, scope, and time as needed. A design approval does not authorize the later merge.

A checkpoint may be a retained commit or a versioned evidence-store record. A temporary worktree or an unreferenced local commit alone is not a retention guarantee. Choose a reference and storage location that survive the intended cleanup.

## 2. Bind the candidate summary to its evidence

Use the [PR template](../../templates/pull-request.md) or an equivalent record. For illustration, the summary associated with `<final-commit>` would contain:

```text
Work-item contract: <item-revision>
Approved design: <design-checkpoint> / <approval-record>
Final candidate: <final-commit>

AC-01: <actual status> / <candidate-environment> / <rejection-evidence>
AC-02: <actual status> / <candidate-environment> / <preservation-evidence>
Reviews: <phase-target-reviewer-verdict-records>
Corrections and reruns: <history-reference>
Remaining risks: <non-required limitation, rationale, owner/follow-up>
Required blockers: <none only after actual evidence confirms this>

Requested action: merge this candidate, close the item, remove listed notes
Final authorization: <candidate-action-approver-time-record>
Retained evidence: <durable locations and retrieval references>
Cleanup scope: <explicit issue-only disposable paths>
```

These placeholders are not PASS results. Required FAIL/BLOCKED/UNVERIFIED or missing reviews still block readiness; putting them under “remaining risks” does not waive them. Preserve expectation corrections and approved scope changes instead of rewriting earlier results.

The summary can be in a commit message, PR, or versioned report with evidence references. When using a commit message, the containing commit supplies its own identity; do not try to embed its not-yet-created hash in itself. Verify that the final commit includes the reviewed candidate. Later material edits require affected checks/reviews and any required approval again.

## 3. Integrate and clean only within authorization

After the required evidence/reviews and final authorization, perform the authorized integration. Record the actual integrated revision, including its relation to the reviewed candidate if squash or rebase changes the commit identity. Reassess any changed contents or runtime context under [Review Gates](../../docs/review-gates.md).

Before removing disposable notes, open the retained references and confirm that the approved design, AC observations, review results, correction history, and authorization can still be retrieved. Copy needed untracked/local-only evidence to the approved retention store before deleting its workspace. A summary or hash without accessible supporting evidence is insufficient.

Remove only the listed issue-specific artifacts. Keep current behavioral documentation and all evidence required by local policy; leave unrelated user/team changes intact. If cleanup changes a reviewed source or execution/contract document, treat it as a candidate change, not harmless housekeeping.

Record the actual integration and cleanup outcome separately from the earlier candidate report. If retention or cleanup remains unresolved, state the completed actions and the remaining work without claiming the full lifecycle is complete.

## Small-work variant

A work-item or PR comment may hold the candidate, required AC observations, applicable review/authorization, and retained evidence references. This example does not require separate checkpoint files, Large reviews, or a new evidence service for Small/Trivial work.
