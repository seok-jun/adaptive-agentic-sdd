# SDD artifact layout

Read this when first setting up the folder for Medium or Large. Do not add an SDD for Trivial, Small, or the Epic management document itself. Keep the number of files and their lifetime, and move the human-facing AS-IS explanation to the existing README. Do not rewrite in-progress work.

| Reader and consuming phase | Working file | Writing rules |
| --- | --- | --- |
| Human: AS-IS status and risks | `README.md` | README below |
| Agent/reviewer: AS-IS investigation and evidence | `01-as-is.md` | [AS-IS](sdd/as-is.md) |
| Human: PLAN changes, decisions, ACs and verification summary | `02-to-be.md` | [TO-BE](sdd/to-be.md) |
| Agent/reviewer: implementation, verification, handoff | `change-plans/{ID}.md` | [Agent Spec](sdd/agent-spec.md) |
| On a premise error or policy change | Correct the relevant source | [Plan correction](sdd/plan-change.md) |

[completion](sdd/completion.md#document-roles) is the source for document roles and cleanup timing, and [verification](verification.md) is the source for verification.

## SDD working document structure

Use the following structure for Medium and above. It applies from newly started SDD work and is not applied retroactively to work already in progress or finished. This rule alone does not cause an existing design to be rewritten. For Medium, if P's `sdd.medium_artifacts` is `condensed`, follow [Medium condensed layout](#medium-condensed-layout) below.

```text
docs/sdd/{feature}/
  README.md
  01-as-is.md
  02-to-be.md
  change-plans/{ID}.md
```

Add `backlog/{ID}.md` only when needed. `{feature}` uses kebab-case, and `{ID}` uses an uppercase prefix + number that is not duplicated within the Issue.

The required content of each document is as follows.

Apply [Visual writing of human-facing documents](agent-instruction-policy.md#visual-writing-of-human-facing-documents) to the human-facing status and plan. Show the current state and the changes and choices first, and separate the Agent execution details. Explain a change for which one sentence is enough with that sentence, and do not fill a quota of diagrams. If an example is needed to choose a form of expression, refer only to the [writing examples](visual-writing-examples.md). This link does not change the document structure, approval authority or review rounds, and does not require preloading the whole guide.

### `README.md`

This is the human-facing AS-IS status and the work entry point. Keep the following content concise.

- The Issue source and the base revision/check time. Link Priority, grade and allowed/forbidden paths directly to the corresponding body items. Do not copy the values and manage them separately.
- The needed sections of linked business/architecture documents
- Present briefly first the problem definition, cause model, scope/boundaries, and the key facts and risks that affect the design
- Show first, with a relationship diagram or a small table, the ownership, connections, flows and states needed to understand the status, and distinguish facts, hypotheses and uninvestigated items. One sentence is allowed for a simple change

- Link each fact and risk to its direct evidence in `01-as-is.md`. Do not restate the original evidence.
- When first writing the README, link the PLAN location `02-to-be.md` as the planned path. Whether it has been written and its progress status are checked in the existing Issue; do not rewrite the README under AS-IS review in order to add a link after the PLAN is written. Keep the summary of changes, decisions and acceptance criteria only in the TO-BE. If actual AS-IS facts, risks or premises change, apply the existing [re-review by meaning and impact](design-review.md#design-re-review-by-meaning-and-impact).



## Medium condensed layout

This applies only to newly started Medium SDDs when `sdd.medium_artifacts` in the `Execution profile` of P's `W/../project/sdd-workflow.md` is `condensed`. If the value is absent or `full` (default), use the structure above as is. Large always uses the structure above.

```text
docs/sdd/{feature}/
  README.md   ← ## AS-IS / ## PLAN / ## Implementation specification
```

- Put three sections in one file. Only the number of files is reduced. The required content of each section is unchanged: `## AS-IS` follows [AS-IS](sdd/as-is.md), `## PLAN` follows [TO-BE](sdd/to-be.md), and `## Implementation specification` follows [Agent Spec](sdd/agent-spec.md).
- When another W document points to `01-as-is.md`, `02-to-be.md` or `change-plans/**`, read it as `## AS-IS`, `## PLAN` or `## Implementation specification` of this README. For example, "For Medium and above, map acceptance criteria, verification means and success evidence in `02-to-be.md`" in the [Verification contract](verification.md) means mapping them in `## PLAN`.
- Put the human-facing explanation (status, changes, decisions) at the front of each section, and the Agent evidence and implementation details after it. The README rules above on linking evidence, not copying, and managing information in one place still apply.
- If the work is re-graded to Large during the work, split it into the four-document structure above before the AS-IS review. Do not use a condensed README as a Large review target.
- The cleanup timing and method follow [completion](sdd/completion.md#document-roles) and finishing's SDD cleanup procedure as they are.

## Sources and selective consumption

“Human-facing” is a point of view on presentation, not an exemption from Agent reading. Link directly, by the relevant section and base revision, and consume the README's problems, premises, invariants and remaining risks that apply to design, Medium implementation entry, a separate IMPLEMENT context and the needed reviews. Do not add reading the whole README to every role; reviews follow the existing allowed inputs by role and Blind Audit isolation.

A human reads the judgment content and risks in the Human View of the current phase and opens only the evidence needed directly. An Agent reads the relevant execution specification and the applied Decisions and ACs, and does not repeat the whole rationale. A reviewer reviews both the Human View and the Agent evidence on the same candidate. The separation does not reduce the review scope or Blind Audit isolation.

The same information is managed in one place. The Issue owns the Issue's goal and boundaries, the AS-IS owns current facts and code evidence, the TO-BE owns settled Decisions, ACs and verification mapping, and the change-plan owns implementation order and test details. In references, leave the repository, pinned revision, path/symbol/item or check time. If a reference cannot be checked because of authority or lifetime, mark it unconfirmed and resolve it before consuming the conclusion. Do not treat the existence of a link as verification success.

If a stable reference to an existing Issue, code, test or review result is enough, do not copy its content. Check the validity of earlier analysis with [Reusing existing analysis](sdd/entry.md#reusing-existing-analysis) and supplement only the differences. A separate `evidence.md` is not required and is used only when there is actual evidence that cannot be preserved in an existing source. The completion result summary links the existing SUMMARY and does not create a new report.

Check a contract reference needed for the current execution when that decision is consumed. Read detailed history needed only for cause re-investigation or audit only when it applies. Leave the key conclusions, conditions and remaining risks in the current artifacts, and do not hide them behind past links. Do not preload every linked document because a reference exists. The current progress status is managed in the Issue/work-record source P defines and is not duplicated across several artifacts. A snapshot at the time of review or approval is preserved as the facts of that time and is not merged over the current progress status. Do not claim actual reading-token savings from file moves or reference conversions alone.

Reference formats are in `templates/sdd/`. They are not new required items or an obligation to fill placeholders; write only the existing obligations of the relevant phase.
