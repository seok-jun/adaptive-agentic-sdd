# Verification of SDD selective reading and per-reader artifact layout

Verified: 2026-10-29. This change is a PR candidate, not the result of a product installation, deployment or policy adoption. The scope of the work is the Korean workflow. M's principles and the English common layer were not changed, and the English edition of the workflow had not been provided from before. (Translated record; the English workflow edition was added later, in preview.5.)

## Sources and baseline

- The consuming project's `install.lock.json` pins `663d925a8ce562225f7a8779d26b16a25fbf8eb7`. The lock and manifest on remote main were checked. The manifest blob is `eb0ed27eed64f3dca394a8f2238050fd3ace9bef` and its SHA-256 is `3450c4330069bd448e0717214a4c753856f2d7b94beb200b77f55304c2044b5c`. The local installation's manifest and workflow are byte-identical to this pinned source. The installation was not modified.
- `9577134` on public `main` is v0.2. The actually installable source is `ko/adaptive-sdd/` on `v1-preview`, and `068618bdda2f8d0571da3099f5e132e4ff17ff1e` exists after the pinned commit. A separate branch was created from the latest tree, which includes that later change's premise investigation, plan correction, review snapshot and external installation support. It was not overwritten with an older tree.
- The current table of contents, agent instructions and research/distribution boundary were checked in a separate research repository. The research repository itself was not made the consumption source, and private research material was not copied into the distribution bundle. The contracts already reflected in the public workflow are the baseline of this implementation.
- The reproduction baseline and the existing per-section SHA-256 values are in `tests/fixtures/sdd-section-map.json`. The distribution bundle's `MANIFEST.json` was updated. The installer verifies directories recursively, so no new runtime or installer branch was needed. The product lock, tags and releases were not changed.

## Causes of inefficiency and observation limits

The existing workflow was 24,510 bytes, with everything from classification to Epic and closing in one file. Even when each Skill asks for 'the relevant section', unrelated rules are easily read along at the file boundary. The same file is referenced again in implementation → review → closing. The artifact rules were also one 11,898-byte file mixing writing, correction and trade-offs. The existing instruction to reuse within the same run was kept, and no separate cache was created.

The PLAN already separated the Human Decision Contract (`02-to-be.md`) from the Agent Execution Spec (`change-plans/**`). So no names were changed and no new human-view/agent-spec files were added. The actual mixing was the AS-IS explanation, risks and code evidence, and the README's Priority, grade and edit paths could be managed twice alongside the Issue.

This is a static analysis of the documents' requirements and reference graph. This initial analysis did not collect a sample of the full artifacts of real user work or agent reading traces, so the duplication rate, unused rate and generated tokens in real operation are not established. No verification or risk item was deleted on the grounds that it 'is not consumed after being written'.

## Split details and consumption relationships

| Source file | New owning file | Consumption step / dependencies |
| --- | --- | --- |
| Grades and automatic escalation of the workflow | `sdd/grade.md` | Execution classification and re-grading; P's risk mapping |
| Entry, progress by grade, analysis reuse and routing guidance of the workflow | `sdd/entry.md` | First write and implementation entry; grade/issue, conditional verification/claim/routing |
| Issue contract, normalization and open dependencies of the workflow | `sdd/issue.md` | Managing, implementing, closing; human judgment and the Issue body source |
| Epic management and transition of the workflow | `sdd/epic.md` | Epic coordination; managing's classification input is grade, common questions are issue, child execution entry is entry |
| Document lifetime, business synchronization and closing order of the workflow | `sdd/completion.md` | Closing; issue/SUMMARY, verification, finishing |
| AS-IS investigation of the artifacts | `sdd/as-is.md` | Investigation, AS-IS review |
| TO-BE and actual alternatives of the artifacts | `sdd/to-be.md` | PLAN human decisions, AC verification mapping |
| Change plan of the artifacts | `sdd/agent-spec.md` | PLAN execution specification, implementation handoff |
| Plan correction of the artifacts | `sdd/plan-change.md` | Only when a premise error or policy change occurs |

`sdd-workflow.md` keeps only the path guide (1,906 bytes). `sdd-artifacts.md` owns the initial folder layout, readers and source links. There are 9 new detailed rules and 4 optional writing templates. Reading both guides and all detailed rules is actually larger than the two original files. The optimization target is per-step consumption, not the total stored size.

implementing reads grade/entry/issue directly and reads the owning files only for an actual AS-IS, PLAN or correction. finishing reads completion/issue directly, and managing reads grade/issue and, conditionally, epic. The claim contract of parallel-development was not changed. The relative links and anchors of the process documents and the paths in the P-generated templates were also updated. Reuse of a confirmed identical version is kept, and unconfirmed, changed or stale evidence is checked again.

## Judgment and lifetime per artifact item

| Information | Classification / change | Consumer and timing / omission risk |
| --- | --- | --- |
| Issue number, Priority, grade, allowed/forbidden | Switched to reference | Managing and entry check the Issue body and the baseline revision/time checked. Prevents drift of copied values; no guessing when inaccessible |
| Problem, cause model, relationships, behavior, key risks | Kept, physically moved | Human AS-IS judgment in the existing README. Provided together with evidence links; omitting risks is forbidden |
| Code paths, symbols, reproduction, facts/hypotheses/uninvestigated items | Kept | Consumed in `01-as-is.md` by design, reviewers and implementers. Needed to judge the validity of facts and premises |
| Direct external dependency versions, production consumers, intent of introduction | Kept (existing conditional) | Investigated only when it affects the judgment. Not expanded into an exhaustive history investigation |
| Document-code drift, premise conflicts, owner/needed step of open items | Kept | AS-IS → PLAN → implementation handoff. Does not block unrelated work; resolved before the consuming step |
| Changed/unchanged behavior, failures, data/state | Kept | Source of product meaning in TO-BE; important decisions are not hidden in the execution specification |
| Decision ID, choice, reason, actual alternatives, cost | Kept; duplicates switched to reference | Human judgment in TO-BE; the change plan references the D-ID. No fictional alternatives or separate trade-off document needed |
| AC and verification means/success evidence | Kept | TO-BE links acceptance criteria and verification. The change plan holds only execution details and does not duplicate the same contract |
| target/caller/callee, invariants, implementation order, schema | Kept | Agent specification → implementation, CODE review. Written only for applicable changes |
| Conventions, explicit departures, exception basis | Kept | PLAN/CODE review. Undeclared tastes do not become new rules |
| Test cases, commands, execution evidence, failure/rollback checks | Kept; evidence referenced | Consumed in verification and closing. Existing results are linked to the pinned target; past PASS is not inherited |
| Restating the original earlier AS-IS, Issue, code or review | Reduced and merged | Link the valid source and write only the differences. Checking reference access, revision, scope and premises is mandatory |
| Separate evidence files, duplicated completion reports | Prevents adding removal candidates | Not created when existing evidence is enough. The needed evidence itself is not removed |

The required working files remain the existing four kinds. The human-facing explanation of the AS-IS is the README, the direct evidence is 01-as-is, the human contract of the PLAN is 02-to-be, and the execution specification is the change plan. Medium proceeds without intermediate approval after the SDD, and Large keeps the existing AS-IS → A/B → PLAN → A/B order. A new AS-IS target is reviewed with both the README and 01-as-is as the same candidate. Existing layouts in progress are not migrated automatically.

The SDD is written and updated during the work and, after the business update based on the final code and the required verification, cleaned up under the existing reference preservation conditions. If there is an active consumer, it is switched to an immutable reference or preserved with an owner and release condition. The roles of the durable business/review documents are unchanged, and no lifetime exception was created for new evidence files either.

## Protection rules and verification

The 19 rule sections of the existing workflow map to their owning files with content hashes. Only link destination moves, cross-file instruction wording and the explicit naming of the two new AS-IS files are normalized, and the body is checked for omissions and duplicates. The artifact items were reviewed with the mapping table above. M/W/P sources, human judgment and STOP, Large A/B and Blind Audit independence, grade/claim/entry, required verification and PASS freshness, handoff, the business update from final code and artifact lifetime were preserved. Skipping the SDD for Small/Trivial is also kept.

- `python -I -B -m unittest discover -s tests -v`: 34 PASS. The existing 25, plus 9 checks for preservation, direct paths, separation of identical evidence, manifest, tampering/omission, measurement input and unique conditions/isolation.
- Includes installation render/check/check-evals, GitHub/local-docs trackers, external harness, Windows generated commands, relative links/anchors and review snapshot. The first run found a broken guide anchor and a Git shell restriction of the Windows sandbox. The anchor was fixed and the same tests were rerun outside the restriction and passed.
- The 60 existing behavior cases keep their content, and 10 new synthetic regression cases were added. Format and ID checks of all 70 PASS. LLM behavior evaluation was not run, so no claim is made of no behavior regression or of an actual compliance rate.
- `git diff --check`: PASS. Only the synthetic book service fixtures were used in the public material. No product code, conversations or private research content was moved.
- The author's self-review, deterministic checks and an independent review by a separate subagent were performed. Real host behavior evaluation and reruns on Linux/macOS were not performed.

## Static cost comparison

Reproduce with: `python -I -B tests/measure_sdd_reading.py`. It outputs the same baseline commit and file lists as JSON. The numbers are the `ceil(UTF-8 bytes / 4)` proxy of the existing evaluation convention, not model tokenizer measurements. In particular they do not match actual Korean tokens.

The selected W rules, Skills and verification (and design-review where applicable) are compared per cold phase. P project documents, code, working artifacts, conditional routing/packet/observations and system/user/tool inputs are excluded from both sides' numbers, while the execution obligations remain. Total model input, generated tokens and tool output overhead are not measured.

| Scenario | Existing full-file proxy | Existing workflow, ideal section choice only | New selected-file proxy | Reduction vs full read | File reads before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| Small implementation | 13,274 | 11,106 | 11,347 | 14.5% | 3→5 |
| Medium design and implementation | 16,249 | 14,080 | 15,090 | 7.1% | 4→9 |
| Large AS-IS | 20,893 | 18,724 | 18,484 | 11.5% | 5→8 |
| Large PLAN | 20,893 | 18,724 | 17,373 | 16.8% | 5→8 |
| Implementation and verification | 16,249 | 14,080 | 11,931 | 26.6% | 4→6 |
| Completion and handoff | 13,885 | 9,989 | 10,079 | 27.4% | 3→4 |
| Epic management | 8,519 | 5,287 | 5,346 | 37.2% | 2→4 |

The ideal-section-choice column also counts artifacts, Skills and verification as whole files. It does not mean an advantage over the optimal section choice of every file. Small, Medium, closing and Epic increase slightly compared with the ideal workflow section choice. Splitting increases the physical stability of partial reading but is not always smaller than perfect partial reading.

Because fixed direct paths are used, search calls are 0 on both sides in the model. Calling once per file increases read calls. The current phase's files can be read together in one tool request, but the actual call count and latency per host are not measured. If the guide is passed through every time or all files are read whole, this comparison does not hold.

Reading Large AS-IS → PLAN → implementation → closing each cold gives repeated bytes of 186,592 → 130,946. In the ideal case of reading each unchanged file only once in the same run, it is 101,066 → 100,493 bytes, a small difference. These numbers are a model summing file lists, not a call trace. Freshness rules take precedence over whether a re-query is needed.

### Sample of writing volume and reader burden of artifacts

`tests/fixtures/sdd-artifact-sample.json` is a fixed synthetic sample, not a real case. It checks that the original facts, risks, Decisions, ACs and execution contracts before and after each remain exactly once. Only the duplicated writing of Issue metadata was replaced with a reference to the source.

| Static sample | Before bytes / proxy | After bytes / proxy |
| --- | ---: | ---: |
| All written text | 3,252 / 813 | 3,081 / 771 |
| Human default reading (excluding evidence details) | 2,099 / 525 | 1,333 / 334 |
| Agent AS-IS evidence reading | 1,410 / 353 | 1,099 / 275 |
| Number of required working files | 4 | 4 |

The written text decreased by 5.3%, the human default reading by 36.5% and one agent evidence file by 22.1%. However, the synthetic AS-IS input including the needed README contract increases from 1,410 to 1,743 bytes. A single-file decrease is not counted as a reduction of the whole role's reading. Actual generated/edited tokens and human understanding were not measured. Reviewers review both AS-IS files and the needed evidence, so the same rate of reduction is not expected. People who need the evidence also read it additionally. The same layout principle is used for Medium/Large, but the generalized effect on various Large cases was not confirmed.

## Risks and next candidates

1. More files may cause call latency and selection errors. Direct paths and preservation checks are provided, but an actual agent evaluation is needed.
2. The total size of the rules increased. The cost can be higher when selective reading fails; further splitting of entry/issue is judged after checking with actual traces which ranges are consumed together.
3. Problems of access permissions, mutable Issues and lifetime of references can occur. Source identity, checks before consumption and the existing cleanup conditions are kept. Actual handoffs across several repositories are unverified.
4. AS-IS reader separation applies only to new work. Actual resumption cases must confirm that README review is not required retroactively of existing work.
5. Generated tokens, total input, tool calls, human understanding and actual compliance with protection conditions are candidates for a separate evaluation with the same fixture/model/run count/budget. Static numbers alone do not decide new model defaults, policy adoption or product pin changes.

No new cache, logging or agent execution structure was added. Merging the PR and changing product installations are not part of this work.

## Appendix: size and move of the existing rule sections

UTF-8 bytes, including headings and subsections. The existing reading guide, which is not a rule, was replaced with the new index.

| Existing section | bytes | Owning file |
| --- | ---: | --- |
| SDD grade | 2853 | `sdd/grade.md` |
| Common contract and project application | 541 | `sdd/entry.md` |
| Implementation start conditions | 1472 | `sdd/entry.md` |
| Artifacts and gates by grade | 1898 | `sdd/entry.md` |
| Reusing existing analysis | 531 | `sdd/entry.md` |
| Verification Strategy | 266 | `sdd/entry.md` |
| Review gate by grade | 261 | `sdd/entry.md` |
| SDD working document structure | 222 | `sdd/entry.md` |
| Execution routing and packets | 1488 | `sdd/entry.md` |
| Methodology application and improvement observations | 325 | `sdd/entry.md` |
| Stabilization-period token diagnostic | 269 | `sdd/entry.md` |
| Parallel work | 271 | `sdd/entry.md` |
| Issue body contract | 3087 | `sdd/issue.md` |
| Legacy Issue normalization | 799 | `sdd/issue.md` |
| Open questions and phase dependencies | 1540 | `sdd/issue.md` |
| Epic management unit | 3297 | `sdd/epic.md` |
| Document roles | 979 | `sdd/completion.md` |
| Business document update | 699 | `sdd/completion.md` |
| Completion procedure | 1817 | `sdd/completion.md` |

The byte counts are those of the Korean sections at the time of the measurement.

### File sizes of the synthetic artifacts

| Working file | Existing bytes | Candidate bytes | Main consumption |
| --- | ---: | ---: | --- |
| README | 504 | 644 | Work entry → human-facing AS-IS state and source links |
| 01-as-is | 1,410 | 1,099 | Investigation, AS-IS review, PLAN evidence |
| 02-to-be | 689 | 689 | Human PLAN judgment, implementation Decision/AC, closing |
| change-plan | 649 | 649 | Implementation, verification, handoff |

In the sample, the four groups of facts each exist exactly once before and after. The duplication rate of fact groups is 0% on both sides; what was removed is the local copy of metadata duplicated with the external Issue. The semantic duplication rate of a real document corpus is not measured. The step links above are consumption locations by design and are not taken to equal actual reading counts.

## Independent review of PR #2 and fixes

A subagent in a separate context that did not take part in the writing independently reviewed the original diff, rules, Human/Agent layout and measurement code against `8f268c97c7092c65965d16efcf5fb086facca7d0`. It found no additional omission in the core STOP, human judgment, verification, lifetime, remote candidate or Blind Audit isolation, and raised the two P2 findings below.

| Finding | Fix and regression prevention |
| --- | --- |
| The Epic "after" measurement omitted the managing Skill's required grade input | Including grade, the reduction was corrected from 45.7% to 37.2% and the read count from 2→3 to 2→4. A check verifies that the required paths extracted from the Skill's actual Inputs are included in the measurement selection |
| Adding a link to the README, an AS-IS target, after writing the PLAN changes its bytes and causes an unnecessary reconfirmation | The planned PLAN path is placed in the initial README. Progress status is managed in the existing Issue. Re-review of actual fact/premise changes and the PLAN A/B are kept, and link changes are not exempted wholesale |

It was clarified that the AS-IS scope of plan correction includes the README's human-facing current state and risks. This is a clarification to prevent stale human judgment, not a separate defect verdict. The new synthetic cases distinguish keeping the existing AS-IS target from the PLAN review. They are not regarded as model behavior execution results.

The same independent reviewer re-checked the fix diff and the directly affected scope and reported that both P2 findings were resolved with no further actionable findings. The reviewer ran the 6 structure checks and the measurement script directly and compared the results. The author's full regression of 32 also PASSES. These are document and static check results, not measurements of actual agent behavior effects.


## Minimal supplement based on diagnosis of actual artifacts

The original text, reduction drafts and identifiers of private cases are not copied into this PR. Only the input linkage and duplicate management risks confirmed in the diagnosis were generalized. No conclusion is drawn that the whole SDD is excessive or that actual tokens were reduced by some rate.

- The `implementing-issues` Inputs, the `execution-packets` implementation entry, `sdd/agent-spec` and the existing templates link the applicable README sections and revision directly. Human-facing wording is not a reading exemption, nor is it forced loading of the whole README. The existing Review Packet/Blind Audit allowed inputs and isolation are unchanged.
- TO-BE owns the Decision/AC source; the change plan owns the references, application locations, execution details and unique expected values. The deleted list is compared with the replacement locations, and preservation of meaning is not claimed only from the hash of retained ranges.
- The AS-IS and layout guidance keep the current conclusion and remaining risks in the current documents and link discarded hypotheses/investigation history as conditional history. On correction, contradictions in the related current documents are also checked. The progress status source is distinguished from the snapshot at approval time, and past product records are not edited retroactively.
- To the existing synthetic book reservation fixture, no retry on expiry and reservation unchanged on notification error were added. A variant that deletes unique conditions one by one while leaving the AC as is detects the omission. No condition or original text of a real product case was copied.
- The existing approval, Review, Verification and closing documents and the Blind Audit Packet range were compared with the previous candidate and preserved with frozen hashes. The existing 34 regression/installation/render/link and anchor/snapshot checks PASS, and the format check of the 70 behavior cases PASSES. One local Git clone block in the sandbox passed on a rerun in the allowed environment.

This minimal supplement was confirmed by the author's diff comparison and automatic checks. The independent review result in the previous section is a record about the earlier candidate and is not applied retroactively as an independent review of this change. Synthetic expected behavior is not an actual model execution result. Actual compliance with per-role required inputs, the frequency of re-querying past evidence, total host tokens/cost, human understanding and execution on other OSes are not measured. The static comparison is limited to the selected rule corpus and does not include product-specific READMEs/evidence or conditional Packets.
