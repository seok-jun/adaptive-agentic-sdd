# PR #6 macOS 핸드오프 실행 결과 — 2026-10-31

macOS 12.7.6 / Intel x86_64, Python 3.14.10, Apple Git 2.37.1, Codex CLI 0.166.0 환경에서 실행했다. Claude CLI와 `python` 명령은 없었다.

핸드오프: PR head `2900393c7b33b1775c6e3c62d35256df9c7e756e`의 `docs/handoff/macos-first-use/`. 설치 대상은 지정된 `1d91d9448621c29e39c248bf1c1f23a098ecb02d`. 두 커밋의 English bundle Git tree는 `a37222e3fa8a64cdc5a83fef2e9829ba3fc90f50`으로 같았다.

## 1. A/B/C 결과와 증거

| 단계 | 결과 | 증거 |
| --- | --- | --- |
| A 설치·commit·push | done, Python 명령 수동 대체 | `python ... init`은 exit 127, `command not found: python`. `python3 -I -B ... init/render/check/check-evals`로 진행. check: `OK pinned copy, lock, and generated files match`; check-evals: `83 case(s), 4 skill(s), 0 problem(s)`. 설치 commit `112634744db1f6347e228fb31d4c8aa51296657c`, 로컬 origin/main push 성공 |
| B Small 작업·종료 | done | T-1 / P2 / Small. claim과 별도 worktree 확보 후 `catalog/search.py`의 `end = start + size`로 수정. `tests/catalog/test_search.py`에 회귀 테스트 추가. 수정 전 회귀 테스트 실패, 수정 후 catalog 3개/전체 4개 통과. 제품 commit `23ac44ca912e7d48dbd2cfba27faa239d43242dc`, merge `27e71bd1f8f103fc9fc6cace3f34ae3ed1803c0e`. 로컬 origin push·fetch·ancestor 검사 성공. T-1 closed, PRODUCT COMPLETE, claim 해제·worktree 제거 확인 |
| C 설치 되돌리기 | done | 설치 commit을 `git revert --no-edit` 후 로컬 origin/main에 push. revert `2e8a9b084dc715d7d14b1bfa8de8337f22d806dd`. 초기 commit과 비교하면 제품 파일 2개만 변경. 기존 AGENTS.md 복원, 설치 경로 5개 모두 부재. 최종 제품 테스트 4개 통과, 작업 트리 clean |

증거 파일:

- [final-state.log](final-state.log): 핸드오프 요청의 git log, ls-remote, status, 코드, 테스트, tracker 출력.
- [tracker/items/T-1.md](tracker/items/T-1.md): 시작·claim·검증·summary·merge·종료·정리 기록. claims/는 비었다.
- [regression-before.log](regression-before.log), [module-after.log](module-after.log), [final-candidate.log](final-candidate.log).
- [installation-files.tsv](installation-files.tsv). 설치 lock과 project draft 원본은 로컬 실행 폴더에만 보관했다.

원격 제품 작업은 테스트용 `remote.git`에만 수행했다. 공개 GitHub 저장소에는 push·댓글·PR 변경을 하지 않았다.

## 2. 저장소 테스트와 안내의 마찰

`python3 -I -B -m unittest discover -s tests`:

- 소스와 필요한 과거 commit 메타데이터 복원 후: **Ran 88 tests in 16.158s; FAILED (failures=2)**. 같은 테스트 `test_generated_external_commands_execute_with_literal_paths`의 check/check-evals 두 subtest가 `/bin/sh: python: command not found`로 실패했다. 다른 ERROR는 없었다.
- 대조 실행: 테스트 프로세스의 PATH에만 `python -> 설치된 python3` 임시 symlink 디렉터리를 추가했다. 소스 수정 없이 **Ran 88 tests in 16.237s; OK**. 셸 프로필이나 시스템 Python은 변경하지 않았다.
- 로그: `repository-tests-native.log`, `repository-tests-native-last15.log`, `repository-tests-python-compat.log`.

확인된 마찰:

1. README: `Run: python -I -B .adaptive-sdd/tools/install.py init --project-root .`. 이 환경에서 그대로 실행하면 exit 127. Python 3은 존재하므로 `python3`로 바꾸어 설치를 계속했다. 설치 후 생성된 AGENTS/skill/check 명령도 `python`을 사용한다. 같은 run에서 `python3`로 동일한 설치 검사를 이미 통과했으므로 그 결과를 재사용했다. `BLOCKED: pinned workflow unavailable`로 종료한 실행은 아니다. 새 세션에서의 자동 대응은 측정하지 않았다.
2. 가이드 1절: `Windows PowerShell example:`만 제공한다. POSIX에서 bundle 복사에 `cp -R`을 사용했다. bundle 66개 manifest 대상 해시는 모두 일치했다.
3. 핸드오프: `Git 2.38 이상`. 실제 Git은 2.37.1이고 `merge-tree --write-tree`가 없다. local-docs adapter에 이미 명시된 임시 worktree merge 대안을 사용했다. 충돌 없이 merge 시도 후 abort·worktree 제거 성공. 이는 실행 차단이 아니었다.
4. 프로젝트 JSON 작성 중 agent가 `build.verification`의 `command`/배열과 `modules.list` 문자열 형태를 잘못 추측했다. render가 schema 오류를 내며 차단했고, `commands` 문자열과 `{path, role}` 객체로 고쳐 통과했다. 이 시행착오는 제품 결함으로 판정하지 않는다.

확인된 Python 마찰의 수정 후보는 README/가이드와 생성 명령에서 Python 3 실행 파일을 일관되게 선택하게 하는 것이다. 원본 방법론·평가 실행기는 수정하지 않았다.

## 3. BLOCKED·권한·실행 조건과 한계

- `git clone https://github.com/seok-jun/adaptive-agentic-sdd.git`은 `Could not resolve host: github.com`으로 실패했다. GitHub connector로 PR, 핸드오프, 고정 SHA의 tree/blob를 받아 `<source-root>`에 소스를 복원했다. 이는 archive 다운로드를 그대로 수행한 첫 경험이 아니다.
- 복원 소스는 로컬 snapshot commit이며 원본 Git history 전체를 가진 clone이 아니다. 최초 테스트의 누락 fixture/Git 오류는 준비 결함으로 구분했다. 모든 소스 파일과 fixture를 보완하고, paired test에 필요한 두 과거 commit metadata를 API에서 얻어 원본 Git SHA와 일치하는 bytes로 복원한 뒤 native 결과를 다시 측정했다. 과거 commit의 tree/history 전체를 복원한 것은 아니다.
- Claude는 설치되어 있지 않아 Claude 실행은 not done. 이 세션의 Codex가 walkthrough를 수행했다. 별도 CLI 세션/모델 API 호출은 하지 않았다.
- 이 agent는 알려진 의심 지점을 미리 읽었다. 따라서 **blind first-use 결과가 아닌 assisted walkthrough**다. 성공률·절차 효과·모델 성능 근거로 일반화하지 않는다.
- 실제 사용자 권한 확인 요청은 0회. 테스트용 `.agents/`, `.git` 쓰기, 로컬 bare remote push, worktree 작업은 이번 환경에서 성공했다. 이 결과를 다른 Codex sandbox의 쓰기 가능성으로 일반화하지 않는다.
- 별도 사용자 답변이 필요한 미해결 제품 결정은 없었다. 핸드오프의 명시된 설정과 한 작업의 merge/push 허용을 사용했다.

## 4. 설치 변경 파일과 Undo 잔여물

설치 commit의 전체 목록은 `installation-files.tsv`에 있다. `.adaptive-sdd/`, 양쪽 도구 skill 입구 8개, `.gitattributes`, CLAUDE.md가 추가되고 기존 AGENTS.md에 block이 추가됐다.

준비 스크립트의 첫 테스트가 만든 `__pycache__` 파일 9개도 agent의 `git add -A`로 설치 commit에 잘못 포함됐다. 이는 agent의 staging 실수다. 이후 테스트에는 프로세스 한정 `PYTHONDONTWRITEBYTECODE=1`을 사용했다. Undo가 해당 9개도 제거했고 최종 제품 diff에는 bytecode가 없다.

Undo 후 main의 `.adaptive-sdd/`, `.agents/`, `.claude/`, `.gitattributes`, CLAUDE.md는 전부 없다. AGENTS.md는 초기 내용과 같다. tracker와 보고서·로그는 저장소 바깥에 의도대로 남아 있다. 로컬/remote의 작업 branch는 보존했으며 그 branch에는 설치가 남는다. README가 설명한 branch별 Undo 동작과 일치한다. 등록된 worktree는 sample 하나뿐이다.

## 5. B에서 읽은 방법론 파일 수와 관찰 한계

중복을 제외하면 약 30개(공통 절차·생성 프로젝트 문서·skill 입구·AGENTS 포함)를 읽었다. 일부 큰 출력이 잘려 재조회했고 필요 이상으로 넓게 읽은 구간이 있었다. 토큰/비용은 수집하지 않았다.

작업 기록의 `r-start` 등 entry ID는 adapter가 요구하는 UTC+random 형식 대신 읽기 쉬운 축약 ID를 사용했다. 별도 모호한 모델명·실제 제공 모델·비용은 만들어 기록하지 않았다. ordered-changes support의 직접 원문 조회는 구현 뒤에 이루어졌고, 그 전에 Issue의 대상·검증 mapping을 사용했다. 따라서 전체 방법론 준수나 control 효과가 완전히 검증됐다고 주장하지 않는다.
