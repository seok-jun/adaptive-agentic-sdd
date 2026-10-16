# 작업 관리 방식: 로컬 문서

이 문서는 W 절차의 Issue·댓글·라벨·assignee·PR·closing reference 표현을 **저장소 밖 공유 폴더의 작업 문서**로 실현하는 방법이다. P 적용 문서 `tracker.md`가 이 방식을 선언하고 `tracker_root`(절대 경로)와 ID 형식을 정한다. W 문서를 읽을 때 아래 대응표로 바꿔 읽는다. 대응표에 없는 GitHub 기능을 전제하는 절차는 실행하지 않고 `BLOCKED: tracker operation unsupported`로 멈춘다.

## 왜 저장소 밖 공유 폴더인가

병렬 lane은 서로 다른 worktree와 branch에서 일한다. claim과 작업 기록이 한 lane의 branch에만 있으면 다른 lane이 볼 수 없다. 그래서 작업 문서와 claim은 모든 worktree가 같은 절대 경로로 읽고 쓰는 `tracker_root`에 둔다. `tracker_root`는 어느 lane의 worktree 안에도 두지 않는다. 이력이 필요하면 `tracker_root`를 별도 git 저장소로 두고 기록할 때마다 commit할 수 있다(P 선언).

## 폴더 구조

```text
<tracker_root>/
  items/<ID>.md        작업 문서(= Issue)
  claims/<ID>.claim    활성 claim(= [CLAIM] + assignee + status:in-progress)
  index.md             선택. 사람이 보는 목록. 원본은 items/
```

## 대응표

| W 절차의 표현 | 로컬 문서 방식 |
| --- | --- |
| Issue 생성 | `items/<ID>.md`를 **이미 있으면 실패하는 방식**으로 만든다. ID 충돌이면 다음 ID로 다시 시도한다 |
| Issue 번호 `#N` | `<ID>` |
| Issue body | 작업 문서의 `## 메타`와 `## 기록`을 뺀 본문 section |
| `priority:*`, `grade:*`, `status:*` 라벨 | `## 메타`의 `priority:`, `grade:`, `status:` 줄. 각각 정확히 하나 |
| assignee | `## 메타`의 `담당:` 줄 |
| Issue 댓글 | `## 기록`에 덧붙이는 항목. 아래 "기록 항목" 형식 |
| 댓글 URL / ID | `items/<ID>.md#<항목 id>` |
| 댓글 `updated_at` | 항목의 `작성` 시각. 항목은 수정하지 않으므로 작성 시각이 곧 갱신 시각이다 |
| `[CLAIM]` | `claims/<ID>.claim`을 이미 있으면 실패하는 방식으로 만들고, 같은 내용을 `## 기록`에 남긴다 |
| `[RELEASE]` | `## 기록`에 `[RELEASE]`를 남긴 뒤 `claims/<ID>.claim`을 지운다 |
| open PR | 아직 main에 병합되지 않은 해당 작업의 branch |
| PR head / base SHA | branch head SHA / 병합 대상 main SHA |
| PR body의 `Closes #N` | `[IMPLEMENTATION SUMMARY]` 항목의 `closes: <ID>` 줄 |
| PR mergeability | `git merge-tree --write-tree origin/main <branch>`(Git 2.38 이상)의 종료 코드 0이면 충돌 없음. 쓸 수 없으면 disposable worktree에서 병합을 시도하고 결과만 기록한 뒤 버린다 |
| PR merge | P 적용 문서 `tracker.md`의 `병합 방법`(merge·squash·rebase)으로 branch를 `origin`의 main에 병합하고 push한다. 병합 주체는 P의 사람 판단 지점을 따른다. 병합한 쪽이 `## 기록`에 `[MERGED]` 항목(`branch:`, `head:` branch head SHA, `main:` 병합 결과 main SHA, `method:`)을 남긴다. 병합 방법이 미정이면 `BLOCKED: tracker operation unsupported` |
| merged 확인 | `git fetch origin main` 뒤, `merge`면 `git merge-base --is-ancestor <branch head> origin/main`이 성공해야 한다. `squash`·`rebase`면 branch head가 main에 없으므로 `[MERGED]`의 `main:` SHA가 `origin/main`의 조상이고 그 commit 메시지가 작업 ID를 담는지 확인한다. 확인한 origin/main SHA를 기록한다 |
| CI | P 적용 문서 `build.md`의 `## 검증 기준`이 정한 로컬 명령. CI가 있으면 같은 문서의 `CI`가 함께 선언 |
| PR 기반 review candidate publication | W 그대로 Issue branch를 `origin`에 push하고 exact SHA를 기록한다. 작업 관리 방식은 이 단계를 바꾸지 않는다 |
| Issue closed (병합 뒤 자동 종료) | GitHub의 자동 종료에 해당하는 동작이 없으므로, merged 확인 뒤 종료 절차를 수행하는 Agent가 `## 메타`의 `status: closed`와 `종료:` 시각을 쓰고 `## 기록`에 `[CLOSED]` 항목(`by-merge: <main SHA>`)을 남긴다. `[IMPLEMENTATION SUMMARY]`의 `closes:`가 이 작업 ID일 때만 한다 |
| Issue not-planned | `## 메타`의 `status: not-planned`와 `종료:` 시각, `## 기록`의 사유 항목 |
| `[PRODUCT COMPLETE]`의 `product-complete:` JSON | `{"schema_version":1,"issue":"<ID>","pull_request":null,"branch":"<branch>","head":"<branch head SHA>","merge_commit":"<[MERGED]의 main SHA>"}` |
| 댓글 갱신(예: 같은 `[IMPLEMENTATION SUMMARY]`를 갱신) | 이전 항목을 고치지 않고 같은 태그의 새 항목을 덧붙이며 `supersedes: <이전 항목 id>`를 적는다. 같은 태그에서 다른 항목이 대체하지 않은 가장 최근 항목이 현재 값이다. 최초 항목은 그대로 남아 W의 "최초 원본 보존"을 충족한다 |
| Issue 검색·중복 확인 | `items/`의 제목·메타·본문 검색. 검색 범위와 결과 수를 보고한다 |
| reopen | `status:`를 다시 열고 `## 기록`에 `[REOPEN]`을 남긴다. 이전 종료 기록은 지우지 않는다 |

## 코드 원격

로컬 문서 방식은 Issue·댓글·라벨·PR 표현만 바꾼다. git 절차는 그대로라서 W의 `git fetch origin main`, Issue branch push, review candidate publication에 코드 원격 `origin`이 필요하다. 회사 git 서버가 있으면 그것을 쓴다. 원격이 없는 저장소는 저장소 밖 로컬 디스크에 bare 저장소를 만들어 `origin`으로 둘 수 있다(`git init --bare <경로>` 뒤 `git remote add origin <경로>`, `git push -u origin main`). 이 경우 reviewer도 같은 경로를 읽을 수 있어야 한다.

## 작업 문서 형식

```markdown
# <ID> <제목>

## 메타
priority: P2
grade: Small
status: open
담당: 없음
생성: 2026-10-19T09:00:00+09:00

<!-- 아래는 W process/issue-priority.md의 신규 Issue 필수 본문 -->
## Priority
...
## 완료 기준
- [ ] ...

## 기록
```

`## 메타`의 값과 본문의 `## Priority`·`## SDD grade` 값은 항상 같아야 한다(W의 본문–라벨 일치 규칙).

## 기록 항목

`## 기록`은 **덧붙이기만** 한다. 이미 쓴 항목을 고치거나 지우지 않는다. 잘못 쓴 항목은 새 항목으로 정정하고 원 항목 id를 가리킨다.

```markdown
### r-20261019T091500-a1 [CLAIM]
작성: 2026-10-19T09:15:00+09:00
작성자: <agent 또는 사람 식별>

agent: <agent-id>
branch: <branch-name>
allowed:
- <path glob>
forbidden:
- <path glob>
```

- 항목 id는 `r-<UTC 시각>-<짧은 임의값>` 형식이다. 같은 문서 안에서 중복되면 다시 만든다.
- 첫 줄 태그(`[CLAIM]`, `[RELEASE]`, `[IMPLEMENTATION SUMMARY]`, `[PRODUCT COMPLETE]`, `[LOCAL CLEANUP]`, `[HUMAN DECISION REQUIRED]`, `[OBSERVATION REVIEW]`, `[WORKFLOW][TOKEN ...]` 등)는 W 절차의 댓글 태그를 그대로 쓴다.
- W의 대화 내용 금지 gate는 기록 항목에도 그대로 적용한다.

## 동시성

- claim은 `claims/<ID>.claim`을 **이미 있으면 실패하는 생성**으로 만든다. PowerShell `New-Item -ItemType File`(이미 있으면 오류), Python `open(path, "x")`처럼 원자적 생성 실패를 확인할 수 있는 방법을 쓴다. 실패하면 이미 claim된 것이다.
- claim 파일 내용은 `[CLAIM]` 기록 항목의 본문과 같다(`agent:`, `branch:`, `allowed:`, `forbidden:`). 생성과 같은 쓰기에서 내용을 채운다. 비었거나 읽을 수 없는 claim 파일은 다른 lane의 claim으로 보고 겹침으로 취급한다.
- 이 방식은 로컬 디스크나 SMB 공유 폴더에서만 쓴다. OneDrive·Dropbox 같은 동기화 폴더는 원자적 생성과 즉시 반영을 보장하지 않으므로 `tracker_root`로 쓰지 않는다.
- 경로 겹침 확인은 `claims/*.claim` 전체의 allowed와 현재 작업의 allowed를 비교한다. claim 생성 뒤 다시 읽어 경쟁 claim이 있으면 W 절차대로 즉시 release한다.
- 작업 문서에 덧붙일 때는 파일 전체를 다시 쓰지 않고 덧붙이기 모드로 항목 하나를 한 번에 쓴다(PowerShell `Add-Content -Encoding utf8`, Python `open(path, "a", encoding="utf-8")`). 파일 전체를 다시 쓰면 다른 Agent가 그 사이에 덧붙인 항목을 잃는다. 다른 Agent의 항목을 덮어쓰지 않도록 쓰기 직전에 파일을 다시 읽고, 쓴 뒤 자기 항목 id가 있는지 확인한다.
- 같은 작업 문서를 두 Agent가 동시에 고쳐야 하는 절차는 없다. 본문과 `## 메타` 수정은 claim을 가진 lane(claim이 없으면 작업 항목 정리를 맡은 Agent)만 하며, 그때만 파일 전체를 다시 쓴다.

## 실패와 한계

- `tracker_root`에 접근할 수 없거나 쓰기에 실패하면 `BLOCKED: tracker unavailable`로 의존 작업을 멈춘다. 저장소 안이나 다른 임의 위치로 우회 저장하지 않는다.
- 공유 폴더는 GitHub처럼 작성자 인증·권한을 강제하지 않는다. 작성자 식별은 자기 보고이며, W의 "허용 작성자" 조건은 P가 선언한 식별 값과의 일치로만 확인한다.
- 로컬 파일은 원격 백업이 없다. P가 `tracker_root`를 git 저장소로 두지 않으면 기록 유실을 복구할 수 없다는 한계를 남긴다.
