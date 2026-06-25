import { NextRequest, NextResponse } from "next/server";
import { getSql } from "@/lib/db";
import { RequirementsRecord } from "@/lib/types";

export async function POST(req: NextRequest) {
  let record: RequirementsRecord;
  try {
    record = await req.json();
  } catch {
    return NextResponse.json({ ok: false, message: "Invalid JSON body" }, { status: 400 });
  }

  if (!process.env.DATABASE_URL) {
    return NextResponse.json(
      { ok: false, message: "Database not configured. Your PDF download is still available." },
      { status: 503 }
    );
  }

  try {
    const sql = getSql();
    await sql`
      INSERT INTO project_requirements (
        submitted_at, version_control, ide, code_push,
        deployment, architecture, design_patterns, orm,
        additional_requirements
      ) VALUES (
        ${record.submitted_at ?? new Date().toISOString()},
        ${record.version_control ?? ""},
        ${record.ide ?? ""},
        ${record.code_push ?? ""},
        ${record.deployment ?? ""},
        ${record.architecture ?? ""},
        ${record.design_patterns ?? ""},
        ${record.orm ?? ""},
        ${record.additional_requirements ?? ""}
      )
    `;
  } catch (err) {
    console.error("Failed to insert requirements record:", err);
    return NextResponse.json(
      { ok: false, message: `Database error: ${(err as Error).message}` },
      { status: 500 }
    );
  }

  return NextResponse.json({ ok: true, message: "Requirements saved successfully." });
}
