# 검증 계약

완료 기준을 검증에 연결하고 구현 중·종료 시 검증을 실행할 때 읽는다. grade 분류는 [sdd-workflow](sdd/grade.md#sdd-grade), 실제 프로젝트 명령은 `S/.adaptive-sdd/project/build.md`가 원본이다. 새 검증을 수량으로 채우지 않으며 해당 grade·변경 영향·Issue가 요구한 범위에 적용한다.

| 현재 작업 | 읽을 절 |
| --- | --- |
| 구현 전 완료 기준과 검증 수단 연결 | [Verification Strategy](#verification-strategy), [등급별 review gate](#grade별-review-gate) |
| 구현 루프·최종 후보 검증·PASS 재사용 | [검증 시퀀싱과 PASS 유효성](#검증-시퀀싱과-pass-유효성) |
| 빌드·테스트 명령 실행 | [검증 환경](#검증-환경) |

## Verification Strategy

P `build.md`는 기존 `build.verification` 명령과 `build.checks`의 command/manual·agent/human·required/optional 수단을 선언할 수 있다. 필수 수동 확인은 대상·절차·기대 결과를 인계하고 실제 관찰 결과·확인자·시점·검증 대상 identity를 근거로 남긴다. 증거를 받기 전에는 미검증이며, 수동 검증 선언 자체를 PASS로 보지 않는다. 실행 명령이 없는 수동 항목에 가짜 command/exit code를 만들지 않는다. 완료 기준을 증명하는 수단이 있어야 한다는 조건은 같다.

P의 테스트 수명이 temporary이면 테스트·fixture·실행 근거와 실제 제품 입력 identity를 선언 위치에 보존·재조회한 뒤 제거한다. 최종 후보와 실행 입력의 대응을 Packet에 연결하고 기존 PASS 재사용 조건을 적용한다. none이면 신규 테스트 대신 선언된 동등한 동작 관찰 근거가 필요하며, fixture/test를 필요로 하는 PLAN finding도 그 resolution expectation을 실제로 증명해야 한다. 증명할 수 없으면 차단하고 테스트 정책을 핑계로 필수 검증을 면제하지 않는다.

구현 전에 각 Acceptance Criterion을 어떤 근거로 판정할지 정한다. 검증 수단은 unit, integration, lint, build, CI와 grade별 review 중 실제로 필요한 것만 선택한다.

프로젝트가 승인하거나 기준으로 지정한 revision의 요구에서 적용 진입점·주체·조건과 기대 결과를 구별해 검증에 연결한다. 정상·실패·취소 중 원 요구나 변경 영향이 있는 경로를 다루며 정해진 경우의 수를 채우지 않는다. 기존 Issue/SDD/change-plan의 대응을 재사용하고 부족한 부분만 보완한다. 새 ID·표·별도 계획 파일은 요구하지 않는다. 기준 원본을 찾지 못하거나 해석이 갈리면 대응 미확인으로 남기고 그 판단에 의존하는 진행은 기존 gate를 따른다.

구현 리뷰와 종료 self-review에서는 기준 요구 → 실제 변경 → 최종 후보의 검증 결과·공백을 대조한다. 이미 채운 대응뿐 아니라 기준 요구에서 빠진 진입점·조건도 확인한다. 최신 문서끼리의 일치나 CI PASS만으로 기준 요구 충족을 대신하지 않는다. 테스트 제거·단언 약화·실행 제외·검증 대상 변경이 있으면 대체 근거와 남은 공백을 기존 SUMMARY에 드러내고 필수 검증 변경은 기존 권한을 따른다. 재사용한 결과는 대상·입력 범위와 재사용 사실을 표시하며 새 실행으로 보고하지 않는다.

- Medium 이상은 `02-to-be.md`에 Acceptance Criterion, 검증 수단, 성공 근거를 대응시킨다.
- Human View에는 완료를 판단할 근거를 유지하고, 상세 test case·명령·실행 evidence는 change-plan에 둔다. 같은 내용을 복제하지 않는다.
- Small은 기존 검증 기준만으로 모든 완료 기준을 증명할 수 있으면 별도 문서를 만들지 않는다. 검증 설계가 필요한 경우에는 구현 전에 같은 대응 관계를 작업 근거에 짧게 명시한다.
- Trivial은 변경 종류에 맞는 targeted validation으로 완료 기준을 증명하고 별도 Verification Strategy 문서를 만들지 않는다.
- 완료 기준을 증명할 수 없거나 검증이 Issue 경계를 넘어야 하면 구현 전에 `BLOCKED`한다.
- 같은 run에서 확인한 환경·JDK·Issue·source 결과는 재사용하고 targeted verification부터 실행한다.

Verification Strategy에는 grade 규칙에 따라 다음 판정을 포함한다.

```text
Independent Review: REQUIRED | NOT REQUIRED
```

Trivial은 항상 `Independent Review: NOT REQUIRED`다. Device QA / Runtime QA 판정이나 handoff를 공통 필수 gate로 자동 추가하지 않는다. P가 단순 참고로 선언한 기기 관측 문서는 비필수 참고 자료로 유지한다. 다만 P의 build.checks 또는 Issue Verification Strategy가 기기·런타임 확인을 required로 명시하면 위 수동 검증 계약을 적용하고 merge/complete 전에 실제 결과를 확인한다. 명시된 필수 검증을 참고 자료로 낮추지 않는다.

## Grade별 review gate

Review A와 기본 code review는 [phase-aware Contract Review Packet](../skills/_shared/execution-packets.md#review-packet)을 사용한다. 해당 phase에 존재하는 artifact·근거만 요구하며 reviewer에게 solution discovery나 repository-wide 재탐색을 시키지 않는다. 필드와 evidence identity는 packet 원본에서 확인한다.

independent review는 구현/문서 author와 다른 reviewer가 수행하고, PR review 또는 댓글에 `PASS` 또는 `BLOCKED`와 unresolved finding을 기록한다. Review A는 caller/callee, path/symbol, invariant와 phase contract 정합성을 확인하고, Review B는 [설계 리뷰](design-review.md#large-설계-이중-독립-리뷰)의 최소 Blind Audit Packet으로 completeness를 감사한다. 사람 판단으로 이 책임을 대체하지 않는다. Review B는 필요한 reconciliation 완료와 unresolved Human Decision/Execution-contract blocker 0을 확인해야 통과하며 Implementation finding과 Non-blocking observation의 수를 0으로 만들 필요는 없다. independent review가 required가 아닌 grade에서는 Agent self-review와 automation이 해당 검증을 맡는다.

| grade | 구현 전 design review | PR code review |
| --- | --- | --- |
| Trivial | Trivial 조건과 대상 범위 self-review | targeted validation + diff ↔ 요청 범위 self-review |
| Small | Issue 경계와 검증 가능성 self-review | diff ↔ 완료 기준 self-review |
| Medium | SDD와 Verification Strategy bounded self-review. shared contract 또는 여러 모듈의 integration 근거가 필요한 경우 independent review를 `REQUIRED`로 판정 | `Independent Review: REQUIRED`이면 bounded independent review 통과 필요, 아니면 self-review |
| Large | AS-IS/PLAN 각각 Review A Contract Review + Human-selected Review B Blind Audit 필요 | 기존 bounded independent code review 1회; 명시적 high-risk escalation만 추가 audit 가능 |

required review가 미완료이거나 boundary 위반, 완료 기준 미충족, 명백한 안전성·정합성 문제가 unresolved이면 구현 또는 merge를 진행하지 않는다.

## 검증 시퀀싱과 PASS 유효성

다음 용어는 grade별 최소 검증과 Issue별 Verification Strategy를 실행하는 공통 기준이다.

- **Verification-affecting input**: production/test source, resource, manifest, runtime asset, build/dependency/configuration, schema/migration/contract, fixture/snapshot/generated input/test expectation처럼 검증 command가 소비하거나 assertion하는 입력이다. 확장자나 `docs` 경로만으로 판정하지 않으며 runtime에서 소비되는 Markdown과 asset도 포함한다.
- **Owning module**: verification-affecting changed file을 실제 path로 포함하는 빌드 모듈(P가 선언한 모듈 단위. Gradle이면 Gradle module)이다. test 이름이나 다른 domain 용어가 아니라 파일 위치로 판정한다.
- **Direct-impact module**: 변경된 public/behavioral contract의 immediate consumer, Issue Verification Strategy가 지정한 영향 module, 또는 구체적 compile/test failure가 직접 영향을 증명한 module이다.
- **Stable final candidate**: 예정된 파일 변경과 이미 확인된 review finding의 필수 수정을 마쳐 더 수정할 계획이 없는 candidate다. 최종 CODE Review PASS는 검증 근거를 준비하는 선행 조건이 아니다. 검증·리뷰에서 추가 수정이 생기면 새 candidate로 갱신한다.
- **Required broad command set**: 이 문서의 grade/change-scope 기준과 Issue Verification Strategy가 요구하는 test/lint/build command 전체다. 특정 root 명령 하나로 고정하지 않으며 Issue의 명시적 요구가 우선한다.

구현 루프에서는 verification-affecting changed file의 owning module을 식별하고 직접 관련 test class 또는 owning-module test를 먼저 실행한다. 여러 module 또는 public/behavioral contract가 바뀌면 changed module과 근거가 있는 direct-impact module까지만 확장한다. transitive consumer 전체를 찾기 위한 repository-wide 추측은 하지 않으며 더 넓은 회귀 범위는 stable final candidate의 required broad command set이 담당한다. targeted failure는 전체 suite보다 실패 test 또는 owning module부터 수정·재실행한다. P가 선언한 계측·기기 테스트 경로는 Issue Verification Strategy나 repository command contract가 명시적으로 요구할 때만 기본 targeted 범위에 포함한다.

각 PASS는 실행한 command와 그 command가 검증한 candidate input 집합에 귀속된다. command가 소비하거나 assertion하는 verification-affecting input이 바뀌면 해당 PASS는 invalidated된다. rebase/base merge나 dependency/build input 변경도 command 결과에 영향을 주면 같은 규칙을 적용한다. Issue/PR comment, review discussion, PR 설명 또는 non-runtime documentation만 바뀌면 runtime 빌드 검증 PASS는 유지할 수 있지만, 그 입력을 사용하는 static validator나 Skill behavior eval은 다시 실행한다.

stable final candidate에서는 required broad command set의 각 command가 current candidate에서 실행된 PASS 또는 입력 불변 근거로 재사용 가능한 PASS를 가져야 한다. 최종 CODE Review/self-review는 이 근거를 확보한 뒤 수행하고, 종료 시 같은 후보에서 리뷰·검증 근거가 모두 유효한지 확인한다. broad verification 뒤 input이 바뀌면 affected targeted verification부터 수행하고, 새 stable final candidate에서 invalidated된 broad command를 다시 실행한 뒤 그 근거로 리뷰한다. 입력이 바뀌지 않은 command는 반복하지 않지만 `완료 시 한 번`을 다른 candidate의 stale PASS 재사용으로 해석하지 않는다.

P가 영향 분석 도구를 선언했으면 그 결과 참조·freshness·소비 조건은 [공통 영향 결과 참조와 로컬 소비](../skills/_shared/execution-packets.md#공통-영향-결과-참조와-로컬-소비) 및 P 적용 문서 `execution-routing.md`를 따르고, 그 결과는 위 검증 의무의 하한이다. 개발 중 부분 PASS와 이전 SHA의 리뷰를 현재 최종 후보의 완료 근거로 승계하지 않는다.

## 검증 환경

빌드·테스트 명령 전에 [build-preflight](../skills/_shared/build-preflight.md)를 적용한다. 환경변수가 비어 있다는 사실만으로 dependency 미설치를 판정하지 않는다. 기기·에뮬레이터 작업은 P 적용 문서 `build.md`에 선언된 절차만 따르며 선언이 없으면 수행하지 않는다. 선택적 기기 확인은 merge·complete의 근거 또는 blocker가 아니다.

required local 빌드 검증이면 다음을 확인한다. 원래 required가 아닌 non-runtime 문서·Skill·eval 변경에 이 절을 이유로 전체 빌드 gate를 추가하지 않는다.

1. preflight 뒤 intended process environment에서 빌드 도구의 version 명령(Gradle이면 `gradlew --version`)으로 실제 launcher/daemon JVM major version이 P의 `JDK major`와 같은지 확인한다. usable current Java/`JAVA_HOME`만으로 통과시키지 않는다.
2. 다르면 required command를 실행하거나 canonical PASS로 기록하지 않는다. 이미 설치되어 검증 가능한 선언 버전 JDK를 현재 process에만 주입하고 version 확인 후 같은 command를 실행한다. 자동 설치·다운로드·영속 환경 변경은 금지한다.
3. 선언과 다른 JVM에서 먼저 발생한 정적 분석/빌드 failure는 환경 failure로 구분하며 product/code regression으로 확정하지 않는다. 선언 버전 JDK에서 같은 required command를 재실행해 판정한다.
4. 선언 버전 JDK 또는 실제 빌드 JVM을 확인할 수 없으면 `BLOCKED: canonical build JDK unavailable`로 중단하고 미실행 command·근거를 기록한다. preflight가 `BLOCKED: JDK unavailable`이면 빌드 도구를 실행하지 않는다.
5. 같은 run에서 검증한 JDK와 도구 확인 결과는 후속 shell에 재주입해 재사용한다. 입력·환경 변경 근거가 없으면 탐색·version 확인을 반복하지 않는다.

실행하지 않은 required 검증은 `미검증`이며 PASS가 아니다. grade상 필요하지 않은 빌드 검증의 미실행은 blocker가 아니다. 실패 수정에 forbidden path가 필요하면 `BLOCKED`하고, 인계 전 changed-file list에 forbidden/unrelated path가 없는지 확인한다.
