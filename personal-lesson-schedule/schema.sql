-- 개인수업 시간표 (personal-lesson-schedule)
-- dow: 0=월 1=화 2=수 3=목 4=금 5=토 6=일
-- start_min / end_min: 자정 기준 분 단위 (예: 09:30 -> 570)

CREATE TABLE IF NOT EXISTS lessons (
  id          TEXT PRIMARY KEY,
  person      TEXT NOT NULL,
  title       TEXT NOT NULL,
  subject     TEXT,
  dow         INTEGER NOT NULL CHECK (dow BETWEEN 0 AND 6),
  start_min   INTEGER NOT NULL CHECK (start_min BETWEEN 0 AND 1440),
  end_min     INTEGER NOT NULL CHECK (end_min BETWEEN 0 AND 1440),
  location    TEXT,
  memo        TEXT,
  created_at  TEXT NOT NULL,
  updated_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_lessons_person_dow ON lessons (person, dow, start_min);
