# 작업 관리 방식: GitHub

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
| `[CLAIM]` / `[RELEASE]` | 해당 태그로 시작하는 Issue comment |
| PR, `Closes #N` | 선언한 저장소의 PR과 본문의 closing reference `Closes #N` |
| `[PRODUCT COMPLETE]`의 `product-complete:` JSON | Issue·PR 번호를 넣은 `{"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40자리 SHA"}` |
| merged / closed | PR merged 상태와 merge commit, Issue closed 상태 |
| CI | 저장소의 required checks. 실제 검증 명령은 P가 선언 |

GitHub 쓰기 권한·토큰·secret은 P와 사람이 관리한다. Agent는 토큰을 만들거나 조회하거나 등록하지 않는다.

코드 원격·신규 lane 기준·PR base는 P tracker.md의 git.remote/base_branch/merge_branch 선언을 따른다. PR 생성 시 base를 명시하고 기본 브랜치를 추측하지 않는다. SDD 게시 저장소·원격·branch는 review 선언을 따르며 제품 PR head나 claim branch와 구분한다. 외부 ID 설정은 GitHub의 실제 발급 ID나 closing reference 문법을 바꾸지 않으며 다른 서비스의 API adapter를 제공하지 않는다.
