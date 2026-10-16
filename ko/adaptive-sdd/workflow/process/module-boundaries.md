# 공통 작업 경계와 lifecycle

실제 module/path·공유 contract·integration 전용 경로·문서 위치는 P가 선언한다. 이 문서는 허용/금지 경계 적용, 현재 Issue의 lifecycle artifact 범위, 병렬 작업의 공통 계약을 소유한다. 제품 경계를 확대하거나 제품별 권한을 만들지 않는다.

## Public contract integration 순서

프로젝트가 공유 contract로 지정한 경로는 다음 순서를 고정한다.

1. integration lane에서 contract와 contract test만 수정한다.
2. contract 변경 PR을 `main`에 먼저 merge한다.
3. 구현 lane들은 최신 `main`을 반영한다.
4. 프로젝트가 지정한 각 구현 모듈을 수정한다.
5. composition root wiring이 필요하면 integration lane에서 연결한다.
6. 프로젝트가 지정한 전체 test/lint/build를 실행한다.

구현 lane이 contract 변경 필요성을 발견하면 contract 파일을 직접 수정하지 않고 차단 사유와 필요한 변경을 보고한다. 실제 contract 경로·구현 모듈·composition root·검증 명령은 P 적용 선언을 따른다.

## Issue 작업 경계

규칙은 다음과 같다.

- agent는 제품 구현 파일 중 `수정 허용`에 적힌 path glob과 그 하위 파일만 수정한다.
- test 파일도 해당 모듈 glob에 포함되어야 수정할 수 있다.
- `수정 금지`가 `수정 허용`보다 우선한다.
- 완료 기준에 필요하더라도 허용 경로 밖 제품 구현 파일을 자동으로 추가하지 않는다.
- 경계 변경이 승인되면 **제품 코드 수정 전에** Issue 본문의 허용/금지 경로를 먼저 갱신한다.
- shared contract 또는 root build 파일이 필요하면 integration 작업으로 전환하거나 별도 integration Issue를 만든다.

한 lane이 여러 구현 모듈을 수정하는 것은 허용한다. 단, **Issue 본문에 각 모듈이 모두 `수정 허용`으로 명시되어 있어야 하고, 다른 활성 lane과 어느 허용 경로도 겹치면 안 된다.**

## Lifecycle artifact 예외

다음 파일/metadata는 제품 구현 ownership과 별개인 **Issue lifecycle artifact**다. 아래 조건을 충족할 때만 `수정 허용`에 별도 기재하지 않고 변경할 수 있다.

### 작업 관리 metadata

현재 Issue의 body, labels, assignee, `[CLAIM]`/`[RELEASE]` comment와 현재 PR body(작업 관리 방식의 대응물)는 해당 Skill 절차가 요구할 때 변경할 수 있다.

다른 Issue의 scope/labels/claim을 현재 작업 편의를 위해 수정하지 않는다.

### Issue-scoped SDD

현재 Issue가 Medium 이상이면 `docs/sdd/{feature}/**`를 SDD 절차에 따라 생성·수정·삭제할 수 있다.

조건:

- `{feature}`가 현재 Issue의 SDD 디렉터리여야 한다.
- 다른 Issue의 `docs/sdd/**`를 수정하지 않는다.
- SDD 외의 product/business 문서를 이 예외로 수정하지 않는다.

### Business 문서

`finishing-issues` 단계에서 **최종 코드 동작과 직접 연결된 기존 `docs/domains/**` 규칙**만 갱신할 수 있다.

조건:

1. runtime/product behavior가 실제로 변경됐다.
2. 변경할 rule/topic이 해당 behavior를 현재 설명하는 문서다.
3. diff 근거로 무엇이 바뀌었는지 확인했다.
4. 다른 활성 lane/PR이 같은 business 문서 파일을 수정 중이지 않다.

4번이 거짓이면 business 문서를 동시에 수정하지 않고 `BLOCKED: documentation lane conflict`로 보고한다. 제품 코드를 되돌리거나 다른 lane의 문서를 덮어쓰지 않는다.

새 business topic 파일을 만들거나 rule ID를 추가/의미 변경하는 작업은 프로젝트 review topic 발동 조건도 다시 확인한다.

### Review 문서

현재 작업이 review 절차에 명시적으로 들어간 경우에만 현재 review topic의 `proposal/review/decision` 파일을 수정한다. 과거 review topic은 상태 갱신 조건 외에는 lifecycle 예외로 수정하지 않는다.

### UI Visual Spec

`managing-issues` Skill이 HTML 생성 조건을 충족한 경우에만 프로젝트가 지정한 별도 디자인 repository의 해당 Issue HTML을 만들거나 갱신한다. 앱 구현 lane이 임의로 Visual Spec을 바꾸지 않는다.

## 병렬 lane 선점

제품 코드 수정 전에는 active lane의 allowed path가 현재 Issue와 겹치지 않는지 확인하고 현재 lane을 claim해야 한다. **claim/release의 실행 순서, metadata와 comment 형식은 `W/skills/parallel-development/SKILL.md`가 canonical owner**이며 이 문서에서 중복 정의하지 않는다.

이 문서가 소유하는 경계 불변식은 다음과 같다.

- 다른 활성 `[CLAIM]` 또는 open PR과 제품 구현 경로가 겹치면 구현하지 않는다.
- shared/root integration-only 경로를 ordinary lane이 claim하지 않는다.
- Issue의 allowed/forbidden이 없으면 제품 코드 수정을 시작하지 않는다.
- claim 이후 새 overlap이 확인되면 제품 코드를 수정하지 않고 lane을 release한다.

## Branch/worktree/cloud

최신 원격 main 확인·isolated lane 생성·동기화·정리는 W `skills/parallel-development/SKILL.md`가 단일 수행 원본이다. branch naming·실제 module과 root/shared 범위는 P 선언을 따른다. 예시 명령으로 fresh base·정상 cleanup 단계를 대체하지 않는다.

## 경계 위반 시 행동

다음 중 하나가 발생하면 현재 구현을 확장하지 않는다.

- 완료 기준에 shared contract 변경이 새로 필요함
- 다른 활성 lane과 제품 구현 path가 겹침
- Issue 허용 경로만으로 컴파일이 불가능함
- architecture 의존성 금지 규칙을 깨야 구현 가능함
- finishing 단계에서 다른 활성 lane과 같은 business 문서 파일을 동시에 수정해야 함

이 경우 수정하지 않은 파일, 필요한 변경, 현재 완료 기준에 미치는 영향을 `BLOCKED`로 보고한다.
