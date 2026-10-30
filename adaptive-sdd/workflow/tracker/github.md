# Work tracking: GitHub

This document describes how the Issue, comment, label, assignee, PR and closing reference expressions of the W procedures are realized with **GitHub Issues and PRs**. The W procedures were first refined on this method, so the expressions map directly. P's application document `tracker.md` declares this method and sets the repository (`owner/name`) and the allowed authors.

| Expression in the W procedures | GitHub |
| --- | --- |
| Issue, `#N` | A GitHub Issue in the declared repository |
| `priority:*`, `grade:*`, `status:*` labels | Issue labels with the same names |
| Epic management document | The `type:epic` label and `Epic` under `## Work type` in the body. No `grade:*`. Child Issues are linked from the body, and the management Issue is closed after the evidence of overall completion is checked |
| assignee | Issue assignee |
| Issue comment, URL, `updated_at` | Issue comment and its URL and `updated_at` |
| `[CLAIM]` / `[RELEASE]` | An Issue comment that starts with that tag |
| PR, `Closes #N` | A PR in the declared repository and the closing reference in its body |
| merged / closed | The PR merged state and merge commit, the Issue closed state |
| CI | The repository's required checks. P declares the actual verification commands |

P and humans manage GitHub write permissions, tokens and secrets. The Agent does not create, look up or register tokens.

The code remote, the base of new lanes and the PR base follow the git.remote/base_branch/merge_branch declarations in P's tracker.md. When creating a PR, state the base explicitly and do not guess the default branch. The SDD publication repository, remote and branch follow the review declaration and are kept distinct from the product PR head and the claim branch. External ID settings do not change GitHub's actually issued IDs or closing reference syntax, and no API adapter for other services is provided.
