# Conditional Device QA

Device QA is a **conditional merge gate**, not a requirement for every pull request.

## Typical triggers

Consider device QA when acceptance criteria depend on:

- real UI/UX interaction,
- camera/files/media upload/display/download,
- permissions,
- notifications,
- lifecycle behavior,
- background scheduling/execution,
- migration followed by real application flow,
- device/platform behavior that unit tests or an emulator cannot prove reliably.

## Flow

```text
Verification Strategy
  -> Device QA required?
      -> NO: normal review/CI path
      -> YES:
          PR marks Device QA REQUIRED
          -> acceptance-criteria-based checklist
          -> observation collection
          -> PASS / FAIL / UNVERIFIED judgment
          -> required PASS before merge
```

## Separate observation from judgment

A useful safety pattern is:

- **collector** records observations and evidence,
- **judge** compares them with the acceptance criteria.

The collector should not invent additional product requirements or perform broad product discovery.

## Checklist source

The QA checklist should come from:

1. issue acceptance criteria,
2. actual changed user/runtime flow.

Do not ask the QA agent to brainstorm a new test strategy after implementation unless the issue explicitly requires exploratory QA.

## Example report

```md
## Device QA

- Build/commit: abc123
- Device/environment: ...
- Time: ...

| Acceptance criterion | Expected | Observed | Evidence |
| --- | --- | --- | --- |
| App opens updated screen | screen is reachable | reached successfully | screenshot / log id |

### Judgment
- PASS / FAIL / UNVERIFIED
```

If required evidence is FAIL or UNVERIFIED, merge remains blocked.
