# Bootstrapping Adaptive Agentic SDD in an Existing Repository

The safest adoption path is incremental. Do not import a mature project's entire workflow on day one.

## Phase 1 — Observe before modifying

Ask the agent to analyze, without changing product code:

- repository/module structure,
- build and test entry points,
- existing CI/release path,
- current issue/ticket system,
- architecture or module-boundary rules,
- durable product documentation,
- places where generated/vendor/shared files should not be changed casually.

The output should distinguish **observed facts** from proposed workflow rules.

## Phase 2 — Create a lean root agent contract

Start with a small `AGENTS.md` that contains:

- how to identify the current work item,
- always-on safety/scope guards,
- task routing,
- build/test command references,
- a few stable architecture invariants.

Do not put every repeated workflow step in the root file.

Use `starter/AGENTS.md` as a shape, not as a file to copy unchanged.

## Phase 3 — Add one implementation Skill

Start with a single canonical implementation Skill:

```text
work item -> preflight -> grade -> bounded analysis -> plan -> implement -> verify -> review -> finish
```

Only split it into issue-management, parallel-development, finishing, QA, or other Skills after repeated use proves the split saves context or removes ambiguity.

## Phase 4 — Define grades

Adopt the smallest useful ladder:

- Trivial,
- Small,
- Medium,
- Large,
- Epic only if your repository actually needs multi-lane breakdown.

Do not classify by story points or expected coding time alone. Classify by failure cost, reversibility, contract surface, and coordination risk.

## Phase 5 — Integrate the real tracker

GitHub Issues are not required. Jira, Linear, or another tracker can be the work-item Source of Truth.

At task start, the agent needs a current ticket identity/revision or trustworthy current snapshot containing at least:

- goal,
- scope/non-scope,
- acceptance criteria,
- dependencies/blockers,
- priority/grade if used,
- relevant linked specs.

If the agent cannot access the tracker directly, avoid silently relying on a stale copied ticket body. Make the snapshot boundary explicit.

## Phase 6 — Pilot with Trivial/Small work

Before testing a Large migration, run several narrow real changes and observe the workflow itself:

- did the agent read unrelated files?
- did it miss existing local rules?
- did it modify outside scope?
- did it repeat setup/install work unnecessarily?
- did it report unrun verification as PASS?
- did the PR explain evidence clearly?

Tune the workflow from observed failures, not hypothetical completeness.

## Phase 7 — Add deeper gates only when justified

Add Medium/Large mechanisms after the lean path works:

- explicit AS-IS / TO-BE artifacts,
- independent contract review,
- revision-bound Human approval,
- independent code review,
- optional Blind Audit for omission/anchoring risk,
- conditional device/runtime QA.

## Portable core vs local safeguards

Promote a rule into the portable methodology only when it generalizes across repositories.

Keep local:

- product-specific privacy restrictions,
- module/path ownership,
- build-tool workarounds,
- shell/encoding quirks,
- emulator/device bootstrapping,
- model/provider routing,
- organization-specific approval systems.

This prevents a successful repository from turning its incident history into everyone else's mandatory ceremony.

## Suggested first prompt

```text
Analyze this repository without modifying product code.

Identify the repository structure, module boundaries, build/test/CI path, work-item system, existing development rules, durable documentation, and high-risk shared paths.

Then propose the minimum Adaptive Agentic SDD bootstrap for this repository. Do not copy a mature workflow wholesale. Separate portable rules from project-local rules, and explain which rules should live in AGENTS.md, a task Skill, or conditional docs.
```
