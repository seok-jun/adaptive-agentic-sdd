# SDD 산출물 배치

Medium·Large에서 폴더를 처음 구성할 때 읽는다. Trivial·Small 및 Epic 관리 문서 자체에는 SDD를 추가하지 않는다. 파일 수와 수명은 유지하며 사람용 AS-IS 설명을 기존 README로 옮긴다. 진행 중 작업은 재작성하지 않는다.

| 독자·소비 단계 | 작업 파일 | 작성 규칙 |
| --- | --- | --- |
| 사람: AS-IS 현황·위험 | `README.md` | 아래 README |
| Agent/reviewer: AS-IS 조사·근거 | `01-as-is.md` | [AS-IS](sdd/as-is.md) |
| 사람: PLAN 변화·결정·AC와 검증 요약 | `02-to-be.md` | [TO-BE](sdd/to-be.md) |
| Agent/reviewer: 구현·검증·인계 | `change-plans/{ID}.md` | [Agent Spec](sdd/agent-spec.md) |
| 전제 오류·정책 변경 시 | 해당 원본을 정정 | [계획 정정](sdd/plan-change.md) |

문서 역할·정리 시점은 [completion](sdd/completion.md#문서-역할), 검증은 [verification](verification.md)이 원본이다.

## SDD 작업 문서 구조

Medium 이상에서 다음 구조를 사용한다. 새로 시작하는 SDD 작업부터 적용하며, 이미 진행 중인 작업과 종료된 작업에는 소급 적용하지 않는다. 이 규칙만으로 기존 설계를 재작성하지 않는다. Medium은 P의 `sdd.medium_artifacts`가 `condensed`이면 아래 [Medium 축약 배치](#medium-축약-배치)를 따른다.

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

사람용 AS-IS 현황과 작업 진입점이다. 아래 내용을 간결하게 둔다.

- Issue 원본과 기준 revision/확인 시점. Priority·grade·허용/금지 경로는 해당 본문 항목을 직접 연결한다. 값을 복사해 별도로 관리하지 않는다.
- 연결된 business/architecture 문서의 필요한 절
- 문제 정의·원인 모델·범위/경계와 설계에 영향을 주는 핵심 사실·위험을 먼저 짧게 제시
- 현황 이해에 필요한 소유·연결·흐름·상태는 관계도나 작은 표로 먼저 보여주고 사실·가설·미조사를 구별. 단순 변경은 한 문장 허용

- 각 사실·위험에서 `01-as-is.md`의 직접 근거로 연결한다. 근거 원문을 재서술하지 않는다.
- README 최초 작성 때 PLAN 위치 `02-to-be.md`를 예정 경로로 연결한다. 작성 여부·진행 상태는 기존 Issue에서 확인하며 PLAN 작성 뒤 링크를 추가하려고 AS-IS 검토 대상 README를 다시 쓰지 않는다. 변화·결정·완료 기준의 요약은 TO-BE에만 둔다. 실제 AS-IS 사실·위험·전제가 바뀌면 기존 [의미·영향별 재검토](design-review.md#의미영향에-따른-설계-재검토)를 적용한다.



## Medium 축약 배치

P `W/../project/sdd-workflow.md`의 `실행 프로필`에서 `sdd.medium_artifacts`가 `condensed`일 때 새로 시작하는 Medium SDD에만 적용한다. 값이 없거나 `full`(기본)이면 위 구조를 그대로 쓴다. Large는 항상 위 구조를 쓴다.

```text
docs/sdd/{feature}/
  README.md   ← ## AS-IS / ## PLAN / ## 구현 명세
```

- 파일 하나에 세 절을 둔다. 줄이는 것은 파일 수뿐이다. 각 절의 필수 내용은 그대로다: `## AS-IS`는 [AS-IS](sdd/as-is.md), `## PLAN`은 [TO-BE](sdd/to-be.md), `## 구현 명세`는 [Agent Spec](sdd/agent-spec.md)을 따른다.
- 다른 W 문서가 `01-as-is.md`·`02-to-be.md`·`change-plans/**`를 가리키면 이 README의 `## AS-IS`·`## PLAN`·`## 구현 명세`로 바꿔 읽는다. 예를 들어 [검증 계약](verification.md)의 "Medium 이상은 `02-to-be.md`에 완료 기준·검증 수단·성공 근거를 대응시킨다"는 `## PLAN`에 대응시킨다는 뜻이다.
- 사람용 설명(현황·변화·결정)을 각 절의 앞에 두고, Agent 근거와 구현 세부는 그 뒤에 둔다. 위 README 규칙의 근거 연결·복사 금지·정보 한 곳 관리는 그대로다.
- 작업 중 Large로 다시 판정되면 AS-IS 검토 전에 위 네 문서 구조로 나눈다. 축약 README를 Large 검토 대상으로 쓰지 않는다.
- 정리 시점과 방법은 [completion](sdd/completion.md#문서-역할)과 finishing의 SDD 정리 절차를 그대로 따른다.

## 원본과 선택적 소비

“사람용”은 표현 관점이며 Agent 읽기 면제가 아니다. 설계·Medium 구현 진입·별도 IMPLEMENT 문맥·필요한 리뷰에서 적용되는 README의 문제·전제·불변조건·남은 위험을 해당 절과 기준 revision으로 직접 연결하고 소비한다. 모든 역할에 README 전체 읽기를 추가하지 않으며 리뷰는 기존 역할별 허용 입력과 Blind Audit 격리를 따른다.

사람은 현재 phase의 Human View에서 판단 내용과 위험을 읽고 필요한 근거만 직접 연다. Agent는 해당 실행 명세와 적용 Decision·AC를 읽으며 rationale 전체를 반복하지 않는다. reviewer는 Human View와 Agent 근거 양쪽을 같은 candidate에서 검토한다. 분리는 검토 범위나 Blind Audit 격리를 줄이지 않는다.

동일 정보는 한 곳에서 관리한다. Issue의 목표·경계는 Issue, 현재 사실·코드 근거는 AS-IS, 확정 Decision·AC와 검증 대응은 TO-BE, 구현 순서·테스트 세부는 change-plan이 소유한다. 참조에는 저장소·고정 revision·경로/심볼/항목 또는 확인 시점을 남긴다. 권한이나 수명 때문에 참조를 확인할 수 없으면 미확인으로 표시하고 결론을 소비하기 전에 해결한다. 링크 존재를 검증 성공으로 보지 않는다.

기존 Issue·코드·테스트·리뷰 결과의 안정적인 참조로 충분하면 내용을 복사하지 않는다. 이전 분석은 [기존 분석 재사용](sdd/entry.md#기존-분석-재사용)으로 유효성을 확인하고 차이만 보완한다. 별도 `evidence.md`는 필수가 아니며 기존 원본으로 보존할 수 없는 실제 근거가 있을 때만 사용한다. 완료 결과 요약은 기존 SUMMARY를 연결하며 새 보고서를 만들지 않는다.

현재 실행에 필요한 계약 참조는 그 결정을 소비할 때 확인한다. 원인 재조사·감사에만 필요한 상세 이력은 해당할 때만 읽는다. 핵심 결론·조건·남은 위험은 현행 산출물에 남기며 과거 링크 뒤로 숨기지 않는다. 참조가 있다는 이유로 연결 문서를 모두 선행 로딩하지 않는다. 현재 진행 상태는 P가 정한 Issue/작업 기록 원본에서 관리하며 여러 산출물에 복제하지 않는다. 검토·승인 당시 snapshot은 당시 사실로 보존하고 현재 진행 상태와 덮어 합치지 않는다. 파일 이동·참조 전환만으로 실제 읽기 토큰 절감을 주장하지 않는다.

참고 서식은 `templates/sdd/`에 있다. 새 필수 항목이나 placeholder 채우기 의무가 아니며 해당 phase의 기존 의무만 작성한다.
