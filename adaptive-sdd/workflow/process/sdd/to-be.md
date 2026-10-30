# SDD to-be

### `02-to-be.md`

This is the Human Decision Contract. It provides the basis for product and design decisions within the Issue's goal and boundaries and the upstream contract. It does not independently change that goal, those boundaries, or that upstream contract.

It keeps the source of product Decisions, ACs and their verification mapping. The change-plan references the existing IDs/items and owns the application locations, verification details and its own fixture conditions. Do not rewrite the same table or gather even its own execution expectations into this document.

- The current problem and the AS-IS → TO-BE behavior change. Put first the forms of expression needed for understanding: a comparison table for policies and options, a relationship diagram/boundary table for ownership and boundaries, a diagram/state table for flows and states, and so on. One sentence is allowed for a simple change
- Behavior that will not change, behavior on failure/error, and explicit data/state definitions
- For each Decision: `D-xxx`, the choice, the reason for the choice, the actual alternatives and trade-offs, the main costs/risks, and what adopting it means
- The Verification Strategy for each Acceptance Criterion. Execution details reference the relevant change-plan.

Do not settle as a design fact an external behavior left unconfirmed in the AS-IS. Confirm premises that determine a design decision with the [investigation evidence](as-is.md#investigation-needed-for-judgment), or link the confirmation owner and needed timing according to [Open questions and phase dependencies](issue.md#open-questions-and-phase-dependencies). Leave premises that can only be confirmed by running something in the relevant verification/implementation handoff, and confirm them before the execution that depends on the premise.

Keep class/method/line evidence to a minimum. Do not hide important product or design decisions only in the Agent spec. If the Human-facing Decisions are too many to understand in a short review session, consider splitting the issue/plan, but do not create a fixed count limit or an additional taxonomy.

Set the writing order as change → choice with its reasons and costs → boundaries to keep, failures and open questions → acceptance criteria and how to confirm them. Refer to the [TO-BE synthetic example](../visual-writing-examples.md#sdd-to-be) only when needed. Preloading all of the status and plan examples above, or a new artifact, is not required; link execution details to the relevant section of the existing change-plan.

### Bounded trade-off capture

Only when two or more actual competing options emerge while checking the Issue, the AS-IS at the declared base revision and direct dependencies, record briefly the choice, the alternatives, the reason for the choice and the cost accepted. For Medium and above, important product and design trade-offs go in a Decision in `02-to-be.md`, and the change-plan references its ID. Trivial/Small use the Issue and do not create a separate trade-off document.

Do not do repository-wide exploration or separate brainstorming to find competing options. Record re-review conditions too only when a clear trigger already exists.
