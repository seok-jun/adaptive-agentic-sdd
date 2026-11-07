# Try-sandbox demo runs — 2026-11-07

Two real agent runs in sandboxes created by `try/setup.py` (English edition). They are the source of the shortened transcript in [`docs/assets/demo.svg`](../../assets/demo.svg). This is a demonstration, not an evaluation: one run per task, no comparison, no grader.

## Setup

- Distribution checkout: `60cf771` plus the uncommitted `try/setup.py` from this change. Each task used a fresh sandbox; setup reported product tests passing and resolver READY.
- Agent: Codex CLI 0.163.0, requested `gpt-6-astra` / `high` (`codex exec`, workspace-write sandbox on Windows). Served model identity was not separately verified.
- Prompt: the selection prompt from the sandbox's `START-HERE.md`, with its last line replaced by one task.
- Deviations from START-HERE: Codex started in the sandbox root (not `product/`) with `--skip-git-repo-check`, because the root is not a Git repository; the checkout was also passed with `--add-dir`. A session-specific Git config trusted only the sandbox's four repositories (Windows sandbox account ownership check). `TMP`/`TEMP`/`TMPDIR` pointed to the sandbox's `scratch/`. One earlier attempt per task stopped immediately with Codex's "not inside a trusted directory" check, before reading any file.

## Results

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

No agent task was run on the Mac.

## Limits

- The Large stop follows a rule the sandbox's product authority document states explicitly (password storage is undecided and needs human decisions). The run shows the workflow honoring a declared product rule, not the agent independently discovering the risk.
- Codex reported host enforcement of P's narrower write paths as unconfirmed: the sandbox writable roots were broader than the task paths, and no denied-write probe was run.
- One agent run per task, on Windows, with one model. Durations were not measured precisely (a few minutes each). No Claude Code run, Korean edition agent run or Trivial task run was made. Sandbox setup and the test suite were checked on Windows and macOS (above); Linux was not run.
- Raw CLI logs contain local paths and remain local; this summary and the demo transcript were prepared from them and from the sandbox records.
