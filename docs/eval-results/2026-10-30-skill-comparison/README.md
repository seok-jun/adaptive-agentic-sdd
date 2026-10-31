# Claude skill comparison — follow-up deferred

## 현재 결정 — 2026-10-31 보류

사용자 결정: 추가 실험과 스킬 개선은 일단 보류한다. 아래의 기존 실행 명령과 원래 핸드오프는 이력이며 재실행 지시가 아니다. 다음 실제 Small 작업에서 기존 실행 근거로 아래 항목만 확인한다. 추가 모델 평가, 스킬 재설계, 채택·병합·출시는 자동 진행하지 않는다. [후속 설계 초안](follow-up-design.md)도 보류한다.

### 지금까지의 결과

- Claude `claude-opus-5-5` / medium을 대상으로 수정 전후 각 3회씩 3개 사례를 비교했다. Codex `gpt-6-astra` / medium을 채점자로 설정했다.
- 총 18회 호출 시도 중 인증 오류 2회는 추론 전에 실패해 INVALID로 보존했다. 나머지 16개 답변을 독립 채점했으며 PASS 11개, FAIL 5개다. 자동 재시도는 없었다.

| 사례 | 수정 전 PASS / FAIL / INVALID | 수정 후 PASS / FAIL / INVALID |
| --- | --- | --- |
| Small 구현 | 0 / 3 / 0 | 0 / 2 / 1 |
| 필수 검증 실패 | 3 / 0 / 0 | 3 / 0 / 0 |
| 실패 근거 누락 | 2 / 0 / 1 | 3 / 0 / 0 |

- **채점 결과는 보존하되 스킬 개선·퇴보의 증거로 확정하지 않는다.** Small 사례는 Issue ID·원본 작업 기록이 없어서 구현 진입을 충분히 시험하지 못했다. 허용 경로의 축약 표현과 채점자의 의미 판정에도 문제가 의심된다. 앞서 설명한 “수정 후 범위 준수 악화”는 입증되지 않았다.
- 첫 모듈 검증 항목의 채점상 개선은 관찰됐지만 위 한계 때문에 실제 실행 개선으로 해석하지 않는다. 완료 처리 사례는 유효한 답변 모두 통과해 개선 효과를 구분하지 못했다.
- 원래 문제의 중요도는 중간, 긴급도는 낮다고 판단했다. 실제 작업의 불필요한 검증 반복을 줄일 가치는 있으나, 현재 결과만으로 큰 평가 체계나 스킬 재설계에 투자하지 않는다.
- 실행기 보호 테스트 8개, 18개 독립 설치 검사, 최종 파일 목록·전사·채점 형식·고정 입력 해시 대조가 통과했다. 이는 실행기 검증이며 의미 채점의 정확성이나 방법론 효과를 보장하지 않는다. 원답변·전사는 저장소 밖에 유지한다.

상세 결과: [paired-summary.md](paired-summary.md), [항목별 기록](paired-results.json), [최종 검증](validation.json). 기존 후보와 이번 실행기·결과는 보존하며 새 채택·병합·출시는 하지 않았다.

### 다음 실제 Small 작업에서 확인할 것

새 보고 양식이나 추가 검증 실행을 요구하지 않는다. 해당 작업의 기존 Issue·명령 로그·변경 목록·완료 요약을 활용한다.

1. **첫 검증:** 실제 변경 파일의 소유 모듈 또는 직접 관련 테스트부터 실행했는가. 더 넓은 명령을 먼저 실행했다면 Issue의 명시 요구나 구체적인 영향 근거가 있었는가.
2. **전체 검증 반복:** 같은 입력에 대해 전체 test/lint/build를 반복했는가. 반복했다면 코드·테스트·의존성·리뷰 수정 등 재실행을 정당화하는 변경이 있었는가.
3. **필수 검증 유지:** 모듈 테스트 성공만으로 끝내지 않고, 최종 후보가 기존에 요구된 전체 검증을 충족했는가. 검증에 영향을 주는 변경 후 낡은 PASS를 재사용하지 않았는가.

문제가 실제 발생한 경우에만 해당 작업의 기존 기록에 작업/후보 참조, 명령 순서, 반복 전후 입력 변경 여부, 관찰 가능한 대기·재작업과 조치를 짧게 남긴다. 새로 비용 계측 체계를 만들거나 확인되지 않은 낭비량을 추정하지 않는다. 정상 진행이면 이 실험을 위해 별도 기록을 추가하지 않는다.

**재개 조건:** 실제 작업에서 설명되지 않는 전체 검증 반복, 잘못된 첫 검증 선택, 무효한 PASS 재사용이 확인되면 해당 근거를 검토해 좁은 개선의 필요성을 다시 판단한다. 관측만으로 모델 실험을 자동 실행하지 않는다. 문제가 확인되지 않으면 보류를 유지한다.

Status: **COMPLETE with two pre-inference authentication INVALIDs**, updated 2026-10-31. All 18 reserved subject samples are accounted for: 16 completed inference and independent grading (11 PASS, 5 FAIL), and two HTTP 403 failures remain INVALID without retry. Sixteen grader calls were made. No overall PASS-rate improvement was observed. See [paired-summary.md](paired-summary.md) for the three-case comparison, all repetitions, item-level findings and limitations; [validation.json](validation.json) records the final audit. Adoption remains a separate user decision.

The original 2026-10-30 handoff below is retained as the experiment contract. Its statements that the runner did not yet exist describe that original handoff, not the current state.

## 2026-10-31 continuation

- Added `tests/run_paired_skill_evals.py`, separate from the older bidirectional runner, and eight failure-oriented unit tests in `tests/test_paired_skill_evals.py`.
- Verified the frozen cases checksum and both exact source commits. Built both bundles from the candidate commit, replaced only the two baseline skill bodies, removed all four answer-key files from both bundles, and regenerated manifests. The resulting difference is exactly the two intended skill files plus `MANIFEST.json`.
- Prepared 18 independent installations in the seed-20261030 order. Every installation passed `init`, `render`, and `check`. Fixtures and prompts remain outside subject projects. Prepared project inventories include hidden and git files.
- User confirmed available allowance and the historical model. Pinned Claude `claude-opus-5-5` / `medium`; Codex `gpt-6-astra` / `medium`. CLI versions: Claude Code 2.1.302, Codex CLI 0.166.0-alpha.5.1 (the executable resolved by the runner; the separately inspected npm wrapper reports 0.163.0).
- The attempted sample was `s001`, II-S02 after, repetition 1. Claude initialization advertised the intended model and only Read/Grep/Glob, with no MCP servers. The service then rejected subscription access for the active organization. This is an environment INVALID, not a behavioral FAIL or evidence of model availability.
- The shell inherited a `CLAUDE_CONFIG_DIR` pointing to a separate integration account. A read-only auth-status check found the default home configuration has a different signed-in Max account/organization. No credentials or account identifiers are stored in repository results. The user explicitly authorized switching to the default home account for the remaining 17 samples. The next sample, `s002` (FI-S02b before), also returned the same organization-access 403 before inference. No API-key or OAuth-token environment override was present. The runner stopped; 16 samples remain unstarted. Neither failed sample was retried. See [account-transition.json](account-transition.json) for the recorded authorization and instruction-context hashes.
- Raw prompts, answers, transcripts, inherited instruction hashes and the resumable journal are outside the repository in the private work directory reported in the chat. Published results contain hashes and outcomes only.
- After the user completed subscription reauthentication, Claude inference and Codex grading succeeded. Auth status reported Pro on the reauthenticated default-home account. The earlier two 403 attempts remain INVALID with zero reported inference usage. The exact account transition is recorded separately; no successful observations from the earlier account are pooled. Full instruction isolation is not proven by prepare-only success. The official [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) documents the model catalog, instruction, shell, web-search and project-document controls used by the runner.

Commands (replace the external directory with the intended fresh/private directory):

```powershell
python -I -B -m unittest discover -s tests -p test_paired_skill_evals.py
python -I -B tests/run_paired_skill_evals.py --prepare-only --workdir <external-directory>
python -I -B tests/run_paired_skill_evals.py --execute --allowance-confirmed --workdir <same-external-directory>
```

Preparation refuses to overwrite an existing work directory. Execution requires the frozen runner and selection identities. Started samples, including INVALID/interrupted samples, are skipped on resume. A first INVALID stops further calls for inspection; it is never silently replaced. Changing account/inherited instruction context requires an explicit recorded decision before resuming, rather than bypassing the context check.

Branch: `codex/claude-skill-ab-experiment`.

## Question and evidence

Does the wording change in `721e086a7c7312c5fd6a590325bde87666c0629c` improve Claude's action plans for II-S02 and FI-S02, while handling missing evidence correctly?

In the [original evaluation](../2026-10-30/README.md), Claude failed II-S02 and FI-S02 in all three runs; Codex passed both in all three runs. Thus **Claude is the subject and Codex is the independent grader**, not the other way around. Original Claude requests used `opus`, with `claude-opus-5-5` reported by the CLI. Original answers were not retained in the repository and cannot be regraded from repository files.

The skill changes are already committed locally in `721e086`. They clarify the first targeted verification and incomplete-status reporting. They are not proven improvements. `v1.0.0-preview.5` remains published at `ee5c60a246a95218e0f429681036fa9bd4bd1e03`; do not move it or merge this experiment into `v1-preview` automatically.

## Frozen comparison

`selection.json` contains the three complete Korean fixtures and rubrics, copied from `721e086`, and a checksum. Freeze these before the first model call; do not change them after seeing results.

- Subject: Claude Code, three independent fresh sessions per case per arm. Pin one exact available Claude model for both arms; prefer the original served model if available. Do not silently substitute a different model mid-run. Record CLI version, requested model, returned model identity, reasoning/effort, loaded instructions and usage.
- Grader: Codex CLI, `gpt-6-astra`, reasoning `medium`, one fresh independent session per answer. Pin that setting across all grades. Hide arm, source SHA, prior scores, other answers and the intended improvement from the grader.
- Budget: 18 subject calls (3 cases × 2 arms × 3 repeats), at most 18 grader calls. No automatic retries. This is a call-count bound, not a currency estimate. Before execution, confirm the home account has sufficient allowance and record the exact Claude model/effort in the selection. No model calls are authorized merely by checking out this branch; resume the user's requested experiment explicitly.
- Use the Korean edition to match the original failures. English static synchronization has been checked, but English behavior is outside this experiment.
- Before arm: skill bodies from `ee5c60a246a95218e0f429681036fa9bd4bd1e03`.
- After arm: skill bodies from `721e086a7c7312c5fd6a590325bde87666c0629c`.
- Everything else comes from `721e086` in both arms. Replace only `workflow/skills/implementing-issues/SKILL.md` and `workflow/skills/finishing-issues/SKILL.md` in the before arm, then regenerate the derived bundle manifest. Assert that the only bundle differences are those two bodies and `MANIFEST.json`.
- Use the **corrected FI-S02 fixture in both arms**. Comparing the old incomplete fixture against the corrected one would confound fixture repair with skill wording. Likewise supply the new missing-evidence case to both arms.
- Every session gets a fresh disposable installation outside the repository. Run `init → render → check` before the subject. Do not expose case rubrics or past results: remove all four `workflow/skills/*/evals/cases.json` answer-key files identically from both disposable bundles before regenerating manifests and installing. Keep the frozen fixtures/rubrics outside subject-accessible projects. These derived bundles are evaluation-only and must not be shipped.
- Allow Claude only `Read`, `Grep`, `Glob`; prohibit writes, shell execution and network tools. Include the truthful harness `install.py check` result in the prompt. The task is an action plan, not actual implementation or command execution. Do not supply `must` / `must_not` to the subject.
- Interleave before/after runs in a reproducible shuffled order, seed `20261030`. Use opaque sample names so paths do not reveal the arm. Keep project settings and source inputs identical except for the intended skill bodies and unavoidable per-run paths/pin hashes.
- Check project inventories before and after every run. A file write, rubric exposure, model mismatch, environment failure or unusable grading is `INVALID`, not `FAIL` or `PASS`. Retain the invalid run and reason; do not silently replace it.

## Runner work still needed

**There is no ready-to-run paired Claude runner in this branch.** The interrupted Codex-subject draft was removed because it targeted the wrong subject and had not been tested. Do not invoke the existing runner blindly for this experiment.

`tests/run_behavior_evals.py` is a useful source for Claude read-only invocation, disposable installation and rubric handling, but currently runs both agents, grades Codex with Claude, reads cases from each bundle, and writes an old hard-coded preview.5 commit label. Those behaviors do not implement this comparison. Add a separate paired runner or explicit paired-mode options that:

1. Read the frozen selection, verify its hash and the exact source commits, and prepare both decontaminated bundles as above.
2. Support a **prepare-only** mode that performs no model calls. Verify installation, fixture equality, allowed source differences, sample ordering and absence of answer keys. Do this first on the home machine.
3. Use Claude only as subject, with an explicit model/effort. Preserve per-item Codex grading booleans and derive PASS from all `must=true` and all `must_not=false`; require actual booleans and exact item correspondence. A grader response without these is invalid.
4. Disable grader tools and use an empty isolated working directory. Supply only fixture, rubric and one untrusted answer as grading data. Check the actual transcript for tool use or leakage.
5. Save each result immediately, so interruption preserves completed runs. Resume must never rerun completed PASS/FAIL or silently mix model/fixture/manifest identities. Do not automatically retry invalid runs.
6. Keep prompts, raw answers and CLI transcripts **outside the repository**. Repository results contain source/model identities, item outcomes, usage, hashes, validity checks and limitations, not raw conversations or reconstructed answers.
7. Produce a three-row before/after table with PASS/FAIL/INVALID counts, per-item misses and all three repetitions. Do not stop early on favorable results or edit the skills during the comparison.

The existing runner's `--setting-sources project` did not exclude the user-level `CLAUDE.md` in the original run. Verify and record the actual home-machine instruction context; use the same context for both arms. Do not claim user instruction isolation from that flag alone. If the exact old served model is unavailable, label this a new-model comparison, not a reproduction of the original failures.

## Interpretation and next decision

This is a **post-hoc diagnostic**: the candidate was already written before these cases and repeats were frozen. The three cases also overlap the incidents motivating the change. It does not meet the procedure's full pre-registered adoption comparison or broader regression requirements.

- Report whether the observed sample improved, regressed or stayed unchanged; three repeats cannot establish a general reliability gain.
- If before and after both pass 3/3, report **no observed improvement / ceiling**, not that the fix was effective.
- FI-S02's historical FAILs cannot be used as the before scores for this corrected-fixture comparison.
- A plan mentioning tests does not prove actual tool order. State this limitation.
- Keep historical results unchanged. Do not change skill text to chase failures inside this run. Any follow-up hypothesis requires a separately frozen experiment.
- Leave adoption, rejection, a new preview release and any merge to the user. No automatic publication.

## 집에서 이어가기

```powershell
git fetch origin
git switch --track origin/codex/claude-skill-ab-experiment
```

이미 로컬 브랜치가 있으면 `git switch codex/claude-skill-ab-experiment`를 사용한다. 작업 트리에 변경이 있으면 먼저 보존한다.

다음 요청을 그대로 전달하면 된다:

> 이 브랜치의 docs/eval-results/2026-10-30-skill-comparison/README.md와 selection.json을 읽고 실험을 이어서 진행해줘. Claude를 평가 대상으로, Codex를 독립 채점자로 사용해 세 사례를 수정 전후 각각 3회 비교해. 먼저 paired runner를 완성하고 모델 호출 없는 prepare-only 검증을 해줘. Claude의 실제 사용 가능한 모델과 effort를 양쪽에 동일하게 고정하고 설정을 기록한 뒤, 18회 행동 실행과 최대 18회 채점 안에서 실행해. 원답변은 저장소 밖에 두고 결과와 한계만 저장소에 남겨. 자동 재시도·스킬 추가 수정·병합·출시는 하지 마.

현재 상태: 스킬 수정 `721e086`의 관련 자동 테스트 44개, 양 언어 설치 및 77개 사례 구조 검사는 통과했다. **이번 전후 모델 비교는 0회 실행**이며 새 PASS나 개선 결론은 없다.
