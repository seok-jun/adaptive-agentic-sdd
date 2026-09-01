# Information-specific Source of Truth

Adaptive Agentic SDD does **not** use one global Source of Truth for every kind of information.

Different questions have different authoritative sources.

| Information | Typical authoritative source |
| --- | --- |
| Current user instruction | Current user/session request |
| Goal / scope / acceptance criteria | Current issue body |
| Global agent guardrails | Repository agent policy |
| Workflow / gates | Canonical workflow/process definitions |
| Module ownership / dependency rules | Architecture boundary document |
| Current behavior (AS-IS) | Current mainline code |
| Durable product rules after implementation | Product/business documentation synchronized to final code |
| UI layout/state | Issue-linked visual specification |
| Historical rationale | Decision records / ADRs |
| Temporary implementation plan | SDD working documents |

## Why not one SSOT?

A single universal authority creates contradictions in legacy and evolving systems.

For example:

- the **issue** describes what should change,
- the **code** describes what currently happens,
- the **architecture policy** describes what boundaries may not be crossed,
- the **visual spec** describes UI state/layout.

These are not competing sources when their information domains are explicit.

## Conflict handling

When two sources conflict within the **same information category**, stop and resolve the conflict before implementation if it affects scope, architecture, or acceptance criteria.
