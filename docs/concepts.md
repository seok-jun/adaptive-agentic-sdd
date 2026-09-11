# Concepts

## Work item as execution specification

The current work item (GitHub Issue, Jira ticket, Linear issue, or equivalent) owns the requested **TO-BE**:

- user/business impact,
- goal,
- scope,
- allowed/forbidden boundaries,
- acceptance criteria,
- dependencies and blockers,
- decisions already fixed by authoritative references.

The work item should not attempt to fully encode the current implementation. That belongs to AS-IS analysis.

## AS-IS vs TO-BE

A useful separation is:

```text
current mainline code = observed AS-IS
current work item     = requested TO-BE
```

A difference between them is expected during feature development.

Do not “fix” code merely because an old document disagrees with the current implementation.

## Progressive disclosure

Agents should begin from a small, stable repository entry contract and load deeper rules only when the current task requires them:

```text
AGENTS.md -> task Skill -> conditional process/domain docs
```

This is a correctness mechanism as well as a token optimization: the entry path stays stable while detailed policy remains owned by the narrowest relevant document.

## Bounded reasoning

The agent should expand context only when a concrete dependency, compile failure, acceptance criterion, contract, or conflict requires it.

The purpose is not to minimize thinking at all costs. It is to avoid unbounded discovery on routine work.

## Review evidence vs Human approval

Independent review produces evidence about a proposal or implementation. It does not automatically grant Human approval.

When Human approval is required, bind it to the actual phase, artifact revision, and decision scope shown to the Human. A material revision requires fresh approval for the changed semantics.

## Evidence

Completion should be backed by evidence appropriate to the change:

- unit tests,
- integration tests,
- lint/static analysis,
- build/package verification,
- CI,
- independent review,
- Human approval when required,
- device/runtime QA.

“Not run” is not equivalent to “passed.”
