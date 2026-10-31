# Installation and customization guide (1.0 preview.7)

This guide covers `v1.0.0-preview.7`. Verify the tag's full commit SHA and pin the copy and the guide to that commit. For an earlier preview, use the guide inside that tag (for example `https://github.com/seok-jun/adaptive-agentic-sdd/blob/<tag>/docs/customization.md`; tags before preview.5 have a Korean guide only, at `ko/docs/customization.md`). The English bundle (`adaptive-sdd/`) and this guide are canonical; the Korean edition of this guide is [`ko/docs/customization.md`](../ko/docs/customization.md).

The generated default check/check-evals commands use literal path quoting for PowerShell on Windows and for POSIX sh elsewhere. Run them in the named shell. The project manages the quoting of custom commands.

If `python3` is unavailable (common on Windows), retry the same arguments with `python` or `py -3` (Python 3.8+); a missing interpreter name is not a failed check, so try the alternative before stopping.

This document explains how to place a copy of the methodology in a project, generate the project-dependent files from project values, and give work to an Agent. It is not part of the copy.

## What this preview is

- **Common principles (M)**: in `methodology/`, `core.md` (minimal workflow, human-judgment requirements, work records and observation), `adaptation.md` (choosing supports based on observation) and `supports/ordered-changes.md` (default support).
- **Execution procedure (W)**: the procedure documents in `workflow/` and four Skills (organizing work, isolating work, design and implementation, verification and closing), the eval system and fictional representative cases. A procedure refined through long operation in one product was moved here with only the product-dependent parts removed.
- **Installer**: `tools/install.py` (Python standard library only). It generates the project-dependent files from project values and checks that the pinned copy and the generated outputs match.
- **Effect not verified.** The procedure has been operated in one product, but this is the first preview of the form moved to other projects.

## What goes where

| What | Location | Who edits it |
| --- | --- | --- |
| Pinned copy | `.adaptive-sdd/methodology/`, `workflow/`, `templates/`, `tools/`, `LICENSE`, `MANIFEST.json` | Nobody edits it. Replace it as a whole when upgrading |
| Project values | `.adaptive-sdd/project.json` | A human (the Agent proposes a draft) |
| P application documents | `.adaptive-sdd/project/*.md` | Generated. Do not edit directly |
| Per-tool Skill entries | `.claude/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md` | Generated |
| Marked blocks | `adaptive-sdd:begin` to `end` in `AGENTS.md`, `CLAUDE.md`, `.gitattributes` | Generated. Existing content outside the blocks is left as it is |
| Generation record | `.adaptive-sdd/install.lock.json` | Installer |
| Work records (local-docs method) | `tracker.root` in `project.json` (a shared folder outside the repository) | The Agent doing the work |

**Principle**: Do not edit the pinned copy or the generated outputs. If something must change, edit `project.json` and generate again. A problem that can only be solved by editing the pinned copy is a missing slot in the common layer, so report it ([Reporting a common problem](#reporting-a-common-problem)).

## 1. Getting the copy

In-repository installation is the default. If you choose external installation, change the destination of the file copy below to `.adaptive-sdd/` under a dedicated installation path outside the product checkout, and use the explicit root options in the next section. OS junctions and hard links are not needed.

Verify and pin this release's full commit SHA with `git ls-remote https://github.com/seok-jun/adaptive-agentic-sdd "refs/tags/v1.0.0-preview.7^{}"`. Keep the verified SHA even if the `v1-preview` branch moves later. Download the source archive of that commit and copy `adaptive-sdd/` to the project's `.adaptive-sdd/` **byte for byte**. Do not rewrite the files with a text editor or an Agent's file-writing tool. Windows PowerShell example:

```powershell
$sourceCommit = "<full commit SHA verified for v1.0.0-preview.7>"
if ($sourceCommit -notmatch '^[0-9a-f]{40}$') { throw "Set sourceCommit to the reviewed full commit SHA." }
$zip = Join-Path $env:TEMP "adaptive-sdd-$sourceCommit.zip"
Invoke-WebRequest "https://github.com/seok-jun/adaptive-agentic-sdd/archive/$sourceCommit.zip" -OutFile $zip
$tmp = Join-Path $env:TEMP "adaptive-sdd-preview"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive $zip -DestinationPath $tmp
$src = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
foreach ($p in "methodology","workflow","templates","tools","LICENSE","MANIFEST.json") { Remove-Item ".adaptive-sdd/$p" -Recurse -Force -ErrorAction SilentlyContinue }
New-Item -ItemType Directory -Force .adaptive-sdd | Out-Null
Copy-Item "$src/adaptive-sdd/*" .adaptive-sdd -Recurse -Force
Remove-Item $tmp -Recurse -Force; Remove-Item $zip -Force
```

POSIX sh example (bash/zsh):

```sh
(
set -eu
sourceCommit='<full commit SHA verified for v1.0.0-preview.7>'
if ! printf '%s\n' "$sourceCommit" | LC_ALL=C grep -Eq '^[0-9a-f]{40}$'; then
  printf '%s\n' 'Set sourceCommit to the reviewed full commit SHA.' >&2
  exit 1
fi
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' 0
trap 'exit 1' HUP INT TERM
curl -fL "https://github.com/seok-jun/adaptive-agentic-sdd/archive/$sourceCommit.zip" -o "$tmp/source.zip"
unzip -q "$tmp/source.zip" -d "$tmp"
src="$tmp/adaptive-agentic-sdd-$sourceCommit"
for p in methodology workflow templates tools LICENSE MANIFEST.json; do
  rm -rf ".adaptive-sdd/$p"
done
mkdir -p .adaptive-sdd
cp -R "$src/adaptive-sdd/." .adaptive-sdd/
)
```

Use `docs/customization.md` from the same archive, or the commit-pinned address in section 3. In `<verified SHA>` below, put exactly the SHA you selected when downloading the archive. Do not specify `--source-tag` for an unreleased commit. Only when you use a published tag, verify the correspondence between that tag and the commit and record them together.

## 2. Creating project values

### External installation and connection

M, W and P are the ownership divisions for common principles, execution procedure, and product facts and settings, respectively. The external installation path is a storage location option; it does not add a separate layer called S or an execution input. Choose a dedicated folder such that it and the product checkout do not contain each other, and place the copy in `.adaptive-sdd/` under it. The following commands are path examples; replace them with locations that are actually allowed. In Windows JSON paths, using `/` reduces confusion over backslash escapes.

```text
python3 -I -B <external-install-path>/.adaptive-sdd/tools/install.py init --project-root <product-checkout> --harness-root <external-install-path>
python3 -I -B <external-install-path>/.adaptive-sdd/tools/install.py render --project-root <product-checkout> --harness-root <external-install-path> --source-tag v1.0.0-preview.7 --source-commit <verified SHA>
python3 -I -B <external-install-path>/.adaptive-sdd/tools/install.py check --project-root <product-checkout> --harness-root <external-install-path>
```

P-owned settings, application documents and the lock are generated at the external installation path; `.agentics/adaptive-sdd.json`, the per-tool Skill entries and the AGENTS/CLAUDE marked blocks are generated in P. No duplicate Skill entries are created at the external installation path. The connection's manifest hash, the lock source at the external installation path, the copy's bytes, and the generated outputs in the product and the installation path are checked together. If the connection is missing or its access/pin information is wrong, there is no fallback to another copy. After upgrading the copy, render with the reviewed external installation path given explicitly as `--harness-root`, and update the connection. The tool does not verify the authenticity of the remote source commit.

The lock of one external installation path is bound to only one P checkout. A new worktree or another checkout creates its own dedicated installation path and connection, and may share the same tracker_root. Do not quietly repoint an already connected installation path to another P. A mode that shares one generated-output lock across several checkouts is not supported. If a cloud host cannot read the external installation path, use the in-repo installation or decide on an accessible placement separately.

When moving an existing installation, copy the pinned copy and the reviewed project.json to the new installation path and connect it with the commands above. Hand-edited entries remaining in P are preserved as KEPT, so review the diff and use `--accept-overwrite` only for those paths. The tool does not automatically delete the old copy, entries or connection. After verification, confirm their ownership and use, and clean them up separately. If the installation is local-only, P decides whether the generated paths are committed or excluded; installation does not grant push permission. Even when the external installation path is managed with Git, the copy keeps its LF bytes.

### Per-project operating settings

Existing schema 1 values continue to be read. Omitted Git values default to origin/main/main, the ID to generated, and the test lifetime to persistent.

| Value | Meaning |
| --- | --- |
| `git.remote`, `git.base_branch`, `git.merge_branch` | Code remote, base for new lanes, product merge target. Separate from actual Git permissions |
| `review.repository`, `review.remote`, `review.branch` | Absolute path, remote and branch of the SDD publication repository. Empty values mean P, git.remote and the Issue branch, respectively. A local bare remote must also allow exact-artifact retrieval |
| `tracker.id_source`, `id_format`, `child_id_rule` | generated or external. external requires a format and keeps the source ID. A human declares the child suffix rule and the issuing authority |
| `project.conversation_language`, `project.conventions` | Conversation/progress-report language; reference to the source of the project's conventions |
| `build.checks` | A list of items with the strings `scope, method, actor, instructions, evidence, required`. method is command/manual, actor is agent/human, required is required/optional |
| `build.test_mode`, `test_format`, `test_preserve_at` | persistent/temporary/none, test format, preservation location for temporary evidence (required for temporary). Relative paths are based on P |
| `routing.role_defaults` | A list of `role, model, reasoning`. role is PLAN/IMPLEMENT/REVIEW/TEST_DOCS/FINISH. A preference; it does not replace qualification or a human's selection for B |
| `routing.capabilities` | A list of `host, model, tier, reasoning, source, identity, valid_until`. tier is cheap/strong/frontier; the expiry is an ISO time that includes the timezone. When selecting, check the actual source, freshness and host support |
| `routing.qualification_records` | Reference to separate role qualification records. Distinct from capability |

The routine Trivial/Small current/manual route needs no positive capability evidence or table entry, subject to the eligibility and deny rules in [W routing](../adaptive-sdd/workflow/skills/_shared/execution-routing.md#two-axis-routing). Other current/manual routes need fresh host evidence or a human-confirmed scoped assessment citing observed results under that contract; a model name or declaration alone is insufficient, and automatic selection still requires an eligible host mapping and fresh role qualification PASS.

If the three execution profile values (`review.large_mode`, `review.blind_reviewer_selection`, `sdd.medium_artifacts`) are omitted, they take their defaults (`dual`, `required`, `full`), which behave the same as earlier previews. If a value is outside the defined values, or `review` or `sdd` contains an unknown key, `render` rejects it (so that a typo does not silently remain as the default). These values are open only in the direction of making W lighter; they do not reduce M's human-judgment requirements, automatic grade escalation, required verification, the CODE Review, or the human judgment for Large merges. A changed value applies from newly started reviews and SDDs. The source of the rules is W [Design review mode](../adaptive-sdd/workflow/process/design-review.md#large-design-review-mode) and [Medium condensed layout](../adaptive-sdd/workflow/process/sdd-artifacts.md#medium-condensed-layout).

The existing commands in `build.verification` and `build.checks` apply together. A manual result must secure the target, confirmer, time and observed evidence, and an unconfirmed required check is not completion. temporary preserves and re-queries the tests/fixtures and execution evidence before removing them, and proves the correspondence between the final code and the inputs. none also blocks when there is no equivalent evidence that proves the completion criteria and the PLAN findings. New settings do not implicitly override earlier instructions; applying them during work follows the existing policy-transition procedure.

### Default in-repository installation

```bash
python3 -I -B .adaptive-sdd/tools/install.py init --project-root .
```

Copies the example only when `.adaptive-sdd/project.json` does not exist. If it exists, it is left untouched. The Agent drafts the values in the order of section 3 below, and a human decides them.

| Value | Content | Who decides |
| --- | --- | --- |
| `project.name`, `project.artifact_language` | Name, language of human-facing artifacts | Human |
| `tools` | Which of `claude-code` and `codex` you use | Human |
| `tracker` | `kind` (`local-docs` or `github`); for local documents, `root` (an absolute path outside the repository, on a local disk or an SMB share — no sync folders), `id_prefix` and `merge_method` (`merge`, `squash`, `rebase`); allowed authors | Human |
| `docs` | Locations of business, SDD, decision records, structure documents and the index | Agent proposes, human confirms |
| `grade_mapping` | Project-specific automatic escalation (e.g. a change to a particular shared module → Medium) | Agent proposes, human confirms |
| `human_judgment` | Human merge of Large execution changes, additional judgment points, recorded delegations (scope, date, confirmer). The `large_epic_merge` key is kept for compatibility and does not automatically waive existing human authority | **Human only** |
| `worktree_root` | A short absolute path for parallel lane worktrees | Human |
| `build` | Build tool, JDK major, execution wrapper, cleanup command, verification commands per change scope | Agent proposes, human confirms |
| `modules` | Module list, shared contracts, root/integration-only paths, dependency rules | Agent proposes, human confirms |
| `routing.deny_models` | Models not to use | Human |
| `priority` | Current stage, implementation queue rules, product-specific Priority examples | Human |
| `evidence` | Evidence that may be written as is, and what must not be moved | Human |
| `visual_spec` | HTML Visual Spec repository (leave empty if there is none) | Human |
| `token_diagnostic` | `ENABLED` or `DISABLED` | Human |
| `review.large_mode` | Large design review mode. `dual` (default, dual Review A and B) or `single` (one independent review) | **Human only** |
| `review.blind_reviewer_selection` | With `dual`, whether a human must choose the Review B model. `required` (default) or `optional` (if a human does not choose, the Agent chooses a model that meets the conditions) | **Human only** |
| `sdd.medium_artifacts` | Medium SDD layout. `full` (default, four documents) or `condensed` (three sections in a single `README.md`) | **Human only** |
| `hard_guard_extra` | Project-specific always-applied rules | Human |
| `skill_eval.cases_dir` | Where eval cases made from incidents are kept | Human |

For the following list values, each item uses only the defined keys. If a key differs or a value is empty, `render` rejects it. The other lists are lists of strings.

| Value | Item format |
| --- | --- |
| `grade_mapping` | `{"change": "change condition", "min_grade": "Medium"}`. min_grade allows only Trivial, Small, Medium and Large. Epic is an optional management unit |
| `human_judgment.delegations` | `{"scope": "delegated scope", "date": "YYYY-MM-DD", "confirmed_by": "person who recorded it"}` |
| `build.verification` | `{"scope": "change scope", "commands": "commands to run"}` |
| `modules.list` | `{"path": "module path", "role": "role"}` |
| `priority.product_examples` | `{"input": "work type", "examples": "Priority examples"}` |

Empty values appear as "Not set" in the generated outputs. Generation proceeds even while values are not set, but procedures that depend on those values (for example, creating work items or confirming a merge in the local-docs method without `tracker.root` or `merge_method`) stop.

Git and SDD publication remotes in the local-docs method follow the declarations above. If there is no remote, follow `Code remote` in W `tracker/local-docs.md`.

## 3. Order of work for the Agent

This guide is not in the copy, so give the Agent its address as well: `https://raw.githubusercontent.com/seok-jun/adaptive-agentic-sdd/<commit-sha>/docs/customization.md`. Replace `<commit-sha>` with the SHA used for the archive, and put that address in `<guide URL>` below as well. For an Agent that cannot access the web, paste the guide from the same archive, or place it in a temporary location outside the repository and give its path.

**① Observe.** Collect facts only, without changing code.

```text
Read .adaptive-sdd/methodology/core.md and .adaptive-sdd/workflow/README.md. Do not modify product code.
Actually check this repository's build and test commands, CI, module structure and dependency direction, how work is managed, existing rule files (AGENTS.md, CLAUDE.md),
and risky shared paths, and summarize them as facts. List what you could not confirm separately.
```

**② Draft project.json.**

```text
Based on the project.json value tables in the installation guide (<guide URL>), show me a draft of .adaptive-sdd/project.json.
For each value, separate the evidence (files, commands) from what you could not confirm, and leave the values decided by "Human only" or "Human" empty and collect them as questions.
Do not write to the file yet.
```

**③ Human decisions.** A human answers. The Agent does not decide human judgment points, delegations, write scope, the work management location, the worktree root, the merge method or prohibited models on the human's behalf (`core.md` `Human judgment` 3). For a delegation, the human states the scope and date directly; the Agent transcribes those words as they are and records that person in `confirmed_by`. The Agent does not propose a delegation or record it more broadly.

**④ Write and generate.**

```text
Write .adaptive-sdd/project.json as just decided, and generate with the commands below. Do not modify the pinned copy.
python3 -I -B .adaptive-sdd/tools/install.py render --project-root . --source-tag v1.0.0-preview.7 --source-commit <verified SHA>
python3 -I -B .adaptive-sdd/tools/install.py check --project-root .
If using the local-docs method, create the items/ and claims/ folders under tracker.root.
Show me the generated AGENTS.md, CLAUDE.md and .gitattributes blocks and the .adaptive-sdd/project/ documents.
```

`render` refuses to generate if the pinned copy differs from `MANIFEST.json`. If someone has hand-edited an already generated file, or a human's file already existed at the same path before installation, it does not overwrite the file and reports it as `KEPT` (the next `render` also leaves it as it is). A human decides whether to change that file (`--accept-overwrite <path>`).

**Allowing writes outside the repository.** `tracker.root` and `worktree_root` are outside the repository. If the Agent tool's default working scope is only inside the repository, those writes are blocked or ask for confirmation every time. Allow the two folders as additional working folders of the tool. For example, Claude Code uses `--add-dir <path>` at launch or `permissions.additionalDirectories` in its settings, and Codex CLI uses `--add-dir <path>` or `writable_roots` under `[sandbox_workspace_write]` in `config.toml`. Option names can differ between tool versions, so check the documentation of the version you use. A human grants the permission.

**Commit and push.** For an in-repository installation, review the generated outputs and the pinned copy, then bring them into the code remote and base branch that P declared. New lanes must be able to retrieve the same copy. Who merges and pushes, and how, follows P's authority; a direct push to the shared base branch is not required. For an external installation, prepare and check the external installation path and connection for each checkout. Whether to share a connection that contains local absolute paths, and the commit/exclude policy for installation files, are decided in P.

**⑤ Trial run on a small task.**

```text
Make [small task] a work item (managing-issues), take a lane (parallel-development), implement it (implementing-issues),
and close it (finishing-issues). When done, show me that the work document's metadata and record entries and the claim file remain as in the W tracker mapping table.
```

**⑥ Improve after real work.** Do this each time a task finishes.

```text
Review this task's closing summary and incident records with "Using observations for the next judgment" in M adaptation.md.
Propose dispositions only for what has evidence, and separate what can be solved with project.json from what requires editing the pinned copy.
If an incident is worth turning into an eval case, show only a draft using the "Turning an incident into a case" rule in W process/skill-evals.md.
```

Actually running the cases to compare supports costs model calls and money. Do it only after a human has decided the scope, number of runs, models and budget, according to the "Comparison and adoption" conditions in W `skill-evals.md`.

## 4. Verification and checks

```bash
python3 -I -B .adaptive-sdd/tools/install.py check --project-root .
python3 -I -B .adaptive-sdd/tools/install.py check-evals --project-root .
```

`check` changes nothing. It recomputes and compares the pinned copy, the lock and the generated outputs, and if they differ, it only reports what differs. It also reports files in the pinned copy that are not in the manifest (`EXTRA`) and leftover files that are no longer generated (`STALE`, for example `.agents/skills` after removing codex from `tools`). The per-tool Skill entries are also set to run this check once in the same run.

If Python is not available, only the pinned copy can be compared against the hashes in `MANIFEST.json` with PowerShell (the generated outputs cannot be checked). In that case the Skill entries stop with `BLOCKED`, so a human checks and then decides whether to proceed:

```powershell
$m = Get-Content .adaptive-sdd/MANIFEST.json -Raw -Encoding UTF8 | ConvertFrom-Json
$m.files.PSObject.Properties | ForEach-Object { $h = (Get-FileHash ".adaptive-sdd/$($_.Name)" -Algorithm SHA256).Hash; if ($h -eq $_.Value) { "OK   $($_.Name)" } else { "DIFF $($_.Name)" } }
```

## Upgrading

1. Get the copy of the newly reviewed commit and the guide of the same version as in section 1. For a published release, verify the tag's commit and follow that tag's guide. Delete the pinned copy folders first and replace them as a whole. Leave `project.json`, `project/` and `install.lock.json` as they are.
2. Run `render` again with the new commit and confirm with `check`. Specify the tag as well only when it meets the conditions below. A human looks at how the generated outputs changed through the diff.
3. Do not switch implicitly in the middle of work in progress. If you switch, record it as an interval starting from that point (`core.md`). Check active owners, running reviews, uncommitted changes and recent work records, and coordinate the Issues and the timing to which the change applies. Project policy changes also follow W [Plan correction and policy transition](../adaptive-sdd/workflow/process/sdd/plan-change.md#plan-correction-and-policy-transition). Do not get valid existing decisions re-approved or automatically repeat the whole review; update only the evidence that was actually invalidated.

When upgrading to an untagged revision, use `render --project-root . --source-commit <verified SHA>` and do not pass a branch name as `--source-tag`. If the commit differs from the previous value and no new tag is given, the previous `source.tag` is removed. Regeneration with the same commit, or without source options, preserves the existing values. A tag that was already left incorrectly can be removed with `--clear-source-tag`. A new tag must always be given together as `--source-tag <actual tag> --source-commit <verified SHA>`. The installer does not look up the remote tag's correspondence, so confirming it is the caller's responsibility, and a successful `check` does not mean that the tag's origin was verified.

When applying this version's requirement and decision recording rules, check the differences between the generated `project/issue-writing-guide.md` and the prohibition rules the project placed itself. Distinguish the minimum record of work requirements from collecting conversation logs, but do not automatically relax the project's information-disclosure or secret-protection restrictions. If a hand-edited generated output is `KEPT`, review the diff and update it only within the permitted scope.

### Switching Epic from an execution grade to a management unit

The W policy from preview.3 limits execution grades to Trivial, Small, Medium and Large. The source for Epic management, verification of common changes and the transition is W [Epic management unit](../adaptive-sdd/workflow/process/sdd/epic.md#epic-management-unit) and [Transition of existing Epics](../adaptive-sdd/workflow/process/sdd/epic.md#transition-of-existing-epics); starting an investigation and reusing analysis follow the [entry conditions](../adaptive-sdd/workflow/process/sdd/entry.md) and [Reusing existing analysis](../adaptive-sdd/workflow/process/sdd/entry.md#reusing-existing-analysis).

- If `grade_mapping` has `min_grade: Epic`, decide the execution grade again from the risk of the actual overall change, and a human updates the project values. The installer does not automatically substitute Large; it raises an error before render.
- Keep an existing `grade:Epic` Issue as a management document (`Work type: Epic`, `type:epic`, no grade), or convert it to a single execution Issue according to its actual scope. Management metadata in local-docs uses `type: epic`.
- Preserve the existing goals, human decisions, merge authority and valid analysis and verification. Do not reset an active lane or repeat analysis and reviews only because of the transition. The `human_judgment.large_epic_merge` key is kept for compatibility.

## Reporting a common problem

Report a problem that cannot be solved with `project.json` and can only be solved by editing the pinned copy as an issue in the public repository (`seok-jun/adaptive-agentic-sdd`). Before that, check your company's or project's information-disclosure policy. Leave out company and product names, code, data and internal paths, and write only the generalized problem and the change needed.

## Methodology-only copy

This section is carried over from the preview.4 English guide; the Korean guide points here instead of repeating it.

A project may instead copy only `methodology/` and `LICENSE`, without W, the templates or the installer. That copy is a thin common layer: it does not contain v0.2's grades, review gates, starter or templates, and the project defines the rest of its way of working. Do not edit the copy; put every project-specific adjustment in the adapter. When upgrading, replace only the copy as a whole and leave the adapter and work records as they are. A problem that can only be solved by editing the copy is reported as in [Reporting a common problem](#reporting-a-common-problem).

| What | Default location (changeable) | Who edits it |
| --- | --- | --- |
| Methodology copy | `.adaptive-sdd/methodology/` | Nobody edits it. Replace it as a whole when upgrading |
| License | `.adaptive-sdd/LICENSE` | Not edited |
| Adapter | `.adaptive-sdd/adapter.md` | The project. `core.md` does not require a separate file, so it may live inside existing working instructions |
| Entry file | Existing `AGENTS.md` or `CLAUDE.md` | The project. Add only a few lines |
| Work records | Where the adapter says | The Agent doing the work |

If you change a default location, also change the `.gitattributes` line and the entry-file lines below.

### Adapter slots

Some slots are required by `core.md`; others are chosen by the project. Do not leave an unknown slot blank; write "undecided" and why.

| Slot | Type | Example |
| --- | --- | --- |
| Task identification method | Required | Issue number; otherwise date and task name |
| Work-record reference location and how to find earlier records | Required | Task document per task under `docs/work/`; find earlier ones by task ID |
| Problem record location | Required | Events section of the task document |
| Closing summary location | Required | End of the same task document |
| Final close decision | Required | Merge confirmed, deployment confirmed |
| Allowed query/write means and scope | Required | Local repository and development DB only; no production writes |
| Human judgment points | Required (`core.md` "Human judgment" 2). The project decides how many and where | Merge and deployment; whether to have design approval. If there are no fixed points, write "No fixed points — stop at unresolved judgment". A delegation counts as a human decision only when a human records it here with its scope, date, and confirmer |
| Checks to run and prohibited scope | Optional | Build and unit tests; commands that must not be run |
| Review path | Optional | When and how many times to get an independent review |
| Repository layout | Optional | Whether code and documents live in one repository |
| Machine-specific paths | Optional | Tool installation paths |

Starting shape of the adapter:

```markdown
# Methodology adapter

## Pin
- Source: <repository URL>
- Commit: <reviewed full commit SHA used for the archive and guide>
- Tag: <verified published tag, or none for an unreleased commit>
- Manifest hash: <sha256 of the manifest.json file>
- Copy location: .adaptive-sdd/methodology/

## Required slots
- Task identification method:
- Work-record reference location and how to find earlier records:
- Problem record location:
- Closing summary location:
- Final close decision:
- Allowed query/write means and scope:
- Human judgment points:

## Project-chosen slots
- Checks to run and prohibited scope:
- Review path:
- Repository layout:
- Machine-specific paths:
```

### Getting the copy, checking hashes and recording the pin

1. Verify the release commit SHA as in [section 1](#1-getting-the-copy). Download `https://github.com/seok-jun/adaptive-agentic-sdd/archive/<commit-sha>.zip`, replacing `<commit-sha>` with that SHA. The archive contains one top-level folder.
2. Copy the archive's `methodology/` contents (`core.md`, `adaptation.md`, `supports/`, `manifest.json`) to `.adaptive-sdd/methodology/` and `LICENSE` to `.adaptive-sdd/LICENSE`, **byte for byte**. Keep the LICENSE (MIT) with the copy because it requires the copyright and permission notice to be retained. Do not rewrite the files with a text editor or an Agent's file-writing tool; a BOM or CRLF would change the hashes. Windows PowerShell example:

```powershell
$sourceCommit = "<full commit SHA verified for v1.0.0-preview.7>"
if ($sourceCommit -notmatch '^[0-9a-f]{40}$') { throw "Set sourceCommit to the reviewed full commit SHA." }
$zip = "adaptive-sdd-$sourceCommit.zip"
Invoke-WebRequest "https://github.com/seok-jun/adaptive-agentic-sdd/archive/$sourceCommit.zip" -OutFile $zip
$tmp = Join-Path $env:TEMP "adaptive-sdd-preview"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive $zip -DestinationPath $tmp
$src = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
New-Item -ItemType Directory -Force .adaptive-sdd | Out-Null
Remove-Item .adaptive-sdd/methodology -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "$src/methodology" .adaptive-sdd/methodology -Recurse
Copy-Item "$src/LICENSE" .adaptive-sdd/LICENSE
```
3. Use `docs/customization.md` from the same archive, or its commit-pinned URL in section 3. Keep the archive, guide, and recorded source commit aligned; do not substitute a later branch tip or an older tag's guide.
4. Compare the hashes. The sha256 of each of the three documents must equal the value in `manifest.json`. The **manifest hash** is the sha256 of the `manifest.json` file itself.

Windows PowerShell:

```powershell
$d = ".adaptive-sdd/methodology"
$m = Get-Content "$d/manifest.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$m.files.PSObject.Properties | ForEach-Object { $h = (Get-FileHash "$d/$($_.Name)" -Algorithm SHA256).Hash; if ($h -eq $_.Value) { "OK   $($_.Name)" } else { "DIFF $($_.Name)" } }
(Get-FileHash "$d/manifest.json" -Algorithm SHA256).Hash.ToLower()
```

`Get-FileHash` prints uppercase hexadecimal. PowerShell's `-eq` is case-insensitive, so the comparison works as is. The last line is the manifest hash.

On macOS or Linux, compare the first three lines of the output below with the values in `manifest.json`. The last line is the manifest hash. You may also have an Agent compute and compare them.

```bash
cd .adaptive-sdd/methodology && sha256sum core.md adaptation.md supports/ordered-changes.md manifest.json
```

On macOS, use `shasum -a 256` instead of `sha256sum`.

5. Record the verified `v1.0.0-preview.7` tag, full commit SHA and manifest hash in the adapter's "Pin" section. For an unreleased commit, record no tag. A tag or branch name alone cannot stand in for the source (`core.md` "Application and improvement observation").

### Line endings and entry file

**Pin line endings.** Add the line below to the project's `.gitattributes`. Without it, on Windows with `core.autocrlf=true`, every new checkout turns the copy into CRLF and the hashes no longer match.

```text
.adaptive-sdd/methodology/** text eol=lf
```

**Entry file.** Add a few lines like the ones below to the existing `AGENTS.md` or `CLAUDE.md`. Do not overwrite existing content.

```markdown
## Working methodology

At the start of work, read and follow `.adaptive-sdd/methodology/core.md`, the documents it references, and `.adaptive-sdd/adapter.md`.
Do not edit `.adaptive-sdd/methodology/`. Put project adjustments only in the adapter.
```

### Order of work for the Agent

Give the Agent the steps below in order, with the guide address as in section 3, and look at each step's result before moving on.

**① Observe.**

```text
Read .adaptive-sdd/methodology/core.md. Do not modify product code.
Actually check this repository's build and test commands, CI, how work is managed,
existing rule files, and risky shared paths, and summarize them as facts. List what you could not confirm separately.
```

**② Draft the adapter.**

```text
For each adapter slot in core.md and the customization guide (<guide URL>),
show the proposed value, the evidence (files, commands), and what you could not confirm, separately. Collect what I need to decide in one place.
```

**③ Human decisions.** A human answers. Usually the write scope, the final close decision, the human judgment points, and prohibited execution scope are decided by a human. The Agent does not decide them instead (`core.md` "Human judgment" 3).

**④ Write the adapter and connect it.**

```text
Write .adaptive-sdd/adapter.md as just decided, and add the lines from the customization guide
(<guide URL>) to the entry file and .gitattributes.
Do not modify .adaptive-sdd/methodology/. For the pin, recompute and record the confirmed hashes,
and record the exact commit SHA selected for the downloaded archive. Do not overwrite existing entry-file content.
```

**⑤ Trial run on a small task.**

```text
Carry out [small task] following the methodology. When done, show that the start record and the closing summary
were actually written to the locations defined in the adapter.
```

**⑥ Adjust after real work.** Do this each time a task finishes.

```text
Look at this task's records and judge whether anything in the adapter should change.
Propose only what has evidence, and separate anything that looks like a problem with the common copy.
```

### Upgrading a methodology-only copy

1. Repeat the steps above with the newly reviewed commit's archive and matching guide. For a published release, verify the tag's commit and use its guide. Delete the copy folder first and replace it as a whole; leftover old files are not caught by the hash comparison.
2. Update the adapter's "Pin" section with the new values and record the date of the change. Do not edit records of earlier intervals.
3. Do not switch implicitly in the middle of a task in progress; follow step 3 of [Upgrading](#upgrading).
