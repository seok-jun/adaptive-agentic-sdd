# Try-sandbox demo runs — 2026-11-07

Real agent runs in sandboxes created by `try/setup.py` (English edition). The two Codex runs below are the source of the shortened transcript in [`docs/assets/demo.svg`](../../assets/demo.svg). This is a demonstration, not an evaluation: one run per task, no comparison, no grader.

These runs used the workflow before 1.1.0, so the Small run below wrote seven records. From 1.1.0 a normal Small task writes three; see the [before/after runs](../2026-11-07-small-redesign/README.md).

## Codex runs on Windows: setup

- Distribution checkout: `60cf771` plus the uncommitted `try/setup.py` from this change. Each task used a fresh sandbox; setup reported product tests passing and resolver READY.
- Agent: Codex CLI 0.163.0, requested `gpt-6-astra` / `high` (`codex exec`, workspace-write sandbox on Windows). Served model identity was not separately verified.
- Prompt: the selection prompt from the sandbox's `START-HERE.md`, with its last line replaced by one task.
- Deviations from START-HERE: Codex started in the sandbox root (not `product/`) with `--skip-git-repo-check`, because the root is not a Git repository; the checkout was also passed with `--add-dir`. A session-specific Git config trusted only the sandbox's four repositories (Windows sandbox account ownership check). `TMP`/`TEMP`/`TMPDIR` pointed to the sandbox's `scratch/`. One earlier attempt per task stopped immediately with Codex's "not inside a trusted directory" check, before reading any file.

## Codex runs on Windows: results

| Task | Grade recorded | Outcome |
| --- | --- | --- |
| Fix `catalog.search.page` so `page([1, 2, 3, 4], 1, 3)` returns `[1, 2, 3]`; add regression tests | Small (P2) | Claimed `catalog/search.py` and `tests/test_search.py`. New tests failed first (`FAILED (failures=5)`), then the fix passed 7 catalog and all 8 product tests. Merged into the local origin `main` (`a1d61d0`), item closed, claim released. Records: CLAIM, IMPLEMENTATION SUMMARY, MERGED, CLOSED, PRODUCT COMPLETE, LOCAL CLEANUP, RELEASE |
| Add password hashing and storage to `members` | Large (P3) | Recorded the item, changed no product file, merged nothing and stopped with `[HUMAN DECISION REQUIRED]` listing purpose, retained data, storage boundary, algorithm/dependencies, access rules and deletion policy |

Independent checks after the runs:

- A fresh clone of the Small sandbox's origin `main` passed all product tests, and `page([1, 2, 3, 4], 1, 3)` returned `[1, 2, 3]`.
- Files modified after the prompt, excluding Git metadata and bare remotes: Small — `product/catalog/search.py`, `product/tests/test_search.py`, `records/items/TRY-1.md`; Large — `records/items/TRY-1.md` only. The selected W checkouts stayed clean and the distribution checkout had no agent changes.

## macOS check

A separate Claude Code session on a Mac verified commit `bb81b27` (this change) without editing it: macOS 12.7.6, Python 3.14.10, Git 2.37.1 (Apple Git-137.1), x86_64.

- `python3 adaptive-agentic-sdd/try/setup.py` (README default) and `--lang ko` both printed product tests passed and resolver READY.
- Rerunning the default command exited 1 with the existing-target refusal; a hash of every path, size, modification time and mode under the target was identical before and after.
- Both `START-HERE.md` files showed POSIX (`sh`) commands, no PowerShell syntax, and every referenced path existed.
- The full suite ran 123 tests, OK, with no `/var` → `/private/var` path failures; the clone stayed clean afterwards.

## Claude Code run on macOS

In a fresh, untouched English sandbox from the macOS check, a new Claude Code session (host-reported model Opus 5.5, `claude-opus-5-5`; requested model and reasoning settings unconfirmed; auto permission mode) received the START-HERE selection prompt with the same Small task. The agent's own read-only report afterwards, with the commands it was asked to print:

- Resolver exit 0, READY. Grade Small, priority P2. Records: CLAIM, IMPLEMENTATION SUMMARY, MERGED, CLOSED, PRODUCT COMPLETE, LOCAL CLEANUP, RELEASE; status closed.
- It reproduced the bug (`[1, 2]`), ran the new tests against a scratch copy of the original `search.py` (`FAILED (failures=1)`; only the tail of that output was kept), then passed 4 catalog and all 5 product tests on both the branch (`222f4aa`) and the merge result (`a535f83`). The merge commit changed `catalog/search.py` and `tests/test_search.py` only.
- Git 2.37 has no `merge-tree --write-tree`, so it used the local-docs adapter's fallback: a trial merge in a disposable worktree under the task scratch, removed afterwards. Its first `git merge --no-ff -F -` failed on Git 2.37 (`could not read file '-'`) without changing `main`; it retried with `-m` and recorded the incident in `[MERGED]`.
- All writes it directed were inside the sandbox (product, local remote, records, `scratch/TRY-1`, which it left in place). The host stored one oversized tool output under its own session folder. Host sandbox enforcement was not configured or tested.
- About 5–7 minutes in total by the agent's estimate; the recorded item lifetime was about 2 minutes.

This report was not independently re-verified from this machine.

## Limits

- The Large stop follows a rule the sandbox's product authority document states explicitly (password storage is undecided and needs human decisions). The run shows the workflow honoring a declared product rule, not the agent independently discovering the risk.
- Codex reported host enforcement of P's narrower write paths as unconfirmed: the sandbox writable roots were broader than the task paths, and no denied-write probe was run.
- One run per agent and task: Codex on Windows (Small and Large) and Claude Code on macOS (Small only). Durations were not measured precisely. No Korean edition agent run, Trivial task run or Claude Code Large run was made. Sandbox setup and the test suite were checked on Windows and macOS (above); Linux was not run.
- Raw CLI logs contain local paths and remain local; this summary and the demo transcript were prepared from them and from the sandbox records.
