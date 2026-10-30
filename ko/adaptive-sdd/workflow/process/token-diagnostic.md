# Token diagnostic

`W/../project/sdd-workflow.md`의 `Token diagnostic mode`가 `ENABLED`일 때만 읽는다. 일반 적용·사건 관측은 [observations](observations.md)를 따르며 이 mode로 비활성화되지 않는다.

| 실제 lifecycle event | 읽을 절 |
| --- | --- |
| Issue 작업 시작 | [START](#start) |
| lane 밖의 상태가 필요한 중단 | [BLOCKED](#blocked) |
| 상태 변경 근거가 있는 재개 | [RESUME](#resume) |
| completed·not-planned 최종 종료 | [END](#end) |

## 안정화 기간 token diagnostic

mode 값은 명시한 `W/../project/sdd-workflow.md`에서 읽는다

이 mode는 workflow 안정화 기간의 한시적 계측이다. 약 20~30개 Issue 또는 약 2주간 표본을 모은 뒤 baseline을 검토하고, 유지 결정이 없으면 위 값을 `DISABLED`로 바꾼다. Skill은 위 P 적용 문서의 mode가 `ENABLED`일 때만 아래 checkpoint를 기록하므로 비활성화할 때 각 실행 절차를 다시 설계하지 않는다.

권위 있는 현재 run token total은 host의 authoritative goal tracker에서 lifecycle event 시점에 한 번만 조회한다. tracker 값이 없으면 숫자를 추정하거나 repository-wide 탐색·별도 분석을 하지 않고 checkpoint를 생략한다. 계측 성공 여부는 구현 의사결정, review, test, CI 범위와 완료 판정을 바꾸지 않는다.

Issue 댓글에 기록하는 token checkpoint는 다음 네 종류뿐이다. command별, 구현 단계별, review turn별 checkpoint는 만들지 않는다.

### START

유효한 claim과 grade gate를 통과해 실제 Issue 작업을 시작할 때 한 번 기록한다. 같은 Issue에 기존 `TOKEN START`가 있으면 새로 기록하지 않는다.

```text
[WORKFLOW][TOKEN START]
issue: #NNN
grade: Trivial | Small | Medium | Large
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

`completed`의 END는 제품 완료가 확인된 뒤 local cleanup과 별개로 기록한다. `not-planned`는 최종 종료가 확정된 시점에 기록한다. 기존 END가 있으면 재기록하지 않는다. tracker가 없으면 checkpoint만 생략하며 일반 관측·verification·review gate는 유지한다.
