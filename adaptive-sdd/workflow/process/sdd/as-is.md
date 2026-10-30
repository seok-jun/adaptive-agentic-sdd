# SDD as-is

The human-facing status is the existing `README.md`; `01-as-is.md`, written under the rules in this file, is the detailed evidence. Check [Artifact structure](../sdd-artifacts.md) only for the initial layout.

### `01-as-is.md`

`README.md` is the source for the problem, cause model, current relationships and risks that a human judges. This file owns the direct evidence for that judgment.

Make the current conclusions, unconfirmed items and remaining risks understandable from the current artifacts. Link discarded hypotheses and the history of past investigation to the relevant section of the existing immutable evidence, and consume them during re-investigation or audit. Do not present them in parallel with the same authority as the current contract. When you correct something, check whether contradictions with the earlier conclusion remain in the applicable statements of the README, TO-BE and change-plan as well, and follow [Plan correction](plan-change.md). Do not retroactively edit past product artifacts or Issues only because of this layout change.

- Agent evidence that distinguishes current behavior from facts that could not be confirmed
- The code paths and symbols checked
- Reproduction or verification evidence
- Drift items if documents and code differ

Set the writing order as facts/hypotheses/uninvestigated items → direct evidence. Refer to W's [AS-IS synthetic example](../visual-writing-examples.md#sdd-as-is) only when concrete wording is needed. Do not use the example's fictional facts as actual product evidence.

#### Investigation needed for judgment

Apply the investigation below only to items that determine a human's choice or the premise of the next work. Reuse valid evidence from the parent analysis; do not require an exhaustive history investigation or a separate analysis document.

| Judgment situation | Evidence to check |
| --- | --- |
| Migrating or integrating based on an existing implementation | The mapping between names and actual identifiers, active entry points, the checked revision and recent operational evidence. Distinguish being active in code from actual operational use |
| Implementation differences or reasons for deactivation affect the choice | Related introduction/change history and tickets, and whether evidence of intent exists. Do not settle intent from the author or time alone |
| Depends on the behavior of an external library or framework | The source, distribution/bytecode or official documentation of the actual dependency version, or a permitted minimal run. Do not use descriptions of another version as evidence for applying it |
| Changing data, logs, endpoints or the transition method | Directly connected external callers, operational consumers and observation methods, and the source and check time of that information. Do not assume there are no consumers because none appear in the code |

Before asking a human to choose, first confirm the facts that can be confirmed within scope. For the remaining uncertainty, write down the evidence checked, access failures, the need to run something or for external confirmation, together with the phase that needs that conclusion. Do not repeat exploration endlessly or make operational queries outside your permissions; ask a human only for the external facts needed. For risks, write the conditions under which they occur and the scope actually observed, and do not estimate frequency without evidence. Operational content is managed in P's existing documents/work records and is not put into the common copy.

A fact that contradicts a required premise, such as evidence that the implementation designated as the baseline is inactive, is reported not as an ordinary difference but as a **premise conflict**. Changing a settled decision follows the human-judgment rules, and only the design and implementation that depend on that premise stop. Do not halt unrelated investigation along with it. In questions to a human, also present the mapping between the identifiers the human uses and the code names.
