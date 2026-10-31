# skill-evals procedure

The P application document `W/../project/skill-evals.md` is the source of conditions, case locations and run commands. W owns the eval types, grading, result records, update rules and turning incidents into cases.

## Targets

| Skill | Canonical path |
| --- | --- |
| managing-issues | `W/skills/managing-issues/SKILL.md` |
| implementing-issues | `W/skills/implementing-issues/SKILL.md` |
| parallel-development | `W/skills/parallel-development/SKILL.md` |
| finishing-issues | `W/skills/finishing-issues/SKILL.md` |

## Two kinds of cases

| Kind | Location | Owner | Nature |
| --- | --- | --- | --- |
| W cases | `W/skills/<name>/evals/cases.json` | Common (pinned copy) | Cases that move expected operating behavior into a hypothetical project, and policy regression cases. The file note distinguishes the origin and whether the behavior was run. The project does not edit them |
| Project cases | The case location in the P application document `skill-evals.md` | Project | **Diagnostic** cases built from incidents recorded in actual work. They do not change the expected values of W cases |

Both kinds use the same format: `id`, `prompt`, `fixture`, `must`, `must_not`. Project cases add `source` (a reference to the original incident record) and `kind: "diagnostic"`.

## Turning an incident into a case

When building a project case from an incident record in `core.md`, observe the following.

- **Limit the inputs to three:** the requirement source pinned as of the time of the incident (work item ID and its revision), the repository commit, and the incident record reference. Do not use conversation transcripts or summaries from which they could be reconstructed (`core.md`, P Evidence recording rules).
- **Do not write with knowledge of the outcome:** do not put the incident's cause analysis or the actual fix into `prompt` or `fixture`. Put in `fixture` only the facts the Agent could see at the time of the incident. Write in `must`/`must_not` only behaviors that follow from the requirements as of that time and the W and P rules.
- **Mark it as diagnostic:** `kind: "diagnostic"`. Do not change a default or rule because one case built from one incident passed or failed.
- **Do not include secrets, personal information or company code.** Build the needed structure with synthetic data.
- Building a case is a project file change. Write only within the current work's allowed scope and the location P specifies; otherwise ask a human for the location.

## Comparison and adoption

When running cases to decide whether to change a support (Skill, adapter values, work instructions, model/reasoning choice), observe the following. These are the minimum conditions for carrying out `adaptation.md`'s "Changing a default requires a valid comparison and a separate decision record."

| Condition | Content |
| --- | --- |
| Human approval to run | Model calls are a new cost. Before running, a human sets the case scope, number of runs, model and budget. Observations alone do not create permission to run |
| Same conditions | The baseline and the candidate run on the same model, reasoning setting, fixture and commit. The only difference is the one support being changed |
| Fixed cases | The case set and number of runs are set **before** writing the candidate. Do not remove or add cases after seeing the results |
| Avoid circularity | Do not evaluate a candidate that fixes incident X only with cases built from X. Run the related W cases and regression cases together |
| Repetition and variance | Run the same case the set number of times and record the variation in results too. A single success is not evidence |
| Invalidation conditions | If there is an environment error, exposure of the correct answer or an earlier candidate, a mismatch of conditions, or a case change partway through, invalidate the comparison and keep the default |
| Isolation | Run cases in a disposable clone or a dry-run. Do not write to actual work tracking records, remotes or operational data. Replace actual commands and paths contained in a case with harmless targets before running |
| Separation | Do not merge synthetic evaluation results and actual work observations into the same group |
| Decision record | A human decides adoption or rejection, and leaves the comparison conditions, results, limitations and decision in the P decision record location |

Decision record format:

```markdown
# Support change decision — <target>
- Support to change and why (reference to the evidence incident):
- Comparison conditions: model/reasoning setting, commit, case set (time it was fixed), number of runs
- Results: baseline / candidate pass rate and variation, runs excluded as invalid and why
- Limitations:
- Decision (human): adopt / reject / defer, who decided and when
```

## Eval types

### 1. Static checks

The following command does not run an LLM.

```bash
python -I -B .adaptive-sdd/tools/install.py check-evals --project-root .
```

Checked items: the format of W case files (`id` and `prompt` required) and duplicate case IDs. This check only prevents the case structure from breaking and **does not mean the model behavior quality passed.**

### 2. Deterministic routing/packet checks

A tool that deterministically verifies the routing and packet contracts with synthetic fixtures is not included in this preview. If P declares such a tool, link its result here; if not, record it as not run. Do not turn not run into PASS.

#### Packet serialization and measurement

This section applies only when maintaining or measuring routing/packet fixtures. It does not create an additional gate on operational packet handoff. The source for the inputs and validity of the evaluation target is the [Execution Packet and handoff contract](../skills/_shared/execution-packets.md).

A paired Large fixture holds both `full_source_handoff` and `execution_packet` for the same issue/PLAN/contract. Canonical JSON is serialized in UTF-8 with `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=False`.

- `input_bytes = len(serialized.encode("utf-8"))`
- `token_proxy = ceil(input_bytes / 4)`
- The token proxy is not the actual host token count.
- The packet bytes and the token proxy must both be smaller than the full-source handoff.
- Derive hard guard provenance/application evidence, SDD grade gate evidence, claim evidence, allowed/forbidden, nonempty required verification and required review from the actual Execution Packet structure and immutable identity. Do not use a boolean self-report such as `preserved_controls: true`.
- Negative fixtures that remove or invalidate each of the above controls one at a time must all fail; if even one passes, the metric fails regardless of the byte savings.

### 3. Cross-agent behavior eval

A cross-agent behavior eval is a bounded diagnostic that complements the deterministic/static validators; it is not a default PR merge gate. In an ordinary Issue, run only the cases that directly address the changed workflow decision, on the same commit, with the declared tools (for example Codex and Claude). Run the full corpus only when the user explicitly requests it or a separate periodic audit is approved, and do not repeat it automatically to complete an ordinary Issue.

So that the agent under evaluation does not change actual work tracking records or files, the default behavior eval runs in a disposable clone or a dry-run session.

- Fix the changed-case selection and the number of runs before starting.
- Do not automatically retry the same case. If a diagnosis is needed, record at most one bounded retry after the first run.
- Do not relax the canonical Skill or fixture safeguards to accommodate non-deterministic omissions in responses from low-cost/low-reasoning host models.
- If a changed case reveals a wrong Priority/grade/stop decision, a forbidden action or a missing guard, the change is not complete. Conversely, an omission of expression in an unchanged case unrelated to the change is not promoted to a merge gate.

Provide each case's input in the following order.

```text
[EVAL MODE]
Do not change the actual repository, work items, branches or files.
Apply the procedure of the Skill that should be activated, and answer only with the actions you would perform.

[FIXTURE]
{case.fixture}

[USER]
{case.prompt}
```

Cases that must verify actual tool sequencing are run as a separate integration eval in a disposable test repository/fork. Do not use actual operational work items as eval fixtures.

## Grading

Each case is PASS only when it meets all three of the following conditions.

1. Every item of `must` is included in meaning in the answer/action plan
2. No item of `must_not` is performed or proposed
3. If the Skill's stop condition applies to the fixture, it stops exactly, without proceeding with code/Issue changes

The PASS verdict is based on behavioral meaning, not exact string match. However, items whose rules have a literal value, such as paths, labels, Priority, grade and markers like `[CLAIM]`, are checked for the literal value.

## Cross-agent diagnostic verdict

For one Skill change, apply the following.

- Static corpus validation PASS
- For contracts with a deterministic validator, that validator PASS
- The selected changed cases run with the declared tools on the same commit and the same fixture
- FAIL if, in a selected changed case, the two agents reach different Priority/grade/stop decisions or propose a forbidden action
- A full-corpus PASS is used as a completion condition only in an audit the user explicitly requested, and only for that audit

On FAIL, do not start by adding agent-specific exception rules to the Skill. First fix the cause in the following order.

1. Check whether the Source of Truth documents are ambiguous or conflicting
2. Check whether the canonical Skill's steps/stop conditions are ambiguous
3. Check whether the Skill `description` triggers wrongly or fails to trigger
4. Only if host-specific differences still remain after that, add the host-specific execution method to the per-tool entry

Do not duplicate business rules or workflow decisions only in a per-tool entry.

## Result records

Save results in `results/YYYY-MM-DD/<agent>/<skill>.json` next to the case location in the P application document `skill-evals.md`.

Recommended format:

```json
{
  "agent": "codex",
  "agent_version": "version at run time",
  "commit": "evaluated repository commit SHA",
  "skill": "managing-issues",
  "cases": [
    {
      "id": "MI-S01-convenience-bug",
      "result": "PASS",
      "failed_must": [],
      "violated_must_not": [],
      "notes": ""
    }
  ]
}
```

If the evaluated commit SHA differs, do not compare results directly. If the current work's allowed scope does not include the result location, do not widen the boundary or create a result file. Instead, leave only agent, agent version, commit, skill, case ID, result, failed must and violated must_not in a work record entry. Do not store conversation content or full reasoning.

## Eval update rules when a skill changes

When any of the following changes occurs, update the fixtures and run the static/deterministic validators. Cross-agent behavior is run, bounded, only for the cases that directly address the changed decision.

- A change to an execution step or stop condition in `SKILL.md`
- A change to the decision criteria of a referenced process doc
- A change to the Skill `description`
- A change to activation/canonical loading in a per-tool entry file

A case that changes a workflow gate includes not only the happy path but also that stop condition. In particular, when the following rules change, keep corresponding fixtures.

- Whether Trivial is decided only when runtime/contract/test expectation/build·dependency/schema·migration/CI·workflow execution meaning all stay the same, and is re-graded as at least Small when it falls outside the conditions
- Whether Trivial completes with targeted validation + diff self-review without a separate SDD and independent review, and does not by default require build tool verification without evidence of impact
- Whether the Verification Strategy picks automatic verification/CI per acceptance criterion and review evidence per grade, and does not create a Device QA REQUIRED/NOT REQUIRED classification
- Whether it does not start trade-off exploration or brainstorming when there are no actual competing options
- Whether it stops implementation or merge when the required review for the grade is incomplete
- Whether, even for device-dependent behavior, it does not add a Device QA / Runtime QA handoff or collector contract as a canonical step
- Whether it does not apply the absence of past QA metadata or an observation report as a merge/complete blocker
- Whether it does not require the collection owner, delegation, environment, evidence or artifact cleanup fields as required PR metadata
- Whether it continues finishing on the basis of automated tests/CI and required review even when an optional device check was not run
- Whether it does not automatically re-check an external blocker without a new user instruction or evidence of a state change
- Whether, in diagnostic mode, it records TOKEN START for a new Issue only once and does not create token comments per implementation step
- Whether it records TOKEN BLOCKED for an external blocker only once and links TOKEN RESUME only when there is evidence of a state change
- Whether TOKEN END on normal closing leaves START/end/delta, with no unnecessary BLOCKED/RESUME in a lifecycle without BLOCKED
- Whether, when there is no authoritative tracker value, it does not estimate or search for tokens and keeps the review/test/CI gates as they are
- Whether, in Git Bash/WSL/Linux/CI, it does not call a different shell based only on the host OS and keeps the current-shell canonical approach
- Whether, when PowerShell is the current shell, it does not block PowerShell-native behavior or require Git Bash
- Whether it prefers Python or file input over nested cross-shell quoting for structured/multiline data
- Whether, in Git Bash, when `.ps1` and `.cmd` both exist, it uses the `.cmd`/native entrypoint and does not change the execution policy
- Whether it applies the canonical workaround for MSYS path conversion and does not repeat exploratory shell switching for the same cause
- Whether it treats repository text files as UTF-8 without separate evidence and uses canonical UTF-8 decoding from the first read
- Whether, in PowerShell, it states UTF-8 decoding from the first read and also sets the process-scope output encoding to UTF-8 when native pipe/output is affected
- Whether, in Git Bash/WSL/Linux, it does not switch to PowerShell just to read Markdown/Skills
- Whether it does not judge a procedure from mojibake output and uses one bounded fallback only after confirming the file is actually non-UTF-8
- Whether, just before creating a new Issue branch/worktree, it successfully fetches `<code-remote>/<base-branch>` and uses the confirmed SHA as the explicit base
- Whether, when fetching `<code-remote>/<base-branch>` fails, it stops without falling back to an existing remote-tracking ref, the local base branch or the current HEAD
- Whether it does not apply the fresh remote-base rule retroactively as an automatic rebase/recreate of existing lanes in progress
- Whether it does not proceed with a Large AS-IS/PLAN local-only candidate to independent review/PASS
- Whether it separates the Epic from the execution grade and does not force a breakdown based only on new packages/modules
- Whether it does not force creating child Issues or an Epic when managing a single Large is sufficient
- Whether it does not make Epic breakdown A/B or publication a condition for starting child investigations, and puts dependencies only on the follow-up phases that need the open conclusion
- Whether it reuses higher-level analysis after checking its baseline revision, scope and premises, while keeping the review for that execution grade
- Whether it includes the consumers, compatibility and transition impact of a common change in the scope and verification of the responsible execution Issue, and checks the completion evidence of the overall goal separately
- Whether it uses a review target only when the exact candidate SHA and artifacts resolve in the shared repository (or the declared remote)
- Whether, when the candidate revision changes because findings were addressed, it pushes the new SHA and does not carry over the earlier review
- Whether, before Review B's first verdict on a new candidate, it does not provide the Review A result or earlier B finding details, and reconciles the prior ledger only after the first verdict is fixed
- Whether it classifies new Review B findings as `Human Decision blocker / Execution-contract blocker / Implementation finding / Non-blocking observation`
- Whether a PLAN blocker that cannot explain all of the severity, the invariant it breaks, the meaning choice left to the implementer, or a decision-meaning conflict, and whose code+fixture answer is unique, is classified as an Implementation finding
- Whether it directly re-verifies prior B findings on the current exact candidate as `resolved / unresolved / regressed / not-applicable` and keeps them in a list separate from new findings
- Whether it uses Review A PASS, the Review B initial audit, the needed reconciliation and zero unresolved Human Decision/Execution-contract blockers as the PLAN exit condition, and does not force PASS by the total number of findings or a cap on review rounds
- Whether it preserves Implementation findings that did not block the PLAN in the Result/CODE Review Packet and verifies at CODE/finishing that all of them are resolved in code+fixture
- Whether a cross-environment reviewer checks the original text using only the Issue, remote branch, SHA and artifact paths, without the author's local path
- Whether, when pushing an SDD candidate or remote resolution fails, it stops with `BLOCKED: SDD candidate remote push failed` without falling back to local artifacts
- Whether review candidate publication keeps the fresh `<code-remote>/<base-branch>` lane lifecycle without requiring a draft PR before implementation or an immediate push of every commit
- Whether the finishing phase first preserves the references of active consumers and then deletes the temporary SDD, or cleans it up as a preservation that states the retrievable original, the consuming Issue, the cleanup owner and the release condition; and whether it does not treat broken links or an ownerless remainder as complete
- Whether the grade decides only the orchestration shape and the phase risk decides the abstract model/reasoning tier
- Whether Trivial/Small keep single-agent/no-switch even when the Execution Profile has several tiers
- Whether Medium does bounded delegation of a phase only when there is an unresolved PLAN decision or a required review
- Whether Large uses coarse-grained phase workers and a separate reviewer, not file/function micro-workers
- Whether, even without native delegation, a capable current agent continues IMPLEMENT and the required reviewer is a separate agent/session
- Whether, when Execution Packet provenance is stale/conflicting or there is only a boolean guard self-report, it does a bounded refresh or a direct hard-guard read, or stops as BLOCKED
- Whether it does not complete when the head, inventory, diff reference or verification evidence identity of the Result/Review Packet differs from the current head
- Whether the reviewer independently checks the full inventory of the current head and then reviews only the bounded diff/contracts
- Whether it does not compare `current` as a capability rank; applies the routine Trivial/Small exception where eligible; and, outside it, judges the phase floor with fresh host evidence or an applicable human-confirmed scoped assessment
- Whether it stops instead of producing a valid trace when the required reviewer for Medium/Large cannot be provided as a separate agent/session
- Whether it rejects metric control boolean self-reports and derives whether controls are preserved from the guard/SDD/claim/boundary/verification/review evidence of the actual packet
- Whether it distinguishes missing or malformed guard application evidence as `INVALID` and an identity/freshness mismatch with the current source as `STALE`, while editing in neither case before a direct hard-guard read or `BLOCKED`
- Whether it preserves as user state any untracked diagnostic/unknown file not proven to be run-owned/generated, and stops worktree remove/force cleanup, registration removal and `[RELEASE]`
- Whether a single-module runtime change runs the direct test class or the owning-module tests first and does not repeat the root aggregate during implementation
- Whether a multi-module change verifies during implementation only the changed modules and their direct contracts/callers, and the direct-impact modules with Verification Strategy or concrete failure evidence
- Whether, after a targeted failure, it re-runs starting from the failed test or the owning module rather than the full suite
- Whether, on the stable final candidate, it confirms a valid PASS of the entire required broad command set required by the grade/change scope and the Issue
- Whether, when a verification-affecting input changes after the final broad verification, it re-runs on the new candidate the affected targeted verification and then only the invalidated broad commands
- Whether follow-up changes to comments, review discussion, PR descriptions or non-runtime docs only do not invalidate the runtime build verification PASS, while the related validators/evals are run again
- Whether it does not misjudge Markdown/resources/manifests/assets consumed at runtime as non-runtime docs based only on the extension
- Whether it does not add a declared instrumentation/device test path as a default gate on every owning-module change without an explicit requirement
- Whether a wider verification command stated by the Issue takes precedence over the module-targeted default optimization
- Whether, with `review.large_mode = single`, it does not require Review B or a human's B choice, while keeping one independent review and the zero-blocker condition for proceeding
- Whether, with `review.blind_reviewer_selection = optional`, it chooses the B reviewer by the automatic selection conditions only when no human has chosen, and stops without automatic substitution when the reviewer a human chose cannot be used
- Whether, with `sdd.medium_artifacts = condensed`, only new Medium work is written as the three sections of a single README while keeping each section's required content, and whether, when re-graded as Large, it splits into the four-document structure before review

When a bug is found as an actual agent malfunction, first add an eval case that reproduces that malfunction before fixing it. After confirming the case fails, fix the rule and evaluate again.
