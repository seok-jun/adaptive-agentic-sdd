# <proposal title> decision

- Status: <Decided|On hold|Rejected>
- Decided by: <name>
- Decision date: <YYYY-MM-DD>
- Related Issue: <#number or none>
- Reviews consulted: <list of review files>

## Adopted option

Following [Visual writing of human-facing documents](../../agent-instruction-policy.md#visual-writing-of-human-facing-documents), show the behavior and responsibilities that change with the adoption before the detailed evidence. Any before/after comparison or relationship figure/table that is needed also shows the boundaries, exceptions and open items that remain. A simple decision needs only one sentence; no new figure or approval step is needed.

- Option: <A/B/...>
- Final behavior/structure:
- Scope:
- Effective from:

Do not use expressions such as `in a better way` or `as the situation requires`; write behavior that can be checked after implementation.

## Reasons for adoption

State which review findings were adopted and the evidence.

| Finding | Adopted | Evidence |
| --- | --- | --- |
| | Adopted/Not adopted | |

## Options not adopted

| Option | Reason for exclusion |
| --- | --- |
| | |

## Current rules that change

- business rule: <ID + change, or none>
- public contract: <symbol + change, or none>
- architecture: <change or none>
- cost/quota: <change or none>
- security/privacy: <change or none>

## Follow-up work

- [ ] Create/update the implementation Issue
- [ ] Update the necessary business documents
- [ ] Update the necessary contract/architecture documents
- [ ] Reflect the verification criteria in the Issue's acceptance criteria

Do not use the decision record itself as the Source of Truth for current product behavior. After implementation, the `main` code and `docs/domains/**` must describe the final behavior.
