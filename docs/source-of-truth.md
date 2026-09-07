# Information-specific Source of Truth

Adaptive Agentic SDD does **not** use one global Source of Truth for every kind of information.

Different questions have different authoritative sources.

| Information | Typical authoritative source |
| --- | --- |
| Current user instruction | Current user/session request |
| Goal / scope / acceptance criteria | Current work item (GitHub Issue, Jira, Linear, etc.) |
| Global agent guardrails | Repository root agent policy |
| Workflow / gates | Canonical workflow/process/Skill definitions |
| Module ownership / dependency rules | Architecture boundary document |
| Current behavior (AS-IS) | Current mainline code and direct runtime evidence |
| Durable product rules after implementation | Product/business documentation synchronized to final code |
| UI layout/state | Work-item-linked visual specification |
| Historical rationale | Decision records / ADRs |
| Temporary implementation plan | SDD working documents |
| Review result | Review record bound to the reviewed revision when available |
| Human approval | Approval record bound to phase + artifact revision + decision scope |

## Why not one SSOT?

A single universal authority creates contradictions in legacy and evolving systems.

For example:

- the **work item** describes what should change,
- the **code** describes what currently happens,
- the **architecture policy** describes what boundaries may not be crossed,
- the **visual spec** describes UI state/layout,
- a **review record** describes the verdict for one reviewed candidate.

These are not competing sources when their information domains are explicit.

## Conflict handling

When two sources conflict within the **same information category**, stop and resolve the conflict before implementation if it affects scope, architecture, acceptance criteria, approval, or durable contract meaning.

Do not use historical comments, stale copied tickets, old planning artifacts, or review verdicts for an older revision to silently override a current authoritative source.
