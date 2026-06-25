import { NextRequest, NextResponse } from "next/server";
import { getSql } from "@/lib/db";

const fallbackTopicSuggestions: { topic: string; created_at: string }[] = [];
const MAX_FALLBACK_TOPICS = 100;

export async function GET() {
  if (!process.env.DATABASE_URL) {
    return NextResponse.json(fallbackTopicSuggestions, { status: 200 });
  }
  try {
    const sql = getSql();
    const rows = await sql`SELECT topic FROM topic_suggestions ORDER BY created_at DESC`;
    return NextResponse.json(rows);
  } catch (err) {
    console.error("Failed to fetch topics:", err);
    return NextResponse.json([], { status: 200 });
  }
}

export async function POST(req: NextRequest) {
  let body: { topic?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false, message: "Invalid JSON body" }, { status: 400 });
  }

  const topic = (body.topic ?? "").trim();
  if (!topic) {
    return NextResponse.json({ ok: false, message: "topic is required" }, { status: 400 });
  }

  if (!process.env.DATABASE_URL) {
    fallbackTopicSuggestions.unshift({ topic, created_at: new Date().toISOString() });
    if (fallbackTopicSuggestions.length > MAX_FALLBACK_TOPICS) {
      fallbackTopicSuggestions.length = MAX_FALLBACK_TOPICS;
    }
    return NextResponse.json({
      ok: true,
      message: "Saved in temporary in-memory storage for this server instance. Configure DATABASE_URL for persistent storage."
    });
  }

  try {
    const sql = getSql();
    await sql`INSERT INTO topic_suggestions (topic) VALUES (${topic})`;
  } catch (err) {
    console.error("Failed to insert topic suggestion:", err);
    return NextResponse.json(
      { ok: false, message: `Database error: ${(err as Error).message}` },
      { status: 500 }
    );
  }

  return NextResponse.json({ ok: true, message: "Suggestion saved successfully." });
}
