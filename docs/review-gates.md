# Review Gates

Review depth scales with risk.

## Small

Default:

- implementation-agent self review.

Independent review is optional when there is a concrete reason.

## Medium

Default:

- bounded review may be applied.

Reviewer input should stay narrow:

- issue,
- relevant AS-IS/TO-BE,
- change plan,
- diff,
- verification evidence.

Do not ask the reviewer to rediscover the entire product.

## Large

Require:

1. **Design review before implementation**
2. **Independent code review before merge**

The design review should check:

- architecture/boundary violations,
- acceptance criteria that cannot be satisfied,
- unsafe failure behavior,
- obviously missing integration ownership.

The code review should check:

- diff vs issue,
- verification evidence,
- regressions,
- scope creep,
- unsafe implementation details.

## Epic

Require:

- breakdown review,
- design review for risky child/integration work,
- independent code review.

## Review is not solution rediscovery

A reviewer should primarily **falsify** the proposed solution:

> Is the proposed change clearly wrong, unsafe, out of scope, or unable to satisfy the acceptance criteria?

This keeps independent review useful without making every review another full repository analysis.
