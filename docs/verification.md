# Verification Strategy

Verification should be designed before implementation for non-trivial work.

## Goal

Every important acceptance criterion should have a plausible proof method.

Example:

| Acceptance criterion | Evidence |
| --- | --- |
| parser rejects invalid input | unit test |
| contract is wired through two modules | integration test |
| application still packages | build |
| UI state is visually correct | device/UI QA |
| background task behaves across lifecycle | real-device/runtime QA |

## Rules

- use the cheapest evidence that reliably proves the criterion,
- do not run expensive broad checks repeatedly when nothing relevant changed,
- do not claim unrun checks as pass,
- if a criterion cannot be proven within the allowed scope, treat the issue as blocked or revise the scope explicitly.

## Targeted first

Prefer:

```text
targeted test
  -> impacted module tests
  -> broader test/lint/build only when required
```

This keeps feedback fast while preserving stronger gates for risky work.
