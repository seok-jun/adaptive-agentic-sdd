# Review briefing

Optional form for the [bounded phase packet](../docs/review-gates.md). Fill only what the task needs; a work-item comment can carry the same information. This is a newly written template, not a record of an executed review. Use separate phase verdicts when required.

## Full briefing — five sections

```text
1. Task and review target
   Work item / contract revision:
   Phase: AS-IS | PLAN | CODE
   Exact candidate / snapshot:
   AC references and concrete review question:

2. Settled contract
   Approved upstream decisions and their evidence:
   Direct contracts / invariants / preserved behavior:
   Relevant policy references and versions:

3. Boundaries and entry points
   Allowed / forbidden modifications:
   Direct paths, symbols, callers/callees:
   Excluded surface and why:

4. Evidence and uncertainty
   AC-to-evidence references with candidate/environment:
   Actual observations, unrun checks, and blockers:
   Known unknowns and regression concerns:

5. Requested response
   Reviewer identity/session and phase/candidate:
   Verdict: PASS | CHANGES_REQUIRED | BLOCKED
   Findings: class, location, evidence, violated AC/contract, correction
   Unknowns / unreviewed surface:
```

Source evidence must remain accessible. Entry points are not a ban on reading dependencies needed to test a claim; broader reads do not grant broader edits. PASS is neither Human approval nor evidence of an unrun check.

## Abbreviated briefing after corrections

Use only when the prior packet remains accessible and its unchanged context is still relevant. A new reviewer must have enough original context to assess the claim; expand the briefing when necessary.

```text
Prior packet / phase / reviewed candidate / finding references:
New candidate / current work-item contract revision:
Changed inputs and identity-comparison evidence, if used:

Finding -> correction -> changed location -> verification evidence:
Affected ACs / dependencies and regression checks rerun:
Reused evidence and why it still applies:
Remaining findings / unverified items / changed boundaries or decisions:

Review question: Are the cited findings resolved without violating the
current ACs, settled contract, or modification boundaries?
Return reviewer identity, phase/new candidate, verdict, findings,
and remaining unknowns using the normal review-result contract.
```

Do not present the previous PASS as a verdict for the new candidate. Material contract changes require the affected phase review, not merely confirmation that individual edits were made.

For an optional Blind Audit, do not send the correction briefing or prior verdict/findings before the auditor fixes an independent initial result. Build a fresh full packet containing the current ACs, contract, candidate, and safety boundaries without persuasive prior-review conclusions; reconcile findings afterward.
