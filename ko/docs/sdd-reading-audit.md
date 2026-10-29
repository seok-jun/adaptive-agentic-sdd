# SDD 선택적 읽기와 독자별 산출물 배치 검증

검증일: 2026-10-29. 이 변경은 PR 후보이며 제품 설치·배포·정책 채택 결과가 아니다. 작업 범위는 한국어 workflow다. M의 원칙·영문 공통 계층은 변경하지 않았고, workflow의 영어판은 기존부터 미제공 상태다.

## 원본과 기준

- 소비 프로젝트의 `install.lock.json`은 `663d925a8ce562225f7a8779d26b16a25fbf8eb7`을 고정한다. 원격 main의 lock과 manifest를 확인했다. manifest blob은 `eb0ed27eed64f3dca394a8f2238050fd3ace9bef`, SHA-256은 `3450c4330069bd448e0717214a4c753856f2d7b94beb200b77f55304c2044b5c`다. 로컬 설치본 manifest·workflow는 이 고정 원본과 바이트가 같다. 설치본은 수정하지 않았다.
- 공개 `main`의 `9577134`는 v0.2다. 실제 설치 가능한 원본은 `v1-preview`의 `ko/adaptive-sdd/`이며 고정 커밋 이후 `068618bdda2f8d0571da3099f5e132e4ff17ff1e`가 존재한다. 해당 후속 변경의 전제 조사·계획 정정·리뷰 snapshot·외부 설치 지원을 포함한 최신 tree에서 별도 브랜치를 만들었다. 과거 tree로 덮어쓰지 않았다.
- 별도 연구 저장소에서 현재 목차·에이전트 지침·연구/배포 경계를 확인했다. 연구 저장소 자체를 소비 원본으로 바꾸지 않았으며 비공개 연구 자료를 배포 묶음에 복사하지 않았다. 공개 workflow에 이미 반영된 계약이 이번 구현의 기준이다.
- 재현 기준과 기존 섹션별 SHA-256은 `tests/fixtures/sdd-section-map.json`에 있다. 배포 bundle의 `MANIFEST.json`을 갱신했다. installer가 디렉터리를 재귀 검증하므로 새 런타임이나 installer 분기 추가는 필요하지 않다. 제품 lock·태그·릴리스는 변경하지 않았다.

## 비효율의 원인과 관찰 한계

기존 workflow는 24,510 bytes이고 분류부터 Epic·종료까지 한 파일에 있었다. 각 Skill이 '해당 절'을 요구해도 파일 경계에서는 관련 없는 규칙까지 함께 읽기 쉽다. 구현→리뷰→종료에서 같은 파일이 다시 참조된다. 산출물 규칙도 11,898 bytes의 한 파일에 작성·정정·trade-off가 함께 있었다. 기존의 동일 run 재사용 지시는 유지했으며 별도 캐시는 만들지 않았다.

PLAN은 이미 Human Decision Contract(`02-to-be.md`)와 Agent Execution Spec(`change-plans/**`)이 분리되어 있었다. 따라서 이름을 바꾸거나 새 human-view/agent-spec 파일을 추가하지 않았다. 실제 혼합은 AS-IS의 설명·위험·코드 근거이며, README의 Priority·grade·수정 경로는 Issue와 이중 관리할 여지가 있었다.

이는 문서의 요구와 참조 그래프에 대한 정적 분석이다. 실제 사용자 작업의 전체 산출물 표본이나 Agent 읽기 trace를 수집하지 않았으므로 실운영 중복률·미사용률·생성 토큰은 확정하지 않는다. '작성 후 소비되지 않는다'는 이유로 검증·위험 항목을 삭제한 것은 없다.

## 분리 내역과 소비 관계

| 원본 파일 | 새 담당 파일 | 소비 단계·의존성 |
| --- | --- | --- |
| workflow의 등급·자동 격상 | `sdd/grade.md` | 실행 분류·재판정; P의 위험 매핑 |
| workflow의 진입·등급별 진행·분석 재사용·routing 안내 | `sdd/entry.md` | 최초 쓰기·구현 진입; grade/issue·조건별 검증/claim/routing |
| workflow의 Issue 계약·정규화·미결 의존성 | `sdd/issue.md` | 관리·구현·종료; 사람 판단·Issue 본문 원본 |
| workflow의 Epic 관리·전환 | `sdd/epic.md` | Epic 조율; managing의 분류 입력은 grade, 공통 질문은 issue, 하위 실행 진입에 entry |
| workflow의 문서 수명·business 동기화·종료 순서 | `sdd/completion.md` | 종료; issue/SUMMARY·verification·finishing |
| artifact의 AS-IS 조사 | `sdd/as-is.md` | 조사·AS-IS review |
| artifact의 TO-BE·실제 대안 | `sdd/to-be.md` | PLAN 사람 결정·AC 검증 대응 |
| artifact의 change-plan | `sdd/agent-spec.md` | PLAN 실행 명세·구현 인계 |
| artifact의 계획 정정 | `sdd/plan-change.md` | 전제 오류·정책 변경이 생긴 때만 |

`sdd-workflow.md`는 경로 안내만 남겼다(1,906 bytes). `sdd-artifacts.md`는 최초 폴더 배치·독자·원본 연결을 맡는다. 새 세부 규칙 9개, 선택적 작성 서식 4개다. 안내 두 개와 세부 규칙을 모두 읽으면 오히려 원문 두 개보다 커진다. 최적화 대상은 전체 저장 크기가 아니라 단계별 소비다.

implementing은 grade/entry/issue를 직접 읽고 실제 AS-IS·PLAN·정정 시에만 담당 파일을 읽는다. finishing은 completion/issue, managing은 grade/issue와 조건부 epic을 직접 읽는다. parallel-development의 claim 계약은 바꾸지 않았다. process 문서의 상대 링크·앵커, P 생성 template의 경로도 갱신했다. 확인한 동일 버전 재사용은 유지하며 미확인·변경·stale 근거는 다시 확인한다.

## 산출물 항목별 판단과 수명

| 정보 | 분류·변경 | 소비자·시점 / 누락 위험 |
| --- | --- | --- |
| Issue 번호·Priority·grade·허용/금지 | 참조 전환 | 관리·진입에서 Issue 본문·기준 revision/확인 시점을 확인. 복제값 drift 방지; 접근 불가 시 추정 금지 |
| 문제·원인 모델·관계·동작·주요 위험 | 유지·물리 이동 | 기존 README에서 사람의 AS-IS 판단. 근거 링크를 함께 제공; 위험 누락 금지 |
| 코드 경로·심볼·재현·사실/가설/미조사 | 유지 | `01-as-is.md`에서 설계·reviewer·구현자가 소비. 사실과 전제의 유효성 판단에 필요 |
| 직접 외부 의존 버전·운영 소비자·도입 의도 | 유지(기존 조건부) | 판단에 영향을 줄 때만 조사. 전수 이력 조사로 확대하지 않음 |
| 문서-code drift·전제 충돌·미결 담당/필요 단계 | 유지 | AS-IS→PLAN→구현 인계. 무관한 작업까지 차단하지 않으며 소비 단계 전에 해소 |
| 변경/불변 동작·실패·데이터/상태 | 유지 | TO-BE의 제품 의미 원본; 실행 명세에 중요한 결정을 숨기지 않음 |
| Decision ID·선택·이유·실제 대안·비용 | 유지·중복 참조 전환 | TO-BE에서 사람 판단, change-plan은 D-ID 참조. 가상의 대안이나 별도 trade-off 문서 불필요 |
| AC와 검증 수단·성공 근거 | 유지 | TO-BE에서 완료 기준과 검증 연결. change-plan에는 실행 세부만 두고 동일 계약을 복제하지 않음 |
| target/caller/callee·invariant·구현 순서·schema | 유지 | Agent 명세→구현·CODE review. 해당하는 변경만 작성 |
| 컨벤션·명시적 이탈·예외 근거 | 유지 | PLAN/CODE 검토. 선언하지 않은 취향을 새 규칙으로 만들지 않음 |
| test case·명령·실행 evidence·실패/롤백 확인 | 유지·근거 참조 | 검증·종료에서 소비. 기존 결과를 고정 target으로 연결; 과거 PASS 승계 금지 |
| 이전 AS-IS·Issue·코드·리뷰 원문 재서술 | 축소·통합 | 유효한 원본을 연결하고 차이만 작성. 참조 접근·revision·범위·전제 확인 필수 |
| 별도 evidence 파일·복제 완료 보고 | 제거 후보의 추가를 방지 | 기존 근거로 충분하면 만들지 않음. 필요한 근거 자체는 제거하지 않음 |

필수 작업 파일은 기존 4종 그대로다. AS-IS의 사람용 설명은 README, 직접 근거는 01-as-is, PLAN의 사람 계약은 02-to-be, 실행 명세는 change-plan이다. Medium은 SDD 후 중간 승인 없이 진행하고 Large는 기존 AS-IS→A/B→PLAN→A/B 순서를 유지한다. 새 AS-IS target은 README와 01-as-is 양쪽을 같은 candidate로 검토한다. 진행 중 기존 배치는 자동 이관하지 않는다.

SDD는 작업 중 작성·갱신하고 최종 코드 기준 business 갱신 및 필수 검증 후 기존 참조 보존 조건으로 정리한다. 활성 소비자가 있으면 불변 참조로 전환하거나 담당·해제 조건으로 보존한다. 영속 business/review 문서의 역할은 그대로이며 새 evidence 파일에도 수명 예외를 만들지 않았다.

## 보호 규칙과 검증

기존 workflow의 19개 규칙 섹션은 담당 파일과 내용 hash로 대응한다. 링크 목적지 이동, 교차 파일 지시 표현, 새 AS-IS 두 파일 명시만 정규화하고 본문 누락·중복을 검사한다. 산출물 항목은 위 대응표로 검토했다. M/W/P 원본, 사람 판단 및 STOP, Large A/B·Blind Audit 독립성, grade·claim·진입, 필수 검증/PASS 최신성, 인계, 최종 코드 business 갱신, 산출물 수명은 보존했다. Small/Trivial의 SDD 생략도 유지한다.

- `python -I -B -m unittest discover -s tests -v`: 32개 PASS. 기존 25개와 보존·직접 경로·동일 근거 분리·manifest·변조/누락·측정 입력 검사 7개다.
- 설치 render/check/check-evals, GitHub/local-docs tracker, 외부 harness, Windows 생성 명령, 상대 링크/앵커, review snapshot을 포함한다. 최초 실행에서 깨진 안내 앵커와 Windows 샌드박스 Git 셸 제약을 발견했다. 앵커를 수정하고 같은 테스트를 제약 밖에서 재실행해 통과했다.
- 기존 행동 사례 60개는 내용 유지, 새 합성 회귀 사례 6개를 추가했다. 총 66개 형식·ID 검증은 PASS다. LLM 행동 평가는 미실행이므로 행동 회귀 없음이나 실제 준수율을 주장하지 않는다.
- `git diff --check`: PASS. 공개물에는 합성 도서 서비스 fixture만 사용했다. 제품 코드·대화·비공개 연구 내용을 옮기지 않았다.
- 작성자 self-review·결정적 검사와 별도 서브에이전트 독립 리뷰를 수행했다. 실제 host 행동 평가·Linux/macOS 재실행은 미수행이다.

## 정적 비용 비교

재현: `python -I -B tests/measure_sdd_reading.py`. 같은 baseline commit과 파일 목록을 JSON으로 출력한다. 수치는 기존 평가 규약의 `ceil(UTF-8 bytes / 4)` proxy이며 모델 tokenizer 측정값이 아니다. 특히 한국어 실제 토큰과 일치하지 않는다.

선택한 W 규칙·Skill·verification(해당 시 design-review)을 cold phase별 비교한다. P 적용 문서·코드·작업 산출물·조건부 routing/packet/관측, system/user/tool 입력은 양쪽 수치에서 제외하되 실행 의무는 유지한다. 전체 모델 입력·생성 토큰·도구 출력 오버헤드는 미측정이다.

| 시나리오 | 기존 파일 전체 proxy | 기존 workflow만 이상적 절 선택 | 새 선택 파일 proxy | 전체 읽기 대비 감소 | 파일 읽기 수 전→후 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Small 구현 | 13,274 | 11,106 | 11,232 | 15.4% | 3→5 |
| Medium 설계·구현 | 16,249 | 14,080 | 14,250 | 12.3% | 4→9 |
| Large AS-IS | 20,893 | 18,724 | 17,946 | 14.1% | 5→8 |
| Large PLAN | 20,893 | 18,724 | 16,956 | 18.8% | 5→8 |
| 구현·검증 | 16,249 | 14,080 | 11,584 | 28.7% | 4→6 |
| 완료·인계 | 13,885 | 9,989 | 10,079 | 27.4% | 3→4 |
| Epic 관리 | 8,519 | 5,287 | 5,346 | 37.2% | 2→4 |

이상적 절 선택 열도 artifact/Skill/verification은 파일 전체로 계산한다. 모든 파일의 최적 섹션 선택 대비 우위를 뜻하지 않는다. Small·Medium·종료·Epic은 이상적 workflow 절 선택보다 소폭 증가한다. 분리는 부분 읽기의 물리적 안정성을 높이지만 완벽한 부분 읽기보다 항상 작지는 않다.

정해진 직접 경로를 쓰므로 탐색 호출은 모델상 양쪽 0회다. 파일 하나당 호출하면 읽기 호출은 증가한다. 한 도구 요청으로 현재 phase 파일을 함께 읽을 수 있지만 host별 실제 호출 수/지연은 미측정이다. 안내를 매번 경유하거나 파일 전체를 모두 읽으면 이 비교가 성립하지 않는다.

Large AS-IS→PLAN→구현→종료를 각각 cold로 읽으면 반복 bytes는 186,592→129,098이다. 동일 run에서 변경 없는 파일을 한 번씩만 읽는 이상적 경우는 101,066→97,131 bytes로 차이가 작다. 이 숫자는 호출 trace가 아니라 파일 목록을 합산한 모델이다. 재조회 필요 여부는 최신성 규칙이 우선한다.

### 산출물 작성량과 독자 부담 표본

`tests/fixtures/sdd-artifact-sample.json`은 실제 사례가 아닌 고정 합성 표본이다. 전후의 사실·위험·Decision·AC·실행 계약 원문이 한 번씩 유지되는지 검사한다. Issue metadata의 중복 작성만 원본 참조로 바꿨다.

| 정적 표본 | 전 bytes / proxy | 후 bytes / proxy |
| --- | ---: | ---: |
| 작성된 전체 텍스트 | 3,252 / 813 | 3,081 / 771 |
| 사람 기본 읽기(근거 상세 제외) | 2,099 / 525 | 1,333 / 334 |
| Agent AS-IS 근거 읽기 | 1,410 / 353 | 1,099 / 275 |
| 필수 작업 파일 수 | 4 | 4 |

작성 텍스트는 5.3%, 사람 기본 읽기는 36.5%, Agent 근거 읽기는 22.1% 줄었다. 실제 생성·수정 토큰이나 사람 이해도를 측정한 것이 아니다. reviewer는 두 AS-IS 파일과 필요한 근거를 모두 검토하므로 같은 비율의 감소를 기대하지 않는다. 근거가 필요한 사람도 추가로 읽는다. Medium/ Large에 같은 배치 원칙을 쓰지만 다양한 Large 사례의 일반화 효과는 확인하지 않았다.

## 위험과 다음 후보

1. 파일 수 증가로 호출 지연·선택 오류가 생길 수 있다. 직접 경로와 보존 검사를 제공했으나 실제 Agent 평가가 필요하다.
2. 규칙 전체 크기는 증가했다. 선택적 읽기 실패 시 비용이 더 커질 수 있으며, entry/issue의 추가 분할은 실제 trace로 함께 소비하는 범위를 확인한 뒤 판단한다.
3. 참조의 접근 권한·가변 Issue·수명 문제가 생길 수 있다. 원본 identity와 소비 전 확인, 기존 정리 조건을 유지했다. 실제 여러 저장소 인계는 미검증이다.
4. AS-IS 독자 분리는 새 작업에만 적용한다. 기존 작업에 README review를 소급 요구하지 않는지 실제 재개 사례로 확인해야 한다.
5. 생성 토큰·전체 입력·도구 호출·사람 이해도·실제 보호 조건 준수는 동일 fixture/모델/횟수/예산의 별도 평가 후보다. 정적 수치만으로 새 모델 기본값·정책 채택·제품 pin 변경을 결정하지 않는다.

새 캐시·로깅·Agent 실행 구조는 추가하지 않았다. PR 병합과 제품 설치본 변경은 이 작업에 포함하지 않는다.

## 부록: 기존 규칙 섹션별 크기와 이동

UTF-8 bytes, heading·하위 절 포함. 규칙이 아닌 기존 읽기 안내는 새 index로 대체했다.

| 기존 섹션 | bytes | 담당 파일 |
| --- | ---: | --- |
| SDD grade | 2853 | `sdd/grade.md` |
| 공통 계약과 프로젝트 적용 | 541 | `sdd/entry.md` |
| 구현 시작 조건 | 1472 | `sdd/entry.md` |
| grade별 산출물과 게이트 | 1898 | `sdd/entry.md` |
| 기존 분석 재사용 | 531 | `sdd/entry.md` |
| Verification Strategy | 266 | `sdd/entry.md` |
| Grade별 review gate | 261 | `sdd/entry.md` |
| SDD 작업 문서 구조 | 222 | `sdd/entry.md` |
| 실행 routing과 packet | 1488 | `sdd/entry.md` |
| 차세대 방법론의 적용과 개선 관측 | 325 | `sdd/entry.md` |
| 안정화 기간 token diagnostic | 269 | `sdd/entry.md` |
| 병렬 작업 | 271 | `sdd/entry.md` |
| Issue 본문 규약 | 3087 | `sdd/issue.md` |
| Legacy Issue 정규화 | 799 | `sdd/issue.md` |
| 미결 사항과 단계별 의존성 | 1540 | `sdd/issue.md` |
| Epic 관리 단위 | 3297 | `sdd/epic.md` |
| 문서 역할 | 979 | `sdd/completion.md` |
| business 문서 갱신 | 699 | `sdd/completion.md` |
| 완료 절차 | 1817 | `sdd/completion.md` |

### 합성 산출물의 파일별 크기

| 작업 파일 | 기존 bytes | 후보 bytes | 주요 소비 |
| --- | ---: | ---: | --- |
| README | 504 | 644 | 작업 진입 → 사람용 AS-IS 현황·원본 링크 |
| 01-as-is | 1,410 | 1,099 | 조사·AS-IS review·PLAN 근거 |
| 02-to-be | 689 | 689 | 사람 PLAN 판단·구현 Decision/AC·종료 |
| change-plan | 649 | 649 | 구현·검증·인계 |

표본에서는 네 사실 묶음이 전후 각각 한 번씩 존재한다. 사실 묶음 중복률은 양쪽 0%이며, 제거한 것은 외부 Issue와 중복되는 metadata의 로컬 사본이다. 실제 문서 corpus의 의미 중복률은 미측정이다. 위 단계 연결은 설계상 소비 위치이며 실제 읽기 횟수와 같다고 보지 않는다.

## PR #2 독립 리뷰와 수정

작성에 참여하지 않은 별도 문맥의 서브에이전트가 `8f268c97c7092c65965d16efcf5fb086facca7d0`을 기준으로 원본 diff·규칙·Human/Agent 배치·측정 코드를 독립 검토했다. 핵심 STOP·사람 판단·검증·수명·원격 candidate·Blind Audit 격리의 추가 누락은 발견하지 않았고 아래 두 P2 지적을 제시했다.

| 지적 | 수정·회귀 방지 |
| --- | --- |
| Epic after 측정에서 managing Skill의 필수 grade 입력 누락 | grade를 포함해 절감률 45.7%→37.2%, 읽기 수 2→3에서 2→4로 정정. Skill의 실제 Inputs에서 추출한 필수 경로가 측정 선택에 포함되는지 검사 |
| AS-IS target인 README에 PLAN 작성 뒤 링크를 추가하면 bytes가 바뀌어 불필요한 재확인 발생 | 최초 README에 예정 PLAN 경로를 둠. 진행 상태는 기존 Issue에서 관리. 실제 사실·전제 변화의 재검토와 PLAN A/B는 유지하며 링크 변경을 일괄 면제하지 않음 |

계획 정정의 AS-IS 범위에 README의 사람용 현황·위험도 포함함을 명확히 했다. 이는 별도 결함 판정이 아닌 stale 사람 판단 방지를 위한 명확화다. 새 합성 사례는 기존 AS-IS target 유지와 PLAN 검토를 구분한다. 모델 행동 실행 결과로 간주하지 않는다.

같은 독립 리뷰어가 수정 diff와 직접 영향 범위를 재확인하여 두 P2의 해결 및 추가 actionable 지적 없음을 보고했다. 리뷰어는 구조 검사 6개와 측정 스크립트를 직접 실행해 결과를 대조했다. 작성 측 전체 회귀 32개도 PASS다. 이는 문서·정적 검사 결과이며 실제 Agent 행동 효과의 실측은 아니다.
