# 용어집

W 문서에 자주 나오는 말을 한 줄씩 풀었다. 규칙의 원본은 각 문서다. 이 용어집은 뜻을 설명할 뿐 규칙을 더하거나 바꾸지 않는다. 뜻이 문서와 다르게 읽히면 문서를 따른다.

## 구조와 설치

| 용어 | 뜻 |
| --- | --- |
| M | 공통 원칙(`methodology/`). 사람 판단 요건·관측 기록·보조 선택 규칙. 프로젝트가 고치지 않는다 |
| W | 공통 실행 절차(`workflow/`). 스킬·절차 문서·평가 사례. 프로젝트가 고치지 않고 버전을 올릴 때 통째로 바꾼다 |
| P | 프로젝트 저장소. 제품 사실·경로·명령·권한을 소유한다. 설정은 `project.json`, 그 값으로 만든 적용 문서는 `W/../project/` |
| 고정 사본(pinned copy) | 해시로 확인한 M·W 사본. `MANIFEST.json`과 `install.lock.json`으로 확인한다 |
| hard guard | 항상 지키는 규칙. 설치 도구가 `AGENTS.md`의 표시 구간에 넣은 `## 항상 적용 hard guard` 절 |
| run | 한 번의 실행(한 대화·세션). "같은 run에서 확인한 것은 재사용한다"는 같은 실행 안에서 다시 읽지 않는다는 뜻 |
| tracker | 작업 관리 방식. `local-docs`(공유 폴더의 문서·claim 파일) 또는 `github`(Issue·PR) |

## 작업 단위와 등급

| 용어 | 뜻 |
| --- | --- |
| Issue(실행 Issue) | 실제로 구현·검증하는 작업 항목 하나 |
| Epic | 여러 Issue를 묶어 관리하는 선택적 관리 문서. 실행 등급이 아니다 |
| grade(실행 등급) | Trivial·Small·Medium·Large. 변경 범위와 위험으로 정하고, 위험 조건에 걸리면 자동으로 올라간다 |
| SDD 작업 문서 | Medium·Large에서 쓰는 작업용 설계 문서. 작업이 끝나면 정리한다 |
| AS-IS | 지금 상태 조사와 근거 |
| PLAN(TO-BE) | 바꿀 방향·사람 결정·완료 기준과 검증 대응 |
| change-plan | 구현 명세(Agent Execution Spec). 구현 순서·테스트 세부 |
| Human View | 사람이 판단하려고 읽는 설명 부분 |
| Human Decision | 사람이 정한 제품·설계 결정. Agent가 대신 만들지 않는다 |
| business 문서 | 구현 완료 뒤에도 남는 현재 제품 동작 설명 |
| Visual Spec | Issue가 연결하는 고정된 HTML 화면 명세 |
| SUMMARY | 작업 종료 요약 기록 |

## 작업 공간과 경계

| 용어 | 뜻 |
| --- | --- |
| lane | 한 Issue를 맡아 진행하는 독립 작업 공간(branch·worktree 또는 클라우드 sandbox) |
| claim(`[CLAIM]`) | "이 경로는 내가 고친다"는 선점 기록. 첫 파일 쓰기 전에 남긴다 |
| release(`[RELEASE]`) | 선점 해제 기록 |
| allowed / forbidden | Issue가 정한 수정 허용 경로 / 수정 금지 경로 |
| shared contract | 여러 모듈이 함께 쓰는 공개 약속(인터페이스·스키마 등). 일반 lane에서 고치지 않는다 |
| root integration | 루트 빌드·설정처럼 통합 작업에서만 고치는 경로 |
| worktree | 같은 저장소를 다른 폴더에 하나 더 꺼낸 작업 사본 |

## 리뷰와 판정

| 용어 | 뜻 |
| --- | --- |
| candidate(검토 후보) | 검토 대상으로 고정한 정확한 커밋(exact SHA)과 그 문서 |
| 원격 게시 | 검토 후보를 선언한 원격 branch에 push해 다른 환경에서도 읽을 수 있게 하는 것 |
| Review A(Contract Review) | 사실·계약·구현 명세가 맞는지 보는 독립 리뷰 |
| Review B(Blind Audit) | Review A 결과를 보지 않고 빠진 사실·숨은 가정·경계 누락을 찾는 독립 리뷰 |
| reconciliation | Review B가 최초 판정을 낸 뒤 이전 지적이 해결됐는지 다시 대조하는 단계 |
| finding | 리뷰 지적 하나 |
| blocker | 다음 단계로 못 가게 막는 지적(Human Decision blocker·Execution-contract blocker) |
| Implementation finding | 다음 단계를 막지는 않지만 구현·종료 때 반드시 해결을 확인할 지적 |
| CODE Review | 구현 뒤 코드 리뷰 |
| PASS / BLOCKED | 통과 / 멈춤. `BLOCKED: <사유>`는 정해진 멈춤 사유다 |
| stop condition(멈춤 조건) | 해당하면 진행하지 않고 멈춰야 하는 조건 |
| STALE / INVALID | 근거가 낡음(출처가 바뀜) / 근거 형식이 깨짐 |

## 실행 배정과 인계

| 용어 | 뜻 |
| --- | --- |
| phase | 단계. PLAN·IMPLEMENT·REVIEW·TEST_DOCS |
| orchestrator / worker / reviewer | 전체를 맡는 담당 / 단계를 위임받은 작업자 / 리뷰 담당 |
| delegation | 다른 agent·session에 일을 맡기는 것. 사람의 "기록된 위임"과는 다른 말이다 |
| tier | 능력 단계. 모델은 `cheap < strong < frontier`, 추론은 `medium < high < extra-high`. `current`는 지금 실행 중인 값 |
| floor | 그 단계에 필요한 최소 능력 단계 |
| qualification | 특정 모델을 특정 역할에 써도 되는지에 대한 기록(PASS·DENIED) |
| current/manual model | 이미 실행 중이거나 사람이 고른 모델. Agent가 자동으로 고르는 후보와 규칙이 다르다 |
| packet | 하위 작업자·리뷰어에게 넘기는 요약 묶음(Execution·Result·Review Packet). 원본 문서를 대신하지 않는 복사본이다 |
| provenance | packet이 어떤 원본(경로·revision·해시)에서 나왔는지 고정한 출처 정보 |
| freshness | 그 출처가 지금도 최신인지 여부 |

## 검증과 기록

| 용어 | 뜻 |
| --- | --- |
| targeted 검증 | 바뀐 모듈·테스트부터 좁게 돌리는 검증 |
| broad 검증 | 최종 후보에서 돌리는 넓은 필수 검증 |
| PASS 재사용 | 같은 후보·같은 입력일 때만 이전 실행 결과를 다시 쓰는 것. 입력이 바뀌면 다시 돌린다 |
| preflight | 빌드·테스트 전에 JDK 같은 실행 환경을 확인하는 단계 |
| 관측(observation) | 시작·인계·종료 때 남기는 적용 기록과 실제 문제 기록 |
| not observed / not collected | 확인한 범위에서 못 봄(0이라는 뜻 아님) / 근거가 없어 수집 못 함 |
| token diagnostic | 안정화 기간에만 켜는 토큰 사용 기록(선택) |

## 프로젝트가 고르는 실행 프로필

`project.json`에서 고른다. 기본값은 지금 동작 그대로다. 규칙의 원본은 괄호 안 문서다.

| 설정 | 값 | 뜻 |
| --- | --- | --- |
| `review.large_mode` | `dual`(기본) / `single` | Large 설계 리뷰를 Review A·B 이중으로 할지, 독립 리뷰 1회로 할지([설계 리뷰](process/design-review.md#large-설계-리뷰-방식)) |
| `review.blind_reviewer_selection` | `required`(기본) / `optional` | Review B 모델을 사람이 꼭 골라야 하는지, 사람이 안 고르면 Agent가 조건에 맞는 모델을 고를 수 있는지([설계 리뷰](process/design-review.md#large-설계-리뷰-방식)) |
| `sdd.medium_artifacts` | `full`(기본) / `condensed` | Medium SDD를 네 문서로 나눌지, `README.md` 한 장으로 줄일지([SDD 산출물 배치](process/sdd-artifacts.md#medium-축약-배치)) |

어느 값도 M의 사람 판단 요건, 등급 자동 격상, 필수 검증, CODE Review를 줄이지 않는다.
