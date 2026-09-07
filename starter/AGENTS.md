# AGENTS.md — Starter

This file should remain small. It defines always-on guards and task routing; repeated procedures belong in Skills.

Replace placeholders and delete irrelevant sections before adopting it.

## Start order

1. Read this file once per run unless it changes.
2. For work-item tasks, read the current Jira/GitHub/other ticket before unrelated backlog items.
3. Route implementation work to `.agents/skills/implementing-issue/SKILL.md`.
4. Load deeper process/domain docs only when the Skill or current change surface requires them.
5. Reuse unchanged context within the same run.

## Always-on guards

- Do not reset, clean, revert, or overwrite unrelated user/team changes.
- Do not invent files, APIs, labels, module names, commands, or architecture rules.
- Do not mix unrelated refactors, renames, formatting sweeps, dependency upgrades, or features into the current work item.
- Respect explicit allowed/forbidden path boundaries.
- If a required dependency, approval, or ownership boundary cannot be determined safely, stop product edits and report the blocker.
- Never report an unrun test/build/lint/runtime check as PASS.
- Keep secrets, production credentials, and private customer/user data out of commits, issue comments, PRs, and logs.

## Task routing

| Task | Canonical path |
| --- | --- |
| Implement an approved work item | `.agents/skills/implementing-issue/SKILL.md` |
| Risk/grade semantics | `docs/sdd-workflow.md` |

Add more Skills only after repeated workflow use shows a real need.

## Project invariants

Document only stable, high-value invariants here, for example:

- `<module A>` must not depend on `<module B>`.
- shared/generated/vendor paths require explicit ownership.
- `<build command>` is the canonical targeted build entry point.

Do not turn this section into a full architecture manual.

## Context efficiency

- prefer direct path/symbol reads,
- avoid repository-wide dumps,
- reuse unchanged work-item/rule context in the same run,
- summarize successful command output,
- expand only failures or concrete uncertainty,
- never trade away required evidence for token savings.
