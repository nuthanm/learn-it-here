/**
 * Neon serverless PostgreSQL connection helper.
 *
 * The connection is created lazily (on first use) so that the Next.js build
 * phase — which imports route modules to collect page metadata — doesn't
 * throw when DATABASE_URL is not set in the build environment.
 *
 * Usage in API routes:
 *   import { getSql } from '@/lib/db';
 *   const sql = getSql();
 *   const rows = await sql`SELECT * FROM topic_suggestions`;
 */
import { neon, NeonQueryFunction } from "@neondatabase/serverless";

let _sql: NeonQueryFunction<false, false> | null = null;

export function getSql(): NeonQueryFunction<false, false> {
  if (!_sql) {
    const url = process.env.DATABASE_URL;
    if (!url) {
      throw new Error(
        "DATABASE_URL is not set. Add it to .env.local (see .env.local.example)."
      );
    }
    _sql = neon(url);
  }
  return _sql;
}
