# Workflow

## 0. Repository bootstrap contract

Before adopting the workflow, identify the repository's actual build/test paths, module boundaries, work-item system, and existing development rules.

Do not start by copying a large policy set from another project. Establish a small root agent contract and add local safeguards only when the repository needs them.

See `docs/bootstrap.md`.

## 1. Work-item definition

Define:

- Priority,
- SDD grade,
- user/business impact,
- goal,
- scope and non-scope,
- allowed/forbidden paths when path boundaries matter,
- acceptance criteria,
- dependencies/blockers,
- authoritative requirement/design references.

The work item narrows the problem before implementation starts. GitHub Issue, Jira, Linear, or another tracker can fill this role.

## 2. Preflight

Before code edits:

- confirm required work-item fields exist,
- confirm blockers are resolved,
- confirm the requested work is allowed to start,
- confirm scope boundaries are usable,
- confirm the agent can access a current work-item revision or snapshot,
- resolve the grade before selecting process depth.

Fail closed when a required boundary or dependency cannot be determined safely.

## 3. Claim / isolation when needed

For parallel agent work:

- claim the lane/work item,
- check overlap with active work,
- use an isolated branch/worktree/sandbox when supported,
- keep product changes inside the allowed boundary.

Parallel isolation is an operational extension, not a requirement for every repository.

## 4. Bounded AS-IS analysis

Start from current mainline code.

Prefer:

1. direct target path,
2. target symbols,
3. direct public contracts,
4. direct callers/callees,
5. related durable documentation,
6. only then broader exploration when concrete evidence requires it.

Record observed behavior, relevant evidence, scope, unknowns, and meaningful drift.

Trivial changes normally skip a separate AS-IS artifact. Small changes may keep AS-IS in the work item or implementation notes.

## 5. TO-BE design + Verification Strategy

Define:

- desired behavior,
- behavior that must remain unchanged,
- failure/error behavior,
- state transitions when relevant,
- concrete change plan,
- acceptance-criterion-to-evidence mapping.

Do not create alternatives merely to satisfy a template. Capture trade-offs only when real competing options already exist.

## 6. Grade gate

Apply the minimum process needed for the risk grade.

- **Trivial**: targeted change + targeted validation + self-review.
- **Small**: lean analysis/implementation + targeted verification + self-review.
- **Medium**: written AS-IS/TO-BE/change plan and bounded review when contract risk warrants it.
- **Large**: explicit AS-IS and plan, independent design/contract review, required Human approval when local policy says the decision is Human-owned, independent code review before merge.
- **Epic**: break down first; define integration ownership; apply Large-level rigor to risky child/integration lanes.

## 7. Revision-addressed design review

When a design artifact requires independent review or Human approval, the candidate should be addressable as an immutable or unambiguous revision when the collaboration environment supports it (for example, a commit SHA or versioned document revision).

The review packet should be phase-aware and bounded to:

- work item / acceptance criteria,
- target phase artifact,
- approved upstream decisions,
- direct public contracts and invariants,
- allowed/forbidden boundaries,
- relevant verification evidence.

A review PASS is not Human approval.

If the reviewed artifact changes in a way that affects decisions, scope, contracts, or acceptance semantics, review/approval must be repeated for the new revision.

See `docs/review-gates.md`.

## 8. Human approval when required

Human approval is a policy gate, not a synonym for reviewer PASS.

When approval is required, bind it to:

- one phase,
- the exact artifact/revision shown to the Human,
- the decision scope being approved,
- approval time/actor according to local audit needs.

Do not silently reuse vague or stale approval after a material revision.

## 9. Implementation

- change only allowed files,
- do not add unrelated refactors/features,
- preserve approved decisions and contracts,
- add direct regression coverage where useful,
- keep implementation aligned with acceptance criteria.

## 10. Verification

Run targeted verification first. Broader verification is required when the changed surface warrants it.

Unrun verification must be reported as unverified, not PASS.

## 11. Self review

Compare the final diff against:

- work-item scope,
- acceptance criteria,
- allowed/forbidden boundaries,
- approved decisions,
- unintended behavior changes.

## 12. Independent code review when required

The reviewer should falsify the implementation against the approved contract and evidence rather than rediscover the entire product.

Large/Epic require independent code review by default. Medium may use bounded independent review when shared contracts or failure cost justify it.

## 13. Durable documentation + final verification

When runtime/product behavior changed, update durable documentation from **final observed code behavior**, not by copying planning prose.

Then run required final verification.

## 14. PR / merge gate

The PR should state:

- work item,
- scope,
- meaningful decisions,
- verification evidence,
- review/approval evidence when required,
- unverified or blocked items.

## 15. Conditional device/runtime QA

If real-device, browser, integration-environment, permission, lifecycle, background, media, or other runtime evidence is required, merge remains blocked until the required observations are collected and judged against acceptance criteria.

## 16. Merge / cleanup / release

After required evidence passes:

- merge,
- close/update the work item,
- remove temporary SDD artifacts when local policy treats them as disposable,
- clean isolated workspaces,
- release the lane.
