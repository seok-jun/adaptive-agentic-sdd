# Risk Grades

Grades control process depth. They are not estimates of implementation time.

## Trivial — Fast-track

Use only when all of the following are true:

- no runtime/product behavior changes,
- no test expectation, schema, dependency, build, API/contract, or workflow execution meaning changes,
- the target is direct and narrow,
- targeted static/path/format validation is sufficient.

Typical examples: typo fixes, link/path corrections, non-executable documentation cleanup.

Default process:

- no separate SDD package,
- no independent review by default,
- targeted validation,
- diff-to-request self-review.

If executable or contract meaning changes, promote to at least Small before editing.

## Small — Lean

Use when the change stays inside one implementation boundary and has no high-risk characteristic.

Default process:

- work item can serve as the plan,
- bounded target/code inspection,
- targeted verification,
- self-review.

Independent review is optional when there is a concrete reason.

## Medium — Standard

Use when multiple implementation boundaries or shared contracts are involved but failure is not in a high-cost category.

Default process:

- explicit AS-IS / TO-BE / change plan,
- verification strategy,
- bounded independent review when contract or integration risk warrants it,
- no repository-wide rediscovery.

## Large — Deep

Use for high-impact changes such as:

- security/privacy boundary changes,
- destructive or difficult-to-reverse migration,
- cross-system consistency or recovery logic,
- authentication/authorization,
- retry/scheduling semantics,
- cost/quota enforcement,
- durable public contract changes,
- similarly expensive failure modes.

Default process:

- explicit AS-IS gate,
- explicit TO-BE/change-plan gate,
- independent design/contract review before implementation,
- Human approval when a product/architecture decision is locally Human-owned,
- broader verification,
- independent code review before merge.

A blind audit can be added when omission/hidden-assumption risk is material. It is an escalation, not a universal portable-core requirement.

## Epic — Breakdown first

Use when the work changes module boundaries, creates modules, spans multiple independently deliverable capabilities, or cannot be safely reasoned about as one implementation lane.

Default process:

- break down first,
- define integration ownership,
- keep child work independently verifiable,
- apply Large-level rigor to risky child/integration work,
- avoid a giant implementation worker that owns the whole Epic.

## Grade escalation

Promote the grade when analysis reveals risk that was not visible in the work item.

Do not downgrade only to avoid review, approval, or verification cost.
