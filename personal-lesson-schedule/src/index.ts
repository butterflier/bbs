/**
 * 개인수업 시간표 (personal-lesson-schedule)
 *
 * - 정적 자산(public/)은 ASSETS 바인딩이 그대로 서빙한다.
 * - /api/* 만 이 Worker가 직접 처리한다.
 * - 조회는 누구나, 등록/수정/삭제는 공유 비밀번호(SHARED_PASSWORD)가 필요하다.
 */

export interface Env {
  DB: D1Database;
  ASSETS: Fetcher;
  SHARED_PASSWORD?: string;
}

interface LessonRow {
  id: string;
  person: string;
  title: string;
  subject: string | null;
  dow: number;
  start_min: number;
  end_min: number;
  location: string | null;
  memo: string | null;
  created_at: string;
  updated_at: string;
}

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

const bad = (message: string, status = 400) => json({ error: message }, status);

/** 길이가 달라도 비교 시간이 값에 덜 좌우되도록 한 상수시간 비교. */
function safeEqual(a: string, b: string): boolean {
  const ea = new TextEncoder().encode(a);
  const eb = new TextEncoder().encode(b);
  let diff = ea.length ^ eb.length;
  const len = Math.max(ea.length, eb.length);
  for (let i = 0; i < len; i++) diff |= (ea[i] ?? 0) ^ (eb[i] ?? 0);
  return diff === 0;
}

function checkPassword(env: Env, supplied: unknown): string | null {
  const expected = env.SHARED_PASSWORD;
  if (!expected) return "서버에 SHARED_PASSWORD가 설정되어 있지 않습니다. (wrangler secret put SHARED_PASSWORD)";
  if (typeof supplied !== "string" || !safeEqual(supplied, expected)) return "비밀번호가 올바르지 않습니다.";
  return null;
}

const MAX_TEXT = 200;

function cleanText(value: unknown, { required = false, max = MAX_TEXT } = {}): string | null | undefined {
  if (value === undefined || value === null) return required ? undefined : null;
  if (typeof value !== "string") return undefined;
  const trimmed = value.trim();
  if (!trimmed) return required ? undefined : null;
  if (trimmed.length > max) return undefined;
  return trimmed;
}

interface ParsedLesson {
  person: string;
  title: string;
  subject: string | null;
  dow: number;
  start_min: number;
  end_min: number;
  location: string | null;
  memo: string | null;
}

/** 입력 본문을 검증해 저장 가능한 형태로 만든다. 문자열을 돌려주면 그게 에러 메시지다. */
function parseLesson(body: Record<string, unknown>): ParsedLesson | string {
  const person = cleanText(body.person, { required: true, max: 40 });
  if (!person) return "이름(person)을 입력해 주세요.";

  const title = cleanText(body.title, { required: true, max: 60 });
  if (!title) return "수업/학생 이름(title)을 입력해 주세요.";

  const subject = cleanText(body.subject, { max: 40 });
  if (subject === undefined) return "과목(subject)이 올바르지 않습니다.";

  const location = cleanText(body.location, { max: 40 });
  if (location === undefined) return "장소(location)가 올바르지 않습니다.";

  const memo = cleanText(body.memo, { max: 500 });
  if (memo === undefined) return "메모(memo)가 올바르지 않습니다.";

  const dow = Number(body.dow);
  if (!Number.isInteger(dow) || dow < 0 || dow > 6) return "요일(dow)은 0(월)~6(일) 사이여야 합니다.";

  const start = Number(body.start_min);
  const end = Number(body.end_min);
  if (!Number.isInteger(start) || start < 0 || start > 1440) return "시작 시간이 올바르지 않습니다.";
  if (!Number.isInteger(end) || end < 0 || end > 1440) return "종료 시간이 올바르지 않습니다.";
  if (end <= start) return "종료 시간은 시작 시간보다 늦어야 합니다.";

  return { person, title, subject, location, memo, dow, start_min: start, end_min: end };
}

async function readBody(request: Request): Promise<Record<string, unknown> | null> {
  try {
    const body = await request.json();
    return body && typeof body === "object" ? (body as Record<string, unknown>) : null;
  } catch {
    return null;
  }
}

async function listLessons(env: Env): Promise<Response> {
  const { results } = await env.DB.prepare(
    `SELECT id, person, title, subject, dow, start_min, end_min, location, memo, created_at, updated_at
       FROM lessons
      ORDER BY person, dow, start_min`,
  ).all<LessonRow>();

  const lessons = results ?? [];
  const persons = [...new Set(lessons.map((l) => l.person))];
  return json({ lessons, persons });
}

async function createLesson(request: Request, env: Env): Promise<Response> {
  const body = await readBody(request);
  if (!body) return bad("요청 본문이 올바른 JSON이 아닙니다.");

  const authError = checkPassword(env, body.password);
  if (authError) return bad(authError, 401);

  const parsed = parseLesson(body);
  if (typeof parsed === "string") return bad(parsed);

  const now = new Date().toISOString();
  const id = crypto.randomUUID();

  await env.DB.prepare(
    `INSERT INTO lessons (id, person, title, subject, dow, start_min, end_min, location, memo, created_at, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  )
    .bind(
      id,
      parsed.person,
      parsed.title,
      parsed.subject,
      parsed.dow,
      parsed.start_min,
      parsed.end_min,
      parsed.location,
      parsed.memo,
      now,
      now,
    )
    .run();

  return json({ id }, 201);
}

async function updateLesson(id: string, request: Request, env: Env): Promise<Response> {
  const body = await readBody(request);
  if (!body) return bad("요청 본문이 올바른 JSON이 아닙니다.");

  const authError = checkPassword(env, body.password);
  if (authError) return bad(authError, 401);

  const parsed = parseLesson(body);
  if (typeof parsed === "string") return bad(parsed);

  const result = await env.DB.prepare(
    `UPDATE lessons
        SET person = ?, title = ?, subject = ?, dow = ?, start_min = ?, end_min = ?, location = ?, memo = ?, updated_at = ?
      WHERE id = ?`,
  )
    .bind(
      parsed.person,
      parsed.title,
      parsed.subject,
      parsed.dow,
      parsed.start_min,
      parsed.end_min,
      parsed.location,
      parsed.memo,
      new Date().toISOString(),
      id,
    )
    .run();

  if (!result.meta.changes) return bad("해당 수업을 찾을 수 없습니다.", 404);
  return json({ id });
}

async function deleteLesson(id: string, request: Request, env: Env): Promise<Response> {
  const body = await readBody(request);
  if (!body) return bad("요청 본문이 올바른 JSON이 아닙니다.");

  const authError = checkPassword(env, body.password);
  if (authError) return bad(authError, 401);

  const result = await env.DB.prepare(`DELETE FROM lessons WHERE id = ?`).bind(id).run();
  if (!result.meta.changes) return bad("해당 수업을 찾을 수 없습니다.", 404);
  return json({ id });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (!url.pathname.startsWith("/api/")) {
      return env.ASSETS.fetch(request);
    }

    if (url.pathname === "/api/lessons") {
      if (request.method === "GET") return listLessons(env);
      if (request.method === "POST") return createLesson(request, env);
      return bad("허용되지 않는 메서드입니다.", 405);
    }

    const match = url.pathname.match(/^\/api\/lessons\/([0-9a-fA-F-]{36})$/);
    if (match) {
      const id = match[1];
      if (request.method === "PUT") return updateLesson(id, request, env);
      if (request.method === "DELETE") return deleteLesson(id, request, env);
      return bad("허용되지 않는 메서드입니다.", 405);
    }

    return bad("없는 경로입니다.", 404);
  },
} satisfies ExportedHandler<Env>;
