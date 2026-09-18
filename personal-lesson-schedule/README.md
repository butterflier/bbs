# 개인수업 시간표 (personal-lesson-schedule)

교사 한 명 기준으로 **월~일 7일 전체**의 개인수업을 실제 시간에 비례해 보여 주는 Cloudflare Worker 앱.
[교실 사용 현황표(classroom-schedule)](https://classroom-schedule.butterflier-v.workers.dev/)와 같은 원리이되,
교실 단위가 아니라 사람 단위이고 주말까지 다룬다.

- 조회: 링크만 있으면 누구나, 로그인 없이 실시간 조회
- 등록·수정·삭제: 공유 비밀번호(`SHARED_PASSWORD`) 필요
- 사람이 두 명 이상 등록되면 상단에 `전체 / 사람별` 필터 버튼이 자동으로 나타남 (한 명이면 숨김)

## 구조

```
wrangler.jsonc     Worker 설정 (D1 바인딩 DB, 정적 자산 ./public)
schema.sql         D1 스키마 (lessons 테이블)
src/index.ts       /api/* 만 처리하는 Worker. 나머지는 ASSETS가 서빙
public/index.html  한 파일짜리 vanilla JS 앱 (화면 + 렌더링 + 폼)
public/fonts/      Paperlogy woff2 4종 (Regular/Medium/SemiBold/Bold)
```

### 렌더링 방식

classroom-schedule과 동일하게, 수업 블록을 테이블 셀에 넣지 않고 **요일 컬럼 안에 절대위치로** 그린다.
`top = (시작분 - 표시시작분) × (62px / 60분)`, `height = 수업길이 × 같은 비율`.

- 요일 인덱스는 **월=0 … 일=6** (`DOW_LABELS`). JS `Date.getDay()`(일=0)와 다르니 변환해서 쓴다.
- 표시 시간 범위는 기본 09:00–22:00이며, 그보다 이르거나 늦은 수업이 있으면 자동으로 늘어난다.
- 같은 요일에 시간이 겹치는 수업은 겹치는 것끼리 묶어 가로로 나눠 배치한다.
- 왼쪽 시간축 컬럼은 `position: sticky; left: 0; z-index: 30` — 수업 블록(`z-index: 10`)보다 **반드시 높아야** 가로 스크롤 시 가려지지 않는다. (classroom-schedule에서 한 번 겪은 버그)

### 디자인 시스템

TIS 교사 페이지 / classroom-schedule과 동일: Paperlogy 폰트, 흰 배경, 모서리 반경 4px 캡,
box-shadow 전부 없음, 그리드선 1.4px `#DEE2E7`, 버튼은 개별 테두리 + 활성 시 accent(`#2F6FEB`) 채움.

## 배포

```bash
npm install

# 1) D1 생성 후, 출력되는 database_id를 wrangler.jsonc의 REPLACE_WITH_DATABASE_ID에 넣는다
npx wrangler d1 create personal-lesson-schedule-db

# 2) 스키마 적용 (원격)
npm run db:init

# 3) 공유 비밀번호 설정 — 이게 없으면 등록/수정/삭제가 전부 401
npx wrangler secret put SHARED_PASSWORD

# 4) 배포
npx wrangler deploy
```

로컬 확인은 `npm run db:init:local` 후 `npx wrangler dev`.
로컬에서 비밀번호를 쓰려면 `.dev.vars` 파일에 `SHARED_PASSWORD=...` 를 넣는다 (git에 커밋하지 말 것).

## API

| 메서드 | 경로 | 비밀번호 | 설명 |
| --- | --- | --- | --- |
| GET | `/api/lessons` | 불필요 | `{ lessons: [...], persons: [...] }` |
| POST | `/api/lessons` | 필요 | 수업 1건 등록 |
| PUT | `/api/lessons/:id` | 필요 | 수업 수정 |
| DELETE | `/api/lessons/:id` | 필요 | 수업 삭제 |

쓰기 요청은 비밀번호를 JSON 본문의 `password` 필드로 보낸다.
화면에서 요일을 여러 개 골라 등록하면 프런트가 요일 수만큼 POST를 반복 호출한다.

수업 레코드: `person`(이름), `title`(수업명/학생명), `subject`, `dow`(0~6), `start_min`, `end_min`(자정 기준 분), `location`, `memo`.

## 폰트

`public/fonts/`의 Paperlogy woff2는 <https://github.com/fonts-archive/Paperlogy> 에서 가져왔다.
폰트가 없어도 시스템 한글 폰트로 fallback 되지만, 디자인 통일을 위해 함께 배포한다.
