# SDD issue

## Issue body contract

For the required sections and canonical body format of a new implementation/bug Issue, `## Required body of a new Issue` in the pinned W's `process/issue-priority.md` is the Source of Truth. Read `W/../project/issue-priority.md` for the product-specific application conditions. This document does not duplicate the same template.

The body values and the `priority:*` and `grade:*` labels must always match.

Issue comments may record `[CLAIM]`, `[RELEASE]` and change history, but **the current goal, scope, boundaries and acceptance criteria are not changed by comments alone.** Once a change is settled, update the body with the same content as well.

General comments on an execution Issue are Agent ↔ Agent work communication. They share AS-IS evidence, review counterarguments, path/symbol, implementation findings, test/verification and handoff, and do not require constant confirmation by a Human. Agreement between Agents is not a Human Decision and cannot implicitly add to or change a settled Decision.

- `[HUMAN DECISION REQUIRED]`: Use only when a new, important product/design Decision outside the work instruction or the settled design scope is needed. STOP the affected work, reflect that Decision, the actual alternatives and trade-offs in the Human View (`02-to-be.md` for Medium and above, the Issue for Trivial/Small), and resume after the Human decides. If the Issue's goal, scope, boundaries or acceptance criteria also change, update the body as well.
- `[IMPLEMENTATION SUMMARY]`: At the end of implementation, record briefly in one comment only whether the settled Decisions were followed, execution deviations, whether a Human escalation occurred, verification results and remaining risks. It is not an additional Human approval gate.

Every change category in [General automatic escalation](grade.md#general-automatic-escalation) and in `### Automatic escalation` of the P project documents must be exposed in the Human Decision. This includes cases where the product behavior meaning, acceptance interpretation or an upstream contract changes, or where a reasonable competing alternative with a different meaning is found. **The obligation to expose a Decision is separate from whether an additional Human decision is needed.** Medium states decisions within the Issue's goal, scope and boundaries in the SDD and proceeds according to the existing gates; it does not require `[HUMAN DECISION REQUIRED]` merely because a category must be exposed. Escalation applies to new, important decisions outside the work instruction or settled design scope described above. Do not ask again for a decision on matters the Issue/design has already decided. Implementation details that do not change the settled product meaning or invariants continue at the Agent's discretion.

Only the roles of the two comments above and of general communication are distinguished. The existing claim/release/token markers and the gates by grade are kept, and no additional comment taxonomy such as `[EVIDENCE]`, `[REVIEW]` or `[RESOLVED]`, new document or approval step is created. Content from existing documents is carried over to reduce required Human reading and duplication, and the volume of work communication between Agents is not artificially limited. Medium's SDD progress without additional approval and Trivial/Small's omission of a separate SDD are also kept.

## Legacy Issue normalization

The following is normalization of execution Issues. Existing Epic management documents follow [Transition of existing Epics](epic.md#transition-of-existing-epics), and the absence of an execution grade or code path does not block coordination or child investigation. If an existing execution Issue lacks even one of the items below, normalize the Issue before editing code.

- The Priority body value and the `priority:*` label
- The SDD grade body value and the `grade:*` label
- User impact
- Goal
- Work scope
- The `Allowed edits` / `Forbidden edits` entries of the work boundaries
- Acceptance criteria
- Dependencies / blockers

Do not edit product code during the normalization step. Write minimal boundaries based on the existing Issue's goal and the current architecture documents, and if a shared path is needed, mark it as integration work.

## Open questions and phase dependencies

A review PASS is the review result for that target; it is not completion of every decision or permission to start all of the next work. Whoever found it, the author, the investigation or a reviewer, link to the existing Issue/SDD for each open question **what must be confirmed or decided, who owns it, and the work or phase that needs the conclusion**. Do not create a new status label, a separate ledger or a gate on the number of questions.

If the work you are about to enter consumes a conclusion, that part waits; investigation and work unrelated to the conclusion may proceed. For example, a decision needed only at deployment time does not block starting an independent investigation, but a question that requires choosing behavior in the PLAN cannot be deferred until deployment. Do not treat an open question as resolved merely because it was exposed, and do not ignore it because it is not among the reviewer findings. The existing review by grade and the human-judgment requirements are kept.

A question common to several Issues is asked once by the Epic owner or the existing coordination owner, who links the source and affected Issues. There is no need to create a new Epic for this. After the decision, the owner updates the open-question marks in the related Issues/SDD or replaces them with a reference to the settled decision, and passes it on to the active owners. Past open-question records are kept as history, but current instructions must not be left differing from each other. If the meaning changes, apply [Plan correction and policy transition](plan-change.md#plan-correction-and-policy-transition).
