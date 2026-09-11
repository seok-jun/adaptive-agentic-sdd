# Verification Strategy and Results

Design verification before non-trivial implementation. Every important acceptance criterion needs a plausible proof method. Use the cheapest evidence that reliably proves it, not the cheapest command regardless of relevance.

## Plan and result traceability

Use a stable AC identifier or an unambiguous criterion reference. Record results in the work item or PR; no separate report is required for small work.

| AC ID | Method / expected result | Target revision / environment | Actual observation | Status | Evidence / reason |
| --- | --- | --- | --- | --- | --- |
| AC-01 | invalid input is rejected; targeted test | candidate identifier / test environment | not executed | UNVERIFIED | awaiting execution |

This row is illustrative, not a test result. Keep the requirement in its authoritative work item; reference it instead of maintaining conflicting copies.

Useful evidence includes unit tests for local logic, integration observations for wiring/contracts, build results for packaging, and device/runtime observations for platform-dependent ACs. A build PASS alone does not prove behavioral ACs.

## Status semantics

- **PASS:** actually executed/observed; evidence satisfies the expected result.
- **FAIL:** actually executed/observed; evidence contradicts the expected result.
- **UNVERIFIED:** not executed, or insufficient evidence for a judgment.
- **BLOCKED:** a named permission, environment, dependency, or other obstacle prevents execution/judgment. Record the obstacle, owner/next action when known, and relevant evidence.

Do not turn generated tests, commands, API requests, queries, intended behavior, or static reasoning into a runtime PASS. Static inspection may be PASS for an AC that genuinely requires only that inspection; it does not prove runtime behavior.

A non-applicable method may be omitted with a reason; it is not PASS. If the underlying AC still applies, provide another valid proof method or leave it unmet. Do not add new status values to hide missing evidence.

## Readiness

Required FAIL, BLOCKED, or UNVERIFIED results block completion/integration. If an AC cannot be proven within the allowed scope, report the blocker or explicitly revise scope/ACs through the authorized decision path and revisit affected gates. Human approval is not a substitute for proof.

Separate task delivery (for example, a prepared candidate or verification plan) from completing the full approved behavior/integration lifecycle.

## Targeted first

```text
targeted check -> impacted module checks -> broader test/lint/build only when required
```

Do not repeat expensive broad checks when nothing relevant changed. Bind evidence to the actual target revision and environment. After material changes, rerun affected checks; reuse other evidence only when its continuing relevance can be established.

## Observation and judgment

An authorized person or runner may collect evidence that an agent cannot obtain. Preserve expected versus actual observations, target identity, and safe evidence references; judge them against ACs without inventing requirements. Do not publish raw sensitive output.

[Device QA](device-qa.md) is an existing conditional pattern. The [restricted-environment API/DB handoff](restricted-environment-verification.md) is an optional draft, not a working connector or validated automation.
