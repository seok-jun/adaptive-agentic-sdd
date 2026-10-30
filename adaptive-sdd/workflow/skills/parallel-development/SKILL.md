---
name: parallel-development
description: Manages claims, isolation, synchronization, release and integration for parallel agent work in this project. Use before the first edit of P work files of an execution Issue, such as SDD, tests and code; when creating a branch/worktree; when checking path conflicts; and when handling shared contracts. Do not use when only drafting an Issue or doing a read-only investigation.
---

The execution inputs are the absolute paths `P` (top level of the project repository), `W` (the pinned procedure copy `W`) and `M` (the pinned common principles `M`). Do not guess P or M from the current folder or from W's parent folder. Apply P's hard guard (`## Always-applied hard guard` in `P/AGENTS.md`) and its application declaration (`W/../project/sdd-workflow.md`). Read the words Issue, comment, label and PR as the work tracking method (`W/tracker/`) declared in `W/../project/tracker.md`. Look up unfamiliar terms in the [Glossary](../../glossary.md).

# Parallel Development

## Read-only investigation and entry into edits

Several readers of the same file are not an edit path conflict. For a read-only investigation only, do not create a new lane, branch/worktree or edit claim. Check the access permissions of the investigation itself, the current instructions and the settled preconditions, and leave the baseline revision. Secure the conclusion of a common rule that is not yet settled before the implementation, integration or deployment that relies on that result.

Apply Inputs, New lane and Claim below before actually creating a lane, or before first creating, editing or deleting P repository work files of an execution Issue. This includes the current Issue's SDD, tests and product code. If you start writing files during an investigation, check the current phase's work instructions, dependencies and boundaries, and secure a lane and claim. Also check existing claims of the same Issue so that two owners do not write to the same SDD or branch at the same time.

When writing an SDD, apply only the conditions of that writing phase. Do not require an AS-IS/PLAN review PASS or readiness for later implementation for a claim made to write the AS-IS. Product implementation starts after the needed grade gates and implementation dependencies are met. The path-listing exception for documents with a defined lifetime is not a claim exemption.

The work tracking method's Issue, observation and claim/release records, and the Epic management document itself, follow the existing management procedure. Do not create the circular condition "an implementation claim must exist before this record can be written". Do not use the description "read-only" to exempt existing write boundaries or required reviews.

## Inputs

If you can confirm that `## Always-applied hard guard` in `P/AGENTS.md` was applied in the same run, do not read it again. If you cannot confirm this because you started as a standalone run or as a sub-agent, read that section first and then proceed. Do not read the common policy documents whole in advance unless there is a conflict condition.

Required:
1. `Allowed edits` / `Forbidden edits` in the current Issue body and labels
2. The current Issue's assignee, recent comments, and linked or open PRs
3. The metadata, among the in-progress claims and PRs of the same repository, that is needed to judge path overlap

If the implementation phase already checked the Issue boundaries and whether paths are shared, reuse that as is.

Only when needed:
- If called standalone, or if the allowed edit paths include shared or root candidates (including root build and settings) in P's application document `module-boundaries.md`, check the relevant parts of the common boundary and lifecycle contract in `W/process/module-boundaries.md` and the actual product boundaries in `W/../project/module-boundaries.md`.
- Only when an instruction or ownership conflict cannot be decided with the existing rules, read `W/process/agent-instruction-policy.md` (common contract and procedure) and `W/../project/agent-instruction-policy.md` (product application, permissions and verification).

If the Issue has no allowed/forbidden edit paths, do not create a new lane or claim; normalize it through the Issue management procedure.

## New lane creation and isolation

This procedure applies only when creating a new Issue branch or worktree. The base of a new lane is a fresh fetch of `<code-remote>/<base-branch>` declared in P's `tracker.md`. Do not use the current local HEAD, a local base branch or an earlier Issue branch as an implicit base.

1. Check that the current repository and remote are the expected targets, and check the current worktree and branch, the uncommitted change (dirty) state, and branch and worktree path conflicts. Use this local state only for contamination and conflict safety checks, not for choosing the base.
2. Compare the Issue's allowed edit paths with in-progress `[CLAIM]`s and open PRs, and check the shared and root boundaries reserved for integration work. If they overlap or touch a shared boundary that is not allowed, do not create a branch or worktree; stop with the matching stop condition.
3. Right before creating the branch or worktree, run `git fetch <code-remote> <base-branch>` in the current shell. If it fails, stop with `BLOCKED: declared base fetch failed`, and do not substitute an existing remote-tracking ref, a local base branch or the current HEAD.
4. If the fetch succeeds, immediately fix the base SHA with `git rev-parse --verify <code-remote>/<base-branch>` and leave it in the work evidence. If the SHA cannot be confirmed, do not create a branch or worktree.
5. Use the confirmed base SHA as the explicit starting point.
   - If there are two or more lanes in the same local clone, create the per-Issue branch and a worktree outside the repository together with `git worktree add <path> -b <branch> <base-sha>`.
   - In an independent cloud clone or sandbox, do not create an additional worktree; create the Issue branch with `git switch -c <branch> <base-sha>` and use the sandbox itself as the lane.
   - A Windows local worktree uses a short path (`worktree root` in P's application document `sdd-workflow.md`).
6. For an external installation, also install and check a harness connection dedicated to the new checkout. Do not rewrite the existing checkout's connection files by changing only the paths, and do not overwrite the entry points of two checkouts with one lock. Share tracker_root for claim coordination.
7. Check that the HEAD of the created lane equals the recorded base SHA, then perform the Claim procedure below in that lane.

Do not edit the W and M pinned copies (`W`, `M`) in lane work.


- Do not choose a different base, or insert a checkout or pull of a local base branch, between the fetch and the creation of the branch or worktree.
- Two agents do not commit to the same branch at the same time.
- Do not automatically rebase or recreate an already created branch or worktree in progress because of this rule. Updating an existing lane applies only the Synchronization procedure.

## Claim

1. From the Priority, the current user instructions and the preconditions, check whether writing investigation results, design or implementation for the current phase is possible now. Do not use an open condition of a later implementation phase as a blocking condition for an earlier claim to write the SDD.
2. Compare the allowed edit paths with the paths of in-progress `[CLAIM]`s and open PRs.
3. If they overlap, `BLOCKED: overlapping lane`.
4. If an ordinary lane needs shared or root paths reserved for integration work, do not claim.
5. Set the current agent as the assignee.
6. Attach `status:in-progress`.
7. Leave a comment in this format.

```text
[CLAIM]
agent: <agent-id>
branch: <branch-name>
allowed:
- <path glob>
forbidden:
- <path glob>
```

8. Check the comments, labels, assignee and open PRs again.
9. If a competing claim appeared, release immediately, and do not edit work files, including the SDD.

## Synchronization

After related changes land in the declared base or merge branch, before the next push:
1. Fetch the needed revisions of the code remote, base branch and merge branch that P declared.
2. Rebase or merge.
3. Resolve conflicts only inside the Issue's allowed edit paths.
4. If forbidden or shared paths are needed, `BLOCKED`.
5. Rerun the affected verification.

## SDD review candidate publication

When pushing AS-IS and PLAN review candidates to the publication repository and branch that P declared, apply [Remote review candidate publication in Design review](../../process/design-review.md#remote-review-candidate-publication). Hand off the evidence that the candidate and documents can be read from the remote, and a re-review of a changed candidate follows the meaning and impact judgment in the same document. The base of a new lane and the lifecycle of existing claims and worktrees keep the procedure above.

## Shared contracts

When it is newly confirmed that an ordinary lane must change shared or root paths:
1. Do not edit those paths.
2. Identify the needed contracts, symbols and files.
3. Check the integration rules in the common boundary and lifecycle contract of `W/process/module-boundaries.md` and the actual product boundaries of `W/../project/module-boundaries.md`.
4. Split it into an integration Issue or a preceding change, and stop or release the lanes that rely on it.
5. When the shared change is merged, take in the declared integration revision and resume.

## Release

For handoff, stop, or cleanup after merge, first record the uncommitted and unpushed state, the PR state, the worktree registration, and the local and remote branch state.

- When only the ownership is passed on because of a handoff or stop, do not delete or force-remove an uncommitted or unmerged worktree. After the `[RELEASE]` comment, removing `status:in-progress` and removing the assignee, report separately that the worktree remains.
- If there is no registered local worktree, as in an independent cloud sandbox, record the state and then apply the ordinary release procedure.
- Product delivery is decided by the merged PR, the closed Issue and `[PRODUCT COMPLETE]`. Local cleanup and releasing ownership are separate from it, and a cleanup failure does not cancel product completion. Local cleanup and lane release follow the procedure below.

### Merged local worktree cleanup

1. Check that the PR is merged and the worktree is clean. If there are uncommitted or unmerged changes, do not delete it; stop.
2. First decide the "no artifacts" exception. If there is work evidence that no local build tool was run in that lane, and you confirmed that `git status --porcelain --untracked-files=all --ignored` is empty, so there are no tracked, untracked or ignored files and no user files at all, skip the build cleanup and leave the reason and evidence. If any of these was not confirmed, or there are artifacts, do not use this exception. If it is not the exception, check the cleanup command in P's application document `build.md` before removing the registration. If none is declared, leave the reason the cleanup was skipped. If one is declared, apply `W/skills/_shared/build-preflight.md` (reusing the JDK from the same run), run that cleanup command in the worktree and record it.
3. If preflight is `BLOCKED: JDK unavailable`, do not move on to removing the registration; stop in that state. If the JDK was found but the build cleanup failed, or uncommitted changes remain after the cleanup, stop with `CLEANUP_BLOCKED`.
4. Keep the Windows worktree root as a short path in the `worktree root` form P declared. Before removal, check that `core.longpaths=true`, applied only to this command, is in effect, and leave the result. If long path support cannot be confirmed, stop with `CLEANUP_BLOCKED`.
5. Remove the worktree from the main clone without a force option. On Windows, use `git -c core.longpaths=true worktree remove <exact-path>`.
   Apply the "no artifacts" exception above and the remaining cleanup protections to every worktree.
6. Independently of the removal command's result, check each of these two conditions.
   - `git worktree list --porcelain` has no registration for that exact path.
   - The actual folder does not exist.
7. If either remains, only read under that exact root and record these values.
   - The number of remaining files and folders
   - The longest path and its length
   - The worktree registration state
   - The local and remote branch state
8. Only if a small, confirmed number of remaining files or empty folders remain under the defined worktree root, you may clean them up one by one and then check the two conditions again. For a bulk residue that cannot be checked one by one, such as thousands of files, do not work around it with another recursive delete or per-file commands or loops; stop safely with `CLEANUP_BLOCKED`.
9. In `[LOCAL CLEANUP]`, leave `complete` or `pending` together with the registration and actual folder check results, the branch state, the evidence and the resume conditions. Use `complete` only when both were confirmed absent. A pending cleanup does not block product completion or observation collection. Only after both the registration and the actual folder are confirmed absent, post the `[RELEASE]` comment, remove `status:in-progress` and remove the assignee. If either remains, the worktree cleanup and lane release are incomplete. If only the cleanup state changes later, leave it in `LOCAL CLEANUP` and do not rewrite the product completion record. The prohibition on deleting user files and on forced removal still holds.

## Output

- Claim state / agent / branch
- Fetch result of the declared code remote and base branch / base SHA of the new lane
- Allowed edit paths / conflicts
- Isolation method
- Shared dependencies
- Release state
- JDK and build tool preflight, cleanup and reuse results
- Windows long path check result
- Local worktree registration and actual folder cleanup state
- If `CLEANUP_BLOCKED`: the exact root, the number of remaining files and folders, the longest path, the registration state, and the local and remote branch state
