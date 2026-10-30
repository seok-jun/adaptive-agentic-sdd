# Common work boundaries and lifecycle

P declares the actual modules/paths, shared contracts, integration-only paths and document locations. This document owns how allowed/forbidden boundaries are applied, the scope of the current Issue's lifecycle artifacts, and the common contract for parallel work. It does not widen product boundaries or create product-specific permissions.

## Public contract integration order

For paths the project designates as shared contracts, the following order is fixed.

1. In an integration lane, edit only the contract and the contract tests.
2. Merge the contract change PR into `main` first.
3. Implementation lanes take in the latest `main`.
4. Edit each implementation module the project designates.
5. If composition root wiring is needed, connect it in an integration lane.
6. Run the full test/lint/build the project specifies.

When an implementation lane finds that a contract change is needed, it does not edit the contract files directly; it reports the blocking reason and the needed change. The actual contract paths, implementation modules, composition root and verification commands follow the P application declaration.

## Issue work boundaries

The rules are as follows.

- Among product implementation files, the agent edits only the path globs written in `Allowed edits` and the files under them.
- Test files can also be edited only if they fall under that module's glob.
- `Forbidden edits` takes precedence over `Allowed edits`.
- Even if needed for the acceptance criteria, do not automatically add product implementation files outside the allowed paths.
- When a boundary change is approved, update the allowed/forbidden paths in the Issue body first, **before editing product code**.
- If a shared contract or root build file is needed, switch to integration work or create a separate integration Issue.

One lane may edit several implementation modules. However, **every module must be stated in the Issue body as `Allowed edits`, and none of the allowed paths may overlap with another active lane.**

## Lifecycle artifact exceptions

The following files/metadata are **Issue lifecycle artifacts**, separate from product implementation ownership. They may be changed without being listed separately in `Allowed edits` only when the conditions below are met. The exception from listing paths is not an exemption from lanes and claims for P working files such as an execution Issue's SDD. The existing management procedures for work tracking metadata and for Epic management documents themselves remain.

### Work tracking metadata

The current Issue's body, labels, assignee, `[CLAIM]`/`[RELEASE]` comments and the current PR body (the counterpart in the work tracking method) may be changed when the relevant Skill procedure requires it.

Do not edit another Issue's scope/labels/claim for the convenience of the current work.

### Issue-scoped SDD

If the current Issue is Medium or higher, `docs/sdd/{feature}/**` may be created, edited and deleted according to the SDD procedure.

Conditions:

- `{feature}` must be the current Issue's SDD directory.
- Do not edit another Issue's `docs/sdd/**`.
- Do not edit product/business documents other than the SDD under this exception.

### Business documents

At the `finishing-issues` stage, only **existing `docs/domains/**` rules directly connected to the final code behavior** may be updated.

Conditions:

1. Runtime/product behavior actually changed.
2. The rule/topic to change is the document that currently describes that behavior.
3. What changed was confirmed from diff evidence.
4. No other active lane/PR is editing the same business document file.

If condition 4 is false, do not edit the business document concurrently; report `BLOCKED: documentation lane conflict`. Do not revert product code or overwrite another lane's documents.

Work that creates a new business topic file, or adds or changes the meaning of a rule ID, also re-checks the project's review topic trigger conditions.

### Review documents

Edit the `proposal/review/decision` files of the current review topic only when the current work has explicitly entered the review procedure. Past review topics are not edited under the lifecycle exception, except under the status update conditions.

### UI Visual Spec

Create or update the Issue's HTML in the separate design repository the project specifies only when the `managing-issues` Skill has met the HTML creation conditions. An app implementation lane does not change the Visual Spec at will.

## Parallel lane claims

Before the first creation, edit or deletion of P working files of an execution Issue, such as its SDD, tests and code, check the allowed paths of active lanes and the claims on the same Issue, and secure the current lane. The existing exceptions for read-only investigation and tracker management records remain. **`W/skills/parallel-development/SKILL.md` is the canonical owner of the execution order of claim/release and of the metadata and comment formats**, and this document does not define them again.

The boundary invariants this document owns are as follows.

- If a product implementation path overlaps with another active `[CLAIM]` or open PR, do not implement.
- An ordinary lane does not claim shared/root integration-only paths.
- If the Issue has no allowed/forbidden, do not start editing product code.
- If a new overlap is found after the claim, do not edit the conflicting working files; release the lane.

## Branch/worktree/cloud

W `skills/parallel-development/SKILL.md` is the single source of how to check the latest remote main and create, synchronize and clean up isolated lanes. Branch naming and the actual modules and root/shared scope follow the P declaration. Example commands do not replace the fresh base or normal cleanup steps.

## Action on boundary violations

If any of the following occurs, do not expand the current implementation.

- The acceptance criteria newly require a shared contract change
- A product implementation path overlaps with another active lane
- It cannot compile with only the Issue's allowed paths
- It can be implemented only by breaking an architecture dependency prohibition rule
- At the finishing stage, the same business document file would have to be edited concurrently with another active lane

In that case, report as `BLOCKED` the files not edited, the needed change and the impact on the current acceptance criteria.
