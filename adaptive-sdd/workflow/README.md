# Execution procedure (W)

After explicit selection and connection checks, route routine Trivial/Small work directly to the [compact route](process/small-work.md). It owns the closed reading set, work item and three records; once eligible, use it instead of the full step routing below. Actual P requirements, required checks, escalation, human decisions and authority remain.

> Recommended external adoption path: explicitly select an external, project-owned and editable W for each task. Read the [task selection contract](activation.md) first. The table below describes this path; the legacy `install.py` path is described after it.

This folder is the **common execution procedure** from Issue through implementation, verification and closing. It was carried over from a procedure refined over long operation in one product, with only the product-specific parts removed. Facts, paths, commands and permissions that differ by product are not kept in this folder; they are kept in the **project application documents** in `W/../project/` and in P's own sources.

## M/W/P structure and paths

| root | Location (external adoption) | Owner | Edited? |
| --- | --- | --- | --- |
| `P` | The product repository | Project | According to project rules |
| `W` | This `workflow/` folder in the project-owned workflow repository selected for the task | Project | Yes, through the project's own review and commit. A task uses the selected commit unchanged |
| `M` | The adopted supports in the same workflow repository (`methodology/` in the starter) | Project, starting from the common methodology | Yes. Adapt or remove them together with the W rules that call them |

M is the methodology, W the execution procedure, and P the product facts, settings and permissions. The resolver supplies the absolute P, W and M paths ([activation](activation.md)). S is not a separate layer or a Skill input.

`W/../project/` is the folder of project application documents next to W in the same workflow repository. When a W document points to `W/../project/<document>`, read that document. It may be edited directly, through the project's review.

References in W documents to the `## Always-applied hard guard` of `P/AGENTS.md` mean P's actual common instructions (when present) plus [task-guard.md](task-guard.md). No AGENTS block is created.

**Legacy `install.py` path.** When a project explicitly chose the older installer, W and M are installed copies (default `P/.adaptive-sdd/`, or another location chosen with `--harness-root`). They are not edited and are replaced as a whole on upgrade. The installer generates `W/../project/` from `W/../project.json`: edit the JSON and generate again instead of editing the output. The hard guard is the section inside the marked block the installer placed in `AGENTS.md`.

## Work tracking

W documents use tracker-neutral terms. An **Issue** is a work item; a **comment** is an entry in its work record; `priority:*`, `grade:*`, `status:*` and `type:epic` are **field values** of the work item, written in label notation; the **assignee** is its owner; a **PR** is a change request to the declared merge target; and the **closing reference** links that change to the Issue it completes (`Closes #N` is W's notation for it). The method declared by the P project document `tracker.md` decides how each of these is stored and written, including any syntax or API. W does not require a GitHub feature: read each expression through the declared method, and stop an operation that method does not map.

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

The observation review skill (`reviewing-observations`) will be carried over in a later release. Until then, observation review follows the procedure in M's `adaptation.md` directly.

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
