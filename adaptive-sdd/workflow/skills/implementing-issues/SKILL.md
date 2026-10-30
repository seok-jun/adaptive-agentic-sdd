---
name: implementing-issues
description: Investigates, designs and implements an approved work item (Issue) of this project, received by Issue number or an explicit reference. Use for requests to progress, implement, work on or wrap up an existing Issue; it connects the SDD, boundary and verification procedures of the current phase. Do not use when only writing a new Issue.
---

The execution inputs are the absolute paths `P` (top level of the project repository), `W` (the pinned procedure copy `W`) and `M` (the pinned common principles `M`). Do not guess P or M from the current folder or from W's parent folder. Follow P's hard guard and application declaration, and read the words Issue, comment, label and PR as the `W/tracker/` method declared in `W/../project/tracker.md`. Look up unfamiliar terms in the [Glossary](../../glossary.md).

# Implementing Issues

## Issue dispatch

1. Read the current body and labels of the designated Issue first. Do not start by searching the whole list of open Issues.
2. Use the Issue as the execution baseline, and keep its Priority, grade, phase dependencies, allowed/forbidden edit paths, acceptance criteria, Visual Spec and common contract references. Do not re-explore requirements that are already settled or make the user enter them again.
3. If it is an Epic management document, update the work breakdown and dependencies through `Epic coordination` in `managing-issues` and then enter the relevant child execution Issue. If there is no child Issue, define and investigate as many as needed. Do not require an implementation claim, an execution grade or AS-IS/PLAN/BREAKDOWN reviews for the management document itself.

## Inputs

If you cannot confirm that `## Always-applied hard guard` in `P/AGENTS.md` was applied in the same run, read that section first. Reuse the same version you already checked.

The required inputs are the current Issue; the current grade, entry and human-judgment conditions in `W/process/sdd/grade.md`, `W/process/sdd/entry.md` and `W/process/sdd/issue.md`; and the application, permissions and actual paths in `W/../project/sdd-workflow.md`. For investigation, read the business and architecture documents directly linked to the Issue, the target code, its direct contracts, and its callers and callees.

For design that writes an SDD, Medium implementation entry, and a separate IMPLEMENT context, directly check the problem, premises, invariants and remaining risks in the relevant `README.md`, using the needed sections and the baseline revision. Being a document for humans does not mean the Agent need not read it. However, do not uniformly read the whole README or the conditional investigation history. For review roles, apply the existing allowed inputs per phase and mode and the Blind Audit isolation unchanged.

Read the sources below **only for the sections needed when taking that action**. Do not use this list as a list to read entirely in advance.

| Action | Source to read |
| --- | --- |
| First SDD layout | `W/process/sdd-artifacts.md` |
| AS-IS investigation and evidence writing | `W/process/sdd/as-is.md` |
| PLAN decisions and trade-off writing | `W/process/sdd/to-be.md` |
| Writing and consuming the implementation specification | `W/process/sdd/agent-spec.md` |
| Premise errors during implementation and policy changes during work | `W/process/sdd/plan-change.md` |
| Large AS-IS/PLAN publication, review and reconfirmation | The sections of `W/process/design-review.md` that match the current phase and review target |
| Verification planning and execution, PASS reuse, code review verdicts | `W/process/verification.md` and the relevant verification in P's application document `build.md` |
| Qualification check for the role you now hold; choosing model, reasoning, delegation and substitute model | The relevant role and selection path in `W/skills/_shared/execution-routing.md` |
| Worker handoff, Result/Review consumption, using declared impact analysis results | The relevant Packet and impact result sections in `W/skills/_shared/execution-packets.md` |
| Claim, lane and isolation for the first write of P work files such as SDD, tests and code | The relevant section of `W/skills/parallel-development/SKILL.md` |
| Shared and root boundaries; judging documents with a defined lifetime | The relevant boundaries in W/P `module-boundaries.md` |
| Instruction conflicts, code vs business document mismatches, inability to interpret the approved scope | The relevant conflict section of W/P `agent-instruction-policy.md` |
| Writing human-facing status, plans and change explanations | `Visual writing of human-facing documents` in `W/process/agent-instruction-policy.md` |

At start, problem discovery, stop and handoff, apply the relevant section of `W/process/observations.md`. When `W/process/token-diagnostic.md` is enabled, leave token records (token checkpoints) matching the current phase event. If the work tracking tool cannot be used, omit only the token records; do not omit the other observation records.

## Input reuse and queries

- Reuse Issues, policies, sources and Issue/PR metadata that were read in the same run and have not changed.
- When any of these signals appears, re-read only the inputs needed for that judgment: a change of the review target SHA, a PR head changed by a push from the current lane, a merge, close, reopen, label, assignee or state change of the Issue/PR, evidence of a base change, or an external state change learned through a webhook, wake-up, external tool result or user instruction. Also re-read the needed metadata right before a merge and right before the closing check after a merge.
- If you need only the state, labels, mergeability or head/base SHA, first use a query that reads only the metadata or only the needed fields. Read the body, comments or diff only when their content is the evidence for the judgment. Do not create a double call that always reads everything again after reading the metadata. If the metadata alone is not enough for a safe judgment, read more of what is needed.

## Investigation and entry into product edits

1. Distinguish whether the current request is a read-only investigation or a product edit, and check the dependencies and blockers needed for that phase. Keep the access permissions and human-judgment conditions of the investigation itself. An open conclusion upstream only makes the implementation, integration or deployment that uses it wait; it does not block the start of the investigation.
2. A read-only investigation does not require an edit claim. Several readers of the same path are not an edit conflict. Before first creating, editing or deleting P work files of an execution Issue, such as SDD, tests and code, secure a lane and claim with `parallel-development`. Apply the current phase's instructions, dependencies and boundaries. Do not require a PASS of a not-yet-written AS-IS/PLAN for a claim made in order to write the SDD. Keep the existing exceptions for work tracking records and for the Epic management document itself.
3. Before editing product code, check the Issue's required body, the match between Priority/grade and labels, the allowed/forbidden edit paths, the acceptance criteria and the current implementation dependencies, and satisfy the implementation start conditions in `W/process/sdd/entry.md` and the `parallel-development` claim. If any one is missing, do not edit product code.
4. At the start and pre-change points that each source defines, leave the start record of `observations.md` and, if enabled, the START of `token-diagnostic.md`. A resume or handoff refers to the existing start record; a new task does not inherit observations from an earlier task.
5. When entering the current phase and role, check the relevant qualification path in `execution-routing.md`, even when using a model that is already running or that a human chose (current/manual) as is. Do not skip the common prohibition (canonical DENY), the actual explicit records and the current capability floor check, whether or not the model changes. Reuse evidence that is still valid for the same role in the same run, and do not require a model PASS for a future phase not yet entered as a start condition now.

## Investigation, design and progress by grade

For upstream and related analysis, check the baseline revision, scope, premises and evidence according to `Reusing existing analysis` in `W/process/sdd/entry.md`, and supplement only the parts that are missing or have changed. Reuse does not exempt the grade's review. Put a common change, including the application, compatibility and transition impact on the work that uses it, into the scope and verification of the owning Issue.

1. Treat the code observed at the declared baseline revision as AS-IS, and what the current Issue requests as TO-BE. Compare only the directly related business documents, and do not revert code to an older behavior because it differs from a document. If a reference implementation, external behavior or operational consumer affects the judgment, apply `Investigation needed for judgment` in `W/process/sdd/as-is.md`.
2. If the Issue conflicts with the architecture or acceptance criteria, judge with `agent-instruction-policy.md`; if that does not resolve it, stop with `BLOCKED: instruction conflict`.
3. Before the first write of a repository file, secure the lane and claim, then write the current artifacts in the order below. The first layout follows `W/process/sdd-artifacts.md`, and writing the current artifact follows the direct path in the table above. Do not explore broadly to create options.

| grade | Execution order |
| --- | --- |
| Trivial | Check the conditions and investigate only the target text and metadata and the direct verification evidence. Do not add a separate SDD or a product AS-IS investigation. If the conditions are exceeded, re-decide it as at least Small before editing. |
| Small | Use the Issue as the plan and proceed without a separate SDD. |
| Medium | Write the needed SDD and verification plan, and implement without additional approval if there is no conflict. The SDD layout follows P's `sdd.medium_artifacts` value. |
| Large | Proceed in this order: write AS-IS → a valid design review for that phase → write PLAN → a valid design review for that phase → implement. |

For Large, the publication and review mode (P's `review.large_mode`), A/B, finding levels, blind isolation, reconfirmation and repeated stalls are decided in one place: `design-review.md`. At each phase, check the evidence of the current review target and `Open questions and phase dependencies` in `W/process/sdd/issue.md`, and proceed only with the work whose needed conclusion is available. Do not substitute a past PASS for missing or stale evidence. Before a re-review, first apply the "review target keep conditions" of the same source, and do not add this procedure to Medium or below or to the default CODE review.

Before editing product files, connect the baseline requirements and acceptance criteria to verification according to `verification.md`, and secure the grade's `Independent Review` verdict. For Medium and above, the Human Decision Contract follows `W/process/sdd/to-be.md`, and the implementation specification follows `W/process/sdd/agent-spec.md`. An acceptance criterion that cannot be proven, or required verification outside the allowed boundary, is `BLOCKED`. Do not make the optional Device QA/Runtime QA a gate for implementation, PR or merge.

For human judgment, directly check `Human judgment points` in P's application declaration. For a new important product or design decision or a change to the settled scope, stop the affected work with `[HUMAN DECISION REQUIRED]`, reflect the decision the human stated in the Human View and the needed Issue body, then resume. Do not presume a human decision from the existence of a file, agreement between Agents, or a review PASS. Keep handling execution details within the settled meaning and invariants.

## Implement

If you find a PLAN premise error during implementation or verification, or the policy of work in progress changes, apply `W/process/sdd/plan-change.md`. Do not leave only an explanation in the SUMMARY while continuing to use a wrong PLAN as the execution baseline.

1. When keeping the implementation role you already hold, or when delegating or switching models, check the qualification evidence for the current role with `execution-routing.md`. Reuse valid evidence secured in the same run. For an unsupported substitute model, required reviewer separation, or an unavailable Review B model chosen by a human, follow that source's conditions and states as they are.
2. If you received the handoff through a Packet, perform `Context and freshness check at implementation entry` in `execution-packets.md` before the first edit. Do not implement without a VALID result that proves the required inputs, guard, claim and direct sources.
3. Edit only product files that are in the allowed edit paths and not in the forbidden edit paths. Do not add features, refactoring, renames, formatting or dependencies outside the acceptance criteria. Do not edit the W and M pinned copies; report the problem as a common issue.
4. If a shared or root path that only integration work edits becomes necessary, do not edit it directly; turn it into an integration dependency according to `module-boundaries.md`. For documents with a defined lifetime, change only the scope their source allows.
5. Apply the test lifetime and executor in P's `build.md`, and prepare a direct regression test or the declared equivalent verification inside the allowed paths. Keep and re-query a temporary test, then delete it. A project that keeps no tests (none) secures alternative evidence. Following the implementation loop in `verification.md`, identify the owning module of the changed files and run the directly related test class or owning-module tests as the first verification. Do not search the whole repository or widen verification without concrete dependencies, direct impact or actual failure evidence.
6. A required UI Visual Spec uses the permanent link pinned in the Issue. If the execution meaning must change for a Trivial, re-decide it as at least Small.
7. Preserve the PLAN's Implementation findings with the handoff and Result rules of `execution-packets.md`, and secure evidence that the code and fixtures/tests at the current head resolved them. Do not raise a Non-blocking observation into a new implementation gate.
8. When you find and resolve an actual problem, record it with `observations.md`, and hand off the original problem, action and result with source references. Do not create incident records or additional SDD or approval gates in normal phases.

When moving from PLAN into the implementation context, apply `Context and freshness check at implementation entry` in `execution-packets.md`. Leave the actual switch evidence, the minimum inputs and the substitution limits, and do not record an unsupported separation or a failed compression as a success. Do not go back and reset an IMPLEMENT lane in progress.

## Verify and handoff

1. When using declared impact analysis results, check their freshness and completeness with `Common impact result reference and local consumption` in `execution-packets.md`. Do not reduce the Issue's or grade's required verification with stale results.
2. Apply the current grade, change scope, verification order and PASS validity of `verification.md`. Fix failures starting with targeted verification, and finish the needed broad verification on the stable final candidate.
3. Before build and test commands, apply `build-preflight.md` and `Verification environment` in `verification.md`, and reuse the environment verified in the same run. Check the actual build JVM, the allowed corrections and the rerun results. Do not record as PASS anything that was blocked by the environment or not run.
4. Do not record a failure or non-run of required verification as PASS. Do not turn build verification that the grade does not need, or the absence of an optional device report, into a new blocker. If an edit or verification would need a forbidden edit path, stop.
5. Compare the diff and all changed paths against the Issue boundaries and acceptance criteria. If a Packet was used, check the validity of the current head, the file list (inventory), the verification evidence and every PLAN handoff item through the Result validation of `execution-packets.md`. If anything is missing, unresolved or stale, do not hand it off as complete.
6. Pass to `finishing-issues` the checked Issue, boundaries, verification and required review evidence, and a brief Result. Do not regather common documents or worker logs from the beginning. Preserve the observation start record, current result, gaps and next actions in the handoff format of `observations.md`.

When stopping or resuming because of external factors, apply the BLOCKED/RESUME conditions of `token-diagnostic.md` and the handoff of `observations.md`. Do not automatically recheck the same unresolved blocker or repeat the record.

## Output

- Issue / grade / current phase and gate / claim and isolation
- Actual changed paths / acceptance criteria / verification and required review results and what is unverified
- Human judgment, scope departures, BLOCKED and resume conditions
- Qualification and valid results of the execution routing and Packets used, and references to the needed pinned evidence
- Observation start, incident and handoff references, and, if enabled, token records or the reason they were not collected
