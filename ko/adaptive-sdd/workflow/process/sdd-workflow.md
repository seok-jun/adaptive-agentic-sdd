# sdd-workflow 수행 절차

공통 SDD grade·일반 자동 격상은 아래 절이 원본이다. 프로젝트 적용 선언·제품 사실·구체 검증 명령·사람 권한은 P 적용 문서 `P/.adaptive-sdd/project/sdd-workflow.md`가 원본이다. W는 공통 분류와 수행법을 소유한다.

## SDD grade

Issue grade는 다음 다섯 값만 사용한다.

| grade | 판정 조건 |
| --- | --- |
| **Trivial** | runtime/contract/test expectation/build·dependency/schema·migration/CI·workflow 실행 의미를 바꾸지 않는 문서·문구·링크·주석·비동작 metadata 정리 |
| **Small** | Trivial이 아니며 한 구현 모듈 안에서 끝나고 아래 자동 격상 조건이 하나도 없는 변경 |
| **Medium** | 두 개 이상 구현 모듈 또는 프로젝트가 지정한 공유 contract가 바뀌지만 Large/Epic 조건은 없는 변경 |
| **Large** | 보안·개인정보·DB 마이그레이션·백그라운드 재시도/스케줄·비용/quota처럼 실패 영향이 큰 변경 |
| **Epic** | 새 모듈을 만들거나 모듈 의존성 방향을 바꾸거나 여러 독립 기능을 하위 Issue로 분해해야 하는 기능군 변경 |

Trivial은 **파일 수가 적다는 이유만으로 선택하지 않는다.** 다음 조건을 모두 만족해야 한다.

- 제품 runtime 동작과 사용자 관찰 결과가 바뀌지 않는다.
- public/internal contract, 테스트의 기대 동작, build/dependency, DB schema/migration이 바뀌지 않는다.
- CI, Skill, agent workflow의 실행 step·gate·stop condition 의미가 바뀌지 않는다.
- 보안·개인정보·비용·quota 정책의 의미가 바뀌지 않는다.

대표 예시는 오타/맞춤법 수정, 깨진 링크의 목적지 교정, 동작 의미를 바꾸지 않는 설명 문구·주석 정리, 현재 상태를 반영하는 비동작 metadata 갱신이다. 실행 코드·테스트·빌드 설정·workflow 실행 규칙을 바꾸거나 문서 변경 자체가 agent/product 동작을 바꾸면 최소 Small이다.

### 일반 자동 격상

여러 조건이 해당하면 가장 높은 grade를 적용한다. 프로젝트는 구체적인 모듈·기술·업무 경로를 아래 위험에 매핑하며 공통 최소 등급을 낮추지 않는다. 공유 contract 격상 대상은 프로젝트 매핑에서 지정한다. 단일 모듈의 다른 contract를 이름만으로 이 대상에 추가하지 않는다.

| 변경 행위 | 최소 grade |
| --- | --- |
| 두 개 이상 구현 모듈 또는 프로젝트가 지정한 공유 contract 변경 | Medium |
| 비밀정보·대화 원문·개인정보 저장·전송·로그 정책 변경 | Large |
| DB schema/migration 변경 | Large |
| 백그라운드 재시도·스케줄·중복 실행 방지 정책 변경 | Large |
| 과금 경로·비용 계산·quota/상한 변경 | Large |
| 모듈 신설 또는 의존성 방향 변경 | Epic |

자동 격상 기준보다 낮은 grade를 사용하려면 사용자의 명시적 예외 지시가 Issue 본문에 기록되어 있어야 한다. agent가 스스로 낮추지 않는다.

## 공통 계약과 프로젝트 적용

아래 공통 단계·리뷰·검증 계약의 원본은 W다. 프로젝트가 선언한 적용 등급/프로필·사람 권한·실제 경로와 최소 검증 명령을 함께 읽는다. 원본 이관만으로 프로젝트의 기존 gate를 늘리거나 줄이지 않는다. `P`는 현재 프로젝트, `W`는 검증한 방법론이며 이 문서의 프로젝트 경로는 P 적용 문서가 선언한 실제 경로에 대응한다. 일반 실행 순서와 형식은 아래 계약을 사용한다.

## 문서 역할

| 종류 | 위치 | 수명 | 역할 |
| --- | --- | --- | --- |
| business 문서 | `docs/domains/**` | 영속 | 구현 완료 후 유지되는 현재 제품 동작 |
| SDD 작업 문서 | `docs/sdd/{feature}/` | 작업 중 | AS-IS 근거, Human Decision Contract, Agent Execution Spec |
| 결정 기록 | `docs/reviews/**` | 영속 | 과거 의사결정의 근거와 대안 |
| 구조 문서 | `docs/architecture/**` | 영속 | 모듈 책임, 의존성, 작업 경계 |

위 위치는 기본값이며 실제 위치는 P 적용 문서의 `문서 역할` 표를 따른다. SDD 작업 문서는 완료 후 삭제한다. business 문서는 SDD 문서나 Issue를 복사하지 않고 **최종 코드 동작을 읽어서** 갱신한다.

## 구현 시작 조건

Trivial/Small/Medium Issue는 다음 조건을 모두 만족하면 구현을 시작할 수 있다.

- 현재 작업 지시가 해당 Issue 구현을 요청한다.
- 필수 본문 항목과 Priority/grade 라벨이 모두 존재하고 서로 일치한다.
- `status:blocked`가 없다.
- 다른 활성 lane의 `[CLAIM]` 또는 PR과 수정 허용 경로가 겹치지 않는다.
- 현재 lane이 `W/skills/parallel-development/SKILL.md`의 claim 절차를 완료했다.

조건 하나라도 충족하지 않으면 코드를 수정하지 않는다.

## grade별 산출물과 게이트

| grade | SDD 문서 | 구현 전 게이트 |
| --- | --- | --- |
| Trivial | 없음 | 범위가 Trivial 조건을 만족하는지 확인 후 진행 |
| Small | 없음 | 구현 시작 조건만 충족하면 진행 |
| Medium | 필요 | SDD 작성 후 구현까지 중간 승인 없이 진행 |
| Large | 필요 | AS-IS → required review → PLAN → required review → 구현. 사람 승인 단계 없음 |
| Epic | 필요 | 하위 작업 분해 → AS-IS → PLAN → 구현. 각 단계는 required review 통과 후 진행 |

### Trivial

별도 `docs/sdd/**` 디렉터리를 만들지 않는다. Issue 본문 또는 현재 사용자 지시가 작업 범위 역할을 하며, 대상 파일과 직접 검증 근거만 확인한다.

- repository-wide discovery를 하지 않는다.
- independent review는 요구하지 않는다.
- 변경 종류에 맞는 targeted validation과 최종 diff self-review는 생략하지 않는다.
- 빌드 도구 검증(P가 선언한 build/test 명령)은 변경이 그 결과에 영향을 주는 근거가 있을 때만 실행한다.
- 작업 중 Trivial 조건을 벗어나는 변경이 필요해지면 수정 전에 최소 Small로 재판정한다.

### Small

Issue 본문이 change plan 역할을 한다. 별도 `docs/sdd/**` 디렉터리를 만들지 않는다.

### Medium

`docs/sdd/{feature}/`를 작성한 뒤 구현을 계속한다. 별도의 중간 사용자 확인을 기다리지 않는다. 단, SDD를 작성하는 과정에서 Issue 목표·범위·경계가 서로 충돌하는 것을 발견하면 구현하지 않고 `BLOCKED`로 보고한다.

### Large

1. `01-as-is.md`를 작성한다.
2. independent review candidate가 준비되면 candidate를 commit하고 현재 Issue branch를 remote에 push한 뒤, 그 exact commit SHA가 remote branch history에서 resolve되고 해당 SHA의 `01-as-is.md` 원문을 remote에서 읽을 수 있는지 확인한다. local commit은 초안 작성 중 허용되지만 local-only SHA는 review/PASS target이 아니다.
3. 같은 exact candidate에 대해 Review A Contract Review와 Review B Blind Audit을 아래 이중 독립 리뷰 규칙에 따라 순서대로 완료한다.
4. 아래 이중 독립 리뷰의 다음 phase 진행 조건을 만족하면 사람 승인을 기다리지 않고 PLAN 작성으로 진행한다. unresolved Human Decision blocker가 있으면 P 적용 문서의 `사람 판단 지점`에 따라 멈춘다. 사실 정합성과 누락 감사는 Agent와 required independent review가 책임진다.
5. `02-to-be.md`와 `change-plans/**`를 작성한다.
6. PLAN independent review candidate도 commit/push하고 exact SHA의 `02-to-be.md`와 `change-plans/**`가 remote Issue branch에서 resolve되는지 확인한다.
7. 같은 exact candidate에 대해 Review A와 Review B를 다시 완료한다.
8. 같은 진행 조건을 만족하면 구현으로 진행한다. 각 phase의 Review A/B 근거가 최초 검토 또는 아래 current-target 재확인 chain으로 현재 exact SHA에 유효해야 한다.
9. 구현 뒤 기존 independent code review 1회와 필수 검증을 거쳐 PR을 준비한다. Large/Epic PR의 병합은 P 적용 문서의 `사람 판단 지점`에 따라 사람이 판단한다.

AS-IS/PLAN finding 반영으로 review-affecting candidate가 바뀌면 새 commit을 같은 Issue branch에 push하고 새 SHA를 review target으로 사용한다. 이전 SHA의 PASS를 새 revision의 PASS로 자동 승계하지 않는다. 검토 근거 재사용은 아래 의미·영향 판정과 current-target 재확인 chain을 따른다. current exact SHA에서 진행 조건을 만족하기 전에는 다음 phase로 진행하지 않는다. push 실패, remote branch에서 exact SHA가 확인되지 않음, remote 원문 조회 실패 중 하나라도 발생하면 local-only artifact로 계속하지 않고 상태를 반드시 `BLOCKED: SDD candidate remote push failed`로 기록해 중단한다. remote branch와 exact SHA만으로 publication은 충분하므로 이 단계에서 PR이나 draft PR을 만들지 않는다. 신규 lane의 fresh `origin/main` base와 기존 branch/worktree lifecycle도 바꾸지 않는다.

cross-environment handoff와 복구에는 최소 Issue 번호, `[CLAIM]`의 branch, remote branch, phase, reviewed artifact 경로, exact remote SHA를 남긴다. 다른 reviewer가 작성자의 local worktree path 없이 이 정보만으로 원문을 확인할 수 있어야 한다. Medium에 Review B를 추가하지 않지만 independent cross-environment SDD review를 명시적으로 수행하면 같은 remote-resolvable candidate 원칙을 재사용한다.

### Epic

Large 절차 전에 하위 Issue와 integration Issue를 먼저 정의한다. breakdown 산출물은 Large와 같은 remote-resolvable exact SHA publication 원칙으로 게시하고 아래 `Grade별 review gate`의 breakdown review(Review A + Human-selected Review B)를 받는다. 위 다음 phase 진행 조건을 만족하면 사람 승인을 기다리지 않고 하위 lane을 시작한다.

## Verification Strategy

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

Trivial은 항상 `Independent Review: NOT REQUIRED`다. Device QA / Runtime QA 판정이나 handoff를 canonical gate로 두지 않는다. P가 기기 관측 참고 문서를 선언했으면 비필수 참고 자료로 사용할 수 있지만 Verification Strategy, PR metadata, merge/complete 조건에는 포함하지 않는다.

## Grade별 review gate

Review A와 기본 code review의 입력은 phase-aware Contract Review Packet으로 제한한다. AS-IS에서는 아직 존재하지 않는 reviewed PLAN/diff/verification을 요구하지 않고 current Issue/acceptance, AS-IS artifact identity, remote base/head, 대상 inventory, 직접 contract/evidence와 author identity를 사용한다. PLAN에서는 current Issue/acceptance, reviewed upstream AS-IS identity, PLAN/change-plan identity, remote base/head, 대상 inventory, 직접 contract/evidence와 author identity를 사용한다. CODE에서는 reviewed PLAN identity, base/head, 전체 changed-file inventory, diff reference와 필요한 hunk/public contract, verification evidence identity, implementation actor identity를 사용한다. reviewer에게 solution discovery나 repository-wide 재탐색을 시키지 않는다.

independent review는 구현/문서 author와 다른 reviewer가 수행하고, PR review 또는 댓글에 `PASS` 또는 `BLOCKED`와 unresolved finding을 기록한다. Review A는 caller/callee, path/symbol, invariant와 phase contract 정합성을 확인하고, Review B는 위 이중 독립 리뷰의 최소 Blind Audit Packet으로 completeness를 감사한다. 사람 판단으로 이 책임을 대체하지 않는다. Review B는 필요한 reconciliation 완료와 unresolved Human Decision/Execution-contract blocker 0을 확인해야 통과하며 Implementation finding과 Non-blocking observation의 수를 0으로 만들 필요는 없다. independent review가 required가 아닌 grade에서는 Agent self-review와 automation이 해당 검증을 맡는다.

| grade | 구현 전 design review | PR code review |
| --- | --- | --- |
| Trivial | Trivial 조건과 대상 범위 self-review | targeted validation + diff ↔ 요청 범위 self-review |
| Small | Issue 경계와 검증 가능성 self-review | diff ↔ 완료 기준 self-review |
| Medium | SDD와 Verification Strategy bounded self-review. shared contract 또는 여러 모듈의 integration 근거가 필요한 경우 independent review를 `REQUIRED`로 판정 | `Independent Review: REQUIRED`이면 bounded independent review 통과 필요, 아니면 self-review |
| Large | AS-IS/PLAN 각각 Review A Contract Review + Human-selected Review B Blind Audit 필요 | 기존 bounded independent code review 1회; 명시적 high-risk escalation만 추가 audit 가능 |
| Epic | breakdown review와 AS-IS/PLAN 각각 Review A + Human-selected Review B 필요 | 하위 작업 및 integration diff의 기존 bounded independent code review; 명시적 high-risk escalation만 추가 audit 가능 |

required review가 미완료이거나 boundary 위반, 완료 기준 미충족, 명백한 안전성·정합성 문제가 unresolved이면 구현 또는 merge를 진행하지 않는다.

## business 문서 갱신

business 문서는 구현 완료 후 **현재 코드가 실제로 하는 동작**을 기록한다.

1. 변경된 심볼의 직접 사용자/배경 진입점을 찾는다.
2. 변경으로 실제 동작이 달라진 규칙만 수정한다.
3. 변경하지 않은 규칙을 재작성하지 않는다.
4. Issue, commit message, SDD 문장을 그대로 옮기지 않는다.
5. code와 기존 business 문서가 다르면 `W/process/agent-instruction-policy.md`의 drift 규칙을 적용한다.

한 줄 규칙이 조건·예외·재시도를 모두 담아 150자를 넘으면 상세 주제 문서로 분리하고 business 인덱스에는 ID, 한 줄 요약, 링크만 둔다.

## Issue 본문 규약

신규 구현/버그 Issue의 필수 section과 canonical 본문 형식은 고정 W의 `process/issue-priority.md`의 `## 신규 Issue 필수 본문`이 Source of Truth다. 제품별 적용 조건은 `P/.adaptive-sdd/project/issue-priority.md`를 읽는다. 이 문서는 같은 template을 복제하지 않는다.

본문 값과 `priority:*`, `grade:*` 라벨은 항상 일치해야 한다.

Issue 댓글은 `[CLAIM]`, `[RELEASE]`, 변경 이력을 기록할 수 있지만 **현재 목표·범위·경계·완료 기준을 댓글로만 변경하지 않는다.** 변경이 확정되면 본문도 같은 내용으로 갱신한다.

Large(이를 따르는 Epic 포함)의 일반 댓글은 Agent ↔ Agent 작업 소통이다. AS-IS 근거, 리뷰 반론, path/symbol, 구현 발견, test/verification, handoff를 공유하며 Human의 상시 확인을 요구하지 않는다. Agent끼리의 합의는 Human Decision이 아니며 확정된 Decision을 암묵적으로 추가·변경하지 못한다.

- `[HUMAN DECISION REQUIRED]`: 작업 지시·확정된 설계 범위를 벗어나는 새 중요한 제품/설계 Decision이 필요할 때만 사용한다. 영향을 받는 작업을 STOP하고, 해당 Decision·실제 대안·trade-off를 Human View(Medium 이상은 `02-to-be.md`, Trivial/Small은 Issue)에 반영한 뒤 Human 결정 후 재개한다. Issue의 목표·범위·경계·완료 기준도 바뀌면 본문을 함께 갱신한다.
- `[IMPLEMENTATION SUMMARY]`: 구현 종료 시 댓글 하나에 확정 Decision 준수 여부, execution deviation, Human escalation 발생 여부, verification 결과, 남은 위험만 짧게 기록한다. 추가 Human 승인 gate가 아니다.

위 `### 일반 자동 격상` 및 P 적용 문서의 `### 자동 격상`의 모든 변경 카테고리는 반드시 Human Decision에 노출한다. 제품 동작 의미, acceptance 해석, 상위 contract가 바뀌거나 의미가 다른 합리적 경쟁 대안이 발견된 경우도 포함한다. **Decision 노출 의무와 추가 Human 결정 필요 여부는 별개다.** Medium은 Issue 목표·범위·경계 안의 결정을 SDD에 명시하고 기존 gate에 따라 진행하며, 노출 카테고리라는 이유만으로 `[HUMAN DECISION REQUIRED]`를 요구하지 않는다. Escalation은 위의 작업 지시·확정된 설계 범위를 벗어나는 새 중요한 결정에 적용한다. 이미 Issue/설계가 결정한 사항에는 결정을 다시 요구하지 않는다. 확정된 제품 의미·불변조건을 바꾸지 않는 구현 세부는 Agent 재량으로 계속한다.

위 두 댓글과 일반 소통의 역할만 구분한다. 기존 claim/release/token marker와 grade별 gate는 유지하며 `[EVIDENCE]`, `[REVIEW]`, `[RESOLVED]` 같은 추가 댓글 taxonomy, 새 문서나 승인 단계를 만들지 않는다. 기존 문서의 내용을 이관해 Human 필수 읽기와 중복을 줄이고 Agent 간 작업 소통량은 인위적으로 제한하지 않는다. Medium의 추가 승인 없는 SDD 진행과 Trivial/Small의 별도 SDD 생략도 유지한다.

## Legacy Issue 정규화

기존 Issue에 아래 항목 중 하나라도 없으면 코드 수정 전에 Issue를 정규화한다.

- Priority 본문 값과 `priority:*` 라벨
- SDD grade 본문 값과 `grade:*` 라벨
- 사용자 영향
- 목표
- 작업 범위
- 작업 경계의 `수정 허용` / `수정 금지`
- 완료 기준
- 의존성 / 차단 요소

정규화 단계에서는 제품 코드를 수정하지 않는다. 기존 Issue의 목표와 현재 architecture 문서를 기준으로 최소 경계를 작성하고, shared 경로가 필요하면 integration 작업으로 표시한다.

### Large/Epic 설계 이중 독립 리뷰

Large/Epic의 AS-IS와 PLAN 최초 candidate에는 서로 다른 별도 agent/session의 두 review를 순서대로 적용한다. 이후 revision은 아래 의미·영향 판정과 재확인 chain을 적용한다. Review A는 author와 분리되고 Review B는 author 및 Review A actor/session과 모두 분리된다. Trivial/Small/Medium, 기본 IMPLEMENT/CODE review에는 Review B를 추가하지 않는다.

- **Review A — Contract Review**: current Issue/acceptance, phase artifact identity, reviewed upstream contract, 직접 caller/callee·invariant·allowed/forbidden, source/diff/verification evidence를 bounded하게 확인해 사실·계약·Agent Execution Spec의 correctness와 consistency를 판정한다.
- **Review B — Blind Audit**: 빠진 현재 상태 사실, 숨은 가정, scope/ownership boundary를 바꾸는 omission, 상위 contract 충돌, PLAN 방향을 뒤집을 수 있는 blocking risk를 찾는다. solution discovery, repository-wide redesign 또는 Review A의 반복 검증으로 확장하지 않는다.

Review B finding은 다음 네 severity 중 하나로 분류한다.

1. **Human Decision blocker**: 확정된 상위 contract/Decision과 충돌하거나 제품 의미, ownership, failure behavior, acceptance 해석이 달라지는 합리적 경쟁 선택지가 남거나 기존 Human Decision scope 변경 또는 새 중요한 제품/설계 Decision이 필요하다. 기존 `[HUMAN DECISION REQUIRED]`만 사용하며 새 결정 taxonomy를 만들지 않는다.
2. **Execution-contract blocker**: Human 제품 판단은 필요하지 않지만 합리적 기술 선택지가 둘 이상이고 그 선택에 따라 public/internal contract, persistence lineage, eligibility, schema mapping, recovery convergence 또는 scope 의미가 달라져 구현자가 임의로 review되지 않은 동작 의미를 고정하게 된다. 해결할 때 `02-to-be.md`의 Human Decision을 불필요하게 늘리지 않고 적절한 `change-plans/**` execution contract와 fixture expectation에 한 방향을 고정한다.
3. **Implementation finding**: 확정된 Decision/contract/scope를 바꾸지 않고 정답이 사실상 하나인 직접 caller 누락, fence 적용 누락, race fixture 부족, mechanical safety bug다. 다음 phase 진행을 차단하지 않으며 finding 기록만을 위한 artifact revision을 강제하지 않는다. Result/Review Packet 또는 동등한 IMPLEMENT handoff에 보존하고 CODE/finishing에서 코드와 fixture 해결을 모두 확인한다.
4. **Non-blocking observation**: 향후 최적화, 선호, 추가 방어 또는 현재 acceptance와 무관한 개선이다. PLAN/IMPLEMENT 완료 gate로 승격하지 않는다.

Review B가 `Human Decision blocker` 또는 `Execution-contract blocker`를 보고할 때는 각 finding에 다음 qualification을 모두 남긴다.

- 어느 blocker severity인지
- 현재 artifact, 확정된 상위 contract 또는 direct boundary 중 깨지는 invariant
- 다음 phase 전에 해결하지 않으면 구현자에게 남는 의미 선택 또는 충돌하는 결정 의미

이 qualification이 없고 코드와 fixture에서 contract-preserving 정답 하나로 수렴하면 `Implementation finding`으로 분류한다. reviewer가 `blocking`이라고 선언한 사실만으로 PLAN blocker가 되지 않는다.

Review A의 blocking finding은 보정 후 A re-check한다. A가 통과한 뒤 Review B reviewer의 model과 reasoning level을 Human이 선택한다. 선택 전에는 Agent가 임의 배정하지 않고 `BLOCKED: blind-audit reviewer selection required`로 중단한다. 선택된 reviewer는 canonical `REVIEW` floor와 role qualification을 만족하고 현재 host에서 사용할 수 있어야 한다. 사용할 수 없거나 부적격이면 다른 reviewer로 자동 fallback하지 않고 `BLOCKED: selected blind-audit reviewer unavailable`로 중단해 Human 재선택을 요청한다. Human 선택은 `review-mode = blind-audit`, 별도 agent/session, capability floor를 완화하지 않는다.

Review B 최초 판정 전에는 Review A의 PASS/BLOCKED verdict, finding 목록, 상세 packet과 이전 Review B finding detail을 제공하지 않는다. Review B 입력은 Issue id/title, `AS-IS | PLAN`, target artifact와 remote-resolvable exact SHA, 상위 목표/직접 소유 경계, 전면 재설계 금지, omission·hidden assumption·boundary-changing blocking risk 탐색 요청으로 제한한다. reviewer는 target artifact에서 직접 인접한 caller/consumer/contract를 확인할 수 있다.

최초 verdict가 고정된 뒤에만 같은 Review B reviewer에게 이전 Review B finding identity와 resolution expectation ledger를 제공한다. reviewer는 이전 finding마다 현재 remote-resolvable exact candidate의 직접 근거로 `resolved / unresolved / regressed / not-applicable` 중 하나를 판정한다. reconciliation은 이전 finding을 자동 PASS로 만드는 절차가 아니며, 최초 verdict의 신규 finding 목록과 이전 finding reconciliation을 분리한다. 이전 B finding이 없으면 reconciliation은 해당 없음으로 명시한다.

unresolved Human Decision blocker 또는 unresolved Execution-contract blocker가 하나라도 있으면 다음 phase를 중단한다. candidate SHA 변경은 변경분 확인의 trigger이며 전체 검토 무효화 판정 자체가 아니다. 아래 영향 판정으로 current exact candidate의 검토 근거를 구성한다. 이전 SHA PASS의 이름만 바꿔 승계하거나 review 횟수로 강제 PASS하지 않는다.

Large/Epic AS-IS·PLAN의 다음 phase 진행 조건은 다음과 같다.

```text
Review A: PASS
Review B: initial blind audit completed; current-target impact/reconfirmation chain valid
Review B reconciliation: prior findings confirmed at current target when present
unresolved Human Decision blocker: 0
unresolved Execution-contract blocker: 0
```

이 조건을 만족하면 Implementation finding 또는 Non-blocking observation이 남아 있어도 Review B PASS로 다음 phase에 진행할 수 있다. 단, Implementation finding은 IMPLEMENT handoff에서 누락할 수 없고 CODE/finishing에서 코드와 fixture 해결이 확인되지 않으면 완료할 수 없다.

IMPLEMENT/CODE는 기존 independent code review 1회를 유지한다. destructive migration, cross-DB atomicity, recovery처럼 명시적인 고위험 escalation 근거가 있을 때만 별도 code audit을 추가할 수 있으며 이를 Large/Epic의 기본 이중 review로 만들지 않는다.

### 의미·영향에 따른 설계 재검토

최초 A와 독립·blind B는 생략하지 않는다. 후속 변경은 기존 Review Packet에 이전/현재 remote target, 전체 변경 inventory와 diff, 수정 finding identity, 영향받는 contract·완료 기준·직접 소비자, 영향 없음의 근거, current-target 재확인 결과를 연결한다. reviewer는 inventory를 독립 확인하고 필요한 주변 근거를 열 수 있어야 한다. 누락 파일이나 근거 접근 실패를 작은 변경으로 추정하지 않고 보완 전 차단한다.

| 확인된 변경 | 필요한 후속 검토 |
| --- | --- |
| 검토 결과 기록만 변경, 대상 artifact bytes 불변 | 새 기록과 대상 분리·identity를 확인. 대상의 기존 검토는 유지하고 결과 기록 변경으로 새 A/B를 자동 생성하지 않음 |
| 표현·설명 보완, 의미 불변이 직접 근거로 확인됨 | A가 변경분·finding·직접 영향을 current target에서 재확인. 기존 B 근거의 적용 가능성과 prior finding 상태도 확인 |
| 국소 실행 계약 보정, 핵심 Decision·상위 계약·경계·감사 전제 불변 | A의 관련 계약·소비자 재확인과 B의 관련 finding·직접 영향 후속 재확인. invalidated 판단만 갱신 |
| 핵심 Decision·상위 계약·작업 경계·복구/실패 의미·감사 전제 변경 | 무효화된 phase의 관련 설계 전반을 A로 검토한 뒤 새 독립 Blind Audit B. upstream AS-IS가 무효화되면 AS-IS부터 재검토 |
| 영향 불명확 | 의미 변경 가능 범위로 보수적으로 확장. 근거 확보 전 PASS 금지; 전제 불변을 증명하지 못하면 새 A/B 경로 |

한 줄 수정도 실행 의미로 판정한다. author의 `설명만 변경` 선언이나 diff 크기는 근거가 아니다. 검토 대상 artifact와 결과 기록은 분리한다. 결과는 기존 Review/Result Packet 또는 Issue 댓글에 두며 결과를 적으려고 대상 본문을 매번 수정하지 않는다. artifact에 결과를 함께 쓴 경우 실제 diff로 의미 불변을 증명해야 한다.

후속 재확인은 이전 finding을 받을 수 있지만 `최초 Blind Audit`이라고 기록하지 않는다. 새 Blind Audit이 필요한 경우 기존 Human의 model/reasoning 선택이 여전히 유효하고 available/qualified이면 재사용할 수 있으나 author/A와 분리된 새 session을 사용하고, 최초 verdict 전에 A 결과·이전 B detail을 숨긴다. verdict 뒤 prior ledger reconciliation을 수행한다. 국소 재확인도 reviewer 독립성을 유지하며 current target 근거 없이 이전 PASS를 복사하지 않는다.

다음 phase 진행 근거에는 최초 blind verdict의 불변 참조, 이후 target 차이/영향 판정과 A/B 재확인 chain, current-target prior finding 상태를 연결한다. 새 blind 조건이 발생하면 chain은 새 최초 verdict에서 다시 시작한다. 이 chain은 review evidence의 재사용만 허용한다.

기록/head-only 변경은 먼저 기존 검토 target 유지 가능성을 확인한다. 전체 변경 inventory를 바탕으로 해당 phase artifact inventory·bytes, Decision scope·upstream 및 검토한 직접 계약/소비자·감사 전제가 불변임을 확인하면 기존 target과 검토 근거를 유지한다. branch head를 검토 target으로 매번 치환하지 않는다. 계약/소비자 의미 변화는 artifact bytes가 같아도 기록-only로 분류하지 않는다.

A finding 보정이 끝나고 A PASS가 고정된 candidate에서만 B를 dispatch한다. A 수정과 B 검토를 겹쳐 stale B 결과를 만드는 일을 피한다. 국소 수정의 A/B는 invalidated 판단·finding·직접 영향을 독립 재확인한다. 새 target의 검토 결과는 그 재확인의 직접 근거이며 최초 blind로 오기하거나 과거 PASS의 target만 바꾸지 않는다.

### 반복 정체 시 전환

같은 phase·contract/Decision 영역에서 같은 finding 또는 같은 의미 충돌이 **수정 → 재확인 뒤 2회 연속** unresolved/regressed이면 다음 자동 리뷰를 시작하지 않는다. finding 이름이나 SHA만 바꿔 같은 충돌의 streak를 초기화하지 않는다. 단순 총 리뷰 수, 무관한 신규 결함 발견은 정체로 세지 않으며 그 영역의 해결을 직접 증명하면 streak를 종료한다.

기존 Review Packet에 영역, 안정된 finding/충돌 identity, 각 수정·재확인 target과 근거, 해결되지 않은 원인을 남긴다. 범위 분리(소유 Issue와 완료 기준 포함), 불명확한 계약에 대한 Human 결정, 추가 근거 확보, 이유와 달라진 검토 범위가 명시된 재검토 중 선택지를 보고한다. 필요한 Human 결정 또는 새로운 근거에 따른 명시적 재검토 사유가 확보된 뒤에만 재개한다. 새 SHA나 시간 경과만으로 자동 재개하지 않는다. 임계값은 검토 면제·강제 PASS가 아니며 blocker는 해결 또는 사람이 정한 범위 결정까지 유지한다.

## SDD 작업 문서 구조

Medium 이상에서 다음 구조를 사용한다. 새로 시작하는 SDD 작업부터 적용하며, 이미 진행 중인 작업과 종료된 작업에는 소급 적용하지 않는다. 이 규칙만으로 기존 설계를 재작성하지 않는다.

```text
docs/sdd/{feature}/
  README.md
  01-as-is.md
  02-to-be.md
  change-plans/{ID}.md
```

필요한 경우에만 `backlog/{ID}.md`를 추가한다. `{feature}`는 kebab-case, `{ID}`는 Issue 안에서 중복되지 않는 대문자 prefix + 번호를 사용한다.

각 문서의 필수 내용은 다음과 같다.

사람용 현황·계획에는 [사람용 문서의 시각적 작성](agent-instruction-policy.md#사람용-문서의-시각적-작성)을 적용한다. 현재 모습과 변화·선택을 먼저 보여주고 Agent 실행 세부는 분리한다. 한 문장으로 충분한 변경은 그 문장으로 설명하며 그림 개수를 채우지 않는다. 표현 선택에 예시가 필요하면 [작성 예시](visual-writing-examples.md)만 참고한다. 이 연결은 문서 구조·승인 권한·review 회차를 바꾸거나 전체 가이드의 선행 로딩을 요구하지 않는다.

### `README.md`

- Issue 번호
- Priority
- grade
- 수정 허용/금지 경로
- 연결된 business/architecture 문서

### `01-as-is.md`

- 문제 정의·원인 모델·범위/경계와 설계에 영향을 주는 핵심 사실·위험을 먼저 짧게 제시
- 현황 이해에 필요한 소유·연결·흐름·상태는 관계도나 작은 표로 먼저 보여주고 사실·가설·미조사를 구별. 단순 변경은 한 문장 허용
- 현재 동작과 확인하지 못한 사실을 구분한 Agent evidence
- 확인한 코드 경로와 심볼
- 재현 또는 검증 근거
- 문서와 코드가 다르면 drift 항목

작성 순서는 문제 → 현재 관계·동작 → 사실/가설/미조사 → 직접 근거로 잡는다. 구체적인 표현이 필요할 때만 W의 [AS-IS 합성 예시](visual-writing-examples.md#sdd-as-is)를 참고한다. 예시의 가상 사실을 실제 제품 근거로 사용하지 않는다.

### `02-to-be.md`

Human Decision Contract다. Issue의 목표·경계와 상위 contract 안에서 제품·설계 결정의 기준이 되며, 이들을 독자적으로 변경하지 않는다.

- 현재 문제와 AS-IS → TO-BE 동작 변화. 정책·선택지는 비교표, 소유·경계는 관계도/경계 표, 흐름·상태는 다이어그램/상태표 등 이해에 필요한 표현을 먼저 둔다. 단순 변경은 한 문장 허용
- 변경하지 않을 동작, 실패/오류 시 동작, 명시적인 데이터/상태 정의
- Decision별 `D-xxx`, 선택, 선택 이유, 실제 대안과 trade-off, 주요 비용/위험, 채택하면 생기는 의미
- Acceptance Criteria별 Verification Strategy. 실행 세부는 해당 change-plan을 참조한다.

클래스/메서드/line evidence는 최소화한다. 중요한 제품·설계 결정을 Agent spec에만 숨기지 않는다. Human-facing Decision이 짧은 리뷰 세션에서 이해하기 어려울 만큼 많으면 issue/plan 분리를 검토하되 고정 개수 상한이나 추가 taxonomy는 만들지 않는다.

작성 순서는 변화 → 선택과 이유·비용 → 유지할 경계와 실패·미결 → 완료 기준과 확인 방법으로 잡는다. 필요한 경우만 [TO-BE 합성 예시](visual-writing-examples.md#sdd-to-be)를 참고한다. 위 현황·계획 예시의 전체 선행 로딩이나 새 산출물은 요구하지 않으며, 실행 세부는 기존 change-plan의 해당 절로 연결한다.

### `change-plans/{ID}.md`

Agent Execution Spec이다. Human Decision의 rationale을 다시 서술하지 않고 적용하는 `D-xxx`를 참조한다. `02-to-be.md`와 경쟁하는 설계 권위를 만들지 않는다.

- target file/symbol과 직접 caller/callee, 필요한 코드 근거
- 변경 내용·구현 순서·보존할 invariant, 해당하는 schema/migration
- test case·검증 명령·실행 evidence
- 롤백 또는 실패 시 확인 지점

`관련 파일`, `필요한 부분`, `적절한 처리`처럼 정확한 대상을 특정하지 않는 문장을 change plan에 쓰지 않는다.

### 검증 시퀀싱과 PASS 유효성

다음 용어는 grade별 최소 검증과 Issue별 Verification Strategy를 실행하는 공통 기준이다.

- **Verification-affecting input**: production/test source, resource, manifest, runtime asset, build/dependency/configuration, schema/migration/contract, fixture/snapshot/generated input/test expectation처럼 검증 command가 소비하거나 assertion하는 입력이다. 확장자나 `docs` 경로만으로 판정하지 않으며 runtime에서 소비되는 Markdown과 asset도 포함한다.
- **Owning module**: verification-affecting changed file을 실제 path로 포함하는 빌드 모듈(P가 선언한 모듈 단위. Gradle이면 Gradle module)이다. test 이름이나 다른 domain 용어가 아니라 파일 위치로 판정한다.
- **Direct-impact module**: 변경된 public/behavioral contract의 immediate consumer, Issue Verification Strategy가 지정한 영향 module, 또는 구체적 compile/test failure가 직접 영향을 증명한 module이다.
- **Stable final candidate**: current diff와 required review finding이 안정화되어 required broad verification 뒤 verification-affecting input을 더 수정할 계획이 없는 candidate다.
- **Required broad command set**: 이 문서의 grade/change-scope 기준과 Issue Verification Strategy가 요구하는 test/lint/build command 전체다. 특정 root 명령 하나로 고정하지 않으며 Issue의 명시적 요구가 우선한다.

구현 루프에서는 verification-affecting changed file의 owning module을 식별하고 직접 관련 test class 또는 owning-module test를 먼저 실행한다. 여러 module 또는 public/behavioral contract가 바뀌면 changed module과 근거가 있는 direct-impact module까지만 확장한다. transitive consumer 전체를 찾기 위한 repository-wide 추측은 하지 않으며 더 넓은 회귀 범위는 stable final candidate의 required broad command set이 담당한다. targeted failure는 전체 suite보다 실패 test 또는 owning module부터 수정·재실행한다. P가 선언한 계측·기기 테스트 경로는 Issue Verification Strategy나 repository command contract가 명시적으로 요구할 때만 기본 targeted 범위에 포함한다.

각 PASS는 실행한 command와 그 command가 검증한 candidate input 집합에 귀속된다. command가 소비하거나 assertion하는 verification-affecting input이 바뀌면 해당 PASS는 invalidated된다. rebase/base merge나 dependency/build input 변경도 command 결과에 영향을 주면 같은 규칙을 적용한다. Issue/PR comment, review discussion, PR 설명 또는 non-runtime documentation만 바뀌면 runtime 빌드 검증 PASS는 유지할 수 있지만, 그 입력을 사용하는 static validator나 Skill behavior eval은 다시 실행한다.

stable final candidate에서는 required broad command set의 각 command가 current candidate에서 실행된 PASS 또는 입력 불변 근거로 재사용 가능한 PASS를 가져야 한다. broad verification 뒤 input이 바뀌면 affected targeted verification부터 수행하고, 새 stable final candidate에서 invalidated된 broad command를 다시 실행한다. 입력이 바뀌지 않은 command는 반복하지 않지만 `완료 시 한 번`을 다른 candidate의 stale PASS 재사용으로 해석하지 않는다.

P가 영향 분석 도구를 선언했으면 그 결과 참조·freshness·소비 조건은 P 적용 문서 `execution-routing.md`를 따르고, 그 결과는 위 검증 의무의 하한이다. 개발 중 부분 PASS와 이전 SHA의 리뷰를 현재 최종 후보의 완료 근거로 승계하지 않는다.

### Bounded trade-off capture

Issue, current main AS-IS, direct dependency를 확인하는 과정에서 실제 경쟁 선택지가 둘 이상 드러난 경우에만 선택, 대안, 선택 이유, 감수 비용을 짧게 기록한다. Medium 이상에서 중요한 제품·설계 trade-off는 `02-to-be.md`의 Decision에 두고 change-plan은 그 ID를 참조한다. Trivial/Small은 Issue를 사용하며 별도 trade-off 문서를 만들지 않는다.

경쟁 선택지를 찾기 위한 repository-wide 탐색이나 별도 brainstorming은 하지 않는다. 재검토 조건도 이미 명확한 trigger가 있을 때만 기록한다.

## 실행 routing과 packet

grade는 orchestration shape를 결정하고 phase risk/decision complexity는 model/reasoning tier를 결정한다. 상세 schema와 fallback 순서는 `W/skills/_shared/execution-routing.md`가 canonical owner다. 이 shared 문서는 관련 routing/packet phase에서만 읽고 fixed pre-read 입력에 추가하지 않는다.

- Trivial/Small은 current agent 한 명이 model switch/delegation 없이 끝낸다. current concrete model이 role DENIED이면 actor 수를 늘리지 않고 qualified replacement 한 명으로 교체한다.
- Medium은 단일 agent가 기본이며 unresolved PLAN decision 또는 required independent review phase만 bounded delegation한다.
- Large는 root/orchestrator가 검토를 통과한 설계와 경계를 소유하고 `PLAN / IMPLEMENT / REVIEW` coarse-grained phase routing을 사용할 수 있다.
- Epic은 breakdown/shared contract/dependency graph를 root가 소유하고 구현을 child Issue execution으로 넘긴다.

Issue body의 optional `## Execution Profile`은 phase별 host-neutral model/reasoning tier, optional concrete model, explicit fallback, escalation 조건을 제공한다. Profile이 없어도 current/manual execution model/reasoning으로 기존 workflow를 계속할 수 있으며, current/manual eligibility는 shared routing contract의 capability + deny/explicit-record 규칙으로 판정한다. Profile은 hard guard, grade/SDD gate, claim, allowed/forbidden, verification, required review, canonical safety deny를 완화하지 않는다. Profile 때문에 model switch/delegation이 생기면 해당 automatic candidate의 fresh role qualification PASS가 필요하다.

Host Capability Map의 concrete mapping은 runtime/adapter가 소유한다. `current`는 capability rank가 아니며 mapping 또는 fresh current-model capability evidence로 phase floor 충족을 별도로 증명해야 한다. canonical DENY가 아니고 governing explicit qualification record가 없는 current/manual model은 fresh capability가 floor를 충족하면 positive registry record 부재만으로 차단하지 않는다. native delegation이 없어도 capable current agent는 IMPLEMENT를 직접 수행할 수 있지만 required reviewer는 구현 주체와 분리된 agent/session이어야 한다. Medium/Large/Epic에서 별도 reviewer/session capability 자체를 제공할 수 없으면 `BLOCKED: separate reviewer unavailable`이다. future reviewer의 concrete model qualification은 PLAN 시작 조건이 아니며 실제 review actor 선택 직전에 검증한다. 지원 capability를 증명할 수 없으면 model을 추정하거나 floor 아래로 downgrade하지 않고 `BLOCKED: routing capability unavailable`로 중단한다.

Model Role Qualification은 tier capability와 별도지만 **모든 운영 모델의 universal positive allowlist는 아니다.** P 적용 문서 `execution-routing.md`가 선언한 safety deny 모델과 explicit qualification record는 항상 강제한다. explicit record가 `DENIED`면 current/manual route도 우회할 수 없고, 존재하는 positive record가 누락·불완전·stale이면 PASS로 추정하거나 무시하지 않는다. 반대로 explicit record가 없는 current/manual model은 fresh Host Capability evidence가 현재 phase floor를 충족하면 positive PASS 링크 부재만으로 `BLOCKED: model role unqualified`가 되지 않는다. Agent가 model switch, delegated worker, reviewer, fallback concrete model을 자동 선택할 때는 해당 role의 fresh immutable PASS evidence가 필요하다. future phase 후보는 실제 선택 시점에 just-in-time 검증한다.

차단 model은 사용자가 명시적으로 지시한 별도 qualification probe Issue에서 synthetic/docs-only fixture, orchestrator-owned claim/isolation/lifecycle, bounded probe role, main 직접 push와 Issue/PR/merge/release 권한 금지, raw observation 보존 조건을 모두 만족할 때만 제한적으로 호출한다. 이 예외는 일반 개발 역할의 PASS가 아니다.

Execution Packet은 상위 Source of Truth를 대체하지 않는 derived cache다. Issue/PLAN/direct contract/canonical guard·process와 SDD gate/claim의 immutable identity와 freshness가 있어야 한다. guard 재사용은 host-enforced propagation 또는 worker direct-read의 immutable evidence object로 증명하며 boolean 자기신고는 인정하지 않는다. 필수 nested value는 nonempty여야 한다. 충돌 또는 version 변화가 있으면 관련 항목만 `STALE`로 두고 bounded refresh하거나 증명 불가 시 중단한다.

Result Packet은 base/head SHA, nonempty changed files/criterion outcomes/verification items, current head의 전체 changed-file inventory 또는 immutable reference, current diff reference, commit-bound verification evidence identity, 명시적 scope/unresolved/escalation/dependency/freshness 상태를 포함한다. command, exit code, outcome만으로 검증 PASS를 인정하지 않는다. Result head, diff, inventory, verification commit/evidence identity가 current head와 다르면 해당 근거는 `STALE`이다.

required review packet은 phase와 mode를 명시한다. Contract Review Packet은 해당 phase에 실제로 존재하는 artifact/evidence만 요구하고, CODE reviewer는 current head의 전체 changed-file inventory를 독립 확인한 뒤 bounded diff/contracts와 PLAN implementation finding handoff의 코드+fixture 해결을 검토한다. Blind Audit 최초 Packet은 Review A verdict/finding/detail과 이전 B finding detail을 제외한 최소 입력만 전달하고, 최초 verdict가 고정된 뒤에만 prior-finding ledger를 별도 reconciliation 입력으로 전달한다. 상세 schema와 Human-selected reviewer 처리 규칙은 `W/skills/_shared/execution-routing.md`를 따른다.

### PLAN 확정 뒤 구현 문맥 인계

Large/Epic의 검토를 통과한 PLAN에서 IMPLEMENT로 전환할 때 기존 Execution Packet을 사용한다. 확정 결정과 핵심 이유, 직접 계약, 실패·복구 조건, 남은 implementation finding, 검증 의무와 claim/guard provenance를 연결한다. 설계 대화, 이전 문서 여러 버전, 전체 도구 로그를 기본 입력으로 상속하지 않는다. 필요한 원문은 경로·구간·불변 참조로 읽는다.

host가 지원하면 같은 모델이라도 별도 구현 문맥을 선택한다. 실제 fresh session/agent 또는 검증된 압축을 사용하고 grade별 actor 수와 기존 model qualification 정책은 유지한다. 전환 미지원·압축 검증 실패 시 기존 직접 구현 fallback에 사유, 최소 입력 참조, 실제 남은 문맥의 한계를 기록한다. shell에서 대화 명령을 실행하거나 전환을 선언한 것만으로 성공 처리하지 않는다. 압축 실패 후 필수 source를 복구할 수 없으면 구현 진입을 차단한다.

수신자는 첫 edit 전에 current Issue/PLAN, 검토한 exact artifact·Decision scope, claim 충돌, guard와 직접 contract의 최신성을 확인한다. 누락/stale packet은 필요한 source만 bounded refresh하고 유효성을 증명할 때까지 edit하지 않는다. 메인에는 Result Packet과 필요한 변경·검증 근거만 반환한다. 이미 구현 중인 작업의 session/branch를 이 규칙 때문에 소급 초기화하지 않는다.

## 차세대 방법론의 적용과 개선 관측

이 프로젝트의 신규 작업은 기존 claim·grade gate 뒤 고정 공통 묶음을 읽고 적용한다. 프로젝트의 승인·쓰기 경계·검증·완료 조건이 우선한다. 연결 파일 유무나 문서 읽기만으로 실행·수집 완료를 선언하지 않는다.


수동 관측 재검토는 사람이 요청할 때만 수행한다. 이 preview에는 재검토 스킬이 아직 없으므로 M의 `adaptation.md` `관측을 다음 판단에 사용하기`를 따른다. 개선 후보는 후보마다 소유 위치와 정확한 내용을 제시하고 사람 확인을 받은 뒤에만 생성·재조회한다. 확인 전 생성은 0회이며, 분석 전용 지시는 쓰기를 금지한다. 기존 원본 보정·후보 자동 구현 권한을 주지 않는다.

같은 run에서 이미 읽은 동일 버전은 재사용한다. 로컬 절대 경로·특정 CLI 설치·별도 설정 파일을 필수로 만들지 않는다. 원본 조회 실패나 pin 불일치는 `적용 미확인`과 이유를 남기며 임의 최신 버전으로 대체하지 않는다. 기존 제품 절차로 가능한 작업은 계속하되 미확인을 적용 성공으로 계산하지 않는다. 진행 작업의 버전은 묵시적으로 바꾸지 않으며 중간 도입은 이후 구간만 부분 적용으로 남긴다.

수집 책임은 현재 작업 Agent, 기준 보존 원본은 이 프로젝트의 Issue 댓글이며 PR의 근거를 그 Issue에서 연결한다. 별도 파일/중앙 장부/전체 세션 수집기를 만들지 않는다. 아래 내용을 기존 시작·인계·`[IMPLEMENTATION SUMMARY]` 기록에 짧게 붙인다. 작업별 시작 원본 한 곳에 고정 정보를 남기고 인계·종료에는 그 URL을 직접 참조해 같은 버전·문서·지원의 본문 복사를 생략할 수 있다. 적용 정보가 바뀌면 변경 시점·새 값·구간을 명시하고 앞 구간을 소급 갱신하지 않는다. 관측하지 못한 항목은 같은 이유·범위로 한 줄에 묶을 수 있으며 전수 조사를 요구하지 않는다. 비용 tracker 유무와 무관하게 실행한다.

| 시점 | 소비와 기록 |
| --- | --- |
| 실제 변경 전 | Issue/run, 고정 revision·pin·읽은 문서와 조회 근거, 적용 지원·구간, 보존 위치. 현재 Issue의 의존성·연결 PR에 있는 이전 관측을 먼저 읽는다. 참조가 없으면 같은 변경 경계의 최근 종료 작업 한 건까지 확인해 관련 원본 URL 또는 `관련 기록 없음/조회 불가`를 남긴다. 전체 이력 탐색은 하지 않는다. |
| 인계·외부 중단 | 시작 댓글 URL, 실제 지원·현재 관측/원본, 미수집 이유, 다음 조치와 재개 위치를 기존 인계에 전달한다. 담당자 변경을 새 START로 처리하지 않는다. 원본 접근 가능 여부와 인계 뒤 실제 읽기 여부를 구별한다. |
| 구현 종료 | 시작 원본과 기존 결과를 직접 참조하고 실제 지원과 계획의 차이, 최종 요구-검증 결과·공백, 요구 누락·실패·재작업·통제 발동/오탐·사람 개입의 확인 범위와 근거, 비용의 출처·범위 또는 미수집 이유, 아래 `작성 모델 기록`의 한 줄, 다음 판단을 기존 SUMMARY에 남긴다. `지원 유지/범위 안 조정/별도 변경 후보/자료 부족`과 근거를 연결한다. 이미 알려진 후속 Issue가 있으면 그 참조를 연결하며 새 Issue·모델 실행을 자동 생성하지 않는다. |
| 최종 종료·정리 전 | 시작·SUMMARY와 필요한 비민감 원본을 다시 조회해 URL·확인 시점·대상 revision(댓글은 ID와 updated_at)·조회 상태를 남긴다. 로컬 worktree만의 파일은 정리 전에 기존 원격 기록에 보존한다. 최종 상태를 같은 SUMMARY에 갱신하고 후속 사실은 수정 시점을 구별한다. 종료 후 발견된 사실은 발견한 후속 작업이 이전 원본을 연결해 기록한다. |

생략 대상은 같은 정보의 본문 복사다. 새 실패·요구 미충족·검증 축소·출처 상실·다음 판단 변경은 현재 SUMMARY에 드러낸다. 기록 부재를 변화 없음·0건·확인 완료로 해석하지 않는다. 시작 원본이 소실되거나 확인한 버전과 다르면 현재 직접 확인한 적용 정보와 상실 범위를 남기고 과거 구간은 미확인으로 둔다. 새 작업은 자기 시작 원본을 사용하며 이전 작업의 참조를 읽기 면제로 쓰거나 비용·모델 관측을 상속하지 않는다. 비용 출처·수집 가능 여부는 현재 구간에서 확인하고 동일한 한계만 묶어 참조한다. 새 값·범위·한계는 명시한다.

관측 항목에는 `도구/CI 근거`, `별도 검토`, `Agent 자기보고`처럼 출처 유형을 구별한다. `관측 없음`에는 확인한 구간·근거를 적으며 원본이나 관찰이 없으면 `미수집`이다. 오탐·예방 효과처럼 원인 해석이 필요한 평가는 근거 없는 확정값으로 기록하지 않는다. 모델 요청 설정과 실제 제공 metadata를 구별하고, 기존 TOKEN marker에는 다른 출처의 수치를 넣지 않는다. 대화/추론 원문·재구성 가능한 요약은 기록하지 않는다.

입력이나 실행 근거가 특정 항목을 언급하지 않는 것은 그 항목을 확인했다는 뜻이 아니다. 검증 실패/수정의 근거만 있는 경우 사람 개입·오탐·요구 누락까지 `관측 없음`으로 채우지 않고 `미수집 — 확인 근거 없음`으로 묶는다. 종료 판단 후보를 남겼어도 후속 별도 작업이 소비하지 않았으면 `후속 소비 미검증`을 명시한다.

다음 관련 작업의 Agent는 이전 원본의 방법론 버전·제품 revision·미결/후속 상태를 현재 작업과 대조해 사용/유보/관련 없음의 이유를 시작 기록에 남긴다. 원본이 없으면 과거 요약만으로 검증된 입력을 복구하지 않는다. 제품별 사실은 제품에 두고 공통 방법론 변경 후보는 제품 사실을 복제하지 않은 일반화된 요구와 원본 참조로 제시한다. 수집 1건과 후속 소비 1건, 합성 평가, 모델/방법론의 인과 효과는 서로 다른 주장이다.

수집 공백·외부 문서 부재는 기존 제품 완료의 새 gate가 아니다. 구현·검증 실패는 기존 규칙대로 처리한다. 이 연결 자체를 변경하는 Issue는 지정한 연결 완료 기준을 검증해야 한다. 기존 기록이 같은 연결을 제공하거나 기록 부담·반복 미사용이 확인되면 기존 권한 안에서 중복 기록의 유지·축소를 검토한다.


공통 원본은 `P/.adaptive-sdd/install.lock.json`의 고정 정보(태그·commit·manifest 해시)를 사용한다.
### 작성 모델 기록

모든 grade의 `[IMPLEMENTATION SUMMARY]`는 SUMMARY를 작성한 Agent의 모델을 한 줄로 남긴다.

```text
모델: 요청 <model>/<reasoning> (출처: 세션 기록|설정 파일|Human 지정) · 실제 제공 <값|미확인>
```

- 역할·actor 식별자(예: `codex-root`, `Codex`)는 모델 값이 아니다.
- 실제 제공값이 `미확인`이어도 확인한 요청값과 출처는 생략하지 않는다. 요청값과 실제 제공값을 모두 확인하지 못하면 각각 `미확인`으로 둔다. 모델명/추론 설정을 자기 추정하지 않는다.
- 이전 작업, 다른 actor, reviewer의 값을 대입하지 않는다. 작업 중 모델이 바뀌면 바뀐 시점과 새 값을 구간별로 남긴다.
- 모델 줄의 누락이나 `미확인`은 완료 gate가 아니다.

host별 조회 위치는 다음과 같다. 세션 기록에는 대화 본문이 함께 있으므로 해당 필드만 추출하고 행 전체를 읽거나 출력하지 않는다.

- Codex: 현재 세션 기록(기본 위치 `~/.codex/sessions/**/rollout-*.jsonl`)의 `turn_context` 항목에 있는 `model`/`effort`가 요청값이다. 현재 세션 기록을 특정할 수 없으면 `~/.codex/config.toml`의 `model`/`model_reasoning_effort`를 `설정 파일` 출처로 남기고 세션과의 일치 여부는 `미확인`으로 둔다. 이 기록에는 서버가 실제로 제공한 모델 값이 없으므로 실제 제공은 `미확인`이다.
- Claude Code: 현재 세션 transcript(기본 위치 `~/.claude/projects/<project>/<session>.jsonl`)의 assistant 응답 `message.model`이 실제 제공값이다. 요청 추론 설정을 이 기록에서 확인하지 못하면 `미확인`으로 둔다.
- 위 필드가 없거나 다른 host면 확인한 범위만 남기고 나머지는 `미확인`으로 둔다. 위 필드의 존재는 2026-10-15 한 PC에서 Codex 세션 기록과 Claude Code transcript 각 1건으로 확인했으며 다른 host 버전·환경에서는 확인하지 않았다.

### 문제 발견 시 기록과 종료 연결

공통 core의 `발견한 문제의 기록과 프로젝트 연결`을 이 제품에서는 다음처럼 소비한다. 작업은 Issue/run으로 식별하고 사건 원본은 **해당 Issue의 일반 작업 댓글**, 종료 요약은 기존 `[IMPLEMENTATION SUMMARY]`다. 최종 종료·수집 자격과 조회 수단은 위 수동 재검토 계약을 그대로 따른다. GitHub 댓글·RELEASE/check는 제품 어댑터의 선택이며 공통 방법론의 필수 형식이 아니다.

- Trivial·Small을 포함해 실제 문제를 발견한 경우에만 기록한다. 요구 누락·검증 공백·실패·불필요한 재작업을 대상으로 하며 예상한 negative test나 정상 탐색을 자동 집계하지 않는다. 문제가 없으면 새 댓글/사건 절/빈 목록/정상 단계 행을 만들지 않는다. 기존 시작·SUMMARY·종료 점검은 유지하며 SDD·추가 댓글 태그·별도 장부는 만들지 않는다.
- 발견한 담당자는 기존 작업 댓글에 **사건 참조, 발생/발견 단계, 수행 담당 역할·식별과 발견 주체, 확인 가능한 모델/추론 설정 및 출처, 관찰한 문제·근거, 조치/결과**를 짧게 남긴다. 새 댓글이면 게시 후 URL/ID를 사건 참조로 삼고, 한 댓글에 여러 사건이면 항목을 구별한다. 같은 사건의 수정·재인계는 그 참조를 재사용한다. 모델 요청값과 실제 host metadata를 구별하고 미제공은 `미확인`으로 둔다. 발견한 리뷰어의 모델을 구현 담당 모델로 대입하거나 원인 불명을 모델 결함으로 단정하지 않는다.
- worker/reviewer는 문제가 있는 경우에만 기존 결과 packet에 해당 정보 또는 원본 참조를 전달한다. Issue 쓰기는 상위 담당자가 취합하며, 이미 보존된 동일 사건을 새 댓글로 복제하지 않는다. 기록 권한/조회·쓰기 실패는 기존 인계/종료 기록에 보존 실패와 확인 가능한 근거를 남기고 임의 파일·서비스에 우회 저장하지 않는다. 기록 실패 자체로 기존 완료 gate를 추가하지 않는다.
- 종료 담당자는 현재 작업에서 남긴 사건 참조를 따라 핵심 사실·담당 metadata·근거·조치/결과를 SUMMARY의 `발견한 문제` 부분에 취합한다. **일반 기록은 재검토 입력에서 제외될 수 있으므로 링크만 남기면 안 된다.** 사건이 없으면 이 부분을 만들지 않고 무문제/0건으로 추정하지 않는다. 해결된 사건도 최초 실패와 보정 결과를 함께 남긴다. 원본이 사라졌으면 남아 있는 사실과 상실 범위를 구분하고 추정 복원하지 않는다.
- SDD나 로컬 worker 결과에만 있는 사건은 삭제·인계 전에 기존 Issue에 보존한다. 검토를 통과한 설계 문서를 사건 기록 때문에 고치지 않는다. PR 이후 CI/리뷰에서 발견한 사건도 같은 SUMMARY에 갱신한다. 최종 종료 뒤 발견은 발견한 후속 작업의 기록/SUMMARY에서 이전 원본을 연결하며, 과거 RELEASE나 수집 기간을 조작하지 않는다.

개선 스킬은 이 SUMMARY와 직접 근거로 동일 사건 중복을 제거하고 단계·역할·모델/추론 설정·문제 유형의 반복 패턴을 조사한다. 요청 설정/실제 metadata/미확인을 구분하고 건수를 실패율이나 모델 순위로 바꾸지 않는다. 제품 사건 원본을 공통 저장소에 자동 게시하지 않는다.

## 안정화 기간 token diagnostic

mode 값은 명시한 `P/.adaptive-sdd/project/sdd-workflow.md`에서 읽는다

이 mode는 workflow 안정화 기간의 한시적 계측이다. 약 20~30개 Issue 또는 약 2주간 표본을 모은 뒤 baseline을 검토하고, 유지 결정이 없으면 위 값을 `DISABLED`로 바꾼다. Skill은 이 문서의 mode가 `ENABLED`일 때만 아래 checkpoint를 기록하므로 비활성화할 때 각 실행 절차를 다시 설계하지 않는다.

권위 있는 현재 run token total은 host의 authoritative goal tracker에서 lifecycle event 시점에 한 번만 조회한다. tracker 값이 없으면 숫자를 추정하거나 repository-wide 탐색·별도 분석을 하지 않고 checkpoint를 생략한다. 계측 성공 여부는 구현 의사결정, review, test, CI 범위와 완료 판정을 바꾸지 않는다.

Issue 댓글에 기록하는 token checkpoint는 다음 네 종류뿐이다. command별, 구현 단계별, review turn별 checkpoint는 만들지 않는다.

### START

유효한 claim과 grade gate를 통과해 실제 Issue 작업을 시작할 때 한 번 기록한다. 같은 Issue에 기존 `TOKEN START`가 있으면 새로 기록하지 않는다.

```text
[WORKFLOW][TOKEN START]
issue: #NNN
grade: Trivial | Small | Medium | Large | Epic
tokens: {current}
```

### BLOCKED

사용자 입력, 외부 인증, 외부 승인처럼 현재 lane 밖의 상태가 필요한 blocker에서 중단하기 직전에 기록한다. 동일 blocker의 미해소 상태에는 최초 한 번만 기록하고 자동 재확인이나 추가 checkpoint를 만들지 않는다.

```text
[WORKFLOW][TOKEN BLOCKED]
issue: #NNN
tokens: {current}
reason: external-blocker
blocker: {non-sensitive category}
resume-condition: {non-sensitive condition}
```

### RESUME

직전 token lifecycle이 `BLOCKED`이고 새로운 사용자 지시 또는 상태 변경 근거로 실제 작업을 재개할 때 한 번 기록한다. `from`은 직전 `TOKEN BLOCKED` 댓글 URL을 사용해 구간을 연결한다.

```text
[WORKFLOW][TOKEN RESUME]
issue: #NNN
tokens: {current}
from: {previous TOKEN BLOCKED comment URL}
```

### END

Issue가 `completed` 또는 `not-planned`로 최종 종료될 때 한 번 기록한다. `start`는 최초 START token, `end`는 현재 token, `used`는 `end - start`다. BLOCKED/RESUME 댓글의 token, blocker category, URL 연결로 각 blocker 구간 증가량과 resume 횟수, 동일 category 재발 여부를 별도로 계산할 수 있어야 한다.

```text
[WORKFLOW][TOKEN END]
issue: #NNN
result: completed | not-planned
start: {start}
end: {end}
used: {delta}
```

현재 lifecycle 상태는 Issue의 기존 token checkpoint 댓글로 판정한다. BLOCKED 없이 끝난 Issue에는 `TOKEN BLOCKED`나 `TOKEN RESUME`을 만들지 않고, 같은 event의 중복 댓글이나 START/BLOCKED/RESUME/END 이외 token checkpoint를 만들지 않는다.

## 병렬 작업

claim/release, branch/worktree, cloud sandbox의 실행 절차는 `W/skills/parallel-development/SKILL.md`가 canonical owner다. 모듈 ownership, shared/root integration 경계는 `P/.adaptive-sdd/project/module-boundaries.md`가 Source of Truth다.

## 완료 절차

구현 후 아래 순서를 바꾸지 않는다.

1. diff를 읽고 실제 동작 변경을 확정한다.
2. 변경된 동작과 직접 연결된 business 문서를 최종 코드 기준으로 갱신한다.
3. Verification Strategy의 test/lint/build/CI와 grade별 required review 결과를 확인한다.
4. P가 선언한 SDD 작업 문서 위치의 현재 작업 폴더를 삭제한다.
5. P 문서 목차와 다른 문서에서 삭제된 SDD 경로 링크를 제거한다.
6. 관련 review 문서에 현재 상태 필드가 있으면 실제 상태와 일치하도록 갱신한다. 과거 결정 내용 자체는 다시 쓰지 않는다.
7. `[IMPLEMENTATION SUMMARY]` 댓글 하나를 남기고 PR 본문에 `Closes #{issue-number}`를 넣는다. 요약을 검증·required review 통과의 대체 근거로 쓰지 않는다.
8. PR merge 후 Issue가 닫혔는지 확인한다.

business 문서를 갱신하기 전에 SDD 문서를 삭제하지 않는다.

완료 기준 하나라도 실패하거나 미검증이면 해당 항목을 체크하지 않고 완료 보고에 남긴다.
