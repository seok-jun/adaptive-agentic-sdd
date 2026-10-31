# First-use runs from the README (2026-10-31)

Three runs in which a fresh agent session read only the README and the installation guide and tried, in a disposable repository with a local bare `origin`: **A** install and commit, **B** "Your first task" (fix an off-by-one in `catalog.search.page` inside `catalog/` and add a regression test), **C** undo the installation. The human answers were written into the prompt in advance, including a one-task instruction to merge. Raw transcripts and the agents' own reports stay outside the repository; the results below were checked against the disposable repositories.

| Run | Source | A install | B first task | C undo |
| --- | --- | --- | --- | --- |
| 1. Claude Code agent (`claude-opus-5-5`), English | candidate `d7a2b27` | done | done: Small, claim before first edit, module tests first, full suite, merge, `[PRODUCT COMPLETE]`, release | done (revert; not pushed) |
| 2. Codex CLI 0.163.0 (`gpt-6-astra`, medium), Korean | candidate `d7a2b27` | installed and checked; **commit blocked**: the `workspace-write` sandbox makes `.git` read-only | not started | blocked |
| 3. Codex, same settings, Korean | published tag `v1.0.0-preview.6` | first attempt: **render blocked**, `.agents/` is read-only in the sandbox. Second attempt with `--add-dir <repo>/.agents` and the Git data folder outside `.git`: done, committed and pushed | **BLOCKED** at implementation entry: no fresh evidence that the current model meets the phase floor | done (revert pushed; checkout equals the initial commit) |

## Findings

1. **First-task blocker in the method (resolved by policy decision c′, 2026-10-31; see the changelog).** `workflow/skills/_shared/execution-routing.md` lets the current model implement only when "fresh Host Capability evidence" shows it meets the phase floor. A first-time project has no `routing.capabilities` entries, and neither the README nor the guide says what counts as that evidence. Run 3 stopped there, as the rule says. Run 1 reported that it treated the host-reported model identity as enough, which is a guess. Resolving it changed what counts as evidence, so the repository owner decided it separately: routine Trivial/Small work now runs on the current model unless it is denied, and other routes keep requiring observed evidence. The runs above used the earlier rule.
2. **Codex sandbox paths (fixed in the README after preview.6).** In Codex `workspace-write`, `.git` and `.agents/` are read-only. An explicit `--add-dir <repo>/.agents` made `.agents/` writable (checked with a one-file probe and in run 3). Git writes need either the human to commit or Git data outside the protected `.git` path; run 3 used a separate Git data folder, which an ordinary repository does not have.
3. **README issues found in run 1 and fixed before preview.6:** an empty `ls-remote` result, `init` example values versus human decisions, the local-docs `items/` and `claims/` folders, and undo after a push.
4. **Other first-use notes (open):** `Invoke-WebRequest` failed where `curl.exe` worked on this machine; Codex's own approval review refused recursive deletion of download folders; run 1 listed six other unclear points (start-record tag, module ownership of `tests/`, fast-forward under `merge`, when acceptance checkboxes are ticked, CRLF files in lanes, and the capability evidence above).

## Limits

Three runs on one Windows machine, with human answers supplied in advance. Run 1 was a Claude agent inside a Claude Code session, not a separate CLI process. These runs show where a first-time user can get stuck; they do not measure how often, or any effect on outcomes, rework or cost.
