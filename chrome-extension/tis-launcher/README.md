# TIS 교무 런처 (크롬 새 탭 확장)

크롬 새 탭을 수업 도구 · TIS 교사용 대시보드 링크 보드로 바꾸는 확장 프로그램입니다.

## 설치 (git 방식 · 권장)

```bash
cd ~/Documents                 # 윈도우 명령 프롬프트라면:  cd %USERPROFILE%\Documents
git clone https://github.com/butterflier/bbs.git
cd bbs
git checkout claude/intelligent-clarke-li1uhy
```

그 다음 크롬에서:

1. 주소창에 `chrome://extensions`
2. 오른쪽 위 **개발자 모드** 켜기
3. **압축해제된 확장 프로그램을 로드** 클릭
4. `bbs/chrome-extension/tis-launcher` 폴더 선택
5. 새 탭을 열면 런처가 뜹니다.

> 이 폴더를 지우거나 옮기면 확장이 비활성화됩니다.

## 업데이트

내용이 바뀌면:

- macOS — `update.command` 더블클릭
- Windows — `update.bat` 더블클릭
- 또는 폴더에서 `git pull`

그리고 `chrome://extensions`에서 이 확장의 **새로고침(↻)** 버튼을 누르면 반영됩니다.

## 링크 직접 수정

`newtab.html`의 `<a class="tile">` 블록을 복사·수정한 뒤 확장을 새로고침하세요.

```html
<a class="tile" href="https://example.com/">
  <span class="name">표시할 이름</span>
  <span class="arrow" aria-hidden="true">↗</span>
  <span class="host">example.com</span>
</a>
```

구획 제목 옆의 `count`(예: `06`)와 머리말의 `링크 10 · 구획 2`도 함께 고쳐주세요.

## 구성

| 파일 | 역할 |
| --- | --- |
| `manifest.json` | 확장 정의 (`chrome_url_overrides.newtab`) |
| `newtab.html` | 새 탭 화면 · 링크 목록 |
| `styles.css` | 라이트/다크 팔레트와 레이아웃 |
| `icons/` | 확장 아이콘 16/48/128px |
| `update.command` / `update.bat` | 최신 버전 내려받기 |

## 새 탭 말고 시작 페이지로만 쓰려면

확장 없이도 됩니다. 크롬 **설정 → 시작 그룹 → 특정 페이지 열기**에 아래 주소를 넣으세요.

https://claude.ai/code/artifact/4f5fb1af-a385-4a9e-943a-c72cfd34de47
