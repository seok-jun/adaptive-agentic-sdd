# Bootstrapping Adaptive Agentic SDD in an Existing Repository

Adopt incrementally. Do not import a mature project's entire workflow on day one.

## Phase 1 — Observe before modifying

Analyze repository/module structure, actual build/test entry points, CI/release capabilities, work-item system, existing rules, architecture boundaries, durable documentation, and generated/vendor/shared paths.

Distinguish observed facts from proposed rules. Missing CI, a database connection, or an independent-agent facility is a capability constraint, not permission to invent successful checks.

## Phase 2 — Establish a lean root contract

Put work-item identification, always-on safety/scope guards, task routing, verified command references, and stable invariants in `AGENTS.md`. Do not put every procedure there.

Use [starter/AGENTS.md](../starter/AGENTS.md) as a shape, not an unchanged drop-in file.

## Phase 3 — Add one implementation Skill

Start with one canonical route:

```text
work item -> preflight -> grade -> bounded analysis -> plan
  -> implement -> verify -> review -> final authorization -> authorized finish
```

The starter consists of three cooperating files. Copy/adapt `starter/AGENTS.md` to the repository root, `starter/.agents/skills/implementing-issue/SKILL.md` to the corresponding local Skill path, and `starter/docs/sdd-workflow.md` to the local `docs/sdd-workflow.md` path. Reconcile existing files instead of overwriting them.

The local contract is self-contained and owns adopted gate semantics; the public repository is not an automatically loaded dependency. Only split additional Skills when repeated use shows context savings or removes ambiguity.

## Phase 4 — Grades, review, and authorization

Adopt [Risk Grades](risk-grades.md): Trivial, Small, Medium, Large, and Epic where breakdown is needed. Classify by failure cost, reversibility, contract surface, and coordination risk, not story points alone.

Keep low-risk analysis and records lean. Large has distinct AS-IS and PLAN independent review decisions. Determine how a separate reviewer is supplied; if unavailable, do not claim required independent review completed.

Separate design approval from final integration permission. Default to explicit final Human approval; any low-risk delegated integration must have a documented scope and eligibility rule. Preserve revision-bound evidence/approval.

## Phase 5 — Integrate the actual tracker

GitHub Issues are not required. The current work item or trustworthy snapshot needs goal, user/business impact, scope/non-scope, ACs, fixed decisions, blockers, grade, modification boundaries, and relevant linked specs.

Make snapshot identity/revision explicit when live tracker access is unavailable. Never silently treat stale copied text as current authority.

## Phase 6 — Pilot narrow work

Before a Large migration, try Trivial/Small tasks. Observe whether the agent reads unrelated files, misses local rules, edits outside scope, repeats setup, mislabels unrun checks, or claims completion without authority.

Use [Developer Guide](developer-guide.md) for daily prompts and expected outputs. Record what actually ran separately from walkthrough expectations. Tune from observed failures, not hypothetical completeness.

## Phase 7 — Add deeper gates selectively

After the lean path works, enable explicit Medium/Large analysis, phase-bound reviews, Human-owned design approvals, independent CODE review, optional Blind Audit for omission/anchoring risk, and conditional runtime QA. Do not make every task follow the deepest path.

## Portable core vs local safeguards

Keep actual module/path ownership, product vocabulary, credentials, model routing, approval-system integration, build/shell/encoding workarounds, and device setup local. Public examples must be fictional and independent of private implementation details.

The [restricted-environment verification draft](restricted-environment-verification.md) is optional and not validated automation. Adopt it only after an authorized pilot; do not silently add it to every Skill run.

## Suggested first prompt

```text
Analyze this repository without modifying product code.
Identify actual structure, boundaries, build/test/CI capabilities, work-item
system, existing rules, durable docs, and high-risk shared paths.
Propose the minimum bootstrap. Separate portable rules from local rules,
place them in root instructions, a task Skill, or conditional docs,
and state unavailable capabilities and required Human decisions.
```
