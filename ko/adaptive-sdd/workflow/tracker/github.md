# 작업 관리 방식: GitHub

## Trivial/Small 간결 묶음

Trivial/Small [간결 경로](../process/small-work.md)의 정상 댓글은 소유권/시작의 `[CLAIM]`, 구현/검증/관측의 `[IMPLEMENTATION SUMMARY]`, `merged`·`closed`·`product-complete`·`cleanup`·`release`를 구분한 `[CLOSED]`의 세 개다. 각 동작의 실제 시각과 근거를 유지하며 나중 사실은 그 시각과 함께 같은 댓글을 갱신할 수 있다. 실패·정정은 세 댓글을 넘을 수 있다. 저장소·허용 작성자·기능은 설정 때 확인하고 이후 변경 여부만 확인한다. 접근 불가/미지원 동작은 의존 작업을 멈추며 토큰 생성/탐색/등록으로 우회하지 않는다.

CLAIM은 `agent`, `branch`, `allowed`, `forbidden` 소유권 payload와 시작 사실을 담는다. CLAIM은 계속 편집 전에 assignee/status와 충돌 재조회가 필요하며 획득 실패는 다른 소유자 상태 정리 권한이 아니다. priority와 grade는 지원하면 생성 시, 아니면 직후 각각 하나 설정하고 다시 읽는다. 간결 본문은 제목을 합칠 수 있으며 중복 값은 일치해야 한다.

허가된 병합 직전 명시적 PR base·metadata·병합 가능성·필수 검사/리뷰·권한을 재조회한다. 병합 후 선언 대상을 fetch하고 tip과 PR의 관측된 merge-result SHA(`merged.main`)를 별도로 고정한다. 실제 PR merged 상태와 해당 대상의 결과 식별을 확인한다. squash/rebase는 task head 포함 여부나 fetched tip을 대신 쓰지 않고 PR의 결과 commit 식별로 검사한다. `Closes #N`이 현재 Issue인지와 실제 Issue closed 상태를 재조회한다. `product-complete`는 adapter JSON `{"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40-character SHA"}`에 실제 merge-result SHA와 완료 시각을 담아 정리와 독립적으로 보존한다.

`cleanup`은 실제 상태/시각과 남은 작업을 기록한다. 필수 정리가 미완료이면 제품 완료를 보존하고 소유권을 유지한다. 해제는 다음 순서를 따른다.

1. 일치하는 활성 CLAIM을 다시 확인한다. `CLOSED.release`에 `claim`(정확한 CLAIM 댓글 ID/URL), 일치하는 `agent`와 `branch`, `state: prepared`, 준비 시각을 기록한다. 준비는 claim을 종료하지 않는다.
2. 자기 assignee/status metadata만 정리하고 재조회하여 제거를 확인한다. 경쟁자 metadata는 바꾸지 않는다. 제거 또는 확인 실패 시 claim을 활성 상태로 유지하고 해제 미완료를 기록한다.
3. 확인 뒤에만 같은 `CLOSED.release`를 `state: released`와 실제 해제 시각으로 갱신하며 준비 사실도 보존한다. 이것이 해당 CLAIM의 최종 해제 기록으로 `[RELEASE]`에 해당하며 CLAIM 댓글을 삭제하지 않는다.
4. CLOSED와 Issue metadata를 다시 읽는다. 일치하는 최종 해제와 자기 활성 metadata의 부재를 관측한 뒤에만 성공을 보고한다. 갱신 실패나 읽을 수 없는 결과는 해제 미확인이며 제품 완료를 보존하고 세 기록을 넘더라도 정정/해제 미완료를 남긴다.

나중 독자는 정확한 CLAIM ID/URL과 agent/branch로 해제 기록을 연결한다. 일치하는 최종 `state: released` 기록이 없으면 CLAIM은 활성 상태다. 누락·prepared·미완료·읽을 수 없는 해제 기록은 해제를 입증하지 않는다. 같은 agent/branch여도 이전 claim의 해제는 후속 claim을 해제하지 않는다. 충돌 확인은 활성 claim의 allowed/forbidden 경로와 소유 metadata 재조회를 사용하며 metadata가 남거나 확인 불가이면 소유권이 완전히 정리됐다고 보지 않는다. 과거 CLAIM/RELEASE 댓글과 CLOSED의 사실/시각은 갱신 때도 보존한다.

이 문서는 W 절차의 Issue·댓글·라벨·assignee·PR·closing reference 표현을 **GitHub Issue와 PR**로 실현하는 방법이다. W는 특정 도구에 묶이지 않는 용어를 쓰며(workflow README 참조), 이 표는 각 용어의 GitHub 실현이다. P 적용 문서 `tracker.md`가 이 방식을 선언하고 저장소(`owner/name`)와 허용 작성자를 정한다.

| W 절차의 표현 | GitHub |
| --- | --- |
| Issue, `#N` | 선언한 저장소의 GitHub Issue |
| `priority:*`, `grade:*`, `status:*` 라벨 | 같은 이름의 Issue 라벨 |
| 생성할 때 Priority·grade 값 지정 | API가 허용하면 생성 요청에 두 라벨을 포함하고, 아니면 생성 직후 추가 |
| `priority:*` 값 교체 | 기존 `priority:*` 라벨을 제거한 뒤 새 라벨 추가 |
| Issue 번호 순서 | GitHub Issue 번호 |
| Epic 관리 문서 | `type:epic` 라벨과 본문 `## 작업 유형`의 `Epic`. `grade:*` 없음. 하위 Issue는 본문에서 연결하며 전체 완료 근거 확인 뒤 관리 Issue를 닫음 |
| assignee | Issue assignee |
| Issue 댓글, URL, `updated_at` | Issue comment와 그 URL·`updated_at` |
| `[CLAIM]` / `[RELEASE]` | 해당 태그로 시작하는 Issue comment. 간결 경로의 최종 RELEASE는 위의 일치하는 `CLOSED.release`로 표현 |
| PR, `Closes #N` | 선언한 저장소의 PR과 본문의 closing reference `Closes #N` |
| `[PRODUCT COMPLETE]`의 `product-complete:` JSON | Issue·PR 번호를 넣은 `{"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40자리 SHA"}` |
| merged / closed | PR merged 상태와 merge commit, Issue closed 상태 |
| CI | 저장소의 required checks. 실제 검증 명령은 P가 선언 |

GitHub 쓰기 권한·토큰·secret은 P와 사람이 관리한다. Agent는 토큰을 만들거나 조회하거나 등록하지 않는다.

코드 원격·신규 lane 기준·PR base는 P tracker.md의 git.remote/base_branch/merge_branch 선언을 따른다. PR 생성 시 base를 명시하고 기본 브랜치를 추측하지 않는다. SDD 게시 저장소·원격·branch는 review 선언을 따르며 제품 PR head나 claim branch와 구분한다. 외부 ID 설정은 GitHub의 실제 발급 ID나 closing reference 문법을 바꾸지 않으며 다른 서비스의 API adapter를 제공하지 않는다.
