# Workflow

## 1. Issue definition

Define Priority, SDD grade, user impact, goal, scope/non-scope, allowed/forbidden paths, acceptance criteria, and dependencies/blockers.

The issue narrows the problem before the implementation agent starts.

## 2. Preflight

Before code edits:

- confirm required issue fields exist,
- confirm labels/metadata match the body,
- confirm blockers are resolved,
- confirm the requested work is allowed to start,
- confirm scope boundaries are usable.

Fail closed when a required boundary or dependency cannot be determined safely.

## 3. Claim / isolation

For parallel agent work:

- claim the issue/lane,
- check overlap with active work,
- create an isolated branch/worktree/sandbox,
- keep product changes inside the allowed boundary.

Shared or integration-owned paths should be separated rather than silently modified by an ordinary lane.

## 4. AS-IS analysis

Start from current mainline code.

Prefer:

1. direct target path,
2. target symbols,
3. direct public contracts,
4. direct callers/callees,
5. only then broader exploration if evidence requires it.

Record observed behavior, relevant code locations, and meaningful drift.

## 5. TO-BE design

Define desired behavior, behavior that must remain unchanged, failure/error behavior, state transitions when relevant, verification strategy, and change plan.

## 6. Trade-off capture

Only when actual competing options are already visible. Do not create alternatives merely to satisfy a template.

## 7. Risk grade gate

Apply the minimum process needed for the risk grade.

## 8. Implementation

- change only allowed files,
- do not add unrelated refactors/features,
- add direct regression coverage,
- keep implementation aligned with acceptance criteria.

## 9. Verification

Run targeted verification first. Broader verification is required when the change surface warrants it.

## 10. Self review

Compare the final diff against issue scope, acceptance criteria, allowed/forbidden boundaries, and unintended behavior changes.

## 11. Durable product documentation + final verification

When runtime/product behavior changed, update durable product documentation from **final code behavior**, not by copying SDD prose. Then run the required final verification.

## 12. PR / code review

The PR should match issue scope, state verification evidence, state unverified items, and apply grade-appropriate review gates.

## 13. Conditional device QA

If the change requires real-device evidence, the PR is blocked until the required observations are collected and judged against acceptance criteria.

## 14. Merge / cleanup / release

After required evidence passes: merge, close the issue, remove temporary SDD artifacts, clean isolated workspaces, and release the work lane.
