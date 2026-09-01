# Risk Grades

The grade controls process depth. It is not business priority.

## Small

Typical characteristics:

- one implementation boundary,
- no high-risk automatic escalation,
- easy local verification.

Default:

- issue acts as change plan,
- no separate SDD package,
- targeted test,
- self-review.

## Medium

Typical characteristics:

- multiple implementation boundaries,
- shared/public contract change,
- wider integration surface,
- but no high-impact failure mode.

Default:

- AS-IS,
- TO-BE,
- change plan,
- verification strategy,
- bounded review when useful.

## Large

Automatically consider Large for changes such as:

- security/privacy behavior,
- persistent data migration,
- retry/scheduling/background policy,
- cost/quota/budget enforcement,
- destructive or high-impact recovery behavior.

Default:

- explicit AS-IS gate,
- TO-BE/change-plan gate,
- design review before implementation,
- independent code review,
- broad enough verification to prove safety.

## Epic

Use when:

- creating a new module,
- changing dependency direction,
- combining multiple independently deliverable capabilities,
- requiring explicit integration ownership.

Default:

- breakdown before implementation,
- integration issue/lane where needed,
- Large-level rigor for risky child work.

## Guard against grade inflation

Do not increase grade merely because a task “feels important.”

Grade should represent **change risk and implementation surface**.

Regularly review whether higher-grade gates actually prevented defects.
