# Human-executed verification handoff

**DRAFT / OPTIONAL.** Form for the [restricted-environment protocol](../docs/restricted-environment-verification.md), not execution authorization or validated automation. Replace placeholders in the approved local environment. Do not publish sensitive inputs or raw outputs.

## Prepared by the verification planner

- Work item / authoritative AC revision:
- Candidate / environment / test-input identities:
- Authorized executor and allowed operation:
- Preconditions, reviewed steps/request/query, limits, side effects, and stop conditions:
- Safe evidence destination and required observations:

| TC ID | AC reference | Input / steps reference | Expected observation fixed before execution | Requirement source |
| --- | --- | --- | --- | --- |
| TC-01 | AC-01 | | | |

Check that the cases actually prove the required ACs, including relevant boundaries and failure behavior. AC-to-TC mapping need not be one-to-one. Review of the plan is not execution evidence.

## Returned by the executor — observations, no PASS decision required

- Candidate actually executed / environment / input identities:
- Executor / execution time:
- Deviations from the prepared steps:

| TC ID | Actual values / observed behavior | Execution error or obstacle | Sanitized evidence reference |
| --- | --- | --- | --- |
| TC-01 | Not executed | | |

Return errors, partial output, and inability to run as observations. Keep the prepared expected values available but do not edit them to fit the result. This separates collection from judgment; it does not hide steps or safety information from the executor.

## Completed by the evaluator after evidence returns

| AC / TC | Expected value / plan revision | Actual observation reference | Candidate / environment | Status | Reason / missing evidence / next action |
| --- | --- | --- | --- | --- | --- |
| AC-01 / TC-01 | | | | UNVERIFIED | No execution evidence yet |

Use [verification statuses](../docs/verification.md). Confirm the executed target matches the requested candidate and the evidence is sufficient for each AC. A successful request alone does not prove downstream effects. A concrete execution obstacle is BLOCKED; missing or insufficient evidence is UNVERIFIED.

## Correction and rerun history — when needed

| AC / TC | Prior expectation / observation / verdict reference | Change and authoritative reason | Decision / revised contract reference, if needed | Affected checks / new candidate / new evidence |
| --- | --- | --- | --- | --- |
| | | | | |

Preserve old observations and verdicts. Distinguish correcting a TC against an unchanged AC from changing the AC itself. Record whether existing evidence remains sufficient or which checks need rerunning; changed code requires fresh affected checks. Keep the earlier result bound to its original candidate. Administrative closure of a TC does not satisfy an unmet required AC.
