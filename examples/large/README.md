# Large Example

**Change:** Add retry-budget enforcement before an external paid operation.

Why Large:

- retry behavior,
- cost exposure,
- failure impact.

Process:

1. AS-IS identifies retry owner and external-call boundary.
2. Design review confirms enforcement can happen before the paid call.
3. TO-BE defines retry ordinal input, accumulated cost input, allow/block decision, and failure behavior.
4. Verification strategy proves just-below limit, at limit, over limit, retry accumulation, and enforcement before the paid operation.
5. Trade-off is recorded only if real competing ownership options exist.
6. Implementation proceeds after design gate.
7. Independent code review checks boundary, ordering, and evidence.
8. Device/runtime QA is required only if real platform behavior cannot be proven by integration tests.
