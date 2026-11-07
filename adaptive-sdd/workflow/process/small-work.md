# Routine Trivial / Small work

Use this compact route for an explicitly selected task performed by one current/manual agent. Small changes behavior inside one implementation module; it retains verification, human decisions, ownership and merge safety with a light work item and normally three records. No separate SDD, plan, packet or default independent review is required.

## Closed reading set

This document owns the Trivial/Small compact procedure. Every applicable common workflow requirement is stated here or reached through the routine sections and exception triggers below. This closes routine navigation through common documents, including their forwarding links; it does not waive substantive product instructions, permissions or explicit project-required checks. The compact forms and exemptions here also apply when an exception opens a full owner document. Medium/Large retain those owners' full procedures.

Read once, reusing unchanged inputs in the same session:

- The selected entry and [task guard](../task-guard.md); M [core](../../methodology/core.md) and [ordered changes](../../methodology/supports/ordered-changes.md); [grade rules](sdd/grade.md).
- The selected profile, every applicable application document in `W/../project/` (except `skill-evals.md` until workflow/eval work), and their actual P originals. Apply project-specific text in full; common forwarding follows this closed set. Before grading, establish P's implementation modules, designated shared contracts and integration-only paths, including the authoritative architecture source. Missing mapping is unresolved input, not evidence of Small eligibility.
- [Priority decision order and When evidence is insufficient](issue-priority.md#priority-decision-order), plus its compact item exception; the declared [local-docs](../tracker/local-docs.md) or [GitHub](../tracker/github.md) adapter's mapping, compact grouping, storage/ownership prerequisites and limits. Confirm tracker setup once, then check for changes. For local-docs, `tracker_root` must be shared outside lane worktrees on local disk or SMB; retain declared-author and backup limitations. Do not create, look up or register GitHub tokens.
- [Execution routing](../skills/_shared/execution-routing.md): only current/manual eligibility in Two-axis routing, Host Capability Map and Model Role Qualification, including stale/incomplete records and unknown identity. Check denies and actual explicit requirements briefly: absence of a positive qualification record alone does not block routine work; an identity insufficient to check denies or an incomplete/expired explicit requirement is not a pass. No automatic model selection or delegation is authorized.
- [Evidence recording rules](issue-writing-guide.md#evidence-recording-rules), [Visual writing of human-facing documents](agent-instruction-policy.md#visual-writing-of-human-facing-documents) and [Context / token efficiency](agent-instruction-policy.md#context--token-efficiency), including Small's saving rules, with the compact writing forms below. The observation exception is stated here; the authoring-model section is needed only for an explicitly requested model evaluation.

## Compact work item

Retain all required facts, with combined headings allowed:

```text
Priority / grade: one value each (local-docs: Meta only, including status)
Goal and impact: observable change, included behavior, one sentence of current user impact
Boundaries: confirmed allowed paths; forbidden paths; excluded behavior
Acceptance criteria: each checkable condition -> file/symbol and check/evidence, in edit order
Dependencies / decisions: prerequisites, or none; open question / answer owner / waiting work
```

Set exactly one priority and grade at creation where supported, otherwise immediately afterward, and read back the saved item. Local-docs keeps priority/grade/status only in Meta; any duplicated values must agree. Use P0 through P3 in decision order; insufficient P1/P2 evidence means P2, uncertain current impact means P3. A user-designated task does not require comparing the whole queue; when actually selecting next work, apply project queue conditions and precedence, grade, conflict and ID order.

Search only related duplicates/current work and obtain IDs by the adapter; local-docs creation must fail on an existing file and record search scope/result count. Normalize a deficient item before product edits. Keep confirmed goal, scope, boundary and AC changes in the current body, not only comments. The item itself is the plan; connect requirements to edits/checks beside existing AC without a duplicate mapping. An open question is one line in this item, not a separate ledger or new label.

## Execution obligations

1. **Entry and authority.** Before code edits, confirm an implementation instruction, the current item re-read, satisfied current-phase dependencies, no blocked status, permitted paths and an acquired claim. Selection alone is not implementation authority. Keep the selected W snapshot. Stop only work dependent on unresolved human judgment; preserve the question when asking is unavailable. Reuse actual decisions and delegations with scope/date/confirmer; never create or widen them.
2. **Grade, write boundaries and sandbox.**
   - **Grading.** Apply every Trivial condition or one-module Small and the highest automatic escalation in the unchanged grade rules; re-grade on scope/risk changes and never lower it yourself.
   - **Write boundaries.** Read-only investigation needs permission and a baseline revision, but no edit claim/new lane. Before the first work-file write, confirm edit, record and scratch/build-output paths. Scripts, messages, caches and compiler outputs are writes: prefer tools/stdin/memory, resolve symlinks/junctions for disk paths and keep process temp/cache settings within permission. Preserve other owners' changes; tests share the same boundaries.
   - **Sandbox.** Confirm sandbox enforcement when required, leave unconfirmed enforcement explicit, and never bypass a denied write.
3. **Lane and claim.** Check repository/remote, dirty state, worktrees, open unmerged task branches and competing claims. For a new lane, fetch the declared base and immediately capture `git rev-parse --verify 'FETCH_HEAD^{commit}'`; create from that SHA and confirm HEAD equals it. Stop on fetch failure; do not recreate an existing active lane automatically. A single isolated clone uses a task branch without an extra worktree. Apply the adapter's exclusive acquisition before owner/status updates, then re-read competing claims; an empty/unreadable local claim is a conflict. GitHub uses CLAIM, assignee/status and conflict re-query. On losing acquisition, undo only your own attempt, never the winner's state.
4. **Implement and verify.** Confirm behavior and names from actual source and direct contracts. Before implementation, map baseline requirements and affected paths to AC evidence, prepare regression tests or P's declared equivalent, and block unverifiable or out-of-boundary verification. Self-review is the default; record an independent-review determination only for an explicit exception. Start with direct/owning-module checks, widen on evidence, and obtain valid success for every P/Issue-required check and CI on the final candidate. Trivial uses suitable targeted checks, with no default build absent build impact. Required unknown/unrun/failed checks remain incomplete; optional QA is not a new AC.
5. **Candidate and review.** Re-read affected inputs when item, head or state changes. PASS applies only to unchanged verified inputs; test deletion, weaker assertions or excluded checks require impact assessment and visible replacement evidence/gaps. Re-run affected targeted and invalidated required checks, not every check automatically, and do not label reuse a new run. After valid final verification, inspect the complete changed-file inventory and all relevant diff hunks without dumping the whole diff, then self-review baseline requirements, scope, AC, failures and risks. Changed candidates require affected verification and renewed final review.
6. **Documents and writing.**
   - **Document synchronization.** Inspect direct user/background entry points and update only changed business rules in directly affected existing documents from final code before final verification; resolve competing document edits first. No behavior change means no synchronization document.
   - **Writing.** Explain change, checks and remaining issues briefly in the project's language, preserving identifiers and original tool output; use a table/diagram only when it aids understanding, with no extra writing-quality gate. Read UTF-8 first, use the current shell and structured/portable input, and never change permanent host settings to work around failures.
   - **Evidence hygiene.** Retain source ID and revision/provision time for requirements, and content/scope/decision-maker/time/source for decisions. Exclude protected data and conversation/reasoning transcripts or reconstructable summaries, use synthetic reproductions, and verify saved content; remove prohibited material by an authorized method or notify a human.

## Three-record lifecycle

Use the declared adapter's compact grouping. Three authored records is the normal path, not a cap on failures, corrections or real handoffs. Each field preserves its actual time, identity and evidence; grouping does not move an action earlier.

1. **CLAIM** combines ownership (`agent`, `branch`, `allowed`, `forbidden`, for both trackers) with start facts: task, selected W commit (legacy pin if applicable), base, current requirement sources and durable record location. Detailed document/support/interval inventories are only for methodology evaluation. No mandatory prior closed-task search or absence statement; directly linked known defects and dependencies remain ordinary inputs.
2. **IMPLEMENTATION SUMMARY** combines `closes`, branch/head/base, AC results, commands/results (including reused and unrun checks), final self-review, decision compliance/deviations, human decisions raised, remaining risks and CLAIM reference. Preserve real incidents briefly with reference, owner, first failure/evidence and action/result; no empty lists, normal-step rows or automatic counting of expected failing tests. Attach source/scope/limits only to figures and events actually reported, distinguishing facts, hypotheses and non-collection. No routine model line, missing-cost inventory, support evaluation or next-method judgment. Explicit model/method/cost evaluation activates its owner; never search host transcript/config folders on this route, even then.
3. **CLOSED** has separately labelled `merged`, `closed`, `product-complete`, `cleanup` and `release` fields. Use the following sequences and the declared adapter's mapping.

### Merge and closure

1. Immediately before authorized merge, re-query metadata, target, mergeability, required checks and reviews. P retains merge authority. GitHub PRs state their base explicitly. Missing local-docs merge method or unverifiable mergeability blocks merge.
2. Fetch the target after merge. Verify the actual merge and closing reference with the adapter before confirming closed status. Keep merge-result SHA separate from fetched tip. Squash/rebase checks use the observed merge-result identity later stored as `CLOSED.merged.main`, not the task head or fresh tip.
3. Confirm closure through the adapter. For local-docs, update and read back closed Meta after successful merge verification and the matching closing reference.
4. Establish product completion and preserve the adapter-specific PRODUCT COMPLETE JSON once, independently of cleanup. Group the actual earlier times and evidence into CLOSED in the cleanup/release sequence below.

No `observation-check unavailable reason=not-shipped` placeholder is required here. Preserve actual check/re-run results, first output, reason, final output and any loss when such a check was performed.

Before deleting a work folder, re-read durable CLAIM/SUMMARY and required non-sensitive worktree-only evidence once, recording retrieval failures/loss without making observation gaps a new product gate. Before handoff, stop or post-merge cleanup/release, record uncommitted/unpushed state, PR state, worktree registration and local/remote branch state in one short line; unfinished work adds precise paths, blocker, resume condition and references. Do not delete an unmerged handoff worktree, create a new start because ownership changes, or automatically re-query an unchanged blocker.

### Cleanup and release

1. Before cleanup, inspect uncommitted, untracked and ignored content and other worktrees. Delete only authorized task-owned artifacts.
2. If required cleanup fails, preserve product completion, record cleanup/release incomplete in CLOSED and retain ownership.
3. After successful required cleanup, re-check ownership under the matching claim. Append CLOSED with actual earlier merge, closure, product-completion and cleanup times/evidence and release **preparation**.
4. Clear only owned metadata and verify removal. For local-docs, delete the matching exclusive claim last, then verify absence. For GitHub, end the exact CLAIM through the adapter's terminal `CLOSED.release` update, then re-query the release and metadata. Preserve historical comments.
5. Report success only after observed release. A preparation field is not proof of deletion or terminal release. On failure, preserve product completion, report release incomplete and append a correction even if it exceeds three records.

Local-docs entries remain append-only with author/time/unique ID, immediate pre-append re-read and post-append ID check. Corrections reference/supersede the original, never rewrite it. GitHub may update its existing comment with later facts and times.

The final report reuses SUMMARY: changed files, each requirement's status, checks/results, unrun checks/reasons and blockers. Failed/unverified AC prevents whole-product completion; observation gaps, optional QA and local cleanup failures have separate statuses. End this task's scope; another task/area/method needs fresh selection/session.

## Exception triggers

Read only the relevant owner sections when triggered; preserve the compact substitutions above and explicit P requirements.

| Trigger | Owner and action |
| --- | --- |
| Competing claim, concurrent actors, creating another checkout (including external dedicated harness connection) | [parallel-development](../skills/parallel-development/SKILL.md), New lane creation and isolation / Claim; confirm shared tracker, checkout connection and short Windows paths; never let two agents commit on one branch |
| Relevant base/merge-branch changes | [Synchronization](../skills/parallel-development/SKILL.md#synchronization); sync before next push, resolve only allowed paths and re-run affected verification; stop for forbidden/shared-path conflicts |
| Shared contract, root/integration path or changed boundary, even in one module | [module-boundaries](module-boundaries.md); boundary decision, integration dependencies and re-grading before expansion |
| Escalation, required independent review, SDD, another actor or higher-risk phase | Relevant full [implementation](../skills/implementing-issues/SKILL.md), [verification](verification.md), [finishing](../skills/finishing-issues/SKILL.md) and routing contracts; unresolved findings still block |
| Before declared build, test or cleanup commands | Applicable [build-preflight](../skills/_shared/build-preflight.md) and [Verification environment](verification.md#verification-environment), reusing unchanged checks; only JVM builds need launcher/daemon JVM checks; retain process-only corrections, bounded discovery and no arbitrary install/download/permanent settings |
| Required manual/device/runtime check, temporary/none test policy | [Verification Strategy](verification.md#verification-strategy); actual target/procedure/expected and observed result, confirmer/time/target identity; preserve and re-query temporary evidence before deletion; none does not waive required checks |
| Premise error, changed AC or policy transition; unresolved phase dependency | [plan-change](sdd/plan-change.md) / [Issue dependencies](sdd/issue.md); correct the current item and existing records with prior instruction, reason, decision reference and effective time, refresh affected checks/review; no separate transition document or question ledger |
| Reference implementation, external consumer or dependency-version behavior affects judgment | [AS-IS investigation](sdd/as-is.md), Investigation needed for judgment; check the relevant revision/version without creating an SDD solely for investigation |
| Changed processing order, one input branching into multiple paths, asynchronous flow, AC with multiple-state transitions, or call order across three-plus components | [Mermaid creation conditions](issue-writing-guide.md#mermaid-creation-conditions); a short condition table or input-to-result examples may replace Mermaid when they show the same paths clearly. Trivial may explain existing flow; changing its behavior requires re-grading |
| User-visible UI/UX change or explicit screen-design request | [Visual artifacts](#visual-artifacts) below and [HTML creation conditions](issue-writing-guide.md#html-visual-spec-creation-conditions) |
| Existing code/document drift or business-document lifecycle exception | [Business document update](sdd/completion.md#business-document-update) / [module-boundaries](module-boundaries.md). The 150-character split/review-topic rule is Medium+ only; use line breaks/lists in the existing compact document, not length-triggered new files |
| Explicit project review topic | [reviews](reviews/README.md); an existing Issue decision section suffices when P permits, preserving proposals/reviews/decisions and required approval; grade alone does not create a topic |
| Removing any registered local worktree | [Merged local worktree cleanup](../skills/parallel-development/SKILL.md#merged-local-worktree-cleanup); check cleanup exceptions, Windows requirements, unknown residue, and registration/folder absence separately; no forced removal or bulk residue workaround |
| Declared impact-result consumption | [execution-packets](../skills/_shared/execution-packets.md), impact result consumption; check freshness/completeness, never narrow required verification |
| Explicit methodology/model evaluation or actual recurring problems needing method judgment | [observations](observations.md) and M adaptation for the requested judgment only; no automatic new Issue, model run or policy-change authority |
| Explicit cost evaluation of this Trivial/Small task with token diagnostic ENABLED | [token-diagnostic](token-diagnostic.md); ordinary compact work is exempt even when mode is ENABLED; only authoritative available values, no estimation/search, no completion gate |
| Explicit BUILD-PREFLIGHT-DIAG | [Conditional diagnostic mode](../skills/_shared/build-preflight.md#conditional-diagnostic-mode); one non-sensitive record, no added searches/re-runs without the keyword |
| Encoding or shell failure | [agent-instruction-policy](agent-instruction-policy.md), UTF-8 / shell procedures; bounded fallback, no broad host/repository search |
| Reprioritization or actual queue selection | [issue-priority](issue-priority.md), Priority change / Order within the same Priority, using the compact fields |
| Workflow/skill/eval behavior change | Project `skill-evals.md` and [skill-evals](skill-evals.md); update directly relevant cases, required static checks and authorized isolated evaluations; full corpus only when requested |

## Visual artifacts

- **Artifact selection.** Honor explicit HTML requests. Otherwise, a project-permitted simple screen artifact/state table may substitute. Do not invent HTML without a declared repository.
- **Pinned reference.** Required Visual Spec uses an accessible commit-pinned link before implementation. Issue owns function; HTML owns UI. Validate the fixed artifact and access.
- **Optional publication and cleanup.** No separate design PR/deployment is required by default on this route. Actual publication retains disclosure/check/merge authority rules and no app-closing Closes in design PRs. Any created design branch/worktree follows the owner's link-preserving cleanup.
