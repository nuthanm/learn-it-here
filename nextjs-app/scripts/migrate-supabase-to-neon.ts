#!/usr/bin/env ts-node
/**
 * One-time data migration: Supabase → Neon DB
 *
 * Copies all rows from the Supabase project_requirements and topic_suggestions
 * tables into the Neon database. Both are plain PostgreSQL so this is a
 * straightforward INSERT … SELECT via Node.js.
 *
 * Prerequisites:
 *   npm install -g ts-node   (or use: npx ts-node scripts/migrate-supabase-to-neon.ts)
 *
 * Environment variables required:
 *   SUPABASE_DB_URL  — Supabase direct connection string (not the anon API URL)
 *                      Format: postgresql://postgres:<password>@db.<ref>.supabase.co:5432/postgres
 *   NEON_DATABASE_URL — Neon connection string
 *                      Format: ******ep-xxx.region.aws.neon.tech/neondb?sslmode=require
 *
 * Usage:
 *   SUPABASE_DB_URL="..." NEON_DATABASE_URL="..." npx ts-node scripts/migrate-supabase-to-neon.ts
 *
 * The script is idempotent: it uses INSERT … ON CONFLICT DO NOTHING so re-running
 * it will not duplicate rows that were already migrated (matching by primary key).
 */

import { Client } from "pg";

async function migrate() {
  const supabaseUrl = process.env.SUPABASE_DB_URL;
  const neonUrl = process.env.NEON_DATABASE_URL;

  if (!supabaseUrl || !neonUrl) {
    console.error(
      "ERROR: Set SUPABASE_DB_URL and NEON_DATABASE_URL environment variables."
    );
    process.exit(1);
  }

  const source = new Client({ connectionString: supabaseUrl });
  const target = new Client({ connectionString: neonUrl });

  console.log("Connecting to Supabase (source)…");
  await source.connect();
  console.log("Connecting to Neon (target)…");
  await target.connect();

  try {
    // ── project_requirements ────────────────────────────────────────────────
    console.log("\nMigrating project_requirements…");
    const { rows: reqRows } = await source.query(
      `SELECT id, submitted_at, version_control, ide, code_push,
              deployment, architecture, design_patterns, orm,
              additional_requirements
       FROM project_requirements`
    );
    console.log(`  Found ${reqRows.length} rows in source.`);

    let reqInserted = 0;
    for (const row of reqRows) {
      const res = await target.query(
        `INSERT INTO project_requirements
           (id, submitted_at, version_control, ide, code_push,
            deployment, architecture, design_patterns, orm,
            additional_requirements)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
         ON CONFLICT (id) DO NOTHING`,
        [
          row.id,
          row.submitted_at,
          row.version_control,
          row.ide,
          row.code_push,
          row.deployment,
          row.architecture,
          row.design_patterns,
          row.orm,
          row.additional_requirements,
        ]
      );
      if (res.rowCount && res.rowCount > 0) reqInserted++;
    }
    console.log(`  Inserted ${reqInserted} new rows (${reqRows.length - reqInserted} already existed).`);

    // ── topic_suggestions ───────────────────────────────────────────────────
    console.log("\nMigrating topic_suggestions…");
    const { rows: topicRows } = await source.query(
      `SELECT id, topic, created_at FROM topic_suggestions`
    );
    console.log(`  Found ${topicRows.length} rows in source.`);

    let topicInserted = 0;
    for (const row of topicRows) {
      const res = await target.query(
        `INSERT INTO topic_suggestions (id, topic, created_at)
         VALUES ($1, $2, $3)
         ON CONFLICT (id) DO NOTHING`,
        [row.id, row.topic, row.created_at]
      );
      if (res.rowCount && res.rowCount > 0) topicInserted++;
    }
    console.log(`  Inserted ${topicInserted} new rows (${topicRows.length - topicInserted} already existed).`);

    console.log("\n✅ Migration complete.");
  } finally {
    await source.end();
    await target.end();
  }
}

migrate().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});
