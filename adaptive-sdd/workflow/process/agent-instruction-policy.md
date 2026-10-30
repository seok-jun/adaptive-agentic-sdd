# agent-instruction-policy procedure

The P application document `W/../project/agent-instruction-policy.md` is the source of conditions, product facts, required verification and human authority. W owns the common rules and how to carry them out.

## Common source and local guards

This document is the source of the common contracts for instruction interpretation, context, document loading and shell/encoding. The actual project hard guards, permissions and document path mapping follow the P source. Local guards apply even before W is verified, and this document does not relax them.

## Normative terms

- **MUST**: when the condition is met, do it without exception.
- **MUST NOT**: when the condition is met, do not do it.
- **MAY**: use only for implementation choices that do not affect the result.

Normative documents do not use, on their own, expressions that leave the scope of action open, such as `if possible`, `appropriately`, `if needed`, `related`, `depending on the situation`, `as you see fit` or `etc.`. Where such an expression is needed, write a verifiable condition together with the action to perform.

## Document loading principles

- `AGENTS.md` is the repository entry hard guard. If it has not changed in the same run, do not read it again.
- For Issue work, first read the target Issue's current body/labels, and add only the decision documents the canonical Skill requires.
- When a Skill names a specific heading/section, do not read the full file with a tool that can read only that section.
- `docs/reviews/**`, completed specs and unrelated business/architecture documents are not default inputs.
- In implementing → parallel → finishing transitions within the same run, pass on and reuse the unchanged Issue/rules/boundaries already checked.
- When a new conflict, scope change, `main` update or verification failure occurs, re-check only the documents needed for that judgment.

`CLAUDE.md` is the Claude entry point and cannot change or invalidate the common rules.

## The Execution Packet is a derived cache

The Execution Packet is a derived cache that passes decisions, already made against the higher Source of Truth in the same run, to a coarse-grained phase worker. It is not a replacement for the source documents.

```text
AGENTS.md hard guard
  > canonical Skill / process
  > current Issue + reviewed SDD / PLAN
  > Execution Packet
```

- If a packet relaxes or conflicts with a higher source, do not execute the packet's instruction.
- The immutable identity and freshness of the hard guard/canonical process, the current Issue/review, the reviewed PLAN and the direct contract must be linked in the packet provenance.
- A boolean self-report such as `guard applied: true` or `runtime_guard_propagation: true` alone does not prove that a hard guard was applied or reused. An immutable evidence object of host-enforced propagation or worker direct-read, bound to the identity of the applied guard source, is required. Without this evidence, the worker reads the needed hard guard section directly.
- If any required nested value of the Issue snapshot, reviewed PLAN, goal, boundaries, contract, acceptance, verification, escalation, SDD grade gate/claim or provenance is empty, do not execute the packet.
- A change in the Issue/PLAN/direct-contract/canonical source version, a new direct dependency, a lane conflict, or a verification failure that contradicts an architecture assumption makes only the affected items `STALE`.
- For stale items, do a bounded refresh of only the needed sources, and use them only after they become `VALID` with new provenance. If freshness cannot be proven, follow that workflow's `BLOCKED` stop condition.
- Do not expand a single invalidation into reloading Issue comments, docs or the whole repository.

## Repository text UTF-8 first-read

A repository text file with no separate evidence of its encoding is read as UTF-8 on the first read. This applies first to `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml` and to the following instruction paths.

- `.agents/skills/**`
- `docs/**`
- `AGENTS.md`
- Other workflow/instruction documents

Keep the current shell's native path, and settle the decoding and any needed output encoding from the first read.


For how to perform the first decoding/output encoding, the failure cause check and the bounded fallback, follow the verified [external procedure](agent-instruction-policy.md). Do not make judgments from mojibake output, and do not repeat the same failed read.

## Execution shell affinity

The shell running the current command is the primary execution shell. Do not choose a different shell based only on the host OS, the list of installed shells or a familiar quoting syntax.

- In Git Bash, use Bash-native commands and the `git`, `gh`, `python`, build tool wrappers, native executables and `.cmd` that can be called from the current shell, directly. Do not wrap commands in `powershell.exe` just because the host is Windows.
- In a PowerShell session, PowerShell-native commands are the normal path. Do not forbid PowerShell itself or require installing Git Bash.
- In WSL/Linux, keep Bash/POSIX-native commands and do not escape to a Windows shell.
- In CI, keep the shell the workflow specifies.


For the specific native/file-input fallback and conflict diagnosis, follow the verified [external procedure](agent-instruction-policy.md). The project application source takes precedence for the current shell, the ban on persistent settings and the meaning of stops.

## External agents and tool permissions

The fact that an external agent or collector name is written in an Issue, PR or checklist is not permission to check, install, authenticate or call that agent's CLI/API. Call it only when the current user instruction or the canonical workflow explicitly grants it.

## Source of Truth depends on the kind of information

Do not resolve every conflict with a single global priority order.

| Kind of information | Source of Truth | Action on conflict |
| --- | --- | --- |
| Current user's work instruction | The explicit user instruction in the current session | If it changes the existing Issue goal, update the Issue body too before implementing. |
| Issue goal, scope, acceptance criteria | The current body of that Issue | Do not change scope through comments alone. |
| Common agent hard guard | `AGENTS.md` | Agent-specific files or Skills cannot relax it. |
| Work procedure | Canonical Skill + the process documents the Skill names | If they conflict, do not implement; identify the conflicting documents. |
| Module dependencies and edit boundaries | `docs/architecture/module-boundaries.md` | Do not cross a boundary unless it is an approved architecture change. |
| Current runtime behavior (as-is) | Current `main` code | If it differs from business documents, treat the code as the observed as-is. |
| Product rules after implementation is complete | `docs/domains/**` | If the Issue to-be changes them, synchronize them with the final code at the completion stage. |
| UI layout, screen states | The immutable HTML Visual Spec the Issue links | Feature policy follows the Issue body. |
| Past decision rationale | `docs/reviews/**` | It is a historical record and does not override current requirements. |
| SDD working documents | `docs/sdd/**` | A temporary plan; it does not change Issue/business rules on its own. |

## When code and business documents differ

1. Confirm that the code is the actual current `main` behavior.
2. Record the difference by file, symbol and rule ID.
3. **Do not change feature code on the basis of a document difference alone.**
4. If the work is document alignment, fix the documents to match the confirmed code behavior.
5. If the work is a feature change, implement the Issue to-be, and at the completion stage bring the business documents in line with the final code.
6. If the intended state cannot be determined, stop with `BLOCKED: instruction conflict`.

## When the Issue and code differ

The Issue is the **to-be**; the code is the **as-is**. Do not conclude from the difference alone that the Issue is wrong.

If the Issue acceptance criteria violate an architecture boundary or cannot all be satisfied at the same time, do not implement, and report the conflicting items as `BLOCKED`.

## No-inference rules

The following are forbidden.

- Guessing the name of a file, module, label, API or setting that does not exist from a similar name
- Adding a feature not in the Issue because it seems needed
- Editing product files outside the allowed paths at will
- Restoring an old review/proposal/handoff as a current requirement
- Designing a new UI structure without a required Visual Spec
- Recording failed/unrun verification as passed
- Running reset/checkout/clean/revert on user changes unrelated to the current work

Look for needed values in the repository and the Issue first. If there is still no safe default after searching, do not guess; report `BLOCKED`.

## Scope expansion rules

In Issue work, edit only the `Allowed edits` paths.

- If a product change outside the allowed paths is needed, do not touch the files; report the blocking reason.
- If a shared contract/wiring is needed, read and follow the integration rules in `docs/architecture/module-boundaries.md`.
- If a separate bug/improvement is not essential to the current acceptance criteria, do not mix it into the current change.

For work requested directly without an Issue, edit only the minimum files that satisfy the user's request.

## Visual writing of human-facing documents

This applies when newly writing or substantively revising Issues, status/plans, proposals/decisions/reviews, business explanations and completion summaries that humans read and judge. Put **the conclusion and what will look different first, and detailed evidence after**. This section sets only principles of expression; it introduces no new permission or approval step.

| What the reader needs to know | Expression to show first |
| --- | --- |
| Policies, options, before/after differences | A small comparison table, or a representative situation and its expected result |
| Ownership, responsibility, system connections, boundaries | A relationship diagram, a context picture or a boundary table |
| Order, branches, failure, retry, states | A flow diagram, a state table/state diagram or a representative sequence |
| Screen layout, interaction | A rough draft that meets the project's Visual Spec criteria |
| A simple change understood in one sentence | That one sentence |

When choosing a picture or table, make the question it answers and the key change visible first. Distinguish the confirmed current state, proposals and open items, and important conditions, failures, exceptions and responsibility boundaries. The picture and the body text/table must convey the same meaning, and the key conditions must be readable without rendering. Do not distinguish states by color alone; if it is complex, separate the overall relationships from the needed details.

Evidence needed only for Agent execution, such as files, functions, commands, logs and check inventories, is linked to the execution specification. Conditions that change a human's judgment, such as cost, risk, expected behavior and permissions, are not hidden from the human-facing explanation. Do not add decorative pictures that fail to show relationships, or verbose prose duplicating the same flow.

Do not add new approvals or independent review rounds, obligations on the number of pictures or examples, fields for reasons for omission, or dependencies on specific tools or external rendering. Do not rewrite existing documents in bulk or create an SDD for a simple change. Check only this section in the phase that writes, revises or reviews, and reuse the check from the same run if nothing changed. Consult other formats and examples in full only when needed.

In the existing review, or the self-review of that grade, check whether the key change or choice can be found from the first explanation, whether the expression shows the relationships it needs to, and whether its conditions and open items match the body. Handle important differences in meaning with the existing source/scope/review rules. This is a check on writing quality within the existing review, not a separate approval step or an automatic completion gate based on the number of pictures. Do not write that improved understanding or reduced review time has been proven without observing actual human use.

In the same review, check whether the explanation lets the reader answer what changes, who is responsible for what, what happens on failure and what is still open. Treat as a meaning mismatch a static relationship line that can be misread as a call order, or an automatic retry added only in a picture. Consult the [mismatch review example](visual-writing-examples.md#review-check) only when that judgment is needed. Record passing link/format checks, actual writing/review behavior and observed human understanding as separate evidence.

## Completion report criteria

Report at least the following.

1. Changed files
2. Completion status for each requirement
3. Verification run and its results
4. Verification not run and why
5. Remaining `BLOCKED` items

If even one acceptance criterion failed or is unverified, do not describe the whole as complete.

## Format that avoids ambiguous instructions

```text
IF <verifiable condition>
THEN <action to perform>
ELSE <next action, or do nothing>
```

Or use a checklist that can be judged. Do not build acceptance criteria from only `better`, `cleanly`, `sufficiently`, `reasonably` or `as much as possible`.

## The Execution Packet is a derived cache — procedure

- For stale items, do a bounded refresh of only the needed sources, and use them only after they become `VALID` with new provenance. If freshness cannot be proven, follow that workflow's `BLOCKED` stop condition.
- Do not expand a single invalidation into reloading Issue comments, docs or the whole repository.
## Repository text UTF-8 first-read — procedure

- In PowerShell, state UTF-8 decoding explicitly, as in `Get-Content -Raw -Encoding utf8 <path>`. When text is passed to a native process or pipe so that the output encoding matters, set the process-scope `$OutputEncoding` and `[Console]::OutputEncoding` to UTF-8 before the first command. Do not change the profile, registry or system locale.
- In Git Bash/WSL/Linux, use the current shell's `cat`, `sed` or a Python UTF-8 helper, and do not switch to PowerShell just to read repository text.
- In CI, use a UTF-8 native read in the shell the workflow specifies.

If the first read fails or mojibake appears, do not judge a Skill, procedure or content from that output. Check the cause, such as the file's BOM, bytes or declared encoding, only once. Only when the file is confirmed to be actually non-UTF-8, use one bounded fallback with the confirmed encoding. Do not repeat the same read command. Do not cycle through several shells or start a repository-wide search for the purpose of checking the encoding.

## Execution shell affinity — procedure

When the current-shell approach fails, the fallback order is as follows.

1. Confirm the canonical invocation for the repository and the current shell.
2. Apply once a portable/native fallback that runs in the current shell, such as a Python helper, the CLI's file input, JSON encode/decode, or a native executable or `.cmd`.
3. Allow a PowerShell cross-shell fallback only when a Windows-only API/behavior is needed and the previous steps cannot handle it, or when the repository provides only a PowerShell script.

For structured/multiline data such as Issue/PR bodies, JSON and Markdown, prefer Python or CLI file input over nested shell quoting. If a temporary file is needed, use a run-owned location outside the repository and clean it up in the same run. In Git Bash, when `foo.ps1` and `foo.cmd` both exist, use `.cmd` or the native executable instead of the `.ps1`, which is affected by the execution policy. Keep normal entrypoint resolution in a PowerShell session, but do not change the execution policy.

A Git Bash MSYS path conversion problem is not a reason to switch shells. For known paths such as device-internal paths (for example `/sdcard/...`), first apply the existing `MSYS_NO_PATHCONV=1` canonical workaround.

If both the current-shell canonical approach and the portable/native fallback fail for the same shell/quoting cause, do not repeat exploratory shell switching. Record the needed external state or permission as a decidable blocker with a resume condition, and follow that workflow's stop condition.

## When code and business documents differ — procedure

1. Confirm that the code is the actual current `main` behavior.
2. Record the difference by file, symbol and rule ID.
3. **Do not change feature code on the basis of a document difference alone.**
4. If the work is document alignment, fix the documents to match the confirmed code behavior.
5. If the work is a feature change, implement the Issue to-be, and at the completion stage bring the business documents in line with the final code.
6. If the intended state cannot be determined, stop with `BLOCKED: instruction conflict`.

## Completion report criteria — procedure

Report at least the following.

1. Changed files
2. Completion status for each requirement
3. Verification run and its results
4. Verification not run and why
5. Remaining `BLOCKED` items

If even one acceptance criterion failed or is unverified, do not describe the whole as complete.

## Context / token efficiency

- Once the target is set, do not fetch unrelated Issue bodies, domains or documents in bulk.
- Narrow the scope by path/symbol/heading, and where supported read only the needed section instead of the full file.
- In implementing → parallel → finishing within the same run, pass on and reuse unchanged context.
- Summarize large logs; on failure, expand only the representative error and the surrounding section needed.
- Do not skip verification or required evidence to save tokens.

### Trivial Issue fast-track

Use `SDD grade: Trivial` only when all the common non-behavioral change conditions of W `process/sdd/grade.md`, verified against the lock, are met. Product-specific application follows `docs/sdd-workflow.md`.

- Do not create a separate SDD or an independent review.
- Read only the target files and direct verification evidence, and do not search the whole repository.
- Limit default verification to targeted validation suited to the kind of change, such as link/path/format/static validators. Do not run build tool verification unless the change affects its result.
- Keep the diff ↔ requested scope self-review.
- If executable code, test expectations, build/dependency, schema, contract or workflow execution meaning changes, do not proceed as Trivial; re-grade as at least Small.

### Additional saving rules for Small Issues

Apply the following rules additionally only to Issues with `SDD grade: Small`.

- Read only the needed files and avoid printing whole files.
- For interfaces and types, look up only the declaration and the surrounding lines needed for the judgment.
- Limit the search scope to the target path/symbol, and do not create large source dumps.
- Reuse workflow and Skill documents already read in full in the same run and not changed.
- For the diff, check only the list of changed files and the needed hunks, and avoid printing the whole diff.
- On build/CI success, check only the final status and summary; only on failure, look up the representative error and the relevant section.
- Do not repeatedly look up the same Issue, source or verification state without reason.
- These rules do not skip the required initial document reads, claim/grade gates, verification, review, QA or completion evidence.
