---
name: managing-issues
description: Use when creating, classifying, reprioritizing or rewriting the body of this project's work items (Issues), and when coordinating the work breakdown and dependencies of an optional Epic. Use for deciding Priority/execution grade, work boundaries, whether a Mermaid flow is needed, and linking a UI/UX HTML Visual Spec. Do not use for code implementation.
---

The execution inputs are the absolute paths `P` (top level of the project repository), `W` (the pinned procedure copy `W`) and `M` (the pinned common principles `M`). Do not guess P or M from the current folder or from W's parent folder. Apply P's hard guard (`## Always-applied hard guard` in `P/AGENTS.md`) and its application declaration (`W/../project/sdd-workflow.md`). Read the words Issue, comment, label and PR as the matching feature of the work tracking method (`W/tracker/`) declared in `W/../project/tracker.md`. Look up unfamiliar terms in the [Glossary](../../glossary.md).

# Managing Issues

## Inputs

If you can confirm that `## Always-applied hard guard` in `P/AGENTS.md` was already applied in the same run, do not read it again. If you cannot confirm this because you started as a standalone run or as a sub-agent, read that section first and then proceed.

Read first:

1. The current user request
2. `## Priority decision order` and `## When evidence is insufficient` in `W/process/issue-priority.md`, and the current stage and product application in `W/../project/issue-priority.md`. When creating an Issue, W's `## Required body of a new Issue` and `## Required labels`; when reprioritizing, W's `## Priority change`
3. `W/process/sdd/grade.md` and the product-specific `### Automatic escalation` in `W/../project/sdd-workflow.md`. For Issue changes, human judgment and open dependencies, `W/process/sdd/issue.md` (the normalization rules are also here)
4. `## Evidence recording rules`, `## Mermaid creation conditions` and `## HTML Visual Spec creation conditions` in `W/process/issue-writing-guide.md`, and `## Evidence recording rules` (personal information and allowed evidence) in `W/../project/issue-writing-guide.md`. Check the product's storage location and dependency limits only when HTML is needed.
5. When changing an existing Issue, that Issue's current body, labels, assignee, comments and linked PR

In an execution tool that cannot read by heading (section), you may read the files above whole. If you can read by section, do not read all three files whole in advance "to understand the project in general".

Read only when needed:

- Only when you need to judge ownership or integration of product, shared or root paths: the common boundary and lifecycle contract in `W/process/module-boundaries.md` and the actual product boundaries in `W/../project/module-boundaries.md`.
- Only when an instruction conflict, a mismatch between code and business documents, or an ambiguous scope actually arises: `W/process/agent-instruction-policy.md` (common contract and procedure) and `W/../project/agent-instruction-policy.md` (product application, permissions and verification).
- Reuse inputs already checked in the same run that have not changed.

Do not search product code broadly unless it is needed to classify the Issue.

## Conversation-content gate

Always check before and after writing a record to the work tracking method.

- Do not quote or translate a conversation log, whole or in part, and do not record a summary from which the original text can be reconstructed. The minimal record of requirements and settled decisions that a human gave for the work follows `Evidence recording rules` in W `issue-writing-guide.md`.
- Distinguish requirement sources and settled decisions from investigation requests and proposals. Use as evidence the allowed work content, IDs, metadata, measurements, and category names from which the original cannot be reconstructed. Do not carry over content the project forbids, even under the name of a requirement.
- The detailed allow list follows `Evidence recording rules` in `issue-writing-guide.md`.
- If evidence cannot be made without forbidden content, `BLOCKED`.
- After writing, check the record again.
- If forbidden content was already written, follow the removal method that P's evidence recording rules and the work tracking method allow. If it cannot be removed, tell a human, and do not wipe out other records wholesale.

## Create a new Issue

1. Decide whether to manage the request as one execution Issue or to split it into several Issues that are each assigned and tracked. Do not split only because it is a new package or large in size. Apply `Epic coordination` below only when several Issues are managed together.
2. Set the Priority from W's common Priority rules and P's current stage and feature facts.
3. Set the SDD grade from W's common grades and general automatic escalation and P's product mapping.
4. Check the actual repository paths and write the allowed and forbidden edit paths. Read `module-boundaries.md` only when you need to judge product, shared or root boundaries.
5. Use the new Issue body sections defined in `W/process/issue-priority.md`.
6. Check that each acceptance criterion is a condition whose success or failure automated tests, CI and the grade's reviews can decide. Do not force a separate Verification Strategy section on every Issue.
7. Attach exactly one `priority:*` label and exactly one `grade:*` label that match the body.
8. When writing or fixing the human-facing description of an Issue, apply [Visual writing of human-facing documents](../../process/agent-instruction-policy.md#visual-writing-of-human-facing-documents). Show the key change first, and explain policy comparisons or ownership and responsibility boundaries with the form of expression they need. A simple change needs only one sentence. In the same step, decide the Mermaid and HTML Visual Spec conditions of `issue-writing-guide.md`, and do not widen the conditions for creating and storing HTML. Reuse criteria that have not changed in the same run.
9. If HTML is needed, apply `HTML minimum content`, `Visual Spec link rules` and `Design PR merge, deployment and cleanup` in W `issue-writing-guide.md` according to the storage and publication method declared in `Visual Spec` of P's application document `issue-writing-guide.md`. If there is no declaration, do not create an HTML Visual Spec. Do not treat a design merge as app approval or completion. If publication or cleanup fails, record the last step that succeeded and the remaining state.
10. Read the finished Issue again and verify its body sections, labels, Visual Spec (when applicable) and the conversation-content check (the gate above).

## Epic coordination

Apply `W/process/sdd/epic.md`. An Epic is not an execution grade. Creating or splitting one requires no independent review, remote publication or A/B pass. Do not apply the grade, paths and implementation verification items used when creating an execution Issue to the management document as is; follow the Epic body and label distinction in `issue-priority.md`.

- Connect the overall goal, acceptance criteria, common guidance and references to child Issues; responsibilities and ordering; the investigation owner of each open question and the later phase that needs its conclusion; and the evidence and owner of overall completion. A separate breakdown file is not required.
- Check by yourself for missing goals, gaps in responsibility, contradictory dependencies and open questions without an owner. An open question by itself does not block the start of a child Issue's investigation. Put a dependency only on the implementation, integration or deployment phase that uses its conclusion.
- Gathering common questions and updating the child open-question markers after a decision follow `Open questions and phase dependencies` in `W/process/sdd/issue.md`. If the name of a requirement that designates a reference implementation and the operational evidence disagree, check it with `Investigation needed for judgment` in `W/process/sdd/as-is.md`, and make only the work that relies on that premise wait.
- Put a common change, together with the work that uses it and its transition impact, into the scope and acceptance criteria of the execution Issue that owns it, and set that Issue's grade. Do not leave a common design only in the management document with the verification responsibility left empty.
- Depending on the investigation results, you may split or merge work and change responsibilities and order within the delegated scope. Adjust the boundary of a lane in progress only after telling its owner about the change and its impact and resolving claim conflicts. Reducing the goal or acceptance criteria, or changing an existing human decision, follows the existing human-judgment rules.
- Close the Epic after confirming the evidence that the overall goal was achieved. Do not force the product-change closing procedure on a management document that has no implementation PR, CI or SDD.

## Triage / reprioritize

For an Epic management document, update responsibilities, dependencies and the evidence of overall completion through `Epic coordination` above, and do not attach an execution grade. The steps below apply to an execution Issue.

1. Read only the current Issue and the minimum evidence that is strictly needed.
2. Decide the Priority again under the current rules.
3. Decide the grade again only if the scope or risk changed.
4. If you change a value, align the body and the labels in the same task.
5. If the scope changed, also decide the boundaries, Mermaid, Visual Spec, dependencies and acceptance criteria again.
6. Check that the changed acceptance criteria can be decided by automated tests, CI and the grade's reviews.
7. Read the finished Issue again.

## Stop conditions

Stop as `BLOCKED` and do not implement if:

- A needed path cannot be checked
- An instruction conflict cannot be resolved even with `agent-instruction-policy.md`
- A required Visual Spec or pinned link cannot be created
- The Priority cannot be set even after applying the documents' defaults
- The work would have to intrude on the scope of another lane in progress
- Evidence that passes the conversation-content check (the gate above) cannot be made

## Output

Briefly report the Issue number and title, Priority, grade and labels, allowed and forbidden edit paths, Mermaid and Visual Spec, the conversation-content check result, and dependencies and BLOCKED. For an Epic management document, report the work type, child responsibilities, dependencies and the evidence of overall completion instead of a grade.
