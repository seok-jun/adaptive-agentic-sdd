# Risk Grades

Grades control process depth, not implementation time. Classify by failure cost, reversibility, contract surface, and coordination risk.

## Required depth

This table is the canonical grade matrix. AS-IS and PLAN are logical sections; separate files are not mandatory.

| Grade | Analysis / plan | Independent design review | Verification | Code review | Design approval |
| --- | --- | --- | --- | --- | --- |
| Trivial | direct target; no separate SDD | no | targeted static/path/format check | self | none by default |
| Small | bounded inspection; work item or notes | optional for concrete risk | targeted AC evidence | self; independent if justified | local policy |
| Medium | explicit AS-IS, TO-BE, change plan | risk-based | AC-to-evidence mapping and relevant integration checks | independent when contract/integration risk warrants it | local policy |
| Large | explicit AS-IS, then TO-BE/change plan | AS-IS and PLAN reviewed separately before implementation | broader evidence for expensive failure modes | independent before merge | when the decision is Human-owned |
| Epic | breakdown and integration ownership first | breakdown review; Large gates for risky child/integration lanes | child evidence plus integration evidence | independent for Large-like lanes | when Human-owned |

**Final integration authorization is a separate gate for every grade.** Default: present the final candidate for explicit Human approval. A documented local policy may pre-authorize narrowly scoped low-risk integration; eligibility and the policy reference must be recorded. Neither a missing policy nor design approval authorizes merge. See [Review Gates](review-gates.md).

## Trivial — Fast-track

Use only when all are true:

- no runtime/product behavior change;
- no test expectation, schema, dependency, build, API/contract, or workflow execution meaning change;
- the target is direct and narrow;
- targeted static/path/format validation is sufficient.

Examples: typo fixes, link corrections, non-executable documentation cleanup. A one-line change to agent approval rules is **not** Trivial. Promote to at least Small before editing whenever execution or contract meaning changes.

## Small — Lean

One implementation boundary with no high-risk characteristic. The work item can be the plan and evidence record. No separate SDD package or independent reviewer by default.

## Medium — Standard

Multiple implementation boundaries or shared contracts without Large-level failure cost. Record explicit AS-IS, TO-BE, change plan, and verification strategy. Review the bounded contract when ambiguity or integration risk warrants it; do not rediscover the repository.

## Large — Deep

High-cost failure, for example:

- security/privacy or authentication/authorization boundaries;
- destructive or difficult-to-reverse migration;
- cross-system consistency/recovery;
- retry/scheduling semantics;
- cost/quota enforcement;
- durable public contract changes.

Review AS-IS observations before relying on them for PLAN. Review the resulting TO-BE/change plan before implementation. Each verdict names its phase and revision. A combined report is allowed; collapsing the two decisions into an unspecified design PASS is not.

Blind Audit is an escalation for material omission/anchoring risk, not a universal Large requirement.

## Epic — Breakdown first

Use when work changes module boundaries, creates modules, spans independently deliverable capabilities, or cannot be reasoned about safely as one lane. Define integration ownership and independently verifiable children. Apply Large rigor to risky children and integration; avoid one giant implementation worker.

## Escalation

Promote when new evidence reveals higher risk. Small diffs can be Large. Do not downgrade to avoid review, approval, or verification cost. Record the reason and revisit affected gates when the grade changes.
