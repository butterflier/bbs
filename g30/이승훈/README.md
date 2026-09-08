# G30 · 이승훈 학생 — 소피아(조치)대학 지원 정리 A4

Notion 페이지 `팀스페이스 홈 / G30 / 이승훈 학생` 의 내용을 바탕으로
학생 정보 · 소피아 대학 스케쥴 · 상세 정보(필요서류/주의사항)를 A4 한 장으로 정리한 자료입니다.

| 파일 | 설명 |
| --- | --- |
| `sophia_a4.html` | A4 레이아웃 원본 (1240 × 1754 CSS px = A4 @150dpi) |
| `이승훈_소피아대학_A4정리.jpg` | 출력용 이미지 (2480 × 3508 px, A4 300dpi) |

## 다시 만드는 방법

Noto Sans KR 폰트를 `/tmp/fonts/NotoSansKR-{regular,medium,bold}.ttf` 에 두고:

```bash
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1240,1754 \
  --screenshot=sophia_a4.png "file://$PWD/sophia_a4.html"

python3 -c "from PIL import Image; \
Image.open('sophia_a4.png').convert('RGB').save('이승훈_소피아대학_A4정리.jpg', \
quality=95, subsampling=0, dpi=(300,300), optimize=True)"
```

## 참고

- 생년월일 / 연락처 / SAT 최고점 / 리포팅 대학명은 Notion 원본에 값이 없어 `미기재`로 표기했습니다.
- `토플 최고점 4.5`는 Notion 원본(`현재 토플성적 최고점 : 4.5`)을 그대로 옮긴 값입니다.
