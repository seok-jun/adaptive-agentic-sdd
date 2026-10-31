# SDD completion

종료의 SUMMARY·사람 판단 계약은 [issue](issue.md), 필수 검증과 PASS 유효성은 [verification](../verification.md)을 적용한다. 확인한 동일 버전은 재사용한다.

## 문서 역할

| 종류 | 위치 | 수명 | 역할 |
| --- | --- | --- | --- |
| business 문서 | `docs/domains/**` | 영속 | 구현 완료 후 유지되는 현재 제품 동작 |
| SDD 작업 문서 | `docs/sdd/{feature}/` | 작업 중 | AS-IS 근거, Human Decision Contract, Agent Execution Spec |
| 결정 기록 | `docs/reviews/**` | 영속 | 과거 의사결정의 근거와 대안 |
| 구조 문서 | `docs/architecture/**` | 영속 | 모듈 책임, 의존성, 작업 경계 |

위 위치는 기본값이며 실제 위치는 P 적용 문서의 `문서 역할` 표를 따른다. SDD 작업 문서는 완료 시 정리하되, 활성 소비자가 참조하는 근거는 [finishing의 참조 보존 조건](../../skills/finishing-issues/SKILL.md#4-remove-temporary-sdd)에 따라 불변 참조로 전환하거나 담당·해제 조건을 정해 보존한다. business 문서는 SDD 문서나 Issue를 복사하지 않고 **최종 코드 동작을 읽어서** 갱신한다.

## business 문서 갱신

business 문서는 구현 완료 후 **현재 코드가 실제로 하는 동작**을 기록한다.

1. 변경된 심볼의 직접 사용자/배경 진입점을 찾는다.
2. 변경으로 실제 동작이 달라진 규칙만 수정한다.
3. 변경하지 않은 규칙을 재작성하지 않는다.
4. Issue, commit message, SDD 문장을 그대로 옮기지 않는다.
5. code와 기존 business 문서가 다르면 `W/process/agent-instruction-policy.md`의 drift 규칙을 적용한다.

한 줄 규칙이 조건·예외·재시도를 모두 담아 150자를 넘으면 상세 주제 문서로 분리하고 business 인덱스에는 ID, 한 줄 요약, 링크만 둔다.

## 완료 절차

구현 후 아래 순서를 바꾸지 않는다.

1. diff를 읽고 실제 동작 변경을 확정한다.
2. 변경된 동작과 직접 연결된 business 문서를 최종 코드 기준으로 갱신한다.
3. SDD 삭제 전에 Verification Strategy에 따른 구현의 필수 검증 근거를 확인하고 누락·무효화된 검증을 수행한다.
4. P가 선언한 SDD 작업 문서 위치의 현재 작업 폴더를 [참조 보존 조건](../../skills/finishing-issues/SKILL.md#4-remove-temporary-sdd)에 따라 삭제하거나 담당·해제 조건을 명시해 보존한다.
5. P 문서 목차와 다른 문서의 SDD 링크는 불필요한 것만 제거하고 활성 소비자의 필요한 참조는 유지·전환한다.
6. 관련 review 문서에 현재 상태 필드가 있으면 실제 상태와 일치하도록 갱신한다. 과거 결정 내용 자체는 다시 쓰지 않는다.
7. 예정된 저장소 파일 변경을 모두 마친 후보를 고정하고 최종 필수 검증 근거를 확보한 뒤 grade별 CODE Review/self-review를 수행한다. 종료 시 두 근거의 유효성을 함께 확인하며, 앞선 검증은 입력 불변 근거가 있을 때만 재사용한다. 상세 순서와 변경 후 재확인은 [finishing-issues의 최종 후보 확인](../../skills/finishing-issues/SKILL.md#5-prepareverify-pr-closure)을 따른다.
8. `[IMPLEMENTATION SUMMARY]` 댓글 하나를 남기고 PR에 이 Issue의 closing reference(`Closes #{issue-number}`, 선언한 작업 관리 방식의 표기)를 넣는다. 요약을 검증·required review 통과의 대체 근거로 쓰지 않는다.
9. PR merge 후 Issue가 닫혔는지 확인한다.

business 문서를 갱신하기 전에 SDD 문서를 삭제하지 않는다.

완료 기준 하나라도 실패하거나 미검증이면 해당 항목을 체크하지 않고 완료 보고에 남긴다.
