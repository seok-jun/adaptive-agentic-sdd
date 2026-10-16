# 작업 관리 방식: GitHub

이 문서는 W 절차의 Issue·댓글·라벨·assignee·PR·closing reference 표현을 **GitHub Issue와 PR**로 실현하는 방법이다. W 절차는 이 방식에서 처음 다듬어졌으므로 표현이 그대로 대응한다. P 적용 문서 `tracker.md`가 이 방식을 선언하고 저장소(`owner/name`)와 허용 작성자를 정한다.

| W 절차의 표현 | GitHub |
| --- | --- |
| Issue, `#N` | 선언한 저장소의 GitHub Issue |
| `priority:*`, `grade:*`, `status:*` 라벨 | 같은 이름의 Issue 라벨 |
| assignee | Issue assignee |
| Issue 댓글, URL, `updated_at` | Issue comment와 그 URL·`updated_at` |
| `[CLAIM]` / `[RELEASE]` | 해당 태그로 시작하는 Issue comment |
| PR, `Closes #N` | 선언한 저장소의 PR과 본문의 closing reference |
| merged / closed | PR merged 상태와 merge commit, Issue closed 상태 |
| CI | 저장소의 required checks. 실제 검증 명령은 P가 선언 |

GitHub 쓰기 권한·토큰·secret은 P와 사람이 관리한다. Agent는 토큰을 만들거나 조회하거나 등록하지 않는다.
