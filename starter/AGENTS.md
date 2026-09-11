# AGENTS.md — Starter

Keep this file small: always-on guards and routing live here; procedures live in the Skill/local contract. Replace placeholders and remove irrelevant examples before adoption.

## Start order

1. Read this file once per run unless it changes.
2. Read the current work item or a trustworthy current snapshot.
3. Route implementation to `.agents/skills/implementing-issue/SKILL.md`.
4. Load deeper process/domain docs only when the task requires them.
5. Reuse context only while its revision and relevance remain unchanged.

## Always-on guards

- Preserve unrelated user/team changes; do not reset, clean, revert, or overwrite them.
- Do not invent files, APIs, commands, schemas, labels, or architecture rules.
- Respect allowed/forbidden modification boundaries. Direct-dependency reads do not authorize edits outside scope.
- Do not mix unrelated cleanup, refactors, upgrades, or features into the work item.
- Stop edits for unresolved required dependencies, authority, ownership, or scope.
- Never report an unrun check as PASS or self-review as independent review.
- Approval to plan, implement, or commit is not approval to merge, close, or release.
- Keep secrets, private organizational/customer details, and sensitive data out of commits, public work items, PRs, and logs.

## Task routing

| Task | Canonical local path |
| --- | --- |
| Implement an approved work item | `.agents/skills/implementing-issue/SKILL.md` |
| Grade / review / approval / evidence semantics | `docs/sdd-workflow.md` |

Add Skills only when observed use justifies them. The local contract is an adoption snapshot; reconcile upgrades explicitly.

## Project invariants

Add only stable, high-value facts, such as `<module A>` must not depend on `<module B>`, explicit ownership of generated/shared paths, and a verified build-command reference. These placeholders are not real repository facts.

## Context efficiency

Prefer direct paths/symbols and bounded packets. Summarize successes, expose failures and uncertainty, retain evidence references, and never remove required verification/review/authorization to save tokens.
