# Concepts

## Issue as execution specification

The issue owns the requested **TO-BE**:

- user impact,
- goal,
- scope,
- allowed/forbidden boundaries,
- acceptance criteria,
- dependencies and blockers.

The issue should not attempt to fully encode the current implementation. That belongs to AS-IS analysis.

## AS-IS vs TO-BE

A useful separation is:

```text
current mainline code = observed AS-IS
current issue         = requested TO-BE
```

A difference between them is expected during feature development.

Do not “fix” code merely because an old document disagrees with the current implementation.

## Bounded reasoning

The agent should expand context only when a concrete dependency, compile failure, acceptance criterion, or conflict requires it.

The purpose is not to minimize thinking at all costs. It is to avoid unbounded discovery on routine work.

## Evidence

Completion should be backed by evidence appropriate to the change:

- unit tests,
- integration tests,
- lint/static analysis,
- build/package verification,
- CI,
- code review,
- device/runtime QA.

“Not run” is not equivalent to “passed.”
