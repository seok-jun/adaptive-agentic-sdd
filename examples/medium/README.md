# Medium Example

**Fictional change:** add a shared request field used by two implementation modules, with backward-compatible behavior and without Large-level failure cost.

1. Define boundaries, contract intent, ACs, and fixed decisions in the work item.
2. Record AS-IS: current contract and direct consumers.
3. Define TO-BE, preserved compatibility, and the change plan's files/symbols.
4. Map ACs to expected unit/integration evidence before implementation.
5. Use bounded independent design/contract review for the shared-contract risk.
6. Implement only authorized boundaries; collect targeted/final AC-linked results.
7. Obtain independent CODE review of compatibility, evidence, and diff scope.
8. Present the final candidate for explicit Human integration authorization.
9. Merge only after required evidence/review and that authorization are satisfied.

Separate sections are sufficient; repository-wide rediscovery is not required unless a concrete dependency, contract conflict, or failure expands the impact surface. Regrade if analysis reveals Large-level risk. This is a walkthrough, not evidence that checks or approvals occurred.
