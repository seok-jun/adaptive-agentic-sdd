# SDD grade

## SDD grade

The grade of an execution Issue uses only the following four values. An Epic is an optional management unit separate from the execution grades.

| grade | Decision condition |
| --- | --- |
| **Trivial** | Cleanup of documents, wording, links, comments or non-behavioral metadata that does not change runtime/contract/test expectation/build·dependency/schema·migration/CI·workflow execution meaning |
| **Small** | A change that is not Trivial, finishes within one implementation module, and has none of the automatic escalation conditions below |
| **Medium** | A change to two or more implementation modules or to a shared contract the project designates, without any Large condition |
| **Large** | A change whose failure impact is large, such as security, personal information, DB migration, background retry/schedule, or cost/quota |

Trivial is **not chosen merely because few files are involved.** All of the following conditions must be met.

- Product runtime behavior and user-observable results do not change.
- Public/internal contracts, the expected behavior of tests, build/dependency and DB schema/migration do not change.
- The meaning of execution steps, gates and stop conditions in CI, Skills and agent workflows does not change.
- The meaning of security, personal information, cost and quota policies does not change.

Typical examples are typo/spelling fixes, correcting the destination of a broken link, cleaning up descriptive wording and comments without changing behavioral meaning, and updating non-behavioral metadata to reflect the current state. If a change modifies executable code, tests, build settings or workflow execution rules, or if the document change itself changes agent/product behavior, it is at least Small.

### General automatic escalation

If several conditions apply, apply the highest grade. The project maps its concrete modules, technologies and business paths to the risks below and does not lower the common minimum grade. The shared contracts subject to escalation are designated in the project mapping. Do not add another contract of a single module to this set by its name alone.

| Change action | Minimum grade |
| --- | --- |
| Change to two or more implementation modules or to a shared contract the project designates | Medium |
| Change to the storage, transmission or logging policy for secrets, raw conversation text or personal information | Large |
| DB schema/migration change | Large |
| Change to background retry, schedule or duplicate-execution prevention policy | Large |
| Change to billing paths, cost calculation or quota/limits | Large |

Creating a new package or module, or changing dependency direction, does not by itself force Epic creation or work decomposition. Decide the execution grade from the actual change scope and the risk conditions above.

To use a grade lower than the automatic escalation criteria, the user's explicit exception instruction must be recorded in the Issue body. The agent does not lower it on its own.
