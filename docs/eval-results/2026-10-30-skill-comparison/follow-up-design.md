# Follow-up design — draft, not executed

Status: **DEFERRED by user decision, 2026-10-31.** This proposal is retained for reference, not queued for execution. Follow the [current disposition and next real-work checks](README.md) instead. No new model calls or skill redesign are authorized by this draft.

## Correct the measurement before changing the skill

The frozen II-S02 input lacks an Issue identity and an authoritative synthetic Issue record. Installed instructions require a specified Issue before implementation. A claim that required fields are satisfied does not specify which record to consume. This can cause an entry-stop decision instead of exercising the implementation sequence the experiment intends to measure.

The fixture names `loan-service/src/main` and `src/test`; the rubric requires staying inside `loan-service/**`. Use fully qualified, unambiguous paths in a new fixture. Define whether the claim is already acquired or whether only the conditions to acquire it are satisfied; these are different states.

The grader instruction requires literal path matching but does not specify that a narrower allowed path set satisfies a broader containment requirement. Author inspection of private evidence raised a false-negative concern. Preserve historical grades as generated, flag the interpretation, and do not claim boundary regression from those grades. This review is not an independent regrade and establishes no revised PASS rate.

For the next diagnostic, supply a synthetic Issue ID, its actual tracker file, explicit acceptance criteria, full allowed/forbidden paths, and claim state. Keep the missing-ID case separately: its expected behavior is to stop without selecting an arbitrary Issue. Do not weaken the operational Issue-selection guard to make an incomplete fixture pass.

## Candidate skill direction

Hypothesis: local explicit wording helps select the first verification step, but implementation prerequisites and boundaries are distributed across dispatch, entry, implementation and output sections. A short Small execution route may reduce omissions without adding rules. This is a hypothesis, not an experimentally established cause.

Draft route, to be reconciled with the canonical owning sections before editing either edition:

1. Resolve the specified Issue and current grade, full allowed/forbidden paths and acceptance criteria.
2. Validate an existing claim or acquire the required lane/claim before the first write, using `parallel-development`; preserve its existing exceptions.
3. Implement only inside that boundary; start verification with the direct test class or owning-module tests. Escalate scope only under the existing verification conditions.
4. On the stable final candidate, satisfy required broad verification and applicable review, then hand off evidence. Small keeps its existing no-separate-SDD behavior.

Prefer moving or tightening the existing Small route and linking to rule owners over adding repeated mandatory prose, a new document, a new approval gate, or a per-step reporting checklist. Do not turn the draft route into a shortcut around current entry guards. Leave finishing behavior unchanged until evidence identifies a concrete gap.

## New comparison, frozen before candidate authoring

Include at least the following distinct behaviors, using synthetic records and harmless local tool targets:

| Case | What it distinguishes |
| --- | --- |
| Complete Small Issue, claim not yet acquired | Claim precedes first write; targeted check precedes broader checks |
| Complete Small Issue, valid existing claim | Claim reuse without duplicate acquisition |
| Missing Issue identity | Correct entry stop; no arbitrary issue selection |
| Necessary change outside allowed paths | Boundary stop or declared integration dependency |
| Targeted test failure | Retry the failing test/module, without preventive whole-repository builds |
| Stable final candidate with a required broad check | Targeted success does not replace final required verification |

Before comparing skills, validate the grader on hand-authored positive/negative examples: equivalent narrower paths, actual out-of-scope changes, claim conditions versus acquired claims, and planned versus executed commands. Keep grading evidence spans/reasons private; publish only item outcomes and hashes. JSON booleans alone validate serialization, not semantic grading accuracy.

Where feasible, use a disposable project with a harmless command recorder to observe actual write/claim/test ordering. Treat action-plan quality and executed behavior as separate measurements; a plan is not proof of tool order. A trace's correspondence to the declared action must itself be checked.

Freeze fixtures, rubric, sample count, exact models/effort and invalidation conditions before writing the new candidate. Use the same corrected environment in both arms. A fresh comparison needs a separately agreed call budget; no new paid calls are initiated by this draft. Do not compare its new fixtures directly with the old grades. Adoption remains a separate decision based on the whole result, including guards and regressions.
