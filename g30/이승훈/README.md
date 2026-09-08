# G30 · 이승훈 학생 — 소피아(조치)대학 지원 정리 (A4 2페이지)

소피아대학 국제교양학부(FLA) 2027년 4월 입학 2차 전형 준비 자료입니다.

| 파일 | 내용 |
| --- | --- |
| `sophia_a4.html` | A4 2페이지 레이아웃 원본 (페이지당 1240 × 1754 CSS px = A4 @150dpi) |
| `이승훈_소피아대학_A4_1p_학생정보-일정.jpg` | 1p — 학생 정보 · 소피아 전형 일정 · FLA 필요서류 · 전체 지원 일정 |
| `이승훈_소피아대학_A4_2p_에세이과제.jpg` | 2p — Personal Statement / Self-Reflective Essay 원문 · 진행 관리 |

각 JPG는 2480 × 3508 px (A4 300dpi).

## 다시 만드는 방법

Noto Sans KR 폰트를 `/tmp/fonts/NotoSansKR-{regular,medium,bold}.ttf` 에 두고:

```bash
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1240,3508 \
  --screenshot=sophia_all.png "file://$PWD/sophia_a4.html"

python3 - <<'PY'
from PIL import Image
im = Image.open('sophia_all.png').convert('RGB')
names = ['이승훈_소피아대학_A4_1p_학생정보-일정.jpg', '이승훈_소피아대학_A4_2p_에세이과제.jpg']
for i, n in enumerate(names):
    im.crop((0, 3508*i, 2480, 3508*(i+1))).save(
        n, 'JPEG', quality=95, subsampling=0, dpi=(300, 300), optimize=True)
PY
```

페이지를 늘리려면 `<div class="page">` 블록을 추가하고 `--window-size` 높이를 `1754 × 페이지수` 로,
크롭 반복 횟수를 페이지수만큼 늘리면 됩니다.

## 데이터 출처

- 학생 정보 : TIS G30 컨설팅 어드민 페이지 (생년월일 · 연락처 · 카카오톡 · 이메일 · 지원 대학 · 리포팅 현황)
  - TOEFL·IELTS **5.0** (2026.08.29 취득 / R 5.0 · L 5.5 · S 5.0 · W 5.0), SAT **1330** (2026.08.22 취득) 은 별도 전달값
- 전형 일정 / 타 대학 일정 : Notion `팀스페이스 홈 / G30 / 이승훈 학생`
- 소피아 FLA 필요서류 및 에세이 문항 : 소피아 FLA 필요서류(04 2차) 요강

## 참고

에세이 수업 계획(수업일 · 에세이 완성일 · 워드수)은 요청에 따라 시트에서 제외했습니다.
전체 지원 일정표의 `에세이 완성` 열도 같은 이유로 함께 삭제했습니다.
소피아 제출물은 **Personal Statement 최대 300단어 + Self-Reflective Essay 최대 400단어 (총 2편)** 입니다.
