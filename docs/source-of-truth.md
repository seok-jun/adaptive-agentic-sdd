# Information-specific Source of Truth

There is no global Source of Truth for every information category.

| Information | Typical authoritative source |
| --- | --- |
| Current user instruction / authorized action | Current explicit user/session request, within applicable guards |
| Goal / scope / ACs | Current work item or trustworthy revisioned snapshot |
| Global agent guardrails | Repository root agent policy |
| Lifecycle / gates | Canonical workflow and review/verification definitions |
| Grade semantics / depth | Risk-grade matrix, or the explicitly adopted local contract |
| Module ownership / dependency rules | Architecture boundary document |
| Current behavior (AS-IS) | Current mainline code and direct runtime evidence |
| Durable product rules | Product/business docs synchronized to final behavior |
| UI layout/state | Work-item-linked visual specification |
| Historical rationale | Decision records / ADRs |
| Temporary implementation plan | Current SDD working document |
| Verification result | AC-linked execution/observation record for the actual revision/environment |
| Review result | Review record for the target phase/revision |
| Human approval / integration authority | Explicit approval or applicable delegation record for target revision and action scope |

The work item states what should change; code shows current implementation; architecture defines allowed boundaries; a review records a verdict for one candidate. These sources answer different questions.

## Conflict handling

Resolve same-category conflicts before implementation when they affect scope, architecture, ACs, approval, or durable contract meaning. Code is evidence of current behavior, not permission to overwrite a requirement. A user request does not silently repeal a guardrail.

Do not use stale copied tickets, historical comments, old plans, or old review verdicts to override a current authority. Identify a snapshot's revision boundary when live access is unavailable.

## Explain once, reference elsewhere

The developer guide, diagrams, and examples explain canonical policy; they do not redefine it. Root instructions route to Skills; avoid multiple independently maintained definitions of one gate.

The starter local contract is a deliberately self-contained adoption snapshot. After adoption, the repository owns its local policy and must reconcile any upgrades explicitly; it does not automatically inherit future public-repository changes.
