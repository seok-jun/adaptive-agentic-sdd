# SDD entry

Apply [issue](issue.md) for the current Issue contract, human judgment and open dependencies, and [grade](grade.md) for the grade decision, together. Do not re-read the same version you have already checked.

## Common contract and project application

W is the source of the common phase, review and verification contracts below. Read them together with the application grade/profile, human authority, actual paths and minimum verification commands the project declares. Carrying over the source alone does not add to or remove the project's existing gates. `P` is the current project and `W` is the verified methodology; the project paths in this document correspond to the actual paths declared by the P project documents. Use the contracts below for the general execution order and format.

## Implementation start conditions

Read-only investigation does not require an edit claim or a new branch/worktree beforehand. Investigating the same file is not an edit path conflict. Check the access permissions for the investigation itself, user instructions and settled preconditions, and record the revision the investigation is based on.

Before first creating, editing or deleting a work file in the P repository for an execution Issue, secure the lane and claim of [parallel-development](../../skills/parallel-development/SKILL.md#read-only-investigation-and-entry-into-edits). This includes SDD, tests and product code. Because the conditions of the current phase apply, a claim for writing the SDD does not require a review PASS for an AS-IS/PLAN that has not yet been written. The tracker's management records and the Epic management document itself keep their existing exceptions. When entering product implementation, meet the conditions below and the relevant grade gate separately.

A Trivial/Small/Medium Issue may start implementation when all of the following conditions are met.

- The current work instruction requests implementation of that Issue.
- All required body items and the Priority/grade labels exist and match each other.
- There is no `status:blocked`.
- Its allowed edit paths do not overlap with another active lane's `[CLAIM]` or PR.
- The current lane has completed the claim procedure of `W/skills/parallel-development/SKILL.md`.

If even one condition is not met, do not edit code.

## Artifacts and gates by grade

| grade | SDD documents | Pre-implementation gate |
| --- | --- | --- |
| Trivial | None | Proceed after confirming the scope meets the Trivial conditions |
| Small | None | Proceed once the implementation start conditions are met |
| Medium | Required | After writing the SDD, proceed to implementation without intermediate approval |
| Large | Required | AS-IS → required review → PLAN → required review → implementation. No human approval step |

### Trivial

Do not create a separate `docs/sdd/**` directory. The Issue body or the current user instruction serves as the work scope, and only the target files and direct verification evidence are checked.

- Do not do repository-wide discovery.
- Independent review is not required.
- Do not skip targeted validation suited to the kind of change or the final diff self-review.
- Run build tool verification (the build/test commands P declares) only when there is evidence that the change affects its result.
- If a change outside the Trivial conditions becomes necessary during the work, re-grade to at least Small before editing.

### Small

The Issue body serves as the change plan. Do not create a separate `docs/sdd/**` directory.

### Medium

Write `docs/sdd/{feature}/` and then continue with implementation. Do not wait for a separate intermediate user confirmation. However, if you find while writing the SDD that the Issue's goal, scope and boundaries conflict with each other, do not implement; report `BLOCKED`.

### Large

Proceed as `README.md` and `01-as-is.md` → AS-IS required review → `02-to-be.md` and `change-plans/**` → PLAN required review → implementation. Apply the remote candidate publication, A/B independence and current-target progress conditions of [Design review](../design-review.md). After implementation, perform the code review and verification for the grade; a Large merge follows the existing human-judgment rules.

## Reusing existing analysis

For a child Issue's AS-IS, first check the original analysis of the parent and related work, its base code revision, its scope and premises, and its evidence. Reference facts that are still valid for the current change and supplement only the missing or changed parts. Do not repeat the same investigation because the phase or document name differs. Reusing analysis does not mean the child Issue is automatically exempted from the review for its grade, or that past verification or a PASS is inherited as the result for the new target.

## Verification Strategy

The mapping of acceptance criteria to verification means, review by grade, targeted and final verification, and PASS reuse follow the [Verification contract](../verification.md). The actual commands and the project's required verification are set by P's `build.md` and the Issue.

## Review gate by grade

[Review gate by grade](../verification.md#review-gate-by-grade) is the source. The Large design review order and re-review are in [Design review](../design-review.md). Do not stack this execution verification onto Epic creation or decomposition.

## SDD working document structure

The document structure for Medium and Large and the roles of the Human Decision and Agent Execution Spec follow [SDD working documents](../sdd-artifacts.md). Do not create a separate SDD for Trivial or Small.

## Execution routing and packets

The grade determines the orchestration shape, and phase risk and decision complexity determine the model/reasoning tier.

- Trivial and Small are finished by one current agent without model switch/delegation. If the current concrete model is role DENIED, do not increase the number of actors; replace it with one qualified replacement.
- Medium defaults to a single agent, and only an unresolved PLAN decision or a required independent review phase is given bounded delegation.
- In Large, the root/orchestrator owns the design and boundaries that passed review and may use `PLAN / IMPLEMENT / REVIEW` phase routing.
- The actual work of an Epic follows the grade of each execution Issue; membership in an Epic alone does not require delegation or parallel execution.

[execution-routing](../../skills/_shared/execution-routing.md) is the source for model capability, qualification and fallback, and [execution-packets](../../skills/_shared/execution-packets.md) is the source for the fields of the derived cache, guard provenance, freshness and result consumption. Read them at the time of that selection or handoff; do not add them as a fixed prerequisite input to every task.

### Implementation context handoff after PLAN is settled

Large PLAN → IMPLEMENT follows [Context and freshness check at implementation entry](../../skills/_shared/execution-packets.md#context-and-freshness-check-at-implementation-entry). Hand over the reviewed decisions, direct contracts, remaining findings and verification obligations, and check the current evidence before the first edit.

## Methodology application and improvement observations

The start, handoff, SUMMARY and closing records of every execution grade follow [Application and improvement observations](../observations.md). When an actual problem is found, link the incident; when writing the SUMMARY, record the authoring model. Observation gaps are not a new gate for product completion.

## Stabilization-period token diagnostic

Apply the START/BLOCKED/RESUME/END of [token-diagnostic](../token-diagnostic.md) only when P's mode is `ENABLED`. What is skipped because there is no tracker is the token checkpoint; do not skip general observation along with it.

## Parallel work

`W/skills/parallel-development/SKILL.md` is the canonical owner of the execution procedures for claim/release, branch/worktree and cloud sandbox. `W/../project/module-boundaries.md` is the Source of Truth for module ownership and the shared/root integration boundaries.
