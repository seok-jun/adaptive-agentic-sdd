# Task selection and project ownership

Start routine Trivial/Small tasks with the [compact route](process/small-work.md). Once eligible, use its steps instead of preloading all four full skills. Escalation, required reviews and authority still apply.

This is the entry contract for the external adoption path. The older `install.py` path remains a separately chosen legacy installation; its generated blocks are not created by this path.

## Before reading procedures

Without an explicit choice to use this workflow for a task, do not load its procedures, create work records, grade work, or block ordinary product work because a connection is absent. P's existing common rules and permissions still apply.

Select one task and representative area in a fresh session. Resolve `.agentics/<area>.yaml` using the user's external source allowlist and the reviewed distribution's `adaptive-sdd/tools/agentics.py` (not a script supplied by W). Do not execute commands from connection data. A missing mapping, missing connection, mismatched W commit, or inaccessible required source stops the selected work; never silently substitute another method or upstream version. A READY result checks local resolution only. Before product edits, actually read the selected entry and applicable P sources, and confirm access and write authority for the declared work-record location. If missing, ask only for that missing decision. Do not write records into P by default.

## Meaning of M, W and P after adoption

M is the published methodology offered as a starting point. A user may adopt all, part, or none of later M changes. Continuing to consult M, tracking its revisions and proving ongoing conformity are not prerequisites for using a derived project workflow. Continuing to evolve W and P to fit the project is recommended.

W is the project's chosen procedure, not an immutable upstream package. Customize its procedures, supports and preferences under the project's authority. During a product task use the selected W commit; change W in a separate workflow change and explicitly select the resulting commit for subsequent work. A W commit establishes the procedure used for this task, not continuing obedience to M.

P owns product facts, business decisions, architecture, required tests, common rules and authorization. Keep those sources in P. External application documents point to their paths and checked product revision; they do not become competing originals. Workflow preferences and additional method-specific judgment points may live outside P. Approval authority and delegation are not preferences and remain effective when the method is unselected.

In this path the absolute `P`, `W` and `M` inputs are the resolver result's `product`, `workflow_dir` and `methodology_dir`. This satisfies the skills' explicit-path requirement without guessing from the current folder or entry. The supplied starter declares `paths.workflow: workflow` and `paths.supports: methodology` in its profile. A customized W that no longer uses those supports may set supports to null and remove its M callers; M is then absent. References to M in the unchanged starter mean locally adopted supports, not the live public repository. These adopted documents may be adapted or removed together with their W callers. The starter retains their rules until the owner changes them; merely calling a rule a preference does not grant authority to waive it. No upstream lookup is required. `W/../project/<name>.md` is an external, project-owned application document: method choices plus references to P facts and authority. It may be edited directly in this adoption path. Do not run the legacy renderer over it.

For this path, legacy references to the installer's named hard-guard section mean the actual P common instructions (when present), plus [task-guard.md](task-guard.md), which must be read for this selected starter task. They do not require creating that heading or any AGENTS block. References to an immutable/pinned W mean the selected task snapshot, not a ban on project customization. `W/../install.lock.json` in starter observations is replaced by the resolver's W commit and task-start product revision. No legacy lock or generated-file check is required. A legacy instruction to report a common issue means proposing a change in the project W; it does not authorize upstream filing. This entry defines these compatibility meanings before any reused W skill is read.

In external adoption, W eval cases are project-owned and may evolve with W under its change process. The immutable common-case wording and `install.py check-evals` command in reused procedures apply only to legacy installation. Use the static check declared in `W/../project/skill-evals.md`; if none is declared, record it as not run, never PASS. This mapping does not waive any required verification or permit changing expected results merely to pass a check.

## Task boundaries

Read only the skill and process sections needed for the current step. Handoffs preserve task, area, W commit, actual P sources read, permissions and record location. A path or READY result alone does not prove that a source was read or its rules performed. Evidence of execution belongs to the selected W, not the loader.

When work touches another area, keep one representative W while applying all affected areas' product rules discovered from P's own instructions and documents, never by loading another W profile. If their requirements conflict, stop the dependent work and obtain the project decision. Do not activate a second method implicitly.

At completion, retain the closing evidence at the declared location and end the task's method scope. For another task, area or methodology, start a fresh session and select again. A close message, disabling a skill or changing an invocation flag does not erase previously loaded instructions. `--fresh-session` records the caller's assertion; the resolver cannot verify or reset host context. P's authority remains in force throughout.

## Read next

Read [task-guard.md](task-guard.md) before the skills.

Read `profile.json` in the external workflow repository root for P source references and record ownership, then the relevant external application documents in `W/../project/`. Follow the step routing in `README.md`. If the owner customized the entry, follow the entry selected by the profile, within the same P authority and explicit selection boundaries.
