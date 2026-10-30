# Execution Packet and handoff contract

The inputs are the M, W and P paths stated in the entry file. The external installation path is an option of the installer, not a separate execution role. Read this document only in the phase that writes, receives or validates a packet; it is not a fixed pre-read input. If model assignment or a qualification decision is needed, read the relevant section of [execution-routing](execution-routing.md).

## When to read and contents

- When composing worker instructions or checking inputs before the first edit: [Source of Truth](#source-of-truth), [Execution Packet](#execution-packet) and its guard, context and freshness validation.
- When a worker returns results or finishing consumes them: [Result Packet](#result-packet).
- When preparing a required review or checking its result: the relevant phase/mode of [Review Packet](#review-packet).
- When consuming impact analysis results P declared: [Common impact result reference and local consumption](#common-impact-result-reference-and-local-consumption).
- For fixture evaluation, serialization and token proxy measurement: [Packet serialization and measurement in skill-evals](../../process/skill-evals.md#packet-serialization-and-measurement). It is not a prerequisite input for operational packet handoff.

## Source of Truth

The precedence is `AGENTS.md hard guard > canonical Skill/process > current Issue + reviewed SDD/PLAN > Execution Packet`. The Execution Packet is a derived cache that does not replace the higher sources. If it conflicts with a higher source or cannot prove provenance/freshness, do not execute that packet item.

W owns the common packet contract, and model assignment, tier, qualification and the number of actors per grade apply the contract of [execution-routing](execution-routing.md) as is. Do not change the model restrictions, permissions or impact analysis conditions P declared through a packet.

## Execution Packet

The Execution Packet is not the whole bundle of sources; it is a cache that carries decisions the orchestrator has already made. The minimum fields are:

- issue identity: id, title, snapshot identity
- phase, recommended model tier and reasoning tier
- reviewed PLAN reference and immutable identity
- goal
- allowed paths and forbidden paths
- required public contracts
- already-resolved decisions and immutable references to their key reasons
- failure/recovery conditions or explicit not-applicable evidence
- context transition: actual host capability evidence, the method used, execution evidence, minimum input references, fallback reason and limits (when applicable)
- target paths/symbols
- phase acceptance criteria
- required verification
- whether review is required
- PLAN implementation finding handoff identity and resolution expectation list
- known blockers
- escalation conditions
- provenance: references and immutable identities of the hard guard, canonical process and direct contracts
- immutable evidence of the SDD grade gate and the claim
- immutable guard application evidence object for host-enforced propagation or worker direct-read

If there are P code conventions to apply, connect the document, section and identity (or check time) in the provenance, and hand off the PLAN's explicit departures/exceptions with them. If none is declared, mark that fact, and do not force a new conventions document. In known blockers, connect [the owner and needed phase of open questions](../../process/sdd/issue.md#open-questions-and-phase-dependencies), and do not expand an open question of a future phase into a blocker for the whole current work.

### Guard application and common packet validation

If the standalone/subagent runtime does not guarantee guard propagation, the worker reads the needed hard guard section of `AGENTS.md` directly.

Guard application evidence must be an object with `kind`, `reference`, the `source identity` of the applied hard guard, and the immutable identity of the evidence itself. Missing, empty or malformed evidence is `INVALID`; an identity/freshness mismatch with the current source is `STALE`. Both fail closed and proceed only by a direct read of the hard guard or `BLOCKED`. A boolean such as `runtime_guard_propagation: true` or `guard applied: true` is not evidence.

Issue snapshot, PLAN identity/reference, goal, allowed/forbidden, required contracts, phase acceptance, verification, escalation, provenance identity and gate/claim evidence must exist and be nonempty down to nested fields. `implementation_findings` is an explicit list, and it may be empty only when the PLAN that passed review has no handoff. If there is a handoff, each item's stable identity, PLAN exact target and resolution expectation must be nonempty; a missing one is `INVALID`, and a mismatch with the current PLAN identity is `STALE`. A missing, empty or malformed required field is `INVALID`. If the packet conflicts with a higher source, discard the related instruction and do a bounded refresh of only the needed canonical source. If freshness cannot be proven, it is `STALE`; after a bounded refresh it becomes `VALID` with new provenance, or `BLOCKED`.

The following events invalidate only the related items.

- Issue body/labels change
- reviewed PLAN artifact change
- base/head/ref change of a direct contract
- discovery of a new direct dependency not in the packet
- compile/test failure that contradicts an architecture assumption
- an active lane/path conflict arises
- hard guard/canonical Skill version change

If such an event is a plan premise error or a policy change during work, correct the source first with [Plan correction and policy transition](../../process/sdd/plan-change.md#plan-correction-and-policy-transition). Do not cover a conflict with the existing PLAN or policy by editing only the Packet. Connect the source to apply now and the needed re-review evidence in the new Packet.

### Context and freshness check at implementation entry

The Execution Packet does not create a new layer; it connects handoff evidence to existing fields. When switching from a Large PLAN that passed review to IMPLEMENT, if the host supports it, choose a separate implementation context even for the same model. Use an actual fresh session/agent or a verified compaction, and do not change the model tier/qualification/number-of-actors-per-grade rules. Record which of the host-supported `fresh-context`, `verified-compaction` or `direct-fallback` was actually performed, with execution evidence. A compaction succeeds only if preservation of the required inputs and a comparison with the current sources are verified. For no support or a compaction failure, leave the reason, the minimum input references and the limits of the history that actually remains, implement directly, and do not mark it as a successful separation. Do not treat as success the mere running of a conversation command in a shell or the declaration of a switch. Failure to recover a required source is `BLOCKED`.

Before the first edit, compare the current Issue snapshot, the PLAN identity, the claim, the guard and the direct contracts. Large has no source of human approval at the design phase; connect the exact target and Decision scope of the reviewed PLAN. If the PLAN differs, it is `STALE`. Detect missing implementation findings by comparing with the list of the PLAN that passed review. A missing resolved decision reason, failure/recovery, verification or required review is also INVALID. A mismatch with the current source is STALE, and only the related source gets a bounded refresh. Conversations, multiple design versions and full tool logs are not the default payload; immutable source references take precedence.

Connect the problem, premises, invariants and remaining risks of the README that also apply in a separate IMPLEMENT context, through the needed sections and baseline revision, to the existing direct contract/provenance and failure/recovery references. Medium implementation entry also consumes the same related inputs, and does not require a new field or reading the whole README in advance. Distinguish the contract of the current execution from history needed only for re-investigation or audit, and check that the required evidence is accessible and fresh. Pass only the allowed inputs per phase/mode below in a Review Packet, and do not use this connection to bypass the Blind Audit isolation of results and history.

The receiver does not edit until it proves validity through a bounded refresh of only the needed sources. Return only the Result Packet and the needed change and verification evidence to the root, and do not re-merge the full worker log. Do not retroactively reset the session/branch of a lane already in IMPLEMENT because of this rule.

## Result Packet

P's verification declaration follows the [verification contract](../../process/verification.md#verification-strategy). The code+fixture/test resolution evidence below may include equivalent behavior observation evidence that P declared, but it must prove the finding's resolution expectation at the current head. A temporary test connects its preservation location, test/fixture hash, the product input identity at the time of the run, and its correspondence to the final candidate. Do not omit evidence because the file is not in the current product tree.

A manual verification item uses `method: manual`, the checker, the check time, the procedure and the actual observed result instead of a command/exit code. Do not invent a command that was not run. The remaining requirements (target commit, immutable evidence identity, input invariance/reuse, required verification result) are the same as for automatic verification; only the command/exit code of a manual item may be absent.

If a worker/reviewer of any phase found an actual problem, include in its existing returned result the incident information/source references according to the conditions of P's application document `W/../project/sdd-workflow.md` and [Recording problems found and linking them to closure](../../process/observations.md#recording-problems-found-and-linking-them-to-closure). Start and handoff observations connect [Consumption and recording by observation point](../../process/observations.md#methodology-application-and-improvement-observations). This conditional incident information is separate from the required `implementation_findings` and acceptance/verification below, and is not a new packet validity gate.

An IMPLEMENT worker returns the following fields instead of full reasoning or a full command log.

- base SHA and head SHA
- changed files
- the full changed-file inventory of the current head or its immutable reference
- current diff/patch immutable reference
- `PASS | FAIL | BLOCKED` per acceptance criterion
- per verification item: execution commit SHA, command, exit code/outcome, evidence kind, immutable evidence identity/reference
- scope drift
- unresolved decisions
- escalation evidence
- compact diff summary
- new direct dependencies
- freshness issues
- PLAN implementation finding handoff and per-item current-head resolution evidence

The command, exit code and outcome of verification are metadata and are not PASS evidence by themselves. The immutable evidence identity is a CI check/run identity or the stable identity/content digest of a same-run host tool-result, and it must be bound to the **actual execution commit SHA**. If the execution commit differs from the commit of the evidence identity, that item is `STALE`. The Result base/head, inventory and diff reference must match the current review target; a mismatch or incompleteness is `STALE` or `INVALID`.

Verification whose execution commit differs from the Result head is reused only when the input invariance condition of [PASS validity](../../process/verification.md#verification-sequencing-and-pass-validity) is proven. Connect to that verification item the original execution commit and immutable evidence identity, the current Result head, the full change inventory/diff reference between the two revisions, and the invariance evidence for the inputs that command consumes or asserts, and mark it as **reused**. The CODE reviewer and the closing owner check that difference and the direct evidence. Do not judge input invariance only by a self-reported boolean, the same branch or command, or document file extensions.

Do not change original execution evidence as if it were newly run at the current head. If an input changed or invariance cannot be proven, leave it `STALE` and rerun in the verification contract's order: targeted → the invalidated required commands on the stabilized candidate. This reuse condition applies only to verification items; it does not exempt the current diff and inventory or the current-head code+fixture resolution evidence of PLAN findings.

The changed files, acceptance map and verification list must be nonempty. Scope drift must be a boolean, and the unresolved/escalation/dependency/freshness fields and `implementation_findings` must be explicit lists. If the PLAN has no Implementation finding handoff, use an empty list. If there is a handoff, each item has the finding identity, the exact target of the PLAN that passed review, the resolution expectation, `resolved | unresolved`, and a code evidence identity and a fixture/test evidence identity bound to the current head. A missing PLAN handoff item, missing code or fixture evidence on either side, a mismatch between evidence and the current Result head, or an `unresolved` item is not judged complete. Each verification item must have an immutable evidence identity bound to the same commit as its execution commit. If a required field is missing or empty, or there is an acceptance `FAIL/BLOCKED`, scope drift, an unresolved decision or a freshness issue, it is not judged complete.

## Review Packet

This section owns the review input and output fields and their validity. Large severity judgment, reviewer selection and independence, A/B order, blind isolation, reconciliation and the conditions for proceeding to the next phase follow [Large design dual independent review](../../process/design-review.md#large-design-dual-independent-review). Review and stop after a change apply [Design re-review by meaning and impact](../../process/design-review.md#design-re-review-by-meaning-and-impact) and [Switching on repeated stalls](../../process/design-review.md#switching-on-repeated-stalls).

Every required review packet has `review_phase: AS-IS | PLAN | CODE`, `review_mode: contract-review | blind-audit | reconfirmation`, an exact remote target identity and reviewer/author identities. Do not force an artifact that does not exist in the phase as a nonempty field.

### Contract Review Packet

The inputs of Review A and the default CODE reviewer are limited per phase.

- `AS-IS`: current Issue id/title/acceptance, AS-IS artifact path and remote-resolvable exact SHA, remote base/head, target inventory or immutable reference, direct contract/source evidence, document author identity
- `PLAN`: current Issue id/title/acceptance, reviewed AS-IS identity, PLAN and change-plan artifact paths and remote-resolvable exact SHA, remote base/head, target inventory or immutable reference, needed direct contracts/evidence, document author identity
- `CODE`: current Issue acceptance, reviewed PLAN identity, base/head SHA, the full changed-file inventory of the current head or its immutable reference, the current diff/patch reference and the needed diff hunks, needed public contracts, verification evidence identity, implementation actor identity, PLAN implementation finding handoff and per-item code+fixture resolution evidence

In the direct evidence of AS-IS/PLAN, connect [the investigation evidence and remaining premises](../../process/sdd/as-is.md#investigation-needed-for-judgment) that drive the judgment. PLAN/CODE include references to the declared P conventions and the reasons for departures and the evidence for exception decisions. The reviewer compares the applicable criteria with the actual instructions/changes, and does not turn personal preference into a new contract. The owner and needed timing of open questions are reflected in the dependencies of the next work, regardless of whether the reviewer found them.

The required fields of the phase must be nonempty down to nested values. The Contract reviewer does not trust the provided list as is; it independently checks the phase target/inventory, then reviews the bounded artifact/diff and contracts. The CODE reviewer independently checks the full changed-file inventory of the current head, and checks whether every Implementation finding identity of the PLAN was handed off and whether each item's code+fixture evidence proves actual resolution at the current head. If there was no handoff, an empty list is allowed. The reviewer identity must differ from the document/implementation actor. Do not expand the check into solution discovery, a repository-wide search or a full-source handoff. If the target/head, inventory, diff or implementation finding resolution evidence differs from the applicable current target, treat the review as `STALE`. Verification evidence is checked together with the actual execution identity of the Result Packet above and the needed input invariance and reuse evidence; if those conditions are not valid, treat it as `STALE`. If there is a missing handoff or an unresolved item, the review is not judged complete.

### Blind Audit Packet

Pass the following minimum inputs only to Review B of a Large AS-IS/PLAN.

- Issue id and title
- `review_phase: AS-IS | PLAN`
- `review_mode: blind-audit`
- target artifact path and remote-resolvable exact SHA
- the upper goal and the direct ownership boundary
- `solution implementation/repository-wide redesign forbidden`
- the request `search for missing facts, hidden assumptions, scope/boundary-changing omissions or blocking risks`
- the document author and Review A actor/session identities, provided only as metadata to prevent overlap

The first packet does not include the Review A verdict/findings/detailed Contract Review Packet or the details of earlier Review B findings. The reviewer may check callers/consumers/contracts directly adjacent to the exact target, but does not expand into full solution discovery. If the target identity differs from the current candidate, or the actor/session separation from the author/Review A cannot be proven, it is `STALE` or `INVALID`.

#### Blind input preparation and check

Prepare the materials given to the first blind review separately from review results. Do not pass a mixed file whole and only tell the reviewer not to read its later part. The remote exact candidate publication conditions are kept; the copy below is a delivery format of the published original text, not an exception that admits a local-only candidate.

1. Fix the needed scope of the target artifact, the Issue body, the upper goal and the direct contracts/conventions. The author first checks whether A/B verdicts, finding IDs or review-derived explanations are mixed into the original text itself. Keep human decisions and substantive constraints, open questions and failure evidence, and separate only the identifying/evaluative information of review results. If the content needs correction, correct and publish the source and apply the existing re-review by impact. Do not change the meaning of the review by arbitrarily summarizing or deleting only the copy.
2. Provide an immutable copy, or an equivalent restricted query, that records the source's remote, exact commit and path, the selected body/line range, and the hashes of the source and the output. Do not use a method in which the whole file, records or commit messages first appear in the tool output and are filtered afterward. local-docs uses the body boundary of [Review input](../../tracker/local-docs.md#review-input). Records are preserved in the source and are not deleted for the review.
3. Pass the reviewer the review material root and the fixed manifest identity, and do not include the source's history, feedback or review records in the input root. Check the location and scope readable from the actual reviewer's OS account/host. If the host provides access restriction, use it, and record in the Packet the scope actually enforced separately from the scope restricted only by instruction. Do not claim that a hash match alone proves OS isolation or absence of semantic leakage.
4. If additional direct evidence is needed before the first verdict, prepare and validate it with the same exact revision and the same result-exclusion conditions, and add it. If a required direct contract cannot be checked because of the material restriction, do not PASS before the scope is supplemented. Also record the additional manifest identity, and do not silently overwrite the existing input.
5. If earlier review results are exposed, record the first blind run as invalid, fix the input and restart with a new separate session. Do not continue on a self-report that the exposed content was forgotten. A later `reconfirmation` may receive earlier findings, but is not marked as the first blind review.

[review_snapshot.py](../../../tools/review_snapshot.py) may be used to extract Git material. It reads the UTF-8 source blob directly to preserve bytes, and `tracker-body` excludes `## Meta` and `## Records`. `artifact` is the whole file, so it does not automatically detect review results mixed into the body. The spec has the form `[{"path":"items/T-1.md","kind":"tracker-body"},{"path":"docs/plan.md","kind":"artifact"}]`, and specifies only the needed sources.

```text
python review_snapshot.py create --repo <source repository> --commit <full commit SHA> --spec <spec.json> --output <new material folder>
python review_snapshot.py check --repo <source repository> --bundle <material folder> --manifest-sha256 <create output digest>
```

The preparer performs `check` against the source and connects that evidence and digest in the Packet. Let the reviewer or a restricted verification means confirm the same digest and the correspondence to the source, but the verification command must not print the excluded original text. The tool does not overwrite an existing output folder, and `check` inspects the source selection, content changes and extra files. The folder does not become immutable at the filesystem level, so if it changes after delivery, do not treat it as the same input. A tool success does not replace the checks of remote publication, host access and content isolation.

The first verdict output has an immutable verdict identity bound to the exact target and a list of new findings. Each new finding includes a stable identity, one of the following severities, and exact-candidate evidence.

- `Human Decision blocker`
- `Execution-contract blocker`
- `Implementation finding`
- `Non-blocking observation`

The additional fields of the two blocker severities are the broken artifact/settled upper contract/direct-boundary invariant, and the meaning choice or conflicting decision meaning left to the implementer if not resolved before the next phase. The source for qualification, severity judgment, resolution location and handoff duty is [Large design dual independent review](../../process/design-review.md#large-design-dual-independent-review).

A separate reconciliation input passes the following to the same Review B reviewer/session at the time the protocol above defines.

- current exact target identity and initial verdict identity
- the stable identity and resolution expectation ledger of each earlier Review B finding

The reconciliation output has, for each earlier finding, `resolved | unresolved | regressed | not-applicable` and current exact-candidate evidence. Keep the new finding list of the first verdict and the results of the prior ledger as separate lists. If there is no earlier ledger, state reconciliation as `not-required`. Do not treat an earlier finding as an automatic PASS; the final PASS and the conditions for proceeding to the next phase follow [the proceed conditions of Design review](../../process/design-review.md#large-design-dual-independent-review).

### Follow-up reconfirmation and repeated stalls

Re-review dispatch, keeping the existing target, and whether a new blind B is needed are decided with [Design re-review by meaning and impact](../../process/design-review.md#design-re-review-by-meaning-and-impact). The stall judgment, stop and resume conditions for the same finding/meaning conflict follow [Switching on repeated stalls](../../process/design-review.md#switching-on-repeated-stalls).

The `review_mode` of the existing Review Packet distinguishes the first `blind-audit` from a later `reconfirmation`. A later packet includes the previous/current remote target identity, the full change inventory/diff reference, prior finding identities and resolution expectations, the affected contracts, acceptance criteria and direct consumers, the evidence for no impact, and the current-target reconfirmation evidence. The reviewer independently checks the inventory and the accessibility of surrounding sources. Missing required evidence is `INVALID`; merely renaming a previous target's result as current is `STALE`.

Connect to the current review evidence the immutable identity of the first blind verdict, the later chain of target differences/impact/A·B reconfirmation, and direct evidence for the state of prior findings at the current target. On a stall, record in the existing packet the area/conflict identity, the fix and reconfirmation target and evidence, and the causes and options. Filling in packet fields alone does not turn an unresolved blocker into a PASS.

## Common impact result reference and local consumption

For the conditions, check `Impact analysis` in P's application document `execution-routing.md`. If P declared no impact analysis tool, this section does not apply. W does not change product restrictions, qualifications, permissions or impact consumption.
