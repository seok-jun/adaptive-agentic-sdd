# Customization guide (1.0 preview — unreleased)

This guide covers the unreleased `v1-preview` branch. Use a reviewed full commit SHA for the copy and the guide. To install the published `v1.0.0-preview.2`, use [its English guide](https://github.com/seok-jun/adaptive-agentic-sdd/blob/v1.0.0-preview.2/docs/customization.md) or [its Korean installer guide](https://github.com/seok-jun/adaptive-agentic-sdd/blob/v1.0.0-preview.2/ko/docs/customization.md). That tag does not support `--harness-root` or the new operating settings described here.

Generated default check and check-evals commands use literal path quoting for PowerShell on Windows and POSIX sh elsewhere; use the named shell. Custom commands remain project-owned.

This guide explains how to place a copy of the methodology in a project, adjust it to the project, and give work to an Agent. It is not part of the copy. The Korean edition is `ko/docs/customization.md`. In this preview the Korean edition installs a fuller copy, `ko/adaptive-sdd/` (methodology plus workflow procedures, skills, evals, and an installer), and follows its own guide; the English edition of those parts is pending.

The unreleased Korean workflow separates the optional Epic management type from its four execution grades. Its upgrade guide explains how to migrate former `grade:Epic` issues and `min_grade: Epic` mappings without silently changing human decisions or restarting active work. See [the Korean upgrade guide](../ko/docs/customization.md#버전-올리기); this is not a new grade requirement for the English methodology-only edition.

The same Korean upgrade guide now covers in-progress policy transitions and installer source identity. A new `--source-commit` without a tag removes the previous tag when the commit changes; a same-commit or source-option-free render preserves it. `--clear-source-tag` repairs an already incorrect tag. A supplied `--source-tag` requires the verified `--source-commit` alongside it; branch names are not tags. The installer does not verify remote tag correspondence. These installer/workflow features still have no English edition.

## Korean installer: external placement and operating settings

The unreleased Korean installer accepts `--harness-root S` alongside product checkout `--project-root P`. Place the pinned bundle at `S/.adaptive-sdd/`; neither root may contain the other. Settings, generated project documents and the lock stay in S. Product entry skills, marked AGENTS/CLAUDE blocks and `.agentics/adaptive-sdd.json` stay in P. External entry checks explicitly bind both roots and check the connection, manifest, lock and generated outputs. A changed bundle requires an explicit render with the reviewed S. Source commit authenticity is still the caller's responsibility.

One S is bound to one checkout. A new worktree needs its own S/connection; tracker storage may be shared. Hosts unable to read S need another accessible placement. Migration does not delete old copies or overwrite hand edits: review KEPT output before accepting individual replacements. The project decides whether to commit or exclude local connection files. In-repository installation must reach the declared base branch through the project's authorized integration process, not a mandatory direct push to main. Preserve LF bytes when versioning S.

Optional schema-1 settings retain defaults for existing installations:

| Settings | Meaning |
| --- | --- |
| `git.remote/base_branch/merge_branch` | Code remote, new-lane base and merge target; defaults origin/main/main |
| `review.repository/remote/branch` | Publication repository absolute path, remote and branch; empty defaults P/code remote/issue branch. A local bare remote still requires exact-artifact reviewer access |
| `tracker.id_source/id_format/child_id_rule` | generated or external IDs; external requires a format and preserves source IDs. Child issuance follows declared authority |
| `project.conversation_language/conventions` | Conversation/report language and convention source reference |
| `build.checks` | List with scope, method, actor, instructions, evidence, required. method: command/manual; actor: agent/human; required: required/optional |
| `build.test_mode/test_format/test_preserve_at` | persistent (default), temporary or none; format and preservation location (required for temporary; relative paths use P) |
| `routing.role_defaults` | role/model/reasoning preferences for PLAN, IMPLEMENT, REVIEW, TEST_DOCS, FINISH |
| `routing.capabilities` | host/model/tier/reasoning/source/identity/valid_until records; cheap/strong/frontier tiers and timezone-qualified ISO expiry |
| `routing.qualification_records` | Separate role qualification evidence reference |

Existing verification commands and new checks both apply. Manual evidence needs target, confirmer, time and observations; requesting a check is not a pass. Preserve and re-query temporary tests, fixtures and execution evidence before removal, linking actual inputs to the final candidate. No-new-test mode still needs equivalent acceptance/finding evidence and cannot waive required verification. Model preferences do not establish capability, qualification or a human's Review B selection. Verify source, freshness and host support when selecting; inherited current/manual reviewers still need actual model/reasoning evidence. These declarations do not grant Git or execution authority or silently replace earlier decisions. Use the existing policy-transition procedure for active work.

The Korean guide and this feature description are synchronized; the full workflow/templates/tools English edition remains pending.

## What this preview is

- **A thin common layer.** `methodology/core.md` defines a minimal workflow, human-judgment requirements, and work records and observation. `methodology/adaptation.md` contains the rules for choosing supports based on observation. `methodology/supports/ordered-changes.md` is one default support.
- **Not a replacement for v0.2.** It does not contain v0.2's grades, review gates, starter, or templates. The project defines the rest of its way of working.
- **Effect not verified.** The structure may change. Until the final 1.0, it is published only as preview tags.

## What goes where

| What | Default location (changeable) | Who edits it |
| --- | --- | --- |
| Methodology copy | `.adaptive-sdd/methodology/` | Nobody edits it. Replace it as a whole when upgrading |
| License | `.adaptive-sdd/LICENSE` | Not edited |
| Adapter | `.adaptive-sdd/adapter.md` | The project. `core.md` does not require a separate file, so it may live inside existing working instructions |
| Entry file | Existing `AGENTS.md` or `CLAUDE.md` | The project. Add only a few lines |
| Work records | Where the adapter says | The Agent doing the work |

If you change a default location, also change the `.gitattributes` line and the entry-file lines below.

## Where to make changes

- Do not edit the common copy. Put every project-specific adjustment in the adapter.
- When upgrading, replace only the copy as a whole and leave the adapter and work records as they are. That way, upgrading the common layer does not collide with project adjustments.
- If a problem can only be solved by editing the copy, treat it as a missing slot in the common layer and report it to the public repository (last section).

## Adapter slots

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

## 1. Getting the copy and recording the pin

1. Select and review a full commit SHA from `v1-preview`. `git ls-remote https://github.com/seok-jun/adaptive-agentic-sdd refs/heads/v1-preview` shows the current candidate; keep the selected SHA even if the branch advances later. Download `https://github.com/seok-jun/adaptive-agentic-sdd/archive/<commit-sha>.zip`, replacing `<commit-sha>` with that SHA. The archive contains one top-level folder.
2. Copy the archive's `methodology/` contents (`core.md`, `adaptation.md`, `supports/`, `manifest.json`) to `.adaptive-sdd/methodology/` and `LICENSE` to `.adaptive-sdd/LICENSE`, **byte for byte**. Keep the LICENSE (MIT) with the copy because it requires the copyright and permission notice to be retained. Do not rewrite the files with a text editor or an Agent's file-writing tool; a BOM or CRLF would change the hashes. Windows PowerShell example:

```powershell
$sourceCommit = "<reviewed full commit SHA>"
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

5. Record the commit SHA and manifest hash in the adapter's "Pin" section. Record a tag only when a published tag has been verified to point to that commit; otherwise record no tag. A tag or branch name alone cannot stand in for the source (`core.md` "Application and improvement observation").

## 2. Placing it in the project

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

## 3. Order of work for the Agent

The first time, give the Agent the steps below in order. Look at each step's result before moving on. This guide is not in the copy, so give the Agent its address: `https://raw.githubusercontent.com/seok-jun/adaptive-agentic-sdd/<commit-sha>/docs/customization.md`. Replace `<commit-sha>` with the exact SHA used for the archive, and substitute that address for `<guide URL>` below. If web access is unavailable, provide the guide from the same archive.

**① Observe.** Collect facts without changing code.

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

## Upgrading

1. Repeat section 1 with the newly reviewed commit's archive and matching guide. For a published release, verify the tag's commit and use its guide. Delete the copy folder first and replace it as a whole; leftover old files are not caught by the hash comparison.
2. Update the adapter's "Pin" section with the new values and record the date of the change. Do not edit records of earlier intervals.
3. Do not switch implicitly in the middle of a task in progress. If you switch, record it as an interval starting at that point. Check active owners, running reviews, uncommitted changes, and recent work records to coordinate which tasks and stages adopt the change. The Korean workflow defines plan correction and policy transition in [process/sdd/plan-change.md](../ko/adaptive-sdd/workflow/process/sdd/plan-change.md#계획-정정과-정책-전환); retain valid prior decisions and review evidence rather than automatically restarting them.

When adopting the requirement/decision recording clarification in `core.md`, check project-owned restrictions as well. Minimal task requirement and decision records are distinct from collecting conversation logs; the clarification does not automatically relax project disclosure or secret-protection rules. In the Korean installer, inspect generated `project/issue-writing-guide.md` differences and any `KEPT` hand-edited outputs before updating them within the permitted scope.

## Reporting a common problem

Report a problem that the adapter cannot solve and that requires editing the copy as an issue in the public repository (`seok-jun/adaptive-agentic-sdd`). Before that, check your company's or project's information-disclosure policy. Leave out company and product names, code, data, and internal paths, and write only the generalized problem and the change needed.
