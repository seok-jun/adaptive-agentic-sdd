# Adaptive Agentic SDD

**Work-item-first · Risk-Gated · Progressive Disclosure · Revision-Bound Approval · Evidence-Based Completion**

Adaptive Agentic SDD is a practical workflow for AI coding agents. It combines specification-driven development, observed AS-IS analysis, risk-based review, bounded exploration, and evidence-based completion.

> Apply the minimum process that reliably prevents costly mistakes, not the maximum process the tooling can support.

## Start here

- Adopting the workflow: [Bootstrap](docs/bootstrap.md).
- Running a task: [Developer guide](docs/developer-guide.md).
- Canonical lifecycle: [Workflow](docs/workflow.md).
- Grade definitions and required depth: [Risk grades](docs/risk-grades.md).

## Workflow at a glance

[![Risk-adaptive workflow overview, with separate review and final authorization gates](assets/workflow-overview-en.svg)](assets/workflow-overview-en.svg)

**[Open the detailed workflow diagram](assets/workflow-detailed-en.svg)**

The overview is a reading aid, not a substitute for the lifecycle contract. The detailed diagram shows separate Large AS-IS and PLAN reviews, evidence blockers, optional Blind Audit, and final Human authorization. Both are editable SVGs; [diagram maintenance](assets/README.md) explains their scope.

## What changed in v0.2

The portable runtime layer adds:

- a Trivial fast-track for non-behavioral changes;
- progressive disclosure: a small root contract routes to a task Skill and conditional documents;
- portable-core versus project-local policy separation;
- phase-aware, revision-addressed review and approval;
- starter files and a gradual bootstrap path.

The pre-merge hardening connects those principles to execution:

- separate Large AS-IS and PLAN review decisions;
- explicit independent-review and optional Blind Audit contracts;
- acceptance-criterion-to-result traceability;
- design approval separated from final integration authorization;
- bounded agent handoffs and revision-aware context reuse;
- a developer guide and updated workflow diagrams.

The [restricted-environment verification draft](docs/restricted-environment-verification.md) is optional and **not an implemented or operationally validated API/DB automation capability**.

## Core principles

1. **Work-item-first.** The current work item defines goal, scope, acceptance criteria, dependencies, and fixed decisions. The tracker is replaceable.
2. **Observed AS-IS.** Current mainline code and direct runtime evidence describe current behavior; stale plans do not.
3. **Information-specific Source of Truth.** Requirements, behavior, architecture, verification, review, and approval have different authoritative sources. See [Source of Truth](docs/source-of-truth.md).
4. **Risk-adaptive depth.** Risk, reversibility, contract surface, and failure cost determine the grade, not coding time or file count alone.
5. **Progressive disclosure.** Load the smallest stable entry contract, then only the Skill and documents relevant to the current phase.
6. **Verification before implementation.** Important ACs need a proof method; actual results must be linked back to them.
7. **Bounded exploration.** Start from direct paths, symbols, contracts, and callers/callees. Expand only for concrete uncertainty.
8. **Review is falsification, not redesign.** Self-review is not independent review. Blind means prior verdicts are withheld, not requirements.
9. **Revision-bound approval.** A review PASS is not Human approval. Design approval is not final merge authorization.
10. **Evidence-based completion.** Unrun checks are not PASS. Required verification, review, authorization, and applicable lifecycle work must actually be completed.

Capture real trade-offs; do not invent alternatives just to fill a template. See [Trade-off Capture](docs/trade-off-capture.md).

## Portable runtime architecture

```text
AGENTS.md: routing + always-on guards
  -> task Skill: execution procedure
      -> conditional process/domain documents
```

The [starter](starter/AGENTS.md) is an adoption snapshot, not a universal drop-in configuration. Replace placeholders, reconcile local policy, and keep its local contract internally consistent. Do not assume copying the Skill also copies all methodology documents.

## Portable core vs project-local policy

Keep work-item boundaries, risk grading, bounded exploration, verification mapping, revision-aware review/approval, and evidence-based completion portable.

Keep module names, environment quirks, actual commands, organization-specific approval systems, model/provider routing, credentials, and business vocabulary local. Do not make every grade use separate SDD files, independent review, or Blind Audit.

## Repository structure

```text
assets/       editable overview and detailed workflow SVGs
docs/        canonical policies, bootstrap, developer guide, optional draft
starter/     lean root contract, implementation Skill, local workflow contract
templates/   work item, AS-IS, TO-BE, change plan, PR, device QA
examples/    fictional Trivial, Small, Medium, and Large walkthroughs
```

## Status

**v0.2 — Portable Working Methodology**

This is a practical workflow, not a universal standard or a claim that all integrations have been implemented. A healthy workflow becomes smaller and sharper through observed use.
