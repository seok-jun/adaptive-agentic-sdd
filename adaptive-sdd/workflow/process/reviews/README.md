# Common design decision review format

This format applies to changes for which the project requires a review topic. The project owns the trigger conditions and the actual records. It does not replace the existing SDD required review, and it does not automatically add independent reviewers or approval rounds.

## Topic structure

```text
docs/reviews/
  NNN-<slug>/
    proposal.md
    review-<agent>.md
    decision.md
  _templates/
```

- `NNN` is a three-digit number: the largest existing number + 1.
- `slug` uses only lowercase English letters and `-`.
- A topic has exactly one `proposal.md`.
- Each reviewer writes only its own `review-<agent>.md` file.
- Exactly one `decision.md` is written after the final decision.

Do not edit the body of another agent's `review-*.md`. Put rebuttals or additional evidence in your own review file.

## Status

Use only the following five status values.

```text
Proposed → In review → Decided
                   ├→ On hold
                   └→ Rejected
```

The status in the `proposal.md` header is the status of the topic.

- Right after the proposal is written: `Proposed`
- When the first review is requested: `In review`
- When the decision is written: one of `Decided`, `On hold`, `Rejected`

The link list in `docs/reviews/README.md` is for navigation. Do not judge current product behavior or implementation state from that index table.

## Required proposal content

Apply [Visual writing of human-facing documents](../agent-instruction-policy.md#visual-writing-of-human-facing-documents) to the human-read proposal, review and decision. Show the key change and choice of a proposal or decision before the detailed evidence. Where needed, choose a comparison table for policy or before/after differences, a relationship diagram or boundary table for ownership and boundaries, and a flow or state representation for order and states. A simple topic needs only one sentence; no fixed number of figures is required.

A proposal includes:

1. The problem
2. The current rule/contract to be changed
3. Two or more options, or the reason only one option is possible
4. The advantages, risks and costs of each option
5. What will not be chosen
6. The questions that need a decision
7. Code/document evidence

Do not evaluate options only with unmeasured expressions such as `looks better`, `more scalable` or `more flexible`. State which call paths, costs, failure modes or maintenance boundaries change.

## Review rules

Each finding in a review states:

- Severity: `Critical`, `Major`, `Suggestion`
- Evidence: the actual file, symbol or document rule ID
- Status: `Confirmed` or `Assumed`
- Impact: which requirement, cost or failure it leads to

Do not mark a verification that was not run as `Confirmed`.

In the same review, check that the first explanation shows the change and the choice, and that the conditions, failures and open items in figures and tables match the body text. A difference in meaning is handled through the existing finding and resolution procedure; it does not create a new approval or reviewer round. The presence or number of figures is not itself a basis for the verdict.

When external model prices or API policies are used as evidence, record the source checked and the date checked. Do not write unit prices from memory.

## Decision rules

`decision.md` includes:

1. The adopted option
2. The reasons for adoption
3. The options not adopted and why
4. The business rules/contracts that change
5. Follow-up Issues
6. When it takes effect

If a decision changes a current business rule in `docs/domains/**`, **do not stop at recording the decision.** Update the final code and the business documents together in the work that completes the implementation.

A past decision is not deleted or overwritten with a new conclusion even if a different choice is made later. A new review topic references the earlier decision.
