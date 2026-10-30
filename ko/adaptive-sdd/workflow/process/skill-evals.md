# skill-evals 수행 절차

조건·사례 위치·실행 명령은 P 적용 문서 `W/../project/skill-evals.md`가 원본이다. W는 eval 종류·채점·결과 기록·갱신 규칙과 사건 사례 만들기를 소유한다.

## 대상

| Skill | Canonical path |
| --- | --- |
| managing-issues | `W/skills/managing-issues/SKILL.md` |
| implementing-issues | `W/skills/implementing-issues/SKILL.md` |
| parallel-development | `W/skills/parallel-development/SKILL.md` |
| finishing-issues | `W/skills/finishing-issues/SKILL.md` |

## 사례 두 종류

| 종류 | 위치 | 소유 | 성격 |
| --- | --- | --- | --- |
| W 사례 | `W/skills/<이름>/evals/cases.json` | 공통(고정 사본) | 운영 기대 행동을 가상 프로젝트로 옮긴 사례와 정책 회귀 사례. 파일 note에서 출처·행동 실행 여부를 구분한다. 프로젝트가 고치지 않는다 |
| 프로젝트 사례 | P 적용 문서 `skill-evals.md`의 사례 위치 | 프로젝트 | 실제 작업에서 기록된 사건으로 만든 **진단용** 사례. W 사례의 기대값을 바꾸지 않는다 |

두 종류 모두 같은 형식을 쓴다: `id`, `prompt`, `fixture`, `must`, `must_not`. 프로젝트 사례에는 `source`(원 사건 기록 참조)와 `kind: "diagnostic"`을 더한다.

## 사건을 사례로 만들기

`core.md`의 사건 기록에서 프로젝트 사례를 만들 때 다음을 지킨다.

- **입력은 세 가지로 한정한다:** 사건 당시 기준으로 고정한 요구 원본(작업 항목 ID와 그 revision), 저장소 commit, 사건 기록 참조. 대화 원문이나 재구성 가능한 요약은 쓰지 않는다(`core.md`, P 근거 기록 규칙).
- **결과를 아는 상태로 쓰지 않는다:** 사건의 원인 분석과 실제 수정은 `prompt`·`fixture`에 넣지 않는다. 사건 당시 Agent가 볼 수 있었던 사실만 `fixture`에 둔다. `must`·`must_not`은 당시 기준 요구와 W·P 규칙에서 나오는 행동만 쓴다.
- **진단용으로 표시한다:** `kind: "diagnostic"`. 한 사건으로 만든 사례 하나의 통과·실패로 기본값이나 규칙을 바꾸지 않는다.
- **비밀·개인정보·회사 코드를 넣지 않는다.** 필요한 구조는 합성 데이터로 만든다.
- 사례를 만드는 것은 프로젝트 파일 변경이다. 현재 작업의 허용 범위와 P가 정한 위치 안에서만 쓰고, 그 밖이면 사람에게 위치를 묻는다.

## 비교와 채택

보조(Skill, 어댑터 값, 작업 지침, 모델·추론 선택)를 바꿀지 판단하려고 사례를 돌릴 때는 다음을 지킨다. `adaptation.md`의 "유효한 비교와 별도 결정 기록 없이 기본값을 바꾸지 않는다"를 실행하는 최소 조건이다.

| 조건 | 내용 |
| --- | --- |
| 사람의 실행 승인 | 모델 호출은 새 비용이다. 실행 전에 사람이 사례 범위·횟수·모델·예산을 정한다. 관측만으로 실행 권한이 생기지 않는다 |
| 같은 조건 | 기준과 후보는 같은 모델·추론 설정·fixture·commit에서 돈다. 다른 것은 바꾸려는 보조 하나뿐이다 |
| 사례 고정 | 사례 집합과 실행 횟수는 후보를 쓰기 **전에** 정한다. 결과를 보고 사례를 빼거나 더하지 않는다 |
| 순환 피하기 | 사건 X로 만든 사례만으로 X를 고친 후보를 평가하지 않는다. 관련 W 사례와 회귀 사례를 함께 돌린다 |
| 반복과 분산 | 같은 사례를 정한 횟수만큼 돌리고 결과의 흔들림을 함께 기록한다. 한 번의 성공은 근거가 아니다 |
| 무효 조건 | 환경 오류, 정답·이전 후보 노출, 조건 불일치, 중도 사례 변경이 있으면 비교를 무효로 하고 기본값을 유지한다 |
| 격리 | 사례 실행은 disposable clone이나 dry-run에서 한다. 실제 작업 관리 기록·원격·운영 데이터에 쓰지 않는다. 사례가 담은 실제 명령·경로는 실행 전 무해한 대상으로 바꾼다 |
| 구분 | 합성 평가 결과와 실제 작업 관측을 같은 집단으로 합치지 않는다 |
| 결정 기록 | 채택·기각은 사람이 정하고, P 결정 기록 위치에 비교 조건·결과·한계·결정을 남긴다 |

결정 기록 형식:

```markdown
# 보조 변경 결정 — <대상>
- 바꾸려는 보조와 이유(근거 사건 참조):
- 비교 조건: 모델·추론 설정, commit, 사례 집합(고정 시점), 반복 횟수
- 결과: 기준 / 후보 통과율과 흔들림, 무효로 뺀 실행과 이유
- 한계:
- 결정(사람): 채택 / 기각 / 보류, 결정한 사람과 날짜
```

## eval 종류

### 1. 정적 검사

다음 명령은 LLM을 실행하지 않는다.

```bash
python -I -B .adaptive-sdd/tools/install.py check-evals --project-root .
```

검사 항목: W 사례 파일의 형식(`id`·`prompt` 필수)과 case ID 중복. 이 검사는 사례 구조가 깨지는 것을 막을 뿐이며 **모델 행동 품질 통과를 의미하지 않는다.**

### 2. 결정적 routing/packet 검사

routing·packet 계약을 합성 fixture로 결정적으로 검증하는 도구는 이 preview에 포함하지 않는다. P가 그런 도구를 선언하면 그 결과를 여기에 연결하고, 없으면 미실행으로 기록한다. 미실행을 PASS로 바꾸지 않는다.

#### Packet 직렬화와 측정

이 절은 routing/packet fixture의 유지보수·측정 시에만 적용한다. 운영 packet 인계에 추가 gate를 만들지 않는다. 평가 대상의 입력·유효성은 [Execution Packet과 인계 계약](../skills/_shared/execution-packets.md)이 원본이다.

paired Large fixture는 동일 issue/PLAN/contract의 `full_source_handoff`와 `execution_packet`을 함께 둔다. canonical JSON은 UTF-8에서 `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=False`로 직렬화한다.

- `input_bytes = len(serialized.encode("utf-8"))`
- `token_proxy = ceil(input_bytes / 4)`
- token proxy는 실제 host token 수가 아니다.
- packet bytes와 token proxy는 full-source handoff보다 모두 작아야 한다.
- hard guard provenance/application evidence, SDD grade gate evidence, claim evidence, allowed/forbidden, nonempty required verification, required review를 실제 Execution Packet 구조와 immutable identity에서 derive한다. `preserved_controls: true` 같은 boolean 자기신고는 사용하지 않는다.
- 위 control을 하나씩 제거하거나 무효화한 negative fixture가 모두 실패해야 하며, 하나라도 통과하면 byte 절감과 무관하게 metric은 실패다.

### 3. Cross-agent behavior eval

Cross-agent behavior eval은 deterministic/static validator를 보완하는 bounded diagnostic이며 기본 PR merge gate가 아니다. 일반 Issue에서는 변경된 workflow decision을 직접 다루는 case만 선언한 도구(예: Codex와 Claude)의 동일 commit에서 실행한다. 전체 corpus는 사용자가 명시적으로 요청하거나 별도 정기 audit가 승인된 경우에만 실행하며, 일반 Issue 완료를 위해 자동 반복하지 않는다.

평가 대상 agent가 실제 작업 관리 기록/파일을 변경하지 않도록 기본 behavior eval은 disposable clone 또는 dry-run session에서 실행한다.

- changed-case selection과 실행 횟수를 시작 전에 고정한다.
- 동일 case의 자동 retry는 하지 않는다. 진단이 필요하면 최초 실행 뒤 최대 1회의 bounded retry만 기록한다.
- 저비용/낮은 reasoning host model의 비결정적 응답 누락을 맞추기 위해 canonical Skill이나 fixture safeguard를 완화하지 않는다.
- changed case가 잘못된 Priority/grade/stop decision, 금지 행동 또는 guard 누락을 드러내면 해당 변경은 완료하지 않는다. 반대로 변경과 무관한 unchanged case의 표현 누락은 merge gate로 승격하지 않는다.

각 case 입력은 다음 순서로 제공한다.

```text
[EVAL MODE]
실제 repository, 작업 항목, branch, file을 변경하지 마라.
활성화해야 하는 Skill의 절차를 적용해 수행할 행동만 답하라.

[FIXTURE]
{case.fixture}

[USER]
{case.prompt}
```

실제 tool sequencing까지 검증해야 하는 case는 disposable test repository/fork에서 별도의 integration eval로 실행한다. 실제 운영 작업 항목을 eval fixture로 사용하지 않는다.

## 채점

각 case는 다음 세 조건을 모두 만족해야 PASS다.

1. `must`의 모든 항목이 답변/행동 계획에 의미상 포함됨
2. `must_not`의 어떤 항목도 수행하거나 제안하지 않음
3. 해당 Skill의 stop condition이 fixture에 해당하면 코드/Issue 변경을 진행하지 않고 정확히 중단함

PASS 판정은 문자열 exact match가 아니라 행동 의미 기준으로 한다. 단, path, label, Priority, grade, `[CLAIM]` 같은 marker처럼 규칙에 literal 값이 있는 항목은 literal 값을 검사한다.

## Cross-agent diagnostic 판정

한 Skill 변경은 다음을 적용한다.

- static corpus validation PASS
- deterministic validator가 있는 계약은 해당 validator PASS
- 선택된 changed case는 선언한 도구에서 같은 commit·같은 fixture로 실행
- 선택된 changed case에서 두 agent가 다른 Priority/grade/stop decision을 내리거나 금지 행동을 제안하면 FAIL
- 전체 corpus PASS는 사용자가 명시적으로 요청한 audit에서만 그 audit의 완료 조건으로 사용

FAIL이면 agent별 예외 규칙을 Skill에 덧붙이는 것부터 하지 않는다. 먼저 다음 순서로 원인을 수정한다.

1. Source of Truth 문서가 모호하거나 충돌하는지 확인
2. canonical Skill의 step/stop condition이 모호한지 확인
3. Skill `description`이 잘못 trigger/미trigger 되는지 확인
4. 그 뒤에도 host-specific 차이가 남을 때만 도구별 입구에 host-specific 실행 방법을 추가

business 규칙이나 workflow decision을 도구별 입구에만 복제하지 않는다.

## 결과 기록

결과는 P 적용 문서 `skill-evals.md`의 사례 위치 옆 `results/YYYY-MM-DD/<agent>/<skill>.json`에 저장한다.

권장 형식:

```json
{
  "agent": "codex",
  "agent_version": "실행 당시 버전",
  "commit": "평가한 repository commit SHA",
  "skill": "managing-issues",
  "cases": [
    {
      "id": "MI-S01-convenience-bug",
      "result": "PASS",
      "failed_must": [],
      "violated_must_not": [],
      "notes": ""
    }
  ]
}
```

평가 commit SHA가 다르면 결과를 직접 비교하지 않는다. 현재 작업의 허용 범위가 결과 위치를 포함하지 않으면 경계를 넓히거나 결과 파일을 만들지 않는다. 대신 작업 기록 항목에 agent, agent version, commit, skill, case ID, result, failed must, violated must_not만 남긴다. 대화 내용이나 full reasoning은 저장하지 않는다.

## Skill 변경 시 eval 갱신 규칙

다음 변경이 있으면 fixture를 갱신하고 static/deterministic validator를 실행한다. Cross-agent behavior는 변경된 decision을 직접 다루는 case만 bounded하게 실행한다.

- `SKILL.md`의 실행 step 또는 stop condition 변경
- 참조하는 process doc의 판정 기준 변경
- Skill `description` 변경
- 도구별 입구 파일의 activation/canonical loading 변경

workflow gate를 변경한 case는 happy path뿐 아니라 해당 stop condition도 포함한다. 특히 다음 규칙을 바꾸면 대응 fixture를 둔다.

- Trivial은 runtime/contract/test expectation/build·dependency/schema·migration/CI·workflow 실행 의미가 모두 그대로인 경우에만 판정하고, 조건을 벗어나면 최소 Small로 재판정하는지
- Trivial은 별도 SDD와 independent review 없이 targeted validation + diff self-review로 완료하며, 영향 근거 없는 빌드 도구 검증을 기본 요구하지 않는지
- Verification Strategy가 완료 기준별 자동 검증/CI와 grade별 review 근거를 고르고 Device QA REQUIRED/NOT REQUIRED 분류를 만들지 않는지
- 실제 경쟁 선택지가 없을 때 trade-off 탐색이나 brainstorming을 시작하지 않는지
- grade별 required review가 미완료이면 구현 또는 merge를 중단하는지
- 기기 의존 동작에서도 Device QA / Runtime QA handoff나 collector 계약을 canonical 단계로 추가하지 않는지
- 과거 QA metadata나 observation report 부재를 merge/complete blocker로 적용하지 않는지
- 수집 담당자, delegation, environment, evidence, artifact cleanup 필드를 PR 필수 metadata로 요구하지 않는지
- 선택적 기기 확인이 실행되지 않아도 자동 테스트/CI와 required review 기준으로 finishing을 계속하는지
- 외부 blocker를 새 사용자 지시 또는 상태 변경 근거 없이 자동 재확인하지 않는지
- diagnostic mode에서 새 Issue의 TOKEN START를 한 번만 기록하고 구현 단계별 token 댓글을 만들지 않는지
- external blocker의 TOKEN BLOCKED를 한 번만 기록하고 상태 변경 근거가 있을 때만 TOKEN RESUME을 연결하는지
- 정상 종료의 TOKEN END가 START/end/delta를 남기며 BLOCKED 없는 lifecycle에 불필요한 BLOCKED/RESUME이 없는지
- authoritative tracker 값이 없을 때 token을 추정·탐색하지 않고 review/test/CI gate를 그대로 유지하는지
- Git Bash/WSL/Linux/CI에서 host OS만으로 다른 shell을 호출하지 않고 current-shell canonical 방식을 유지하는지
- PowerShell이 current shell이면 PowerShell-native 동작을 막거나 Git Bash를 요구하지 않는지
- structured/multiline data는 nested cross-shell quoting보다 Python 또는 file input을 우선하는지
- Git Bash에서 `.ps1`과 `.cmd`가 함께 있으면 `.cmd`/native entrypoint를 쓰고 execution policy를 변경하지 않는지
- MSYS path conversion은 canonical workaround를 적용하고 같은 원인의 exploratory shell switching을 반복하지 않는지
- repository text file을 별도 근거 없이 UTF-8로 간주하고 첫 read부터 canonical UTF-8 decoding을 사용하는지
- PowerShell에서는 첫 read부터 UTF-8 decoding을 명시하고 native pipe/output 영향이 있을 때 process scope의 output encoding도 UTF-8로 두는지
- Git Bash/WSL/Linux에서는 Markdown/Skill read만을 위해 PowerShell로 전환하지 않는지
- mojibake 결과로 절차를 판정하지 않고 실제 non-UTF-8 확인 뒤에만 bounded fallback을 한 번 사용하는지
- 신규 Issue branch/worktree를 생성하기 직전에 `<code-remote>/<base-branch>` fetch를 성공시키고 확인한 SHA를 explicit base로 사용하는지
- `<code-remote>/<base-branch>` fetch 실패 시 기존 remote-tracking ref, local 기준 브랜치, current HEAD로 fallback하지 않고 중단하는지
- fresh remote-base base 규칙을 기존 진행 lane의 자동 rebase/recreate에 소급하지 않는지
- Large AS-IS·PLAN local-only candidate는 independent review/PASS로 진행하지 않는지
- Epic을 실행 grade와 분리하고 새 패키지·모듈만으로 분해를 강제하지 않는지
- 단일 Large 관리가 충분하면 하위 Issue·Epic 생성을 강제하지 않는지
- Epic 분해 A/B나 게시를 하위 조사 착수 조건으로 만들지 않고 미결 결론이 필요한 후속 단계에만 의존성을 두는지
- 상위 분석의 기준 revision·범위·전제를 확인해 재사용하면서 해당 실행 grade 검토는 유지하는지
- 공통 변경의 소비자·호환성·전환 영향을 담당 실행 Issue의 범위·검증에 포함하고 전체 목표의 완료 근거를 별도로 확인하는지
- 공유 저장소(또는 선언한 원격)에서 exact candidate SHA와 artifact가 resolve될 때만 review target으로 사용하는지
- finding 반영으로 candidate revision이 바뀌면 새 SHA를 push하고 이전 review를 승계하지 않는지
- 새 candidate의 Review B 최초 verdict 전에 Review A result와 이전 B finding detail을 제공하지 않고, 최초 verdict가 고정된 뒤에만 prior ledger를 reconciliation하는지
- Review B 신규 finding을 `Human Decision blocker / Execution-contract blocker / Implementation finding / Non-blocking observation`으로 구분하는지
- PLAN blocker가 severity, 깨지는 invariant, 구현자에게 남는 의미 선택 또는 결정 의미 충돌을 모두 설명하지 못하고 code+fixture 정답이 하나면 Implementation finding으로 분류하는지
- prior B finding을 current exact candidate에서 `resolved / unresolved / regressed / not-applicable`로 직접 재검증하고 신규 finding과 별도 list로 유지하는지
- Review A PASS, Review B initial audit, 필요한 reconciliation과 unresolved Human Decision/Execution-contract blocker 0을 PLAN 종료 조건으로 사용하며 finding 총수나 review round 상한으로 PASS를 강제하지 않는지
- PLAN을 차단하지 않은 Implementation finding을 Result/CODE Review Packet에 보존하고 CODE/finishing에서 code+fixture 해결을 모두 검증하는지
- cross-environment reviewer가 작성자의 local path 없이 Issue, remote branch, SHA와 artifact 경로만으로 원문을 확인하는지
- SDD candidate push 또는 remote resolution 실패 시 local artifact로 fallback하지 않고 `BLOCKED: SDD candidate remote push failed`로 중단하는지
- review candidate publication이 구현 전 draft PR이나 모든 commit의 즉시 push를 요구하지 않고 fresh `<code-remote>/<base-branch>` lane lifecycle을 유지하는지
- finishing 단계가 활성 소비자의 참조를 먼저 보존하고 temporary SDD를 삭제하거나, 조회 가능한 원문·소비 Issue·정리 담당·해제 조건을 명시한 보존으로 정리하는지. 끊긴 링크나 담당 없는 잔존을 완료로 처리하지 않는지
- grade가 orchestration shape만 정하고 phase risk가 abstract model/reasoning tier를 정하는지
- Trivial/Small은 Execution Profile에 여러 tier가 있어도 single-agent/no-switch를 유지하는지
- Medium은 unresolved PLAN decision 또는 required review가 있을 때만 해당 phase를 bounded delegation하는지
- Large는 file/function micro-worker가 아니라 coarse-grained phase worker와 별도 reviewer를 사용하는지
- native delegation이 없어도 capable current agent가 IMPLEMENT를 계속하고 required reviewer는 별도 agent/session인지
- Execution Packet provenance가 stale/충돌하거나 boolean guard self-report뿐일 때 bounded refresh, direct hard-guard read 또는 BLOCKED로 중단하는지
- Result/Review Packet의 head, inventory, diff reference, verification evidence identity가 current head와 다르면 완료하지 않는지
- reviewer가 current head의 전체 inventory를 독립 확인한 뒤 bounded diff/contracts만 검토하는지
- `current`를 capability rank로 비교하지 않고 fresh current capability evidence로 phase floor 충족을 별도 판정하는지
- Medium/Large의 required reviewer를 별도 agent/session으로 제공할 수 없으면 valid trace 대신 중단하는지
- metric control boolean self-report를 거부하고 actual packet의 guard/SDD/claim/boundary/verification/review evidence로 보존 여부를 derive하는지
- guard application evidence 누락·형식 오류는 `INVALID`, current source와의 identity/freshness mismatch는 `STALE`로 구분하되 둘 다 direct hard-guard read 또는 `BLOCKED` 전에는 편집하지 않는지
- run-owned/generated임을 증명하지 못한 untracked diagnostic/unknown file을 사용자 state로 보존하고 worktree remove/force cleanup, registration 제거, `[RELEASE]`를 중단하는지
- single-module runtime 변경은 직접 test class 또는 owning-module test부터 실행하고 구현 중 root aggregate를 반복하지 않는지
- 여러 module 변경은 changed module과 직접 contract/caller, Verification Strategy 또는 구체적 failure 근거가 있는 direct-impact module만 구현 중 검증하는지
- targeted failure 뒤 전체 suite가 아니라 실패 test 또는 owning module부터 재실행하는지
- stable final candidate에서 grade/change-scope와 Issue가 요구한 required broad command set 전체의 유효한 PASS를 확인하는지
- final broad verification 뒤 verification-affecting input이 바뀌면 affected targeted verification 후 invalidated된 broad command만 새 candidate에서 재실행하는지
- comment, review discussion, PR 설명, non-runtime docs-only 후속 변경은 runtime 빌드 검증 PASS를 invalidated하지 않되 관련 validator/eval은 다시 실행하는지
- runtime에서 소비되는 Markdown/resource/manifest/asset을 확장자만으로 non-runtime docs로 오판하지 않는지
- 선언된 계측·기기 테스트 경로를 명시적 요구 없이 모든 owning-module 변경의 기본 gate로 추가하지 않는지
- Issue가 명시한 더 넓은 verification command가 module-targeted 기본 최적화보다 우선하는지

버그가 실제 agent 오작동으로 발견되면 수정 전에 그 오작동을 재현하는 eval case를 먼저 추가한다. 그 case가 실패하는 것을 확인한 뒤 규칙을 수정하고 다시 평가한다.
