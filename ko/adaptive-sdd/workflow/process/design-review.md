# 설계 리뷰

Large의 AS-IS·PLAN 설계 리뷰 절차 원본이다. 실제 해당 phase의 검토를 준비하거나 finding을 반영할 때 읽는다. Epic 생성·분해에는 적용하지 않는다. Medium에서 명시적으로 수행하는 환경 간 SDD 리뷰에는 아래 원격 후보 게시 조건만 재사용하며 Review B를 추가하지 않는다.

| 현재 작업 | 읽을 절 |
| --- | --- |
| 최초 AS-IS·PLAN 검토 | [설계 단계](#large-설계-단계), [후보 게시](#원격-검토-후보-게시), [이중 독립 리뷰](#large-설계-이중-독립-리뷰) |
| 검토 후 candidate 변경 | [의미·영향 판정](#의미영향에-따른-설계-재검토) |
| 구현 중 PLAN 전제 오류·정책 변경 | [계획 정정과 정책 전환](sdd-artifacts.md#계획-정정과-정책-전환) 뒤 아래 영향 판정 |
| 같은 의미 충돌이 수정·재확인 후 반복 | [반복 정체 시 전환](#반복-정체-시-전환) |

reviewer의 model·floor·qualification은 [execution-routing](../skills/_shared/execution-routing.md), 전달 필드와 evidence identity는 [execution-packets](../skills/_shared/execution-packets.md)가 원본이다. 이 문서는 리뷰 순서·독립성·진행 조건을 소유한다. 프로젝트의 사람 권한은 `S/.adaptive-sdd/project/sdd-workflow.md`를 적용한다.

## Large 설계 단계

1. `01-as-is.md`를 작성하고 아래 원격 후보 게시 조건으로 검토 대상을 고정한다.
2. 같은 exact candidate에서 아래 Review A → Review B와 필요한 reconciliation을 완료한다.
3. 아래 검토 조건과 [단계별 의존성](sdd-workflow.md#미결-사항과-단계별-의존성)을 만족하는 범위에서 사람 승인을 추가로 기다리지 않고 `02-to-be.md`와 `change-plans/**`를 작성한다. 미결 결론이 필요한 작업은 P의 사람 판단 규칙에 따라 기다린다.
4. PLAN도 원격 후보 게시와 A → B를 수행한다. 최초 검토 또는 current-target 재확인 chain이 현재 exact candidate에서 진행 조건을 만족해야 구현한다.
5. 구현 뒤 [등급별 code review와 필수 검증](verification.md#grade별-review-gate)을 거쳐 PR을 준비한다. Large 병합은 기존 사람 판단 규칙을 따른다.

## 원격 검토 후보 게시

AS-IS·PLAN independent review candidate는 P `tracker.md`가 선언한 게시 저장소·원격·branch의 exact commit으로 고정한다. 미지정 기본값은 현재 제품 저장소와 Issue branch다. 외부 harness 저장소나 reviewer가 접근 가능한 로컬 bare 원격도 가능하다. 제품 claim의 branch와 문서 게시 branch를 별도로 기록한다.

1. 초안 중 local commit은 허용한다. 검토 인계 직전에 artifact를 소유한 선언 저장소에서 candidate를 commit하고 선언된 게시 remote branch로 push한다. 공유 branch는 게시 담당을 조율하고 다른 lane 변경을 포함하거나 force push하지 않는다. P의 commit/push 권한은 별도로 충족한다.
2. remote branch history에 exact candidate SHA가 있고 해당 SHA의 artifact 원문(AS-IS는 `01-as-is.md`, PLAN은 `02-to-be.md`와 `change-plans/**`)을 remote에서 읽을 수 있는지 확인한다. local-only SHA, local remote-tracking ref, 작성자의 worktree 존재만으로 review/PASS target을 인정하지 않는다.
3. 환경 간 인계·복구에는 Issue 번호, 제품 `[CLAIM]`의 branch, 게시 저장소와 remote branch, phase, 그 저장소 기준 artifact 경로와 exact remote SHA를 남긴다. reviewer가 작성자 worktree 없이 원문을 확인할 수 있어야 한다. 코드 근거가 다른 저장소이면 그 repository·revision·경로도 별도로 연결한다.
4. review-affecting 변경은 새 commit을 선언된 게시 branch에 push하고 아래 의미·영향 판정과 current-target 재확인 chain을 적용한다. 이전 SHA의 PASS를 자동 승계하지 않는다. 기록/head-only 변경은 먼저 기존 target 유지 조건을 확인한다.

push 실패, remote branch에서 exact SHA 확인 실패, remote 원문 조회 실패 중 하나라도 있으면 `BLOCKED: SDD candidate remote push failed`로 중단한다. local-only artifact로 계속하지 않는다. remote branch와 exact SHA만으로 publication은 충분하므로 이 단계에서 PR이나 draft PR을 만들지 않는다. 모든 commit의 즉시 push를 요구하지 않으며 신규 lane의 선언한 fresh 기준 branch와 기존 branch/worktree·claim lifecycle은 [parallel-development](../skills/parallel-development/SKILL.md)를 그대로 따른다.

## Large 설계 이중 독립 리뷰

Large의 AS-IS와 PLAN 최초 candidate에는 서로 다른 별도 agent/session의 두 review를 순서대로 적용한다. 이후 revision은 아래 의미·영향 판정과 재확인 chain을 적용한다. Review A는 author와 분리되고 Review B는 author 및 Review A actor/session과 모두 분리된다. Trivial/Small/Medium, 기본 IMPLEMENT/CODE review에는 Review B를 추가하지 않는다.

- **Review A — Contract Review**: current Issue/acceptance, phase artifact identity, reviewed upstream contract, 직접 caller/callee·invariant·allowed/forbidden, source/diff/verification evidence를 bounded하게 확인해 사실·계약·Agent Execution Spec의 correctness와 consistency를 판정한다.
- Review A는 AS-IS의 판단을 좌우하는 기준·외부 동작·운영 근거와 PLAN의 P 컨벤션 참조·이탈 이유도 대조한다. 선언되지 않은 개인 선호를 기준으로 새 finding을 만들지 않는다. 필요한 조사와 컨벤션 기록의 범위는 [SDD 작업 문서](sdd-artifacts.md)를 따른다.
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

현재 phase의 판단을 바꾸지 않고 미래 단계에서만 필요한 사람 질문은 현재 phase blocker로 올리지 않고 담당·필요 단계로 연결한다. 반대로 지금 설계/실행 의미를 선택해야 하는 미결을 미래 질문으로 미뤄 통과시키지 않는다.

Review A의 blocking finding은 보정 후 A re-check한다. A가 통과한 뒤 Review B reviewer의 model과 reasoning level을 Human이 선택한다. 선택 전에는 Agent가 임의 배정하지 않고 `BLOCKED: blind-audit reviewer selection required`로 중단한다. 선택된 reviewer는 [routing의 `REVIEW` floor와 role qualification](../skills/_shared/execution-routing.md)을 만족하고 현재 host에서 사용할 수 있어야 한다. 사용할 수 없거나 부적격이면 다른 reviewer로 자동 fallback하지 않고 `BLOCKED: selected blind-audit reviewer unavailable`로 중단해 Human 재선택을 요청한다. Human 선택은 `review-mode = blind-audit`, 별도 agent/session, capability floor를 완화하지 않는다.

Review B 최초 판정 전에는 Review A의 PASS/BLOCKED verdict, finding 목록, 상세 packet과 이전 Review B finding detail을 제공하지 않는다. Review B 입력은 Issue id/title, `AS-IS | PLAN`, target artifact와 remote-resolvable exact SHA, 상위 목표/직접 소유 경계, 전면 재설계 금지, omission·hidden assumption·boundary-changing blocking risk 탐색 요청으로 제한한다. reviewer는 target artifact에서 직접 인접한 caller/consumer/contract를 확인할 수 있다.

실제 전달 자료는 [Blind 입력 준비와 확인](../skills/_shared/execution-packets.md#blind-입력-준비와-확인)으로 결과와 분리하고 원본 identity·추출 범위·접근 가능성을 확인한다. Packet에서 finding을 뺐어도 artifact나 상위 본문에서 노출되면 독립성 조건을 충족하지 않는다.

최초 verdict가 고정된 뒤에만 같은 Review B reviewer에게 이전 Review B finding identity와 resolution expectation ledger를 제공한다. reviewer는 이전 finding마다 현재 remote-resolvable exact candidate의 직접 근거로 `resolved / unresolved / regressed / not-applicable` 중 하나를 판정한다. reconciliation은 이전 finding을 자동 PASS로 만드는 절차가 아니며, 최초 verdict의 신규 finding 목록과 이전 finding reconciliation을 분리한다. 이전 B finding이 없으면 reconciliation은 해당 없음으로 명시한다.

unresolved Human Decision blocker 또는 unresolved Execution-contract blocker가 하나라도 있으면 다음 phase를 중단한다. candidate SHA 변경은 변경분 확인의 trigger이며 전체 검토 무효화 판정 자체가 아니다. 아래 영향 판정으로 current exact candidate의 검토 근거를 구성한다. 이전 SHA PASS의 이름만 바꿔 승계하거나 review 횟수로 강제 PASS하지 않는다.

Large AS-IS·PLAN의 다음 phase 진행 조건은 다음과 같다.

```text
Review A: PASS
Review B: initial blind audit completed; current-target impact/reconfirmation chain valid
Review B reconciliation: prior findings confirmed at current target when present
unresolved Human Decision blocker: 0
unresolved Execution-contract blocker: 0
```

이 조건은 검토의 진행 조건이다. 충족하면 Implementation finding 또는 Non-blocking observation이 남아 있어도 Review B PASS가 가능하지만, 실제 다음 작업은 [미결 사항과 단계별 의존성](sdd-workflow.md#미결-사항과-단계별-의존성)도 확인한다. reviewer가 finding으로 만들지 않은 미결 결정도 결론이 필요한 작업의 선행 조건이다. Implementation finding은 IMPLEMENT handoff에서 누락할 수 없고 CODE/finishing에서 코드와 fixture 해결이 확인되지 않으면 완료할 수 없다.

IMPLEMENT/CODE는 기존 independent code review 1회를 유지한다. destructive migration, cross-DB atomicity, recovery처럼 명시적인 고위험 escalation 근거가 있을 때만 별도 code audit을 추가할 수 있으며 이를 Large의 기본 이중 review로 만들지 않는다.

## 의미·영향에 따른 설계 재검토

최초 A와 독립·blind B는 생략하지 않는다. 후속 변경은 기존 Review Packet에 이전/현재 remote target, 전체 변경 inventory와 diff, 수정 finding identity, 영향받는 contract·완료 기준·직접 소비자, 영향 없음의 근거, current-target 재확인 결과를 연결한다. reviewer는 inventory를 독립 확인하고 필요한 주변 근거를 열 수 있어야 한다. 누락 파일이나 근거 접근 실패를 작은 변경으로 추정하지 않고 보완 전 차단한다.

| 확인된 변경 | 필요한 후속 검토 |
| --- | --- |
| 검토 결과 기록만 변경, 대상 artifact bytes 불변 | 새 기록과 대상 분리·identity를 확인. 대상의 기존 검토는 유지하고 결과 기록 변경으로 새 A/B를 자동 생성하지 않음 |
| 표현·설명 보완, 의미 불변이 직접 근거로 확인됨 | A가 변경분·finding·직접 영향을 current target에서 재확인. 기존 B 근거의 적용 가능성과 prior finding 상태도 확인 |
| 검증 수단만 강화: 제품 Decision·상위 계약·완료 기준·제품 경계·실패/복구 의미·runtime 의존성과 기존 감사 전제 불변 | A가 변경된 검증 계획의 실행 가능성·완료 기준 대응과 기존 B 근거의 적용 가능성을 current target에서 확인. B의 기존 finding 해결 근거에 영향이 있으면 관련 부분만 B 후속 재확인. 그 영향이 없다는 직접 근거가 있으면 B를 다시 호출하지 않으며 새 blind를 요구하지 않음 |
| 국소 실행 계약 보정, 핵심 Decision·상위 계약·경계·감사 전제 불변 | A의 관련 계약·소비자 재확인과 B의 관련 finding·직접 영향 후속 재확인. invalidated 판단만 갱신 |
| 핵심 Decision·상위 계약·작업 경계·복구/실패 의미·감사 전제 변경 | 무효화된 phase의 관련 설계 전반을 A로 검토한 뒤 새 독립 Blind Audit B. upstream AS-IS가 무효화되면 AS-IS부터 재검토 |
| 영향 불명확 | 의미 변경 가능 범위로 보수적으로 확장. 근거 확보 전 PASS 금지; 전제 불변을 증명하지 못하면 새 A/B 경로 |

한 줄 수정도 실행 의미로 판정한다. author의 `설명만 변경` 선언이나 diff 크기는 근거가 아니다. 검토 대상 artifact와 결과 기록은 분리한다. 결과는 기존 Review/Result Packet 또는 Issue 댓글에 두며 결과를 적으려고 대상 본문을 매번 수정하지 않는다. artifact에 결과를 함께 쓴 경우 실제 diff로 의미 불변을 증명해야 한다.

검증 수단 강화는 기존 완료 기준을 보존하면서 테스트·검증 근거를 보강하는 경우다. 승인된 테스트 경로 추가만으로 제품 경계 변경이라고 판정하지 않지만, 경로 쓰기 권한·claim은 별도로 충족한다. 테스트 명목의 제품 seam·runtime 의존성·완료 기준 변경이나 기존 검증 제거/약화는 이 행에 넣지 않고 실제 의미·영향으로 판정한다. 최초 required review를 생략하는 예외가 아니며, 영향 불명확이면 표의 해당 행을 따른다.

후속 재확인은 이전 finding을 받을 수 있지만 `최초 Blind Audit`이라고 기록하지 않는다. 새 Blind Audit이 필요한 경우 기존 Human의 model/reasoning 선택이 여전히 유효하고 available/qualified이면 재사용할 수 있으나 author/A와 분리된 새 session을 사용하고, 최초 verdict 전에 A 결과·이전 B detail을 숨긴다. verdict 뒤 prior ledger reconciliation을 수행한다. 국소 재확인도 reviewer 독립성을 유지하며 current target 근거 없이 이전 PASS를 복사하지 않는다.

다음 phase 진행 근거에는 최초 blind verdict의 불변 참조, 이후 target 차이/영향 판정과 A/B 재확인 chain, current-target prior finding 상태를 연결한다. 새 blind 조건이 발생하면 chain은 새 최초 verdict에서 다시 시작한다. 이 chain은 review evidence의 재사용만 허용한다.

기록/head-only 변경은 먼저 기존 검토 target 유지 가능성을 확인한다. 전체 변경 inventory를 바탕으로 해당 phase artifact inventory·bytes, Decision scope·upstream 및 검토한 직접 계약/소비자·감사 전제가 불변임을 확인하면 기존 target과 검토 근거를 유지한다. branch head를 검토 target으로 매번 치환하지 않는다. 계약/소비자 의미 변화는 artifact bytes가 같아도 기록-only로 분류하지 않는다.

A finding 보정이 끝나고 A PASS가 고정된 candidate에서만 B를 dispatch한다. A 수정과 B 검토를 겹쳐 stale B 결과를 만드는 일을 피한다. 국소 수정의 A/B는 invalidated 판단·finding·직접 영향을 독립 재확인한다. 새 target의 검토 결과는 그 재확인의 직접 근거이며 최초 blind로 오기하거나 과거 PASS의 target만 바꾸지 않는다.

## 반복 정체 시 전환

같은 phase·contract/Decision 영역에서 같은 finding 또는 같은 의미 충돌이 **수정 → 재확인 뒤 2회 연속** unresolved/regressed이면 다음 자동 리뷰를 시작하지 않는다. finding 이름이나 SHA만 바꿔 같은 충돌의 streak를 초기화하지 않는다. 단순 총 리뷰 수, 무관한 신규 결함 발견은 정체로 세지 않으며 그 영역의 해결을 직접 증명하면 streak를 종료한다.

기존 Review Packet에 영역, 안정된 finding/충돌 identity, 각 수정·재확인 target과 근거, 해결되지 않은 원인을 남긴다. 범위 분리(소유 Issue와 완료 기준 포함), 불명확한 계약에 대한 Human 결정, 추가 근거 확보, 이유와 달라진 검토 범위가 명시된 재검토 중 선택지를 보고한다. 필요한 Human 결정 또는 새로운 근거에 따른 명시적 재검토 사유가 확보된 뒤에만 재개한다. 새 SHA나 시간 경과만으로 자동 재개하지 않는다. 임계값은 검토 면제·강제 PASS가 아니며 blocker는 해결 또는 사람이 정한 범위 결정까지 유지한다.
