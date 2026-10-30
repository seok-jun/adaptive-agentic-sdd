# Execution procedure (W)

This folder is the **common execution procedure** from Issue through implementation, verification and closing. It was carried over from a procedure refined over long operation in one product, with only the product-specific parts removed. Facts, paths, commands and permissions that differ by product are not kept in this folder; they are kept in the **P project documents** generated at installation.

## M/W/P structure and paths

| root | Location in an installed project | Owner | Edited? |
| --- | --- | --- | --- |
| `P` | Top level of the project repository | Project | According to project rules |
| `W` | `W/` | Common (this folder) | Not edited. Replaced as a whole when the version is upgraded |
| `M` | `M/` | Common methodology (`core.md`, `adaptation.md`, supports) | Not edited |

M owns the common methodology, W owns the execution procedure, and P owns product facts, settings and permissions. The installation location does not change this division. The default copy is `P/.adaptive-sdd/`; an external installation selects a different storage location with `--harness-root`. S is not a separate layer or a Skill input.

`W/../project/` below is the actual relative path of the project documents installed together with W, and P owns them. The generated entry file also states that location. The installer generates the P project documents under `W/../project/` from the values in `W/../project.json`. When a W document points to `W/../project/<document>`, read that generated output. Do not edit the generated output by hand. To change a value, edit `project.json` and generate again.

The `## Always-applied hard guard` of `P/AGENTS.md` in W documents is the section inside the marked block that the installer placed in `AGENTS.md`.

## Work tracking

Read the Issue, comment, label, assignee, PR and closing reference expressions in W documents as translated into the method declared by the P project document `tracker.md`.

- [Local documents](tracker/local-docs.md): work documents and claim files in a shared folder outside the repository
- [GitHub](tracker/github.md): GitHub Issues and PRs

Do not run a procedure that assumes a capability absent from the declared method's mapping table; stop instead.

## Default document locations

`docs/domains/**` (business documents), `docs/sdd/{feature}/` (SDD working documents), `docs/reviews/**` (decision records), `docs/architecture/**` (architecture documents) and `docs/README.md` (document index) in W documents are defaults. The actual locations follow the `Document roles` table of the P project document `sdd-workflow.md`.

## Reading order

For a term you have not seen before, find its one-line explanation in the [Glossary](glossary.md). The glossary adds no rules.

1. M's `core.md` (common methodology and human-judgment requirements)
2. The hard guard of the P project documents and the application declaration for the relevant step
3. The W skill for the relevant step and the W process sections that match its input conditions. Reuse the same version checked in the same run, and do not preload every document by following links.

Skills are in `skills/<name>/SKILL.md`.

| Step | Skill |
| --- | --- |
| Work organization (Issue creation and classification) | `managing-issues` |
| Work isolation (claim and lane) | `parallel-development` |
| Design and implementation | `implementing-issues` |
| Verification and closing | `finishing-issues` |

The execution grades are Trivial, Small, Medium and Large. An Epic is an optional management unit; its creation, decomposition and coordination of overall completion are done in `managing-issues`. Each child execution Issue follows its own grade, and a decomposition review is not required as a condition for starting investigation. The policy source is [Epic management unit](process/sdd/epic.md#epic-management-unit).

The observation review skill (`reviewing-observations`) will be carried over in the next preview. Until then, observation review follows the procedure in M's `adaptation.md` directly.

## Sources of the detailed rules

[sdd-workflow](process/sdd-workflow.md#rules-to-read-for-the-current-step) only gives the paths for the current step. The sources of the classification, entry, Issue, Epic and closing rules are the responsible files in `process/sdd/`. Skills link those files directly and do not duplicate the rules.

| Rule | Source |
| --- | --- |
| Roles and required content of SDD documents | [sdd-artifacts](process/sdd-artifacts.md) |
| Acceptance criteria, verification by grade, PASS reuse, verification environment | [verification](process/verification.md) |
| Large design review, remote candidate, re-review | [design-review](process/design-review.md) |
| model, floor, qualification, fallback | [execution-routing](skills/_shared/execution-routing.md) |
| packet fields, guard evidence, freshness, result consumption | [execution-packets](skills/_shared/execution-packets.md) |
| Recording start, handoff and closing observations and actual problems | [observations](process/observations.md) |
| Token checkpoints during an enabled period | [token-diagnostic](process/token-diagnostic.md) |
| Skill evaluation and synthetic packet measurement | [skill-evals](process/skill-evals.md) |

## Origin and changes

The original was taken from one product's procedure repository as of 2026-10-17. For rules whose evidence was a product history number, only the rule was kept. Device and emulator procedures, product-specific tools (impact analyzer, observation helper, connection tool) and product model names were not carried over; where they are needed, the P project documents declare them.
