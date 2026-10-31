---
name: finishing-issues
description: Closes the work on an Issue of this project whose implementation is done. Use for the final diff review, business document synchronization, verification and CI gates, SDD cleanup, the PR closing keyword, merge confirmation and lane release. Do not use before the implementation is ready to close.
---

The execution inputs are the absolute paths `P` (top level of the project repository), `W` (the pinned procedure copy `W`) and `M` (the pinned common principles `M`). Do not guess P or M from the current folder or from W's parent folder. Follow P's hard guard and application declaration, and read the words Issue, comment, label and PR as the `W/tracker/` method declared in `W/../project/tracker.md`. Look up unfamiliar terms in the [Glossary](../../glossary.md).

# Finishing Issues

Closing an Epic management document checks the evidence that the overall goal was achieved, in `Epic coordination` of `managing-issues`. Do not require the product-change closing order below for the management document itself, which has no code, PR, CI, SDD or claim. Do not close an Epic only because its child Issues are marked closed.

## Inputs

If you cannot confirm that `## Always-applied hard guard` in `P/AGENTS.md` was applied in the same run, read that section first. Reuse inputs and verification results that were checked in the implementation phase and have not changed. For queries and updates, apply the `Input reuse and queries` section of `implementing-issues`, and do not read that whole skill again.

The required inputs are the current Issue body and labels; the current diff; the closing order and SUMMARY contract in `W/process/sdd/completion.md` and `W/process/sdd/issue.md` (and `W/process/sdd/grade.md` if the grade is decided again); and the permissions, paths and verification in P's application declaration. If there is a PR, read the needed PR and CI metadata; if the execution behavior changed, read the directly related business documents.

In the order below, read **only the relevant section** of each needed source.

| Action | Source to read |
| --- | --- |
| Checking the validity of Large AS-IS/PLAN evidence | The current review target, next-phase condition and reconfirmation sections of `W/process/design-review.md` |
| Verification, code review by grade, PASS reuse | `W/process/verification.md` and the relevant verification in P's application document `build.md` |
| Packets, implementation context switch, consuming declared impact analysis results | The relevant Packet and impact result sections in `W/skills/_shared/execution-packets.md` |
| Qualification check for keeping a closing role already held, or for reviewer assignment | The relevant role and selection path in `W/skills/_shared/execution-routing.md` |
| Checking the SDD's decisions and implementation specification | The contract to check in `W/process/sdd/to-be.md` or `W/process/sdd/agent-spec.md` |
| Judging business document lifetime and shared and root boundaries | The relevant boundaries in W/P `module-boundaries.md` |
| Conflicts between instructions or diff and the Issue, or between code and business documents | The relevant conflict section of W/P `agent-instruction-policy.md` |
| Gathering observations, preservation before SDD deletion, product completion observation | The relevant phase section of `W/process/observations.md` |
| Stop, resume and end of enabled token records | The relevant event in `W/process/token-diagnostic.md` |
| Worktree cleanup and releasing ownership | Release and the relevant cleanup section of `W/skills/parallel-development/SKILL.md` |

When entering a closing role, check that role's common prohibition (canonical DENY), actual explicit records and current capability floor with `execution-routing.md`, even when using a model that is already running or that a human chose (current/manual) as is. Reuse evidence that is still valid for the same role in the same run, and do not skip this check because the model is not changing.

## Finish in fixed order

### 1. Confirm actual change

1. Directly check the base/head SHA and the **full changed file list (inventory)** of the current head, and read the diff. Do not trust only a list a worker picked for you. If you received a Result Packet, validate the current diff, file list and evidence with `execution-packets.md`.
2. Distinguish behavior changes from formatting, comment and generated file changes, and connect each actual change to the Issue's acceptance criteria. Also check the "baseline requirement → verification" mapping of `verification.md` in reverse, and show in the SUMMARY any missing entry points or conditions, the substitute evidence for weakened or unrun verification, and the gaps.
3. Compare the Human Decision, the implementation specification and the diff. If there is a new important decision or a change of meaning that a human did not make, stop the affected work and the closing with P's `[HUMAN DECISION REQUIRED]` procedure. Do not substitute agreement between Agents or a review PASS for a human decision.
4. For Large, check according to `design-review.md` that the evidence for the current review target of each of AS-IS and PLAN is valid, and that the needed reconfirmation and reconciliation are finished (based on the mode set by P's `review.large_mode`). Do not justify a missing or stale PASS, or a separation, selection or isolation failure, by the fact that "it is already implemented". If there is no valid evidence, stop the closing. Do not require a human to reread the whole detailed review.
5. Safely revert out-of-scope changes within the allowed edit paths, or `BLOCKED`. If it can be resolved only by editing the W and M pinned copies, report it as a common problem.

Also check the implementation context switch evidence and the substitution limits through the relevant Packet contract. Do not presume a compression or handoff that lost required evidence to be a success, and do not regather full logs. Do not close a blocker that stopped work through a repeated stall without the resolution evidence that `design-review.md` defines or a human's scope decision.

Check the human-facing change documents and the PR and completion summary below against `Visual writing of human-facing documents` in `agent-instruction-policy.md`, in the same self-review or required review. Do not create gates such as additional approval, review rounds or a number of diagrams, and keep simple explanations short.

### 2. Synchronize business documents

Only if the execution behavior changed, check the directly affected business rules and topics of P. Check the actual behavior with the **final code** instead of the descriptions in the Issue or SDD, and update only the existing rules that changed.

If another lane or PR in progress is editing the same business file, it is `BLOCKED: documentation lane conflict`. The allowed scope of documents with a defined lifetime follows `module-boundaries.md`. If the execution or product behavior did not change, do not create or edit business documents for the sake of synchronization.

### 3. Verify before SDD cleanup

1. When using declared impact analysis results, check their freshness and completeness with `Common impact result reference and local consumption` in `execution-packets.md`. Do not reduce required verification with stale results, and do not inherit a review PASS from an earlier SHA.
2. Before deleting the SDD, check the required verification evidence of the implementation, and run verification that is missing or has become invalid. A targeted rerun after inputs changed, a required broad rerun, and PASS reuse when inputs are unchanged follow `verification.md`. A check at this point does not replace the CODE Review and completion verdict of the final candidate after cleanup. If a CODE Review happened before the business synchronization, preserve it as past evidence; the CODE Review of the new candidate is decided in step 5.
3. Before build and test commands, apply `build-preflight.md` and `Verification environment` in `verification.md`. Do not conclude that an environment failure is a product regression. Use as formal evidence only the check of the declared actual build JVM and the result of an allowed correction limited to this process. Do not record as PASS anything that was not run or was blocked by the environment.
4. Check the commands, results and needed CI. A failure or non-run of required verification means not complete. In the completion report, identify the required commands that failed or were not run and the results actually observed. If a command name or result evidence is unavailable, state what is missing and keep the task incomplete until the needed evidence is checked. Do not guess command names or results. Do not turn a build that the grade does not need, as for Trivial, or the absence of the optional Device QA/Runtime QA or reports, into a new gate.
5. Check again that all changed paths match the Issue's allowed/forbidden edit paths. If there is a Result Packet, it must meet the verification evidence based on the current head and the resolution conditions of PLAN Implementation findings in `execution-packets.md`. A self-report that "the command succeeded" alone does not prove a PASS.
6. For an external blocker, record the state and resume conditions, and apply `observations.md` and, if enabled, the BLOCKED/RESUME of `token-diagnostic.md`. Do not resume without evidence of resolution, recheck automatically, or repeat the record.

### 4. Remove temporary SDD

Before deletion, preserve discovery incidents that exist only in the SDD or in local results into the existing Issue with `Recording problems found and linking them to closure` in `observations.md`. Do not turn a reviewed SDD into an incident ledger. If preservation fails, show it in the handoff and closing, but do not make the collection a new completion gate.

Not applicable to Trivial and Small. If there is an SDD:

1. After finishing the business synchronization and the needed verification, clean up **only the current Issue's SDD**. Check the direct references from linked in-progress Issues and plans, and delete contracts and decision evidence that are in use only after applying the reference preservation conditions below. The reviewed documents must remain retrievable after deletion from the exact commit right before the deletion. Do not hide a partial deletion or a design edit as "cleanup".
2. Remove links that are no longer needed from the document index P declared and from related documents. Do not remove a link that an in-progress consumer needs; replace it with a retrievable pinned reference or a contract document that continues to be maintained.
3. If a changeable status value in past review records is stale, update only that status value.

**Reference preservation conditions:** Before deleting, check that the original text and direct dependent documents a consumer needs can actually be retrieved by the exact revision and path. If you move content into a document that continues to be maintained, check that the meaning is kept. When editing another lane's documents, coordinate with its owner and claim, and do not hide a contract change behind a link-only change. If a needed reference switch cannot be finished now, preserve the current SDD folder and leave in the existing SUMMARY the consuming Issue, the reason for preservation, the cleanup owner and the release condition (the consumer's reference switch or the end of the dependency). Preservation with a confirmed owner handoff and retrievability is an allowed cleanup-complete state and does not automatically block product closing. A state that has not secured accessible original text or a cleanup owner is not an allowed preservation. The owner cleans up within existing permissions and claims after the release condition is met. Do not keep the files unconditionally until the whole Epic is closed, and do not delete files remaining after completion without permission.

### 5. Prepare/verify PR closure

First finish the planned repository file changes, such as the business synchronization, the deletion of the current SDD or its preservation under the conditions above, and cleanup of links and review status. Commit the result and fix the current base/head, full diff and file list as the final review candidate. Do not complete a candidate that differs from the target of a past CODE Review with the existing PASS.

1. Before the CODE Review and self-review, secure PASS evidence valid for the current candidate for the required broad verification command set of `verification.md`. Reuse a PASS from step 3 whose inputs are unchanged by preserving its run record, and run only verification that is missing or has become invalid, such as a static checker that reads the cleaned-up documents, in the order of the relevant contract. If a verification fix changes files, first settle the new candidate and its verification evidence.
2. Apply `Review gate by grade` in `verification.md` to the current candidate. For Trivial and Small, check the relevant self-review; for Medium, the `Independent Review` verdict; for Large, the valid result of one independent code review with a defined scope. If the Trivial conditions are exceeded, re-decide it as at least Small. Reuse a review already valid for the same candidate, and do not add Review B to the default CODE review.
3. Give the required reviewer the current CODE Review Packet of `execution-packets.md`, including the verification evidence secured earlier. The reviewer independently checks the validity and reuse conditions of the verification evidence, the completeness of the full file list and the PLAN handoff items, and whether they are resolved by the current code and fixtures. The reviewed original text of a deleted SDD is referenced by the exact commit right before the deletion. If needed evidence is missing, or findings that must be resolved or INVALID/STALE remain, do not move on to merge or completion.
4. After the review, check that all review and verification evidence of the current candidate is valid. If repository files change, for example by applying review findings, fix the new candidate, update the affected verification, then secure the CODE Review and self-review evidence for that candidate. Do not repeat verification whose inputs did not change, and do not widen build PASS reuse into automatic inheritance of the earlier CODE Review target.

Connect the PR and SUMMARY records below to the valid review and verification evidence of the candidate above. If only the PR metadata changes and the repository candidate stays the same, do not redo the same CODE Review.

1. Compare the PR scope with the Issue boundaries and acceptance criteria, and add the closing reference to this Issue (`Closes #{issue-number}`, written as the declared tracker method defines).
2. Summarize decision compliance, execution departures, judgments raised to humans, verification and remaining risks in the one existing `[IMPLEMENTATION SUMMARY]`. If it already exists, update it; do not add a new document or a human approval gate.
3. Apply the closing, authoring model and discovery incident rules of `observations.md` to the same SUMMARY. Preserve the original problem, owner, action and result, and source references, and also gather CI and review incidents after the PR. If there are no incidents, do not create an empty incident list.
4. Connect the observation start record, the actual support and use, gaps, cost sources, the authoring model and the next judgment in the format of the relevant source. Do not make an unconfirmed model or uncollected observations a product closing gate, and do not record a synthetic evaluation PASS or a self-report as evidence of effect.
5. Merge a Large PR only if, according to P's human judgment points, a human merges it directly or explicitly instructs the merge of that PR. Do not merge on a general instruction to proceed, a review PASS or a CI pass alone.
6. Do not say it is complete before the required CI, reviews and the remaining completion conditions are met.

### 6. Merge confirmation and release

1. Right before the merge and at the closing check after the merge, read the needed metadata fresh, and check that the PR was actually merged and the Issue closed.
2. Before cleanup, retrieve the observation start record, the SUMMARY and the needed sources again from a durable location. Leave the results and retrieval gaps in the SUMMARY as the product completion observation of `observations.md`. Do not leave a local worktree as the only source for later observation.
3. Apply `Closing observation check` in `observations.md`. Prepare this preview's `observation-check unavailable reason=not-shipped` result and the needed first output and rerun reasons, but do not make it a new blocking condition for closing or release.
4. Record `[PRODUCT COMPLETE]` once, with the result of the check above and the closing keyword and merge SHA of the PR actually merged into the merge target branch P declared. After the tag on the first line, put the `product-complete:` JSON in the declared tracker method's format (for GitHub, `{"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40-character SHA"}`). Product completion is separate from local cleanup and releasing ownership; do not create duplicate completion records for the same lifecycle.
5. Run Release and Merged local worktree cleanup of `parallel-development`. Before removing the registration, check that there are no untracked diagnostic or unidentified files for which neither creation by this run nor generated-file status has been established. Preserve such files as user state, stop the registration removal and RELEASE, and report the lane release as incomplete.
6. The "no artifacts" exception, the build cleanup, the separate absence checks for the registration and the actual folder, the allowed residue cleanup and the order of releasing ownership follow that source. Reuse the current claim and environment evidence, and do not bypass the protection policy with forced cleanup or a loop of individual deletions over bulk files.
7. If cleanup or release is pending, report the exact path, state and resume conditions, but do not cancel product completion. Leave cleanup-only follow-up updates in `[LOCAL CLEANUP]`, and do not rewrite the product completion record.
8. Once product completion is confirmed, apply the END of `token-diagnostic.md`, if enabled, separately from local cleanup. For `not-planned`, use the matching closing format of the same source when the final close is settled instead of a merge.

## Incomplete conditions

Do not call a product Issue complete if:

- An acceptance criterion failed or is unknown, required CI failed, a required review is not finished, or a finding that must be resolved is unresolved
- Required current review target evidence in `design-review.md` is missing or stale, a required reconciliation is not finished, or a Human Decision/Execution-contract blocker is unresolved
- Required PLAN handoff items, code/fixture resolution or verification evidence in `execution-packets.md` are missing, unresolved or INVALID/STALE
- A required business document contradicts the final code, or there is a documentation lane conflict
- The required SDD cleanup is not finished, the PR's closing reference is missing, or there is an unresolved product work BLOCKED

Report `CLEANUP_BLOCKED`, residue in the registration or the actual folder, and unidentified files separately as incomplete local cleanup. Unconfirmed observation and model records and non-required device checks keep the non-blocking conditions each source defines. The prohibition on deleting user files still applies.

## Output

- Actual changed paths / acceptance criteria results / business document state
- Verification, CI, required reviews, and the validity of the current review target and Packet evidence
- SDD cleanup / PR, Issue and product completion / observation gathering references
- If enabled, token BLOCKED/RESUME/END records or the reason they were not collected
- Local cleanup and lane release / unverified items, BLOCKED and resume conditions
