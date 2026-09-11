# Trivial Example

**Fictional change:** fix a typo in explanatory prose without changing executable examples, requirements, or workflow meaning.

The direct target is narrow; static comparison and formatting/link inspection can prove the request. No runtime, build, test, schema, dependency, API, or agent-execution meaning changes.

Use a brief work-item entry, make the correction, run the relevant static checks, and self-review the diff. Record what was actually inspected; no separate SDD package or independent review is required by default. Present the final candidate for Human authorization, or record an applicable explicit low-risk integration delegation.

Do not report a runtime test PASS when none ran. This is a walkthrough, not execution evidence.

**Counterexample:** changing a Markdown rule from “wait for approval” to “merge automatically” changes execution meaning and is not Trivial. Regrade according to risk before editing.
