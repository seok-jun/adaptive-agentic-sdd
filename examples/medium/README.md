# Medium Example

**Change:** Add a new shared request field used by two implementation modules.

Process:

1. Issue defines boundary and contract intent.
2. AS-IS identifies current contract and direct consumers.
3. TO-BE defines the new field and backward-compatible behavior.
4. Verification strategy maps contract behavior to unit/integration tests.
5. Change plan names concrete files/symbols.
6. Implementation modifies only approved boundaries.
7. Bounded review checks contract compatibility and diff scope.
8. PR merges after required tests/review.

Repository-wide rediscovery is not required unless a concrete compile/dependency failure expands the impact surface.
