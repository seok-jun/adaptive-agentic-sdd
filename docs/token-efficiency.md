# Token / Context Efficiency

Adaptive Agentic SDD treats context as a budget, not a proof of diligence.

## Progressive disclosure

Prefer this instruction architecture:

```text
small root contract
  -> task router
      -> canonical task Skill
          -> conditional process/domain documents
```

The root contract should contain only always-on hard guards, task routing, and a few stable invariants. Repeated procedures belong in Skills/process documents.

## Default rules

- read the current work item before unrelated backlog items,
- start from direct path/symbol instead of repository-wide browsing,
- inspect declarations plus the surrounding lines needed for the decision rather than dumping full files,
- load domain/architecture/process documents only when the current path or decision requires them,
- reuse unchanged context within the same run,
- do not rediscover requirements already fixed by the work item,
- run targeted checks before broad checks,
- summarize successful logs and expand only failures,
- inspect changed-file lists and relevant hunks before full diffs,
- do not ask review/QA agents to redesign the product,
- do not create trade-off exploration when no real competing option exists.

## Never optimize away evidence

Token savings must not remove:

- required first reads,
- scope/grade gates,
- verification,
- independent review required by grade,
- Human approval required by policy,
- runtime/device QA required by acceptance criteria,
- completion evidence.

The rule is **less irrelevant context, not less proof**.

## Same-run reuse

When an agent moves through planning -> implementation -> finishing in one run, unchanged work-item metadata, root instructions, source excerpts, and verification state should be reused rather than repeatedly fetched.

## Project-local exceptions

Some repositories need extra preflight for build tools, shells, encoding, emulators, environments, or model/provider routing. Keep those rules local unless they generalize across projects.
