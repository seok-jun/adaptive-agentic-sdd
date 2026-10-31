# Adaptive Agentic SDD

**Short for small changes, deep for risky ones.** Risk-adaptive spec-driven development (SDD) for Claude Code or Codex on existing codebases.

[![Release](https://img.shields.io/github/v/release/seok-jun/adaptive-agentic-sdd?include_prereleases&label=release)](https://github.com/seok-jun/adaptive-agentic-sdd/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**English** | [한국어](ko/README.md)

Most SDD tools run the same spec → plan → tasks routine for every change. That is why SDD often feels like waterfall for a one-line fix. Adaptive SDD first decides how risky a change is, then applies only the planning, review and verification that risk needs. A link fix gets a self-check. A database migration gets written analysis, two independent design reviews and a human merge.

> **Preview.** This is `v1.0.0-preview.6` on the `v1-preview` branch. Its effect on outcomes, rework or cost has not been measured, and its structure may change before 1.0. See [Status and evidence](#status-and-evidence).

## How depth scales

Every execution work item gets one of four grades (an optional Epic that groups work items has none). The grade comes from risk, not from file count, and the agent cannot lower an automatic escalation on its own.

| Grade | When | Design documents | Review before code | Review of the change |
| --- | --- | --- | --- | --- |
| **Trivial** | No change to runtime behavior, contracts, tests, build or workflow meaning (typos, links, comments) | None | Self-check of the Trivial conditions | Targeted check + self-review |
| **Small** | Not Trivial, within one module, no escalation condition | None; the work item is the spec | Self-review of boundaries and verifiability | Self-review against the acceptance criteria |
| **Medium** | Two or more modules, or a shared contract the project designates | SDD: four short documents, or one page if the project chooses `condensed` | Bounded self-review; independent review when marked `REQUIRED` | Independent review if `REQUIRED`, otherwise self-review |
| **Large** | Security, personal data, DB schema/migration, background retry/schedule, billing or quota | SDD: four documents | AS-IS and PLAN each get Review A plus a blind Review B whose model a human chooses by default (a project can opt into one review, or let the agent choose the B model) | One independent code review; a human merges or explicitly orders that merge |

For each changed file that affects verification, the first check is the tests of the module that owns it, and checks widen only on evidence; a documentation-only Trivial change gets a targeted check that fits it. The required checks run on the final candidate, and a PASS is reused only when its inputs did not change. Definitions: [grades](adaptive-sdd/workflow/process/sdd/grade.md), [review gates](adaptive-sdd/workflow/process/verification.md#review-gate-by-grade).

## See it in action

Illustrative, shortened transcripts. Real output depends on your project settings.

```text
You:   Fix the broken link in docs/setup.md. Use Adaptive SDD.
Agent: Created T-12. Grade: Trivial — documentation only, no behavior change.
       Claimed T-12 (allowed: docs/setup.md).
       Fixed the link and checked that the target resolves.
       Self-review: the diff matches the requested scope.
       [IMPLEMENTATION SUMMARY] recorded. Branch ready for merge; claim released after merge.
```

```text
You:   Add a column for refund reasons to the payments table. Use Adaptive SDD.
Agent: Created T-31. Grade: Large — DB schema/migration (automatic escalation).
       Wrote the AS-IS analysis from the current code and schema.
       AS-IS Review A: PASS. Review B (blind): waiting for you to choose the reviewer model.
       ...
       PLAN reviews passed. Implemented within the allowed paths.
       Module tests first, then the required checks on the final candidate: PASS.
       Independent code review: PASS. Large changes need you to merge or explicitly order this merge — stopping here.
```

## Quick start

You need Python 3.8+, Git, and Claude Code or Codex. Start from a clean working tree (commit or stash your changes first).

If the agent runs in a sandbox, it must be able to write `.agents/` and `.claude/` and to commit. In Codex's `workspace-write` sandbox, `.agents/` and `.git` are read-only: start Codex with `--add-dir <repository>/.agents`, and make the installation commit yourself if Git writes are refused.

**1. Paste this into your agent** from the root of your repository:

```text
Install Adaptive Agentic SDD v1.0.0-preview.6 in this repository.
Installation guide: https://github.com/seok-jun/adaptive-agentic-sdd/blob/v1.0.0-preview.6/docs/customization.md

1. Resolve the tag to its full commit SHA:
   git ls-remote https://github.com/seok-jun/adaptive-agentic-sdd "refs/tags/v1.0.0-preview.6^{}"
   If it prints nothing, stop and tell me: the tag's commit could not be resolved.
2. Download the archive of that commit and copy its adaptive-sdd/ folder byte for byte to .adaptive-sdd/
   with a copy command, not a file-writing tool. Do not modify product code.
3. Run: python -I -B .adaptive-sdd/tools/install.py init --project-root .
4. Follow section 3 of the guide: observe this repository, then show me a draft of
   .adaptive-sdd/project.json with the evidence for each value. init copies example values; for every value
   the guide marks "Human" or "Human only", do not keep the example: ask me. Do not write the file yet.
5. After I answer, write project.json, run render with --source-tag v1.0.0-preview.6 --source-commit <SHA>,
   run check, create items/ and claims/ under tracker.root if I chose local-docs,
   and show me every file that was added or changed.
```

For the Korean edition, use `ko/adaptive-sdd/` and [`ko/docs/customization.md`](ko/docs/customization.md) instead.

**2. Answer the questions.** Only you decide the human-judgment points, delegations, where work items live (`github`, or `local-docs` in a shared folder outside the repository), the worktree folder, the merge method and the review profile. The verification commands per change scope (`build.verification`, or manual checks in `build.checks`) matter most: without a declared way to verify, implementation stops as `BLOCKED` because acceptance cannot be proven.

**3. Check the result.**

- `python -I -B .adaptive-sdd/tools/install.py check --project-root .` prints `OK      pinned copy, lock, and generated files match`.
- `python -I -B .adaptive-sdd/tools/install.py check-evals --project-root .` ends with `0 problem(s)`.
- `git status` shows only the paths below.

| Added or changed | What it is |
| --- | --- |
| `.adaptive-sdd/` | The pinned copy, your `project.json`, generated project documents and the lock file |
| `.claude/skills/<4 skills>/SKILL.md`, `.agents/skills/<4 skills>/SKILL.md` | Short entry files for Claude Code and Codex (only for the tools you chose) |
| `AGENTS.md`, `CLAUDE.md`, `.gitattributes` | One marked block from `adaptive-sdd:begin` to `adaptive-sdd:end`; your existing content outside it is kept |

**Undo.** Before you commit: run `git restore` on the files that existed before, and delete `.adaptive-sdd/`, the skill entry folders it created and any of `AGENTS.md`, `CLAUDE.md`, `.gitattributes` the installer created. After you commit: revert the installation commit, and push the revert if the installation was pushed; a branch created after the installation keeps it until you revert it on that branch or merge a branch that contains the revert into it. Work records under a `local-docs` tracker folder are outside the repository and are not touched.

## Your first task

```text
Using Adaptive SDD, create a work item for <a small change inside one module>, then implement it and close it.
```

It is ready to merge when the work item has a grade and acceptance criteria, a claim was taken before the first edit, the owning module's tests ran first and the required checks passed on the final candidate, an `[IMPLEMENTATION SUMMARY]` records decisions, verification and remaining risks, and the change request links back to the work item. Who merges follows your settings. It is done after the agent confirms the actual merge, closes the work item and records `[PRODUCT COMPLETE]`. After real work, the improvement loop in the [guide](docs/customization.md#3-order-of-work-for-the-agent) uses closing records, not opinions, to decide what to change.

## What you get

- **Four skills:** `managing-issues` (create and grade work items), `parallel-development` (claims and isolated worktrees), `implementing-issues` (design and implementation by grade), `finishing-issues` (verification, closing and cleanup).
- **Work tracking:** GitHub Issues and PRs, or work documents in a shared folder outside the repository. The procedures use tracker-neutral terms; each [adapter](adaptive-sdd/workflow/tracker/) maps them. Other trackers have no adapter yet.
- **Human-judgment boundaries:** the agent stops and asks instead of deciding scope reductions, delegations, Large merges or new product decisions ([core.md](adaptive-sdd/methodology/core.md)).
- **An installer** (Python standard library only) that generates the project-specific files from `project.json` and checks every pinned file against its hash.
- **An evaluation kit:** behavior cases for each skill, a cross-agent runner and rules for turning a recorded incident into a test case ([skill-evals.md](adaptive-sdd/workflow/process/skill-evals.md)).

Repository layout: `adaptive-sdd/` is the English bundle you install (canonical), `ko/` is the Korean edition with the same layout, `methodology/` is the core methodology alone, and `docs/` holds the installation guide and evaluation records.

## Status and evidence

- **Not measured:** no effect on outcomes, rework or cost has been measured. The procedures were refined in one product; that does not prove they work elsewhere.
- **Behavior evaluations:** a first cross-agent baseline ran 12 Korean cases × Claude Code and Codex × 3 runs (Claude Code 21 PASS / 14 FAIL / 1 INVALID, Codex 22 PASS / 14 FAIL) — [record](docs/eval-results/2026-10-30/README.md). A post-hoc paired check of two wording fixes found no overall improvement — [record](docs/eval-results/2026-10-30-skill-comparison/paired-summary.md). Failures are published as they were graded. In the baseline and in the preview.6 tracker check, the answer-key files were readable inside the evaluated projects, so those two runs are not clean evidence; the paired check removed them.
- **This release:** all 65 executable tests passed on Windows with Python 3.12.2, both 66-file bundle manifests matched, and an archive of the reviewed candidate (`277cfc5`) passed `init`, `render`, `check` and `check-evals` (77 cases) for both editions with both trackers. An independent read-only review (Codex `gpt-6-astra`, high) found no blocker; its findings were fixed and reconfirmed. In two first-use runs from this README, a Claude Code agent installed the methodology, finished a Small task and undid the installation; a Codex run installed it, but its sandbox blocked Git writes, so it did not reach the task. A bounded behavior check of the changed wording is [recorded](docs/eval-results/2026-10-31-tracker-neutral/README.md) as weak evidence. POSIX execution and live GitHub tracker operations were not run.
- **Model routing:** routine Trivial/Small tasks run on the current model unless denied, subject to [routing eligibility](adaptive-sdd/workflow/skills/_shared/execution-routing.md#two-axis-routing). Medium and above, independent reviews and delegation need observed evidence for the model; a name or declaration alone is not enough ([first-use record](docs/eval-results/2026-10-31-first-use/README.md)).
- **Not a guarantee:** this is guidance for agents and people, not a security boundary or an agent runner.

The full history of checks and reviews is in [CHANGELOG.md](CHANGELOG.md).

## Versions

- Preview tags are `v1.0.0-preview.N` on the `v1-preview` branch. Published tags are never moved; fixes come as new tags. Pin a copy by tag, commit SHA and manifest hash.
- To upgrade, replace only the pinned copy, keep `project.json`, the tracker records and work records, and render again ([guide](docs/customization.md#upgrading)).
- The earlier v0.2 methodology is on `main` and tag [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0). v1 is not an automatic upgrade from v0.2.

## License

[MIT](LICENSE)
