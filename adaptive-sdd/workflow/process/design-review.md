# Design review

This is the source of the Large AS-IS and PLAN design review procedure. Read it when actually preparing the review of the relevant phase or reflecting findings. It does not apply to Epic creation or decomposition. A cross-environment SDD review performed explicitly in Medium reuses only the remote candidate publication conditions below and does not add Review B.

| Current work | Section to read |
| --- | --- |
| Checking the review mode the project chose | [Review mode](#large-design-review-mode) |
| Initial AS-IS and PLAN review | [Design phases](#large-design-phases), [Candidate publication](#remote-review-candidate-publication), [Dual independent review](#large-design-dual-independent-review) |
| Candidate change after review | [Meaning and impact decision](#design-re-review-by-meaning-and-impact) |
| PLAN premise error or policy change during implementation | [Plan correction and policy transition](sdd/plan-change.md#plan-correction-and-policy-transition), then the impact decision below |
| The same conflict of meaning repeats after fix and reconfirmation | [Switching on repeated stalls](#switching-on-repeated-stalls) |

[execution-routing](../skills/_shared/execution-routing.md) is the source for the reviewer's model, floor and qualification, and [execution-packets](../skills/_shared/execution-packets.md) is the source for the handoff fields and evidence identity. This document owns the review order, independence and progress conditions. For the project's human authority, apply `W/../project/sdd-workflow.md`.

## Large design review mode

The project chooses two values in the `Execution profile` of `W/../project/sdd-workflow.md`. If a value is not declared, the default is used. The defaults are the same as the behavior before this section existed.

| Setting | Value | Application |
| --- | --- | --- |
| `review.large_mode` | `dual` (default) | Apply the [Dual independent review](#large-design-dual-independent-review) below as is |
| | `single` | Read as the "single mode" below |
| `review.blind_reviewer_selection` | `required` (default) | A human chooses the Review B reviewer. If none is chosen, `BLOCKED: blind-audit reviewer selection required` |
| | `optional` | Allows the "automatic Review B reviewer selection" below. Not applicable with `single` |

No value changes the following: the human-judgment requirements of M's `core.md`, the grade decision and automatic escalation, [Remote review candidate publication](#remote-review-candidate-publication), the reviewer's `REVIEW` floor and separation from the author, the blocker classification and the requirement of 0 blockers in the progress conditions, the one default CODE review, and human judgment for a Large merge. A change of value applies from a newly started initial AS-IS or PLAN review; a phase whose initial review has already started finishes in the mode in effect at that time. To change the mode of an in-progress phase, a human decides it explicitly for that phase.

**single mode.** For each initial Large AS-IS and PLAN candidate, apply one independent review by a separate agent/session distinct from the author.

- In addition to the scope Review A checks, this review also covers Review B's search questions (missing current-state facts, hidden assumptions, omissions that change the scope/ownership boundaries, upstream contract conflicts, and blocking risks that could overturn the direction). Do not widen it into solution discovery or a repository-wide redesign.
- Findings are classified with Review B's four severities and blocker qualification below.
- Blind Audit input isolation, human selection of the B reviewer, and reconciliation do not apply. The same reviewer directly reconfirms the resolution of earlier findings on the current target.
- The conditions for proceeding to the next phase are as follows.

```text
Independent review (single): PASS at current target
unresolved Human Decision blocker: 0
unresolved Execution-contract blocker: 0
```

- In the remaining sections of this document, read "A → B" and "Review B reconfirmation" as the reconfirmation of this independent review, and read the cases needing a "new independent Blind Audit B" as "independently reviewing the whole invalidated phase again in a new session separate from the author". [Switching on repeated stalls](#switching-on-repeated-stalls) applies as is.

**Automatic Review B reviewer selection (`dual` + `optional`).** If, after Review A PASS, a human has chosen the B reviewer's model and reasoning, use that choice exactly as with `required`. If the chosen reviewer cannot be used, do not automatically switch to another reviewer; it is `BLOCKED: selected blind-audit reviewer unavailable`. If no human has chosen, the Agent may choose by the automatic selection rules of [execution-routing](../skills/_shared/execution-routing.md). In that case the candidate must have a fresh qualification PASS for the independent reviewer role, a `REVIEW` floor of `strong + high` or above, and a separate session distinct from both the author and the Review A actor/session; `frontier` is not chosen without existing escalation evidence. If no candidate meets the conditions, stop in that source's `BLOCKED` state. Record in the Review Packet the fact of the automatic selection, the evidence for the selection, and the requested model and reasoning. Blind input isolation and reconciliation remain unchanged.

## Large design phases

The file layout below applies to new SDD work. Work in progress under the existing layout keeps the existing AS-IS target (`01-as-is.md`), and rewriting or re-review is not required retroactively.

1. Write the human-facing AS-IS `README.md` and the evidence `01-as-is.md`, and fix the review target with the remote candidate publication conditions below.
2. On the same exact candidate, complete Review A → Review B below and the needed reconciliation.
3. Within the scope that meets the review conditions below and the [phase dependencies](sdd/issue.md#open-questions-and-phase-dependencies), write `02-to-be.md` and `change-plans/**` without waiting for additional human approval. Work that needs an open conclusion waits according to P's human-judgment rules.
4. The PLAN also goes through remote candidate publication and A → B. Implement only when the initial review or the current-target reconfirmation chain meets the progress conditions on the current exact candidate.
5. After implementation, prepare the PR through the [code review by grade and required verification](verification.md#review-gate-by-grade). A Large merge follows the existing human-judgment rules.

## Remote review candidate publication

AS-IS and PLAN independent review candidates are fixed as an exact commit on the publication repository, remote and branch declared by P's `tracker.md`. The default when unspecified is the current product repository and the Issue branch. An external harness repository or a local bare remote the reviewer can access is also possible. Record the branch of the product claim and the document publication branch separately.

1. Local commits are allowed during drafting. Right before handing over for review, commit the candidate in the declared repository that owns the artifacts and push it to the declared publication remote branch. On a shared branch, coordinate the publication owner, and do not include other lanes' changes or force push. P's commit/push permissions are met separately.
2. Confirm that the exact candidate SHA is in the remote branch history and that the original artifacts at that SHA (for AS-IS, `README.md` and `01-as-is.md`; for PLAN, `02-to-be.md` and `change-plans/**`) can be read from the remote. A local-only SHA, a local remote-tracking ref, or the existence of the author's worktree alone is not accepted as a review/PASS target.
3. For cross-environment handoff and recovery, leave the Issue number, the branch of the product `[CLAIM]`, the publication repository and remote branch, the phase, the artifact paths relative to that repository, and the exact remote SHA. The reviewer must be able to check the originals without the author's worktree. If the code evidence is in another repository, link that repository, revision and paths separately as well.
4. For a review-affecting change, push a new commit to the declared publication branch and apply the meaning and impact decision and the current-target reconfirmation chain below. A PASS on an earlier SHA is not inherited automatically. For a record/head-only change, first check the conditions for keeping the existing target.

If any of push failure, failure to confirm the exact SHA on the remote branch, or failure to retrieve the remote originals occurs, stop with `BLOCKED: SDD candidate remote push failed`. Do not continue with local-only artifacts. The remote branch and exact SHA alone are sufficient for publication, so do not create a PR or draft PR at this step. Immediate push of every commit is not required, and the declared fresh base branch of a new lane and the existing branch/worktree and claim lifecycle follow [parallel-development](../skills/parallel-development/SKILL.md) as they are.

## Large design dual independent review

For the initial Large AS-IS and PLAN candidates, apply two reviews in order, by separate agents/sessions different from each other. Later revisions apply the meaning and impact decision and the reconfirmation chain below. Review A is separate from the author, and Review B is separate from both the author and the Review A actor/session. Do not add Review B to Trivial/Small/Medium or to the default IMPLEMENT/CODE review.

- **Review A — Contract Review**: Checks, in a bounded way, the current Issue/acceptance, the phase artifact identity, the reviewed upstream contract, direct caller/callee, invariants, allowed/forbidden, and source/diff/verification evidence, and judges the correctness and consistency of the facts, contracts and Agent Execution Spec.
- Review A also compares the baselines, external behavior and operational evidence that determine the AS-IS judgment, and the PLAN's references to P conventions and its reasons for departing from them. Do not create a new finding based on an undeclared personal preference. The needed investigation follows [AS-IS](sdd/as-is.md), and convention records follow [Agent Spec](sdd/agent-spec.md).
- **Review B — Blind Audit**: Looks for missing current-state facts, hidden assumptions, omissions that change the scope/ownership boundary, upstream contract conflicts, and blocking risks that could overturn the PLAN direction. It does not expand into solution discovery, repository-wide redesign, or repeated verification of Review A.

A Review B finding is classified into one of the following four severities.

1. **Human Decision blocker**: It conflicts with a settled upstream contract/Decision, or a reasonable competing option remains that changes the product meaning, ownership, failure behavior or acceptance interpretation, or a change to the scope of an existing Human Decision or a new important product/design Decision is needed. Use only the existing `[HUMAN DECISION REQUIRED]`, and do not create a new decision taxonomy.
2. **Execution-contract blocker**: No Human product judgment is needed, but there are two or more reasonable technical options, and depending on that choice the public/internal contract, persistence lineage, eligibility, schema mapping, recovery convergence or scope meaning changes, so the implementer would end up fixing a behavior meaning that has not been reviewed. When resolving it, do not unnecessarily add Human Decisions to `02-to-be.md`; fix one direction in the appropriate `change-plans/**` execution contract and fixture expectation.
3. **Implementation finding**: A missing direct caller, missing fence application, insufficient race fixture, or mechanical safety bug that does not change a settled Decision/contract/scope and has effectively one correct answer. It does not block progress to the next phase, and an artifact revision only to record the finding is not forced. Preserve it in the Result/Review Packet or an equivalent IMPLEMENT handoff, and confirm in CODE/finishing that both the code and fixture resolve it.
4. **Non-blocking observation**: A future optimization, preference, additional defense, or improvement unrelated to the current acceptance. It is not promoted to a PLAN/IMPLEMENT completion gate.

When Review B reports a `Human Decision blocker` or an `Execution-contract blocker`, it leaves all of the following qualification on each finding.

- Which blocker severity it is
- The invariant that breaks among the current artifact, the settled upstream contract or the direct boundary
- The meaning choice left to the implementer, or the conflicting decision meaning, if it is not resolved before the next phase

If this qualification is absent and the code and fixture converge on one contract-preserving correct answer, classify it as an `Implementation finding`. A reviewer declaring it `blocking` does not by itself make it a PLAN blocker.

A human question that does not change the current phase's judgment and is needed only at a future phase is not raised as a current-phase blocker; link it to its owner and the needed phase. Conversely, do not let an open question that requires choosing a design/execution meaning now pass by deferring it as a future question.

A blocking finding of Review A is re-checked by A after correction. After A passes, the Human chooses the model and reasoning level of the Review B reviewer. Before the choice, the Agent does not assign one arbitrarily; it stops with `BLOCKED: blind-audit reviewer selection required`. However, if the project has chosen `review.blind_reviewer_selection: optional`, apply the automatic selection conditions of [Review mode](#large-design-review-mode) above. The chosen reviewer must meet [routing's `REVIEW` floor and role qualification](../skills/_shared/execution-routing.md) and be usable on the current host. If it cannot be used or is not eligible, do not automatically fall back to another reviewer; stop with `BLOCKED: selected blind-audit reviewer unavailable` and request a Human re-selection. A Human choice does not relax `review-mode = blind-audit`, the separate agent/session, or the capability floor.

Before Review B's initial verdict, do not provide Review A's PASS/BLOCKED verdict, its finding list, its detailed packet, or the details of earlier Review B findings. Review B's input is limited to the Issue id/title, `AS-IS | PLAN`, the target artifact and its remote-resolvable exact SHA, the upstream goal and direct ownership boundary, a prohibition on full redesign, and a request to search for omissions, hidden assumptions and boundary-changing blocking risks. The reviewer may check the caller/consumer/contract directly adjacent to the target artifact.

The material actually handed over is separated from the results through [Blind input preparation and check](../skills/_shared/execution-packets.md#blind-input-preparation-and-check), and its source identity, extraction scope and accessibility are confirmed. Even if findings were removed from the Packet, the independence condition is not met if they are exposed in the artifact or the upstream body.

Only after the initial verdict is fixed, provide the same Review B reviewer with the identities of earlier Review B findings and the resolution expectation ledger. For each earlier finding, the reviewer decides one of `resolved / unresolved / regressed / not-applicable` from direct evidence in the current remote-resolvable exact candidate. Reconciliation is not a procedure that turns earlier findings into an automatic PASS, and the new finding list of the initial verdict is kept separate from the reconciliation of earlier findings. If there are no earlier B findings, state that reconciliation is not applicable.

If there is even one unresolved Human Decision blocker or unresolved Execution-contract blocker, stop the next phase. A change of candidate SHA is a trigger for checking the changes, not itself a decision that the whole review is invalidated. Build the review evidence for the current exact candidate with the impact decision below. Do not inherit an earlier SHA's PASS by merely renaming it, or force a PASS by the number of reviews.

The conditions for a Large AS-IS or PLAN to proceed to the next phase are as follows.

```text
Review A: PASS
Review B: initial blind audit completed; current-target impact/reconfirmation chain valid
Review B reconciliation: prior findings confirmed at current target when present
unresolved Human Decision blocker: 0
unresolved Execution-contract blocker: 0
```

These conditions are the progress conditions of the review. If they are met, Review B PASS is possible even when Implementation findings or Non-blocking observations remain, but the actual next work also checks [Open questions and phase dependencies](sdd/issue.md#open-questions-and-phase-dependencies). An open decision that a reviewer did not make into a finding is also a precondition of the work that needs its conclusion. Implementation findings cannot be omitted from the IMPLEMENT handoff, and the work cannot be completed unless CODE/finishing confirms that the code and fixture resolve them.

IMPLEMENT/CODE keeps the existing one independent code review. A separate code audit may be added only when there is explicit high-risk escalation evidence, such as a destructive migration, cross-DB atomicity or recovery, and this is not made into Large's default dual review.

## Design re-review by meaning and impact

The initial A and the independent, blind B are not skipped. For a follow-up change, link in the existing Review Packet the previous/current remote target, the full change inventory and diff, the identities of the fixed findings, the affected contracts, acceptance criteria and direct consumers, the evidence of no impact, and the current-target reconfirmation results. The reviewer must be able to confirm the inventory independently and open the surrounding evidence needed. Do not presume a missing file or a failure to access evidence to be a small change; block until it is supplemented.

| Confirmed change | Follow-up review needed |
| --- | --- |
| Only the review result record changed; target artifact bytes unchanged | Confirm the separation and identity of the new record and the target. Keep the existing review of the target, and do not automatically create a new A/B because the result record changed |
| Wording or explanation supplemented, with unchanged meaning confirmed by direct evidence | A reconfirms the changes, findings and direct impact on the current target. Also check the applicability of the existing B evidence and the status of prior findings |
| Only the verification means strengthened: product Decisions, upstream contracts, acceptance criteria, product boundaries, failure/recovery meaning, runtime dependencies and existing audit premises unchanged | A checks on the current target the executability of the changed verification plan, its mapping to the acceptance criteria, and the applicability of the existing B evidence. If the evidence for resolving B's existing findings is affected, B follow-up reconfirmation of only the related part. If there is direct evidence of no such impact, do not call B again and do not require a new blind |
| Local execution contract correction; key Decisions, upstream contracts, boundaries and audit premises unchanged | A's reconfirmation of the related contracts and consumers and B's follow-up reconfirmation of the related findings and direct impact. Update only the invalidated judgments |
| Change to key Decisions, upstream contracts, work boundaries, recovery/failure meaning or audit premises | Review the related design of the invalidated phase as a whole with A, then a new independent Blind Audit B. If the upstream AS-IS is invalidated, re-review from the AS-IS |
| Impact unclear | Expand conservatively to the scope where meaning could change. No PASS before evidence is secured; if the premises cannot be proven unchanged, the new A/B path |

Even a one-line edit is judged by its execution meaning. The author's declaration of `explanation-only change` or the diff size is not evidence. Keep the review target artifact and the result record separate. Results go in the existing Review/Result Packet or an Issue comment, and the target body is not edited each time to write results. If results were written into the artifact, unchanged meaning must be proven by the actual diff.

Strengthening the verification means is the case of reinforcing test and verification evidence while preserving the existing acceptance criteria. Adding an approved test path alone is not judged a product boundary change, but path write permission and the claim are met separately. A change to a product seam, runtime dependency or acceptance criteria in the name of testing, or the removal/weakening of existing verification, does not go in this row and is judged by its actual meaning and impact. This is not an exception that skips the initial required review, and if the impact is unclear, follow the corresponding row of the table.

A follow-up reconfirmation may receive earlier findings but is not recorded as an `initial Blind Audit`. When a new Blind Audit is needed, the Human's existing model/reasoning choice may be reused if it is still valid and available/qualified, but use a new session separate from the author/A, and hide the A results and earlier B details before the initial verdict. After the verdict, perform the prior ledger reconciliation. A local reconfirmation also keeps reviewer independence and does not copy an earlier PASS without current-target evidence.

The evidence for proceeding to the next phase links the immutable reference of the initial blind verdict, the later target differences/impact decisions and the A/B reconfirmation chain, and the status of prior findings on the current target. If a new blind condition arises, the chain starts again from the new initial verdict. This chain permits only the reuse of review evidence.

For a record/head-only change, first check whether the existing review target can be kept. If, based on the full change inventory, you confirm that the phase artifact inventory and bytes, the Decision scope and upstream, the reviewed direct contracts/consumers and the audit premises are unchanged, keep the existing target and review evidence. Do not replace the review target with the branch head every time. A change in contract/consumer meaning is not classified as record-only even if the artifact bytes are the same.

Dispatch B only on a candidate where A finding corrections are finished and A PASS is fixed. Avoid overlapping A fixes with B review and producing stale B results. The A/B of a local fix independently reconfirm the invalidated judgments, findings and direct impact. The review result on a new target is the direct evidence of that reconfirmation; do not misrecord it as an initial blind or merely change the target of a past PASS.

## Switching on repeated stalls

If, in the same phase and contract/Decision area, the same finding or the same conflict of meaning is unresolved/regressed **2 times in a row after fix → reconfirmation**, do not start the next automatic review. Do not reset the streak of the same conflict by merely changing the finding name or the SHA. The simple total number of reviews and the discovery of unrelated new defects are not counted as a stall, and directly proving the resolution of that area ends the streak.

Leave in the existing Review Packet the area, the stable finding/conflict identity, each fix and reconfirmation target with its evidence, and the cause that was not resolved. Report the options among: scope separation (including the owning Issue and acceptance criteria), a Human decision on the unclear contract, securing additional evidence, and a re-review with its reason and changed review scope stated. Resume only after the needed Human decision or an explicit re-review reason based on new evidence has been secured. Do not resume automatically because of a new SHA or the passage of time alone. The threshold is not a review exemption or a forced PASS, and the blocker is kept until it is resolved or a human decides the scope.
