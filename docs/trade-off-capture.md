# Trade-off Capture

Trade-off documentation is useful when real competing options exist.

It becomes wasteful when the process forces an agent to manufacture alternatives.

## Rule

```text
IF bounded Issue / AS-IS / dependency analysis reveals
   two or more real competing choices
THEN record the trade-off briefly
ELSE do not perform additional discovery just to create a trade-off section
```

## Minimal format

```md
## Trade-off

- Selected:
- Alternative:
- Why selected:
- Cost accepted:
```

Optional:

```md
- Revisit when:
```

Add a revisit condition only when a concrete trigger already exists.

## Avoid

- repository-wide exploration solely to find alternatives,
- mandatory brainstorming,
- five-option comparison tables for routine changes,
- speculative architecture redesign outside issue scope.

## Purpose

Trade-off Capture preserves a decision that **actually occurred**.

It is not an excuse to make every task a design workshop.
