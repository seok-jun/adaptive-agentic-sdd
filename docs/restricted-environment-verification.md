# Restricted-environment Verification Handoff

**DRAFT / OPTIONAL — proposed protocol, not implemented or operationally validated automation.**

This extension is for environments where an agent cannot directly access a database or integration runtime. It is not a default Skill dependency. It does not grant access, bypass restrictions, or replace required verification.

## Proposed flow

```text
AC-linked verification plan
  -> agent prepares request/query specification and expected observations
  -> authorized executor reviews and runs in an approved environment
  -> sanitized evidence is returned
  -> results are judged against ACs
```

Preparation and execution are separate. A generated request/query remains UNVERIFIED until appropriate actual evidence exists. A specific access/environment obstacle is BLOCKED under the normal status contract.

## Handoff packet

Include AC ID, target candidate/environment identity, preconditions, expected observation, allowed operation, known side effects, execution owner, and a safe result-record format.

For an API request, identify method, endpoint placeholder, inputs, authentication mechanism placeholder, expected response, and side effects. Do not execute automatically merely because a request was generated.

For a DB check, use only an explicitly supplied, approved schema contract. Do not invent tables/columns. Prefer reviewed read-only statements with narrow predicates, suitable result limits, and local resource safeguards; read-only does not mean cost-free. Missing schema details are unresolved input, not an invitation to guess. Mutating statements and production execution are outside this draft's default scope.

Placeholders such as `<approved_endpoint>`, `<approved_relation>`, and `<sample_key>` are specifications, not executable fixtures or real infrastructure identifiers.

## Evidence and safety

The executor records expected versus actual behavior, candidate/environment, time, and a sanitized evidence reference. Never publish credentials, connection strings, real internal endpoints, raw production rows, private schemas, or sensitive responses in the public repository.

Judge evidence using [Verification](verification.md). A request returning successfully does not by itself prove every downstream database AC. Required missing evidence still blocks completion; Human approval does not manufacture PASS.

## Returned observations and follow-up

The optional [verification handoff form](../templates/verification-handoff.md) separates the prepared plan, executor observations, evaluator judgment, and correction history. The executor need not decide PASS; return actual values, candidate/environment/input identities, time, errors or obstacles, and safe evidence references. Keep the original expectations with the plan rather than asking the executor to rewrite them.

1. Before execution, check AC-to-TC coverage and that the proposed observations can prove the ACs. One AC may need multiple TCs; a TC may support several ACs.
2. After return, check target identity and evidence sufficiency, then judge against the referenced AC/plan revision. Incomplete results remain UNVERIFIED, or BLOCKED when a specific obstacle prevents judgment.
3. If an expectation is disputed, use the correction-versus-requirement-change rule in [Verification](verification.md). Preserve prior evidence and decisions.
4. After a code correction, select and rerun affected TCs, including relevant regressions; bind the new observations to the new candidate. Record why any other evidence is reusable.

Fictional decision examples, not executed results:

| Situation | Required follow-up |
| --- | --- |
| AC says “reject at or above 10”; TC incorrectly expects acceptance at 10 | Correct the TC from the unchanged AC, preserve its prior expectation/observation/verdict, and reassess whether the evidence is sufficient |
| The desired rule changes to “reject above 10” after observing the result | Obtain the required scope/AC decision, record the new contract, and revisit affected checks/reviews; do not silently edit the expectation |
| Code is corrected for the boundary | Rerun the boundary and affected regression TCs on the new candidate |
| The executor cannot access the approved environment and the user asks to close the TC | Keep the required AC blocked unless another valid proof is provided or scope/ACs are explicitly revised |

## Before promotion beyond draft

Pilot the protocol with authorized fictional or sanitized fixtures. Confirm query safety, clear handoff ownership, reproducible observations, correct status reporting, and no sensitive output leakage. Record actual observations separately from expectations. Until then, describe this as a proposed extension, not a deployed feature or measured success.
