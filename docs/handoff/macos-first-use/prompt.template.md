You are trying an open-source methodology for the first time, in a disposable demo repository (the current directory). Nothing here is production. Work only inside __ROOT__.

Start by reading this README and follow it exactly, as a first-time user would:
https://github.com/seok-jun/adaptive-agentic-sdd/blob/__SHA__/README.md

This is an unreleased candidate after v1.0.0-preview.6. Wherever the README or guide says `v1.0.0-preview.6`, use the full commit `__SHA__` instead (archive https://github.com/seok-jun/adaptive-agentic-sdd/archive/__SHA__.zip, guide at the same commit), and omit `--source-tag` but keep `--source-commit __SHA__`. Use the English edition (adaptive-sdd/).

I cannot answer questions during this run. These are my answers as the human; treat them as given whenever the README or guide says to ask me:
- project.name "Library demo"; artifact_language "English"; tools: claude-code and codex.
- tracker: kind local-docs, root `__ROOT__/tracker`, id_prefix T, id_source generated, merge_method merge, allowed_authors empty.
- worktree_root `__ROOT__/wt`.
- git: remote origin, base_branch main, merge_branch main (origin is a local bare repository).
- build: tool "python unittest", module_unit "top-level package directory", verification: changes under catalog/ -> `python3 -m unittest discover -s tests/catalog -t .`; changes under members/ -> `python3 -m unittest discover -s tests/members -t .`; final candidate -> `python3 -m unittest discover -s tests -t .`. test_mode persistent. Everything else in build empty.
- modules.list: catalog/ (search), members/ (registry). No shared contracts.
- human_judgment: keep defaults, no delegations. Review profile and SDD layout: defaults. token_diagnostic DISABLED. priority.current_stage "demo"; other priority values empty.
- For this run only, I explicitly instruct you to merge the first task's branch into main with the merge method above and push it to origin, once its required checks pass. This instruction covers that one task only.

Then do these three parts in order:

A. Install, following the README Quick start, and commit the installation to main and push it.

B. Run the README "Your first task" with this change: "catalog.search.page returns one item too few per page (page([1,2,3,4], 1, 2) returns [1] instead of [1, 2]). Fix it inside catalog/ and add a regression test." Follow the installed skills until the task is closed as the README describes.

C. Undo the whole installation following the README "Undo" section, leaving the task's product fix in place. Then check what remains of the methodology.

Finally write `__ROOT__/report.md` (outside the repository) with these sections, short and factual:
1. Result of each part A/B/C: done / blocked, with evidence (commands and their output lines, file paths, commit SHAs).
2. Every point where the README or guide was unclear, wrong or missing a step, with the exact sentence and what you had to guess.
3. Every place you stopped as BLOCKED or would have asked me, and why.
4. Files added or changed by the installation, and whether the Undo left anything behind.
5. Rough count of methodology files you read in part B.
Do not invent results; write "not done" where you did not do something.
