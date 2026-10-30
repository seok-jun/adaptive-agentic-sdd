# Glossary

One-line explanations of terms that appear often in the W documents. Each document remains the source of its rules. This glossary only explains meaning; it adds or changes no rule. If a term reads differently here than in a document, follow the document.

## Structure and installation

| Term | Meaning |
| --- | --- |
| M | Common methodology (`methodology/`): human-judgment requirements, observation records, rules for choosing supports. The project does not edit it |
| W | Common execution procedure (`workflow/`): skills, procedure documents, evaluation cases. The project does not edit it; an upgrade replaces it as a whole |
| P | The project repository. It owns product facts, paths, commands and permissions. Settings live in `project.json`; the project documents generated from them live in `W/../project/` |
| Pinned copy | The M and W copy checked by hash, verified against `MANIFEST.json` and `install.lock.json` |
| Hard guard | Rules that always apply: the `## Always-applied hard guard` section the installer places in the marked block of `AGENTS.md` |
| Run | One execution (one conversation or session). "Reuse what was checked in the same run" means do not re-read it within that execution |
| Tracker | The work tracking method: `local-docs` (documents and claim files in a shared folder) or `github` (Issues and PRs) |

## Work units and grades

| Term | Meaning |
| --- | --- |
| Issue (execution Issue) | One work item that is actually implemented and verified |
| Epic | An optional management document that groups several Issues. It is not an execution grade |
| Grade (execution grade) | Trivial, Small, Medium or Large. Set by change scope and risk; risk conditions escalate it automatically |
| SDD working documents | Working design documents for Medium and Large. They are cleaned up when the work ends |
| AS-IS | Investigation of the current state and its evidence |
| PLAN (TO-BE) | The intended change, human decisions, acceptance criteria and their verification mapping |
| Change plan | The implementation specification (Agent Execution Spec): implementation order and test details |
| Human View | The explanatory part a human reads to make a judgment |
| Human Decision | A product or design decision made by a human. An agent never makes one on a human's behalf |
| Business documents | Descriptions of current product behavior that remain after implementation |
| Visual Spec | A pinned HTML screen specification linked from an Issue |
| SUMMARY | The closing summary record of a task |

## Workspaces and boundaries

| Term | Meaning |
| --- | --- |
| Lane | An isolated workspace in which one Issue is carried out (a branch and worktree, or a cloud sandbox) |
| Claim (`[CLAIM]`) | A record saying "I will edit these paths", written before the first file write |
| Release (`[RELEASE]`) | A record that gives a claim up |
| Allowed / forbidden | The paths an Issue allows to be edited / forbids from being edited |
| Shared contract | A public agreement used by several modules (interfaces, schemas and so on). Not edited in an ordinary lane |
| Root integration | Paths such as root build files and settings that only integration work edits |
| Worktree | An additional working copy of the same repository checked out in another folder |

## Reviews and verdicts

| Term | Meaning |
| --- | --- |
| Candidate (review candidate) | The exact commit (exact SHA) and its documents fixed as the review target |
| Remote publication | Pushing a review candidate to the declared remote branch so other environments can read it |
| Review A (Contract Review) | An independent review of whether facts, contracts and the implementation specification are correct |
| Review B (Blind Audit) | An independent review that, without seeing Review A's result, looks for missing facts, hidden assumptions and boundary omissions |
| Reconciliation | The step after Review B's first verdict that checks again whether earlier findings were resolved |
| Finding | A single review comment |
| Blocker | A finding that prevents moving to the next phase (Human Decision blocker, Execution-contract blocker) |
| Implementation finding | A finding that does not block the next phase but must be confirmed resolved during implementation and closing |
| CODE Review | The code review after implementation |
| PASS / BLOCKED | Passed / stopped. `BLOCKED: <reason>` is a defined stop reason |
| Stop condition | A condition under which work must not proceed and must stop |
| STALE / INVALID | Evidence is out of date (its source changed) / evidence is malformed |

## Execution routing and handoff

| Term | Meaning |
| --- | --- |
| Phase | A step: PLAN, IMPLEMENT, REVIEW, TEST_DOCS |
| Orchestrator / worker / reviewer | The owner of the whole task / a worker given a phase / the reviewer |
| Delegation | Handing work to another agent or session. Different from a human's "recorded delegation" |
| Tier | Capability level. Models: `cheap < strong < frontier`; reasoning: `medium < high < extra-high`. `current` means the value currently running |
| Floor | The minimum capability level a phase needs |
| Qualification | A record of whether a given model may be used in a given role (PASS, DENIED) |
| Current/manual model | A model already running or chosen by a human. Its rules differ from those for candidates an agent chooses automatically |
| Packet | A summary bundle handed to a worker or reviewer (Execution, Result, Review Packet). A copy that never replaces the source documents |
| Provenance | Pinned source information (path, revision, hash) showing which source a packet came from |
| Freshness | Whether that source is still current |

## Verification and records

| Term | Meaning |
| --- | --- |
| Targeted verification | Narrow verification that runs the changed module or tests first |
| Broad verification | The wide required verification run on the final candidate |
| PASS reuse | Reusing an earlier run's result only for the same candidate and the same inputs. If an input changes, run again |
| Preflight | The step that checks the execution environment, such as the JDK, before builds and tests |
| Observation | Application records and actual problem records kept at start, handoff and closing |
| Not observed / not collected | Not seen within the checked scope (not zero) / not collected because there is no source |
| Token diagnostic | Optional token-usage recording, enabled only during a stabilization period |

## Execution profile chosen by the project

Chosen in `project.json`. The defaults keep the earlier behavior. The source of each rule is in parentheses.

| Setting | Values | Meaning |
| --- | --- | --- |
| `review.large_mode` | `dual` (default) / `single` | Whether Large design review uses the dual Review A and B, or one independent review ([Design review](process/design-review.md#large-design-review-mode)) |
| `review.blind_reviewer_selection` | `required` (default) / `optional` | Whether a human must choose the Review B model, or an agent may choose a qualifying model when no human has ([Design review](process/design-review.md#large-design-review-mode)) |
| `sdd.medium_artifacts` | `full` (default) / `condensed` | Whether a Medium SDD uses four documents or a single `README.md` ([SDD artifact layout](process/sdd-artifacts.md#medium-condensed-layout)) |

None of these values reduces M's human-judgment requirements, automatic grade escalation, required verification or the CODE Review.
