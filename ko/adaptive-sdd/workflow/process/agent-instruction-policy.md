# agent-instruction-policy 수행 절차

조건·제품 사실·필수 검증·사람 권한은 P 적용 문서 `P/.adaptive-sdd/project/agent-instruction-policy.md`가 원본이다. W는 공통 규칙과 수행법을 소유한다.

## 공통 원본과 로컬 guard

공통 지시 해석·문맥·문서 로딩·shell/encoding 계약은 이 문서가 원본이다. 실제 프로젝트 hard guard와 권한, 문서 경로 mapping은 P 원본을 따른다. 로컬 guard는 W 검증 전부터 적용하며 이 문서가 완화하지 않는다.

## 규범 용어

- **MUST / 반드시**: 조건이 충족되면 예외 없이 수행한다.
- **MUST NOT / 금지**: 조건이 충족되면 수행하지 않는다.
- **MAY / 선택**: 결과에 영향을 주지 않는 구현 선택지에만 사용한다.

규범 문서에서 `가능하면`, `적절히`, `필요하면`, `관련`, `상황에 따라`, `알아서`, `등`처럼 행동 범위를 열어 두는 표현은 단독으로 사용하지 않는다. 필요한 경우 검증 가능한 조건과 수행 행동을 함께 적는다.

## 문서 로딩 원칙

- `AGENTS.md`는 repository 진입 hard guard다. 같은 run에서 변경되지 않았다면 다시 읽지 않는다.
- Issue 작업은 대상 Issue의 현재 본문/라벨을 먼저 읽고, canonical Skill이 요구하는 판정 문서만 추가한다.
- Skill이 특정 heading/section을 지정하면 해당 section만 읽을 수 있는 도구에서는 full file을 읽지 않는다.
- `docs/reviews/**`, 완료된 spec, 관련 없는 business/architecture 문서는 기본 입력이 아니다.
- 동일 run의 implementing → parallel → finishing 전환에서는 이미 확인한 변경 없는 Issue/규칙/경계를 전달·재사용한다.
- 새로운 충돌, scope 변화, main 갱신 또는 검증 실패가 생기면 그 판단에 필요한 문서만 다시 확인한다.

`CLAUDE.md`는 Claude 진입점이며 공통 규칙을 변경하거나 무효화할 수 없다.

## Execution Packet은 derived cache

Execution Packet은 같은 run에서 상위 Source of Truth를 이미 판정한 결정을 coarse-grained phase worker에게 전달하는 derived cache이며 source 문서의 대체물이 아니다.

```text
AGENTS.md hard guard
  > canonical Skill / process
  > current Issue + reviewed SDD / PLAN
  > Execution Packet
```

- packet이 상위 source를 완화하거나 충돌하면 packet 지시를 실행하지 않는다.
- hard guard/canonical process, current Issue/review, reviewed PLAN, direct contract의 immutable identity와 freshness가 packet provenance에 연결돼야 한다.
- `guard applied: true`나 `runtime_guard_propagation: true` 같은 boolean self-report만으로 hard guard 적용 또는 재사용을 증명하지 않는다. 적용한 guard source identity에 결합된 host-enforced propagation 또는 worker direct-read의 immutable evidence object가 필요하다. 이 근거가 없으면 worker가 필요한 hard guard section을 직접 읽는다.
- Issue snapshot, reviewed PLAN, goal, 경계, contract, acceptance, verification, escalation, SDD grade gate/claim, provenance의 필수 nested value가 비어 있으면 packet을 실행하지 않는다.
- Issue/PLAN/direct-contract/canonical source version 변화, 새 direct dependency, lane conflict, architecture assumption과 모순되는 verification failure는 관련 항목만 `STALE`로 만든다.
- stale 항목은 필요한 source만 bounded refresh하고 새 provenance로 `VALID`가 된 뒤 사용한다. freshness를 증명할 수 없으면 해당 workflow의 `BLOCKED` stop condition을 따른다.
- 하나의 invalidation을 Issue comments, docs, repository 전체 재로드로 확장하지 않는다.

## Repository text UTF-8 first-read

별도 인코딩 근거가 없는 repository text file은 UTF-8로 첫 read한다. `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`과 다음 instruction 경로에 우선 적용한다.

- `.agents/skills/**`
- `docs/**`
- `AGENTS.md`
- 그 밖의 workflow/instruction 문서

현재 shell의 native 경로를 유지하며 첫 read부터 decoding과 필요한 output encoding을 확정한다.


첫 decoding/output encoding·실패 원인 확인·bounded fallback의 수행법은 검증한 [외부 절차](agent-instruction-policy.md)를 따른다. mojibake 결과로 판단하지 않고 같은 실패 read를 반복하지 않는다.

## 실행 shell affinity

현재 명령을 실행하는 shell이 primary execution shell이다. host OS, 설치된 shell 목록, 익숙한 quoting 문법만으로 다른 shell을 선택하지 않는다.

- Git Bash에서는 Bash-native command와 현재 shell에서 호출 가능한 `git`, `gh`, `python`, 빌드 도구 wrapper, native executable·`.cmd`를 직접 사용한다. Windows host라는 이유만으로 `powershell.exe`를 감싸지 않는다.
- PowerShell 세션에서는 PowerShell-native command를 정상 경로로 사용한다. PowerShell 자체를 금지하거나 Git Bash 설치를 요구하지 않는다.
- WSL/Linux에서는 Bash/POSIX-native command를 유지하고 Windows shell로 탈출하지 않는다.
- CI에서는 workflow가 지정한 shell을 유지한다.


구체적인 native/file-input fallback과 충돌 진단 수행은 검증한 [외부 수행법](agent-instruction-policy.md)을 따른다. current shell·영속 설정 금지와 stop 의미는 프로젝트 적용 원본이 우선한다.

## 외부 agent와 도구 권한

Issue, PR, checklist에 외부 agent나 collector 이름이 적혀 있다는 사실은 그 agent의 CLI/API를 확인·설치·인증·호출할 권한이 아니다. 호출은 현재 사용자 지시 또는 canonical workflow가 명시적으로 부여한 경우에만 수행한다.

## Source of Truth는 정보 종류별로 구분한다

전역 우선순위 하나로 모든 충돌을 해결하지 않는다.

| 정보 종류 | Source of Truth | 충돌 시 행동 |
| --- | --- | --- |
| 현재 사용자의 작업 지시 | 현재 세션의 명시적 사용자 지시 | 기존 Issue 목표를 바꾸면 구현 전에 Issue 본문도 갱신한다. |
| 이슈의 목표·범위·완료 기준 | 해당 Issue의 현재 본문 | 댓글만으로 범위를 변경하지 않는다. |
| 공통 agent hard guard | `AGENTS.md` | agent별 파일이나 Skill이 완화할 수 없다. |
| 작업 절차 | canonical Skill + Skill이 지정한 process 문서 | 충돌하면 구현하지 말고 충돌 문서를 특정한다. |
| 모듈 의존성과 수정 경계 | `docs/architecture/module-boundaries.md` | 승인된 architecture 변경이 아니면 경계를 넘지 않는다. |
| 현재 실행 동작(as-is) | 현재 `main` 코드 | business 문서와 다르면 코드를 관찰된 as-is로 취급한다. |
| 구현 완료 후 제품 규칙 | `docs/domains/**` | Issue to-be가 바꾸면 완료 단계에서 최종 코드와 동기화한다. |
| UI 배치·화면 상태 | Issue가 연결한 immutable HTML Visual Spec | 기능 정책은 Issue 본문을 따른다. |
| 과거 결정 근거 | `docs/reviews/**` | 역사 기록이며 현재 요구사항을 덮어쓰지 않는다. |
| SDD 작업 문서 | `docs/sdd/**` | 임시 계획이며 Issue/business 규칙을 독자적으로 바꾸지 않는다. |

## 코드와 business 문서가 다를 때

1. 코드가 실제 현재 `main` 동작인지 확인한다.
2. 차이를 파일·심볼·규칙 ID로 기록한다.
3. **문서 차이만을 근거로 기능 코드를 바꾸지 않는다.**
4. 문서 정합성 작업이면 확인된 코드 동작에 맞춰 문서를 수정한다.
5. 기능 변경이면 Issue to-be를 구현하고 완료 단계에서 business 문서를 최종 코드에 맞춘다.
6. 의도된 상태를 결정할 수 없으면 `BLOCKED: instruction conflict`로 중단한다.

## Issue와 코드가 다를 때

Issue는 **to-be**, 코드는 **as-is**다. 차이만으로 Issue가 틀렸다고 판단하지 않는다.

Issue 완료 기준이 architecture 경계를 위반하거나 서로 동시에 만족할 수 없으면 구현하지 않고 충돌 항목을 `BLOCKED`로 보고한다.

## 추론 금지 규칙

다음을 금지한다.

- 존재하지 않는 파일·모듈·라벨·API·설정 이름을 비슷한 이름으로 추정
- Issue에 없는 기능을 필요해 보인다는 이유로 추가
- 허용 경로 밖 제품 파일을 임의 수정
- 오래된 review/proposal/handoff를 현재 요구사항으로 복원
- 필수 Visual Spec 없이 새 UI 구조 설계
- 실패/미실행 검증을 통과로 기록
- 사용자 변경을 현재 작업과 무관하게 reset/checkout/clean/revert

필요한 값은 저장소와 Issue에서 먼저 찾는다. 검색 후에도 안전한 기본값이 없으면 추정하지 않고 `BLOCKED`로 보고한다.

## 범위 확장 규칙

Issue 작업에서는 `수정 허용` 경로만 수정한다.

- 허용 경로 밖 제품 변경이 필요하면 파일을 건드리지 않고 차단 사유를 보고한다.
- shared contract/wiring이 필요하면 `docs/architecture/module-boundaries.md`의 integration 규칙을 읽고 따른다.
- 별도 버그/개선이 현재 완료 기준에 필수적이지 않으면 현재 변경에 섞지 않는다.

Issue 없이 직접 요청된 작업은 사용자 요청을 만족하는 최소 파일만 수정한다.

## 사람용 문서의 시각적 작성

사람이 읽고 판단할 Issue, 현황·계획, 제안·결정·리뷰, business 설명과 완료 요약을 새로 쓰거나 실질적으로 고칠 때 적용한다. **결론과 달라지는 모습을 먼저, 상세 근거는 그다음**에 둔다. 이 절은 표현 원칙만 정하며 새 권한이나 승인 단계를 도입하지 않는다.

| 독자가 알아야 할 것 | 먼저 보여줄 표현 |
| --- | --- |
| 정책·선택지·전후 차이 | 작은 비교표 또는 대표 상황과 기대 결과 |
| 소유·책임·시스템 연결·경계 | 관계도, 컨텍스트 그림 또는 경계 표 |
| 순서·분기·실패·재시도·상태 | 흐름도, 상태표/상태도 또는 대표 시퀀스 |
| 화면 배치·조작 | 프로젝트 Visual Spec 기준에 맞는 거친 시안 |
| 한 문장으로 이해되는 단순 변경 | 그 한 문장 |

그림·표를 선택할 때는 답할 질문과 핵심 변화가 먼저 보이게 한다. 확인된 현재 상태·제안·미결, 중요한 조건·실패·예외·책임 경계를 구별한다. 그림과 본문/표가 같은 의미를 전달해야 하며 렌더링 없이도 핵심 조건을 읽을 수 있게 한다. 색만으로 상태를 구분하지 않고, 복잡하면 전체 관계와 필요한 상세를 나눈다.

파일·함수·명령·로그·검사 inventory처럼 Agent 실행에만 필요한 근거는 실행 명세로 연결한다. 비용·위험·기대 동작·권한 등 사람의 판단을 바꾸는 조건은 사람용 설명에서 숨기지 않는다. 관계를 드러내지 못하는 장식용 그림이나 같은 흐름의 장황한 산문 복제는 추가하지 않는다.

새 승인이나 독립 review 회차, 그림 개수·사례 수 의무, 생략 사유 항목, 특정 도구·외부 렌더링 의존성은 추가하지 않는다. 기존 문서를 일괄 재작성하거나 단순 변경에 SDD를 만들지 않는다. 작성·수정·검토하는 phase에서 이 절만 확인하고, 변경 없는 같은 run의 확인은 재사용한다. 다른 서식·예시 전체는 필요한 경우에만 참고한다.

기존 리뷰 또는 해당 grade의 self-review에서 첫 설명으로 핵심 변화·선택을 찾을 수 있는지, 표현이 필요한 관계를 보여주는지, 본문과 조건·미결이 같은지 확인한다. 중요한 의미 차이는 기존 source/범위/review 규칙으로 처리한다. 이는 기존 리뷰의 작성 품질 확인이며 별도 승인 단계나 그림 개수 기반 자동 완료 gate가 아니다. 실제 사람의 사용 관측 없이 이해 향상이나 검토 시간 절감을 입증했다고 쓰지 않는다.

같은 리뷰에서 독자가 무엇이 달라지는지, 누가 무엇을 책임지는지, 실패하면 무엇이 일어나며 무엇이 아직 미결인지 해당 설명으로 답할 수 있는지 확인한다. 정적 관계선을 호출 순서로 오해하게 하거나 그림에만 자동 재시도를 추가한 경우에는 의미 불일치로 처리한다. [불일치 리뷰 예시](visual-writing-examples.md#review-check)는 해당 판단이 필요할 때만 참고한다. 링크·서식 검사의 통과, 실제 작성/리뷰 행동, 사람의 이해 관측은 서로 다른 근거로 기록한다.

## 완료 보고 기준

최소 다음을 보고한다.

1. 변경 파일
2. 요구사항별 완료 여부
3. 실행한 검증과 결과
4. 실행하지 못한 검증과 이유
5. 남은 `BLOCKED`

완료 기준이 하나라도 실패·미검증이면 전체를 완료라고 표현하지 않는다.

## 모호한 지시를 작성하지 않는 형식

```text
IF <검증 가능한 조건>
THEN <수행할 행동>
ELSE <다음 행동 또는 아무것도 하지 않음>
```

또는 판정 가능한 체크리스트를 사용한다. `좋게`, `깔끔하게`, `충분히`, `적당히`, `최대한`만으로 완료 기준을 만들지 않는다.

## Execution Packet은 derived cache — 수행

- stale 항목은 필요한 source만 bounded refresh하고 새 provenance로 `VALID`가 된 뒤 사용한다. freshness를 증명할 수 없으면 해당 workflow의 `BLOCKED` stop condition을 따른다.
- 하나의 invalidation을 Issue comments, docs, repository 전체 재로드로 확장하지 않는다.
## Repository text UTF-8 first-read — 수행

- PowerShell에서는 `Get-Content -Raw -Encoding utf8 <path>`처럼 UTF-8 decoding을 명시한다. text를 native process나 pipe에 전달해 output encoding이 영향을 주는 경우 첫 명령 전에 process scope의 `$OutputEncoding`과 `[Console]::OutputEncoding`을 UTF-8로 설정한다. profile, registry, system locale은 변경하지 않는다.
- Git Bash/WSL/Linux에서는 current-shell의 `cat`, `sed` 또는 Python UTF-8 helper를 사용하고 repository text read만을 위해 PowerShell로 전환하지 않는다.
- CI에서는 workflow가 지정한 shell에서 UTF-8 native read를 사용한다.

첫 read가 실패하거나 mojibake가 보이면 해당 출력으로 Skill·절차·내용을 판정하지 않는다. 파일의 BOM·bytes·선언된 encoding 등 원인을 한 번만 확인한다. 실제 non-UTF-8 파일임이 확인된 경우에만 확인한 encoding으로 bounded fallback을 한 번 사용한다. 같은 read command를 반복하지 않는다. encoding 확인을 이유로 여러 shell을 순회하거나 repository-wide 탐색을 시작하지 않는다.

## 실행 shell affinity — 수행

current-shell 방식이 실패했을 때 fallback 순서는 다음과 같다.

1. repository와 현재 shell의 canonical invocation을 확인한다.
2. Python helper, CLI의 file input, JSON encode/decode, native executable·`.cmd`처럼 현재 shell에서 실행 가능한 portable/native fallback을 한 번 적용한다.
3. Windows-only API/동작이 필요하고 앞 단계로 처리할 수 없거나 repository가 PowerShell script만 제공할 때만 PowerShell cross-shell fallback을 허용한다.

Issue/PR body, JSON, Markdown 같은 structured/multiline data는 nested shell quoting보다 Python 또는 CLI file input을 우선한다. 임시 파일이 필요하면 repository 밖 run-owned 위치를 사용하고 같은 run에서 정리한다. Git Bash에서 `foo.ps1`과 `foo.cmd`가 함께 있으면 execution policy 영향을 받는 `.ps1` 대신 `.cmd` 또는 native executable을 사용한다. PowerShell session의 정상 entrypoint resolution은 유지하되 execution policy를 변경하지 않는다.

Git Bash의 MSYS path conversion 문제는 shell 전환 사유가 아니다. 기기 내부 경로(예: `/sdcard/...`)처럼 알려진 경로는 기존 `MSYS_NO_PATHCONV=1` canonical workaround를 먼저 적용한다.

같은 shell/quoting 원인에 대해 current-shell canonical 방식과 portable/native fallback이 모두 실패하면 exploratory shell switching을 반복하지 않는다. 필요한 외부 상태나 권한을 판정 가능한 blocker와 resume condition으로 기록하고 해당 workflow의 stop condition을 따른다.

## 코드와 business 문서가 다를 때 — 수행

1. 코드가 실제 현재 `main` 동작인지 확인한다.
2. 차이를 파일·심볼·규칙 ID로 기록한다.
3. **문서 차이만을 근거로 기능 코드를 바꾸지 않는다.**
4. 문서 정합성 작업이면 확인된 코드 동작에 맞춰 문서를 수정한다.
5. 기능 변경이면 Issue to-be를 구현하고 완료 단계에서 business 문서를 최종 코드에 맞춘다.
6. 의도된 상태를 결정할 수 없으면 `BLOCKED: instruction conflict`로 중단한다.

## 완료 보고 기준 — 수행

최소 다음을 보고한다.

1. 변경 파일
2. 요구사항별 완료 여부
3. 실행한 검증과 결과
4. 실행하지 못한 검증과 이유
5. 남은 `BLOCKED`

완료 기준이 하나라도 실패·미검증이면 전체를 완료라고 표현하지 않는다.

## 컨텍스트 / 토큰 효율

- 대상이 정해졌으면 관련 없는 Issue body, domain, 문서를 일괄 조회하지 않는다.
- path/symbol/heading으로 범위를 좁히고, 지원되는 경우 full file 대신 필요한 section만 읽는다.
- 같은 run의 implementing → parallel → finishing에서 변경 없는 context를 전달·재사용한다.
- 대량 로그는 요약하고 실패 시 대표 오류와 필요한 주변 구간만 확장한다.
- 토큰 절약을 이유로 검증이나 필수 근거를 생략하지 않는다.

### Trivial Issue fast-track

`SDD grade: Trivial`은 lock으로 검증한 W `process/sdd-workflow.md`의 공통 비동작 변경 조건을 모두 만족할 때만 사용한다. 제품별 적용은 `docs/sdd-workflow.md`를 따른다.

- 별도 SDD와 independent review를 만들지 않는다.
- 대상 파일과 직접 검증 근거만 읽고 repository-wide 탐색을 하지 않는다.
- 기본 검증은 링크/path/format/static validator 등 변경 종류에 맞는 targeted validation으로 한정한다. 빌드 도구 검증은 변경이 그 결과에 영향을 주지 않는 한 실행하지 않는다.
- diff ↔ 요청 범위 self-review는 유지한다.
- 실행 코드, 테스트 기대값, build/dependency, schema, contract 또는 workflow 실행 의미가 바뀌면 Trivial로 진행하지 않고 최소 Small로 재판정한다.

### Small Issue 추가 절약 규칙

`SDD grade: Small`인 Issue에만 다음 규칙을 추가 적용한다.

- 필요한 파일만 읽고 전체 파일 출력은 피한다.
- 인터페이스·타입은 선언부와 판단에 필요한 주변 줄만 조회한다.
- 검색 범위를 대상 path·symbol로 제한하고 대량 source dump를 만들지 않는다.
- 같은 run에서 이미 전문을 읽었고 변경되지 않은 workflow·Skill 문서는 재사용한다.
- diff는 변경 파일 목록과 필요한 hunk만 확인하고 전체 diff 출력은 피한다.
- 빌드·CI 성공 시 최종 status와 summary만 확인하고, 실패 시에만 대표 오류와 관련 구간을 추가 조회한다.
- 같은 Issue·source·검증 상태를 근거 없이 반복 조회하지 않는다.
- 이 규칙으로 필수 최초 문서 읽기, claim·grade gate, 검증, review, QA 또는 완료 근거를 생략하지 않는다.
