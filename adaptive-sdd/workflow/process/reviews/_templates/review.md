# <proposal title> review — <reviewer name>

- Target: `proposal.md`
- Reviewer: <agent or human name>
- Date written: <YYYY-MM-DD>
- Conclusion: <Approve|Conditional approve|Oppose>

## Basis for the conclusion

Apply [Visual writing of human-facing documents](../../agent-instruction-policy.md#visual-writing-of-human-facing-documents) in the same review. Check that the key change and choice can be found, that the needed relationships are visible, and that the conditions, failures and open items in figures and tables match the body text. When the impact or resolution of a finding needs a comparison or relationship explanation, show it with the finding; write a simple finding as a short sentence. Do not require a number of figures or a new approval/reviewer round.

State the conclusion in 1–3 sentences. For a conditional approval, number the conditions that must be met before implementation.

For the human-facing explanation, check that answers about changes, responsibilities and failure/open questions can be found in the body text. If a table or figure answers differently from the body text, state the broken condition and its impact in the findings below. Distinguish the meaning of static relationship lines from the actual execution order, and do not turn an uninvestigated item into normal behavior or a settled choice. Only when needed, consult the [mismatch example](../../visual-writing-examples.md#review-check); do not create a separate review table or judge by the number of figures.

## Findings

| Severity | Status | Evidence | Impact | Required change |
| --- | --- | --- | --- | --- |
| Critical/Major/Suggestion | Confirmed/Assumed | `<path>:<line>` or rule ID | Failure, cost, security or quality impact | Item to change in the proposal |

Mark an opinion written without evidence as `Status=Assumed`.

## Checked by running

| Command/verification | Result |
| --- | --- |
| `<command>` | Success/failure + key result |

Do not put a verification that was not run in this table.

## Not checked

- <item not verified>: <reason>

## Conditions for conditional approval

Write only when the conclusion is a conditional approval.

1. <A verifiable condition that must change in the proposal, code or documents>

## Alternatives

Write only when the conclusion is opposition or the current proposal must change. State concretely the behavior that changes and the trade-offs.
