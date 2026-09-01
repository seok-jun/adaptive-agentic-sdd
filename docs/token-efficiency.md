# Token and Context Efficiency

Adaptive Agentic SDD treats context/reasoning cost as an engineering constraint.

## Principles

### 1. Read only what is directly relevant

Avoid loading unrelated issues, unrelated domains, historical reviews by default, and broad architecture documents when no boundary question exists.

### 2. Start narrow

Use:

```text
issue
-> direct path
-> direct symbol
-> public contract
-> direct callers/callees
-> broaden only if concrete evidence requires it
```

### 3. Reuse context in the same run

Do not re-read unchanged issue bodies, process rules, source files, or environment resolution.

### 4. Do not re-discover fixed requirements

Once the issue has explicitly decided a requirement, the implementation agent should not repeat product discovery unless a conflict appears.

### 5. Targeted verification first

Run the smallest useful check during development. Run expensive broad checks at the appropriate completion gate.

### 6. Review/QA should not redesign

Independent agents should receive a bounded evidence package and check correctness, not restart product exploration.

## Adaptive reasoning budget

```text
Small  = Lean
Medium = Standard
Large  = Deep
Epic   = Breakdown + Deep + Independent Review
```

The goal is not “low token usage at any cost.” The goal is **spending reasoning where failure is expensive**.
