# Developer Execution Guide

For adoption, start with [Bootstrap](bootstrap.md). For policy, use [Workflow](workflow.md), [Risk Grades](risk-grades.md), [Review Gates](review-gates.md), and [Verification](verification.md). This guide explains daily use; it does not add mandatory gates.

## 1. Request a bounded plan

```text
Read the current work item <reference/revision> and repository rules.
Do not modify files yet. State the grade and reason, goal, ACs,
allowed/forbidden modifications, unknowns, verification methods,
and required review/approval gates. Propose the smallest sufficient plan.
```

Expected: observations separated from assumptions and proposals. If the tracker is unavailable, provide an authorized current snapshot with its revision boundary. Do not paste sensitive material into a public work item.

## 2. Review and authorize implementation

Check scope, preserved behavior, failure handling, and whether ACs can be proven. For Large, expect separate AS-IS and PLAN review verdicts; a single unspecified design PASS is insufficient.

```text
Approve implementation of PLAN <revision> for <scope>.
Keep <boundaries> unchanged. Commit to <working-branch> only if needed.
Do not merge, close the work item, or release. Stop for material scope changes.
```

This is implementation permission, not blanket future approval. Replace placeholders with actual repository facts. Do not invent commands, paths, or approval records.

## 3. Read the candidate report

Expect the final revision, changed surface, AC-linked actual results, required review records, documentation sync, remaining risks, and requested next action.

A PASS must point to an executed check or appropriate direct observation. Generated commands and proposed expected results are not runtime evidence. A separate agent invocation/person must perform any required independent review; self-review must be labeled as such.

Trivial/Small can use a few lines in the issue/PR rather than separate SDD reports. A documentation change affecting agent execution rules is not automatically Trivial.

## 4. Handle interruptions without expanding scope silently

| Situation | Action |
| --- | --- |
| Out-of-scope edit is necessary | stop those edits; request an explicit boundary update |
| New high-cost risk is found | regrade and revisit affected gates |
| Required environment/permission is unavailable | record BLOCKED with reason; do not claim PASS |
| A check was not run | record UNVERIFIED and the missing evidence |
| Independent reviewer is unavailable | leave required review unmet; arrange another reviewer |
| Material changes follow review/approval | recheck affected evidence, re-review, and request fresh applicable approval |

Resume with an explicit candidate/work-item revision and resolved blocker. Reuse unchanged evidence only when it remains relevant.

## 5. Final Human Review and authorization

```text
Present candidate <revision> for final Human Review.
Include AC results, required review evidence, documentation sync,
limitations, and the exact requested integration action. Do not merge yet.
```

After required evidence/review are satisfied:

```text
Approve merging candidate <revision> into <target-branch>.
<Explicitly include or exclude closing the work item / release.>
```

Do not grant this approval while required ACs remain FAIL, BLOCKED, or UNVERIFIED. Applicable pre-authorized low-risk integration is a documented local policy exception, not an agent assumption.

## Choosing the light path

Use the [canonical matrix](risk-grades.md), not task duration. A typo may be Trivial, a bounded behavior fix Small, a shared low-cost contract change Medium, and a one-line authorization change Large. Epic is broken down before child implementation.

See [Trivial](../examples/trivial/README.md), [Small](../examples/small/README.md), [Medium](../examples/medium/README.md), and [Large](../examples/large/README.md) examples. They are fictional walkthroughs, not execution evidence.

## Restricted environments — optional draft

The [API/DB verification handoff draft](restricted-environment-verification.md) describes a proposed separation between artifact preparation, authorized execution, and judgment. It does not add DB connectivity or assert operational validation. Do not load it for unrelated work.

## Reading the diagrams

The [overview](../assets/workflow-overview-en.svg) shows the normal path and grade-dependent preparation. The [detailed diagram](../assets/workflow-detailed-en.svg) makes blockers and optional paths explicit. Canonical policy takes precedence over a diagram label.
