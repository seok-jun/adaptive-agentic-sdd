# Token / Context Efficiency

Context is a budget, not proof of diligence.

## Progressive disclosure

```text
small root contract -> task router -> task Skill -> conditional process/domain docs
```

Keep always-on guards, routing, and stable invariants at the root. Repeated procedures belong in Skills/process docs. Load one canonical definition rather than several prose copies.

## Default reads

- Read the current work item before unrelated backlog.
- Start from direct path/symbol, declarations and needed surrounding lines, then direct contracts/callers/callees.
- Load domain and architecture rules when the actual path or decision requires them.
- Inspect changed-file lists and relevant hunks before full diffs.
- Reuse unchanged context; summarize successful logs and expand failures/uncertainty.
- Run targeted checks before broad checks; do not rediscover fixed requirements or invent trade-off exploration.

## Agent handoff budget

Pass the task, phase, target revision, AC references, authorized modification boundaries, fixed decisions, direct evidence, and known unknowns. Do not preload the parent's entire conversation or unrelated history.

Return a concise verdict/result, concrete findings, evidence locations, changed surface, and unverified/blocked items. Keep source evidence available; a summary must not conceal uncertainty or prevent auditing.

For Blind Audit, withhold the primary review verdict/findings until its initial result is fixed. Do not omit ACs or safety boundaries. See [Review Gates](review-gates.md).

## Reuse and expansion

Reuse work-item, rules, source excerpts, and verification context only while their versions and relevance are unchanged. If the requirement, artifact, scope, or governing rule changes, refresh affected parts and revisit dependent gates. A previous session's summary is not proof of current state.

Record a concrete reason for widening exploration (for example, a caller contradicts a claimed invariant). Allowed/forbidden **edits** are not a ban on reading a direct dependency. Broader reads do not grant broader write permission.

No universal token cap or provider/model matrix belongs in the portable core. Tune local budgets from observed use, without claiming unmeasured savings.

## Never optimize away evidence

Do not remove required first reads, scope/grade gates, independent review, verification, applicable runtime QA, Human authorization, or completion evidence to save tokens. The rule is less irrelevant context, not less proof.

Keep build-tool, shell, encoding, device, environment, and model-routing exceptions local.
