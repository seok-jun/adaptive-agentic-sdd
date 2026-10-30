# Execution routing

The inputs are the M, W and P paths stated in the entry file. The external installation path is an option of the installer, not a separate execution role. First check the model restrictions, impact analysis and probe conditions in P's application document `W/../project/execution-routing.md`.

Read this for the current/manual qualification check when entering or keeping the current phase/role, for model/reasoning selection, and for switch/delegation or reviewer assignment. Reuse evidence that is still valid for that role in the same run, and do not skip the qualification check because there is no model switch. It is not a fixed pre-read input. If you only need to write, receive or validate a packet, read the relevant section of [Execution Packet and handoff contract](execution-packets.md).

## Contents

- [Two-axis routing](#two-axis-routing)
- [Host Capability Map](#host-capability-map)
- [Model Role Qualification](#model-role-qualification)
- [Qualification probe exception](#qualification-probe-exception)
- [Execution Profile](#execution-profile)
- [Packet and impact result handoff](#packet-and-impact-result-handoff)

## Source of Truth

W owns the common routing/qualification contract, and P owns the profile it applies, explicit model restrictions, permissions and local impact analysis inputs. The packet's Source of Truth, guard application and freshness validation are owned by the [handoff contract](execution-packets.md#source-of-truth).

## Two-axis routing

The grade sets only the orchestration shape.

| grade | orchestration |
| --- | --- |
| Trivial / Small | One current agent completes it without model switch or delegation; if the current concrete model is role DENIED, replace it with one qualified replacement |
| Medium | A single agent is the default; only an actual unresolved PLAN decision or a required independent review phase gets bounded delegation |
| Large | The root/orchestrator owns the design and boundaries that passed review, and may delegate only the coarse-grained `PLAN / IMPLEMENT / REVIEW` phases |

An Epic is an optional management unit separate from the execution grades above. Its owner coordinates the goal, guidance, work breakdown, dependencies and overall completion, and each child execution Issue is routed by its own grade. Creating or breaking down an Epic does not require a separate worker, independent reviewer or model selection, and doing it as a single Large is also allowed.

Phase risk and decision complexity set the abstract tier.

- model tier: `current | cheap | strong | frontier`
- reasoning tier: `current | medium | high | extra-high`
- Do not store vendor/model names in canonical documents as tier mappings or price information. However, a canonical safety deny that blocks use before qualification may state a stable normalized model identifier.
- `current` is not a capability rank; it means the currently running model/reasoning. For capability comparison, use only the rank `cheap < strong < frontier`. A `current` choice is judged separately by whether fresh current-model capability evidence meets that phase's floor.

| phase/risk | minimum model tier | reasoning tier |
| --- | --- | --- |
| approved mechanical IMPLEMENT | cheap | medium |
| TEST_DOCS | cheap | medium |
| ordinary Large IMPLEMENT | current | high |
| required independent REVIEW | strong | high |
| PLAN with a competing design choice remaining | strong | high |
| destructive/shared-contract/migration/security/authority/recovery/atomicity PLAN | strong | extra-high |
| A high-risk phase above that is still unresolved at strong | frontier candidate | extra-high |

`frontier` is forbidden by default. It becomes a bounded candidate only when there is both stated high-risk escalation evidence and evidence that the strong tier did not resolve it, and it is never chosen automatically. A compile failure, a command typo or a fixture correction is not risk escalation evidence.

Fallback does not change the order below. Distinguish the qualification rules for **a current/manual model that is already running or that the user explicitly chose for the current phase** from those for **a candidate the Agent switches to or delegates to automatically**.

1. Fix the orchestration shape by grade.
2. Fix the minimum capability floor by phase risk.
3. For a current/manual concrete model, first decide the canonical safety deny and the actual explicit record with the current/manual rules of [Model Role Qualification](#model-role-qualification) below. If those conditions and fresh Host Capability evidence meet the phase floor, keep the current/manual route.
4. If an explicit model/tier in the Execution Profile requires a switch from the current model, or the Agent automatically chooses a worker/reviewer/fallback concrete model, a **fresh qualification PASS** for that development role is needed.
5. If an automatic candidate's tier is at or above the floor and it has a fresh role qualification PASS, use it.
6. If there is no explicit fallback or it is not eligible, search deterministically the remaining fresh host mappings at or above the floor, starting from the lowest eligible tier, and require a fresh role qualification PASS for each automatic candidate. `frontier` is not included in this fallback without the existing escalation evidence.
7. If automatic selection is needed and every capability candidate is role-ineligible, it is `BLOCKED: model role unqualified`; if no capability candidate can be proven at all, it is `BLOCKED: routing capability unavailable`.

A profile and fallback cannot downgrade below the floor. Do not guess a concrete model/tier that does not exist or whose support is not confirmed. **Do not require in advance, as a precondition, the concrete model qualification of a future phase not yet entered.** Validate it just in time with the rules above, right before checking the actual current/manual model in that phase or choosing a switch/delegation candidate.

## Host Capability Map

P's `routing.role_defaults` are preferred candidates, and `routing.capabilities` is the evidence reference for the host mapping. The fact that a human wrote it in a settings file alone does not prove capability, availability or role qualification. When choosing, check the host, concrete model, supported reasoning, source identity and validity period. For role qualification, use P's `qualification_records` reference or actual runtime evidence separately.

When the current or human-chosen model is not changed but inherited as is by a separate reviewer session, judge it as the current/manual path if the host confirms that the actual concrete model and reasoning are identical. Do not classify it as automatic model selection only because it is a separate session. If the Agent newly chooses the model or reasoning, apply the existing automatic selection qualification rules. If the host cannot confirm the reasoning, distinguish the confirmed requested value from the unconfirmed provided value. If floor compliance cannot be confirmed by fresh host evidence that the supported setting was actually applied, do not presume compliance; block that reviewer assignment. The separate actor/session and Human-selected B selection conditions are kept.

The runtime or host adapter owns the concrete mapping, and the canonical Skill consumes only the following schema.

- host identity
- supported model tiers
- list of concrete model identifiers per tier
- current concrete model identifier and current-model capability
- supported reasoning levels
- whether native model switching is supported
- whether native delegation is supported
- whether a separate reviewer/session is supported
- mapping source and version/immutable identity, freshness

Even without a mapping, if fresh evidence proves that the current model meets the phase floor, you may continue under the current/manual eligibility rules. If there is no native delegation but the current model meets the floor, the current agent performs IMPLEMENT directly, and this reason alone does not block the whole Large. A required independent REVIEW is performed in an agent/session separate from the implementer, regardless of whether IMPLEMENT delegation is supported. If the capability provenance is stale, do not use the concrete mapping; check fresh current capability evidence or block.

Host capability does not replace the role qualification of an automatic route and does not override a canonical safety deny. A current/manual route is not blocked by the mere absence of a positive qualification record, according to the bootstrap rules above.

For Medium/Large, if independent review is required and there is no separate reviewer agent/session capability, do not create a valid execution trace; stop with `BLOCKED: separate reviewer unavailable`. Validate the concrete model role qualification of a future reviewer right before choosing the actual review actor, not as a PLAN start condition.

As an exception, Review B of a Large AS-IS/PLAN is routed only after a Human chooses the concrete model and reasoning level. If there is no choice, do not search automatic reviewer mappings or fallback; it is `BLOCKED: blind-audit reviewer selection required`. This exception applies when P's `review.blind_reviewer_selection` is `required` (default). If it is `optional` and there is no Human choice, apply the automatic candidate rules above (fresh role qualification PASS, floor, separate session, `frontier` excluded) under the automatic selection conditions of [Large design review mode](../../process/design-review.md#large-design-review-mode). If `review.large_mode` is `single`, there is no Review B, so this paragraph does not apply. The chosen value must satisfy all of the canonical REVIEW floor of `strong + high` or above, supported reasoning, the canonical deny and independent-reviewer role qualification. If the chosen model/session cannot be used on the host or is not eligible, stop with `BLOCKED: selected blind-audit reviewer unavailable` without a silent fallback, and ask the Human to choose again. The Human's choice does not change `review-mode = blind-audit` or the requirement for a separate agent/session different from both the author and the Review A actor.

## Model Role Qualification

Role qualification evidence has a concrete model identifier, `PASS | DENIED`, a list of allowed roles, an immutable evidence identity and freshness. The target roles are:

- standalone Issue owner
- orchestrator / PLAN owner
- bounded IMPLEMENT worker
- TEST_DOCS worker
- independent reviewer
- finishing / PR / merge / release owner

Model Role Qualification is **not a universal positive allowlist in which every operating model must be registered in advance.** The canonical safety deny and explicit qualification results are enforced policy, and a fresh PASS is needed when the Agent automatically switches or delegates to a model.

- If an explicit qualification record is `DENIED`, the model cannot be used in an ordinary development role anywhere: current/manual, profile or fallback.
- If an explicit positive record exists but is missing, incomplete or stale, do not presume PASS, and do not bypass it by ignoring that record.
- A current/manual model without an explicit qualification record is not blocked by the mere absence of a positive registry if it is not canonical DENIED and fresh Host Capability evidence meets the current phase floor.
- The Agent does not choose an automatically selected switch/delegated worker/reviewer/fallback model without a fresh qualification PASS for that role.
- Validate the qualification of a future phase right before choosing the actual actor. Do not block the current phase by requiring, at PLAN start, a PASS link for a reviewer model not yet chosen.

For product-specific concrete denies and probe permissions, check `Model restrictions` in P's application document `execution-routing.md`. The common schema or a PASS does not relax these restrictions.

## Qualification probe exception

A blocked model is called, in a limited way, only in a separate qualification probe Issue that the user explicitly instructed, and only when all of these conditions are met: a synthetic/docs-only fixture, orchestrator-owned claim/isolation/lifecycle, a bounded `qualification_probe` role, no direct push to main and no Issue/PR/merge/release permissions, and preservation of raw observations. This exception is not a PASS for ordinary development roles and does not apply to ordinary product Issues.

For product-specific conditions, also check `Qualification probe exception` in P's application document `execution-routing.md`. W does not change product restrictions, qualifications, permissions or impact consumption.

## Execution Profile

The optional `## Execution Profile` in the Issue body provides, per phase, `model-tier`, an optional concrete `model`, `reasoning-tier`, optional `fallback-model-tier`/`fallback-model`, and `ESCALATION.only-if`.

- If there is no Profile, keep the current execution model/reasoning and the existing flow.
- A Profile does not override the hard guard, SDD gates, claim, allowed/forbidden, required verification or required review.
- The Trivial/Small single-agent policy takes precedence over multi-phase routes. However, if the current concrete model is role DENIED, replace it with one qualified replacement without increasing the number of actors.
- Keeping current/manual under a Profile, or choosing a model switch/delegation, fallback or reviewer, applies the [fallback order](#two-axis-routing) and [Model Role Qualification](#model-role-qualification) above.

## Packet and impact result handoff

After assignment, read only the contract needed at the point of creating or consuming a packet.

- Worker instructions and input checks before the first edit: [Execution Packet](execution-packets.md#execution-packet).
- Returning worker results and consuming results in finishing: [Result Packet](execution-packets.md#result-packet).
- Required reviewer input and result checks: [Review Packet](execution-packets.md#review-packet). For the Large review order and the proceed and stop conditions, also apply [Design review](../../process/design-review.md#large-design-dual-independent-review).
- Consuming impact analysis results P declared: [Common impact result reference and local consumption](execution-packets.md#common-impact-result-reference-and-local-consumption).

Fixture evaluation, serialization and token proxy measurement follow [Packet serialization and measurement in skill-evals](../../process/skill-evals.md#packet-serialization-and-measurement). Do not read it as a prerequisite input for operational assignment.
