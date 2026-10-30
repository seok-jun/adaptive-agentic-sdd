# Verification contract

Read this when linking acceptance criteria to verification and when running verification during implementation and at closing. For grade classification, [sdd-workflow](sdd/grade.md#sdd-grade) is the source; for the actual project commands, `W/../project/build.md` is the source. Do not fill in new verification by quantity; apply it to the scope required by the grade, the change impact and the Issue.

| Current work | Section to read |
| --- | --- |
| Linking acceptance criteria to verification means before implementation | [Verification Strategy](#verification-strategy), [Review gate by grade](#review-gate-by-grade) |
| Implementation loop, final candidate verification, PASS reuse | [Verification sequencing and PASS validity](#verification-sequencing-and-pass-validity) |
| Running build and test commands | [Verification environment](#verification-environment) |

## Verification Strategy

P's `build.md` may declare the existing `build.verification` command and the command/manual, agent/human, required/optional means of `build.checks`. For a required manual check, hand over the target, procedure and expected result, and leave as evidence the actual observed result, the confirmer, the time and the identity of the verification target. Until the evidence is received it is unverified, and the manual verification declaration itself is not treated as a PASS. Do not invent a fake command/exit code for a manual item that has no command to run. The condition that there must be a means of proving the acceptance criteria is the same.

If P's test lifetime is temporary, preserve and re-retrieve the tests, fixtures, execution evidence and the actual product input identity in the declared location, and then remove them. Link the correspondence between the final candidate and the execution inputs in the Packet, and apply the existing PASS reuse conditions. If it is none, equivalent declared behavior-observation evidence is needed instead of new tests, and a PLAN finding that needs a fixture/test must also actually prove its resolution expectation. If it cannot be proven, block; do not use the test policy as an excuse to exempt required verification.

Before implementation, decide by what evidence each Acceptance Criterion will be judged. Choose only the verification means actually needed among unit, integration, lint, build, CI and the review for the grade.

From the requirements at the revision the project approved or designated as the baseline, distinguish the application entry points, actors, conditions and expected results, and link them to verification. Cover the paths among normal, failure and cancellation that the original requirement or the change impact touches; do not fill in a fixed number of cases. Reuse the mappings in the existing Issue/SDD/change-plan and supplement only what is missing. New IDs, tables or separate plan files are not required. If the baseline source cannot be found or interpretations diverge, leave the mapping as unconfirmed, and progress that depends on that judgment follows the existing gates.

In the implementation review and the closing self-review, compare baseline requirements → actual changes → the verification results and gaps of the final candidate. Check not only the mappings already filled in, but also any entry points and conditions in the baseline requirements that have been omitted from those mappings. Agreement among the latest documents or a CI PASS alone does not stand in for meeting the baseline requirements. If there is test removal, weakened assertions, excluded runs or a change of verification target, expose the substitute evidence and the remaining gaps in the existing SUMMARY; changes to required verification follow the existing authority. Reused results show the target, the input scope and the fact of reuse, and are not reported as new runs.

- For Medium and above, map the Acceptance Criterion, verification means and success evidence in `02-to-be.md`.
- The Human View keeps the evidence for judging completion, and the detailed test cases, commands and execution evidence go in the change-plan. Do not duplicate the same content.
- For Small, if all acceptance criteria can be proven with the existing verification baseline alone, do not create a separate document. If verification design is needed, state the same mapping briefly in the work evidence before implementation.
- Trivial proves its acceptance criteria with targeted validation suited to the kind of change and does not create a separate Verification Strategy document.
- If the acceptance criteria cannot be proven or verification would have to cross the Issue boundaries, `BLOCKED` before implementation.
- Reuse the environment, JDK, Issue and source results checked in the same run, and run targeted verification first.

The Verification Strategy includes the following verdict according to the grade rules.

```text
Independent Review: REQUIRED | NOT REQUIRED
```

Trivial is always `Independent Review: NOT REQUIRED`. Do not automatically add a Device QA / Runtime QA verdict or handoff as a common required gate. A device observation document that P declares as simple reference is kept as non-required reference material. However, if P's build.checks or the Issue Verification Strategy explicitly marks a device or runtime check as required, apply the manual verification contract above and confirm the actual result before merge/complete. Do not lower explicitly stated required verification to reference material.

## Review gate by grade

Review A and the default code review use the [phase-aware Contract Review Packet](../skills/_shared/execution-packets.md#review-packet). Require only the artifacts and evidence that exist in that phase, and do not make the reviewer do solution discovery or a repository-wide re-exploration. Check the fields and evidence identity in the packet source.

An independent review is performed by a reviewer different from the implementation/document author, who records `PASS` or `BLOCKED` and the unresolved findings in the PR review or a comment. Review A checks caller/callee, path/symbol, invariants and consistency with the phase contract, and Review B audits completeness with the minimal Blind Audit Packet of [Design review](design-review.md#large-design-dual-independent-review). Human judgment does not replace this responsibility. Review B passes only after confirming that the needed reconciliation is complete and that there are 0 unresolved Human Decision/Execution-contract blockers; the number of Implementation findings and Non-blocking observations does not need to be 0. In a grade where independent review is not required, Agent self-review and automation take on that verification.

| grade | Pre-implementation design review | PR code review |
| --- | --- | --- |
| Trivial | Self-review of the Trivial conditions and target scope | targeted validation + self-review of diff ↔ requested scope |
| Small | Self-review of the Issue boundaries and verifiability | Self-review of diff ↔ acceptance criteria |
| Medium | Bounded self-review of the SDD and Verification Strategy. If a shared contract or integration evidence across several modules is needed, decide independent review as `REQUIRED` | If `Independent Review: REQUIRED`, a bounded independent review must pass; otherwise self-review |
| Large | Review A Contract Review + Human-selected Review B Blind Audit required for each of AS-IS/PLAN | One existing bounded independent code review; only an explicit high-risk escalation may add an additional audit |

If a required review is incomplete, or a boundary violation, unmet acceptance criteria, or an obvious safety or consistency problem is unresolved, do not proceed with implementation or merge.

## Verification sequencing and PASS validity

The following terms are the common basis for running the minimum verification by grade and each Issue's Verification Strategy.

- **Verification-affecting input**: an input that a verification command consumes or asserts on, such as production/test source, resource, manifest, runtime asset, build/dependency/configuration, schema/migration/contract, fixture/snapshot/generated input/test expectation. Do not decide by extension or `docs` path alone; Markdown and assets consumed at runtime are included.
- **Owning module**: the build module (the module unit P declares; for Gradle, a Gradle module) that contains a verification-affecting changed file by its actual path. Decide by file location, not by test name or another domain term.
- **Direct-impact module**: an immediate consumer of a changed public/behavioral contract, an impacted module the Issue Verification Strategy designates, or a module whose direct impact a concrete compile/test failure proved.
- **Stable final candidate**: a candidate in which the planned file changes and the required fixes for review findings already confirmed are finished, with no further edits planned. A final CODE Review PASS is not a precondition for preparing verification evidence. If verification or review produces additional edits, update to a new candidate.
- **Required broad command set**: the whole set of test/lint/build commands required by the grade/change-scope criteria of this document and by the Issue Verification Strategy. It is not fixed to one particular root command, and the Issue's explicit requirements take precedence.

In the implementation loop, identify the owning module of each verification-affecting changed file and run the directly related test class or the owning-module tests first. If several modules or a public/behavioral contract change, expand only to the changed modules and the direct-impact modules with evidence. Do not make repository-wide guesses to find all transitive consumers; the wider regression scope is the job of the required broad command set on the stable final candidate. For a targeted failure, fix and re-run starting from the failing test or the owning module rather than the whole suite. Include the instrumentation or device test paths P declares in the default targeted scope only when the Issue Verification Strategy or the repository command contract explicitly requires them.

Each PASS belongs to the command run and the set of candidate inputs that command verified. If a verification-affecting input that the command consumes or asserts on changes, that PASS is invalidated. A rebase/base merge or a dependency/build input change follows the same rule when it affects the command result. If only Issue/PR comments, review discussion, the PR description or non-runtime documentation change, the runtime build verification PASS may be kept, but a static validator or Skill behavior eval that uses those inputs is run again.

On the stable final candidate, each command of the required broad command set must have a PASS run on the current candidate or a PASS reusable on evidence that its inputs did not change. The final CODE Review/self-review is performed after securing this evidence, and at closing, confirm that the review and verification evidence are all valid on the same candidate. If an input changes after broad verification, perform the affected targeted verification first, re-run the invalidated broad commands on the new stable final candidate, and then review on that evidence. Commands whose inputs did not change are not repeated, but do not read `once at completion` as reuse of a stale PASS from a different candidate.

If P has declared an impact analysis tool, the reference, freshness and consumption conditions of its results follow [Common impact result reference and local consumption](../skills/_shared/execution-packets.md#common-impact-result-reference-and-local-consumption) and the P project document `execution-routing.md`, and those results are a lower bound on the verification obligations above. Do not carry over partial PASSes during development or reviews of an earlier SHA as completion evidence for the current final candidate.

## Verification environment

Apply [build-preflight](../skills/_shared/build-preflight.md) before build and test commands. Do not decide that a dependency is not installed merely because an environment variable is empty. Device and emulator work follows only the procedure declared in the P project document `build.md`; if nothing is declared, it is not performed. An optional device check is neither evidence nor a blocker for merge or complete.

For required local build verification, check the following. Do not use this section as a reason to add a full build gate to non-runtime document, Skill or eval changes that were not originally required.

1. After preflight, in the intended process environment, confirm with the build tool's version command (`gradlew --version` for Gradle) that the actual launcher/daemon JVM major version equals P's `JDK major`. Do not pass on a usable current Java/`JAVA_HOME` alone.
2. If they differ, do not run the required command or record it as a canonical PASS. Inject a JDK of the declared version that is already installed and verifiable into the current process only, confirm the version, and run the same command. Automatic installation, download and persistent environment changes are forbidden.
3. A static analysis/build failure that first occurred on a JVM different from the declaration is classified as an environment failure and is not settled as a product/code regression. Re-run the same required command on the declared-version JDK to decide.
4. If the declared-version JDK or the actual build JVM cannot be confirmed, stop with `BLOCKED: canonical build JDK unavailable` and record the commands not run and the evidence. If preflight is `BLOCKED: JDK unavailable`, do not run the build tool.
5. Reuse the JDK and tool check results verified in the same run by re-injecting them into subsequent shells. Without evidence of an input or environment change, do not repeat the search and version check.

A required verification that was not run is `unverified` and is not a PASS. Not running build verification that the grade does not require is not a blocker. If fixing a failure needs a forbidden path, `BLOCKED`, and before handoff confirm that the changed-file list contains no forbidden/unrelated paths.
