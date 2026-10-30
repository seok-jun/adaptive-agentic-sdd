# SDD agent-spec

When they apply, use [TO-BE's trade-off](to-be.md#bounded-trade-off-capture) for product and design judgments on actual competing alternatives, and [Plan correction](plan-change.md) for premise errors.

### `change-plans/{ID}.md`

This is the Agent Execution Spec. It does not restate the rationale of a Human Decision; it references the `D-xxx` it applies. It does not create design authority that competes with `02-to-be.md`.

Link the existing Decision and AC IDs/items of the TO-BE together with the base revision, and write only the application locations, execution/verification details, additional fixture expectations and differences. Do not duplicate decision explanations or the whole verification table. Conditions unique to the execution specification are not duplication and are kept. When deleting or condensing a list, compare the conditions in the deleted part with their replacement location to confirm nothing is missing. Do not judge preservation only from the identity of the kept part, and do not move all test details into the TO-BE.

Link the README's problems, premises, invariants and remaining risks that apply to design, implementation and handoff directly by the needed section and base revision. Have the relevant role consume the contracts needed for the current execution, and distinguish the detailed history for cause re-investigation or audit so that it is read only when it applies. The review inputs by role and Blind Audit isolation are not changed.

- Target file/symbol, direct caller/callee and the necessary code evidence
- Change content, implementation order, invariants to preserve, and the applicable schema/migration
- Test cases, verification commands and execution evidence
- Checkpoints for rollback or failure

Link the document, section and revision, or the check time, of the P conventions to be applied, and if the instructed structure differs from that baseline, write the reason and the evidence for the needed exception decision. Do not treat a choice of one of several previously allowed styles as a violation because of a later preference alone. Do not make a new style into a common rule, and do not force a separate convention document or approval step because no baseline is declared. Expose unconfirmed baselines in the handoff, and resolve only actual instruction conflicts under the existing authority rules.

Do not write sentences in a change plan that do not identify the exact target, such as `related files`, `the necessary parts` or `appropriate handling`.
