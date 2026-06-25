import ContentTable from "@/components/ContentTable";
import CodeBlock from "@/components/CodeBlock";

export function SqlDeveloperOverview() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>SQL Developer</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        SQL fundamentals and cross-database query patterns for SQL Server, Oracle, and PostgreSQL.
      </p>
      <ul className="text-sm list-disc pl-5" style={{ color: "var(--body)" }}>
        <li className="mb-1"><strong>Query Comparison</strong> — side-by-side syntax differences across the three databases</li>
      </ul>
    </div>
  );
}

export function SqlQueryComparison() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>SQL Server vs Oracle vs PostgreSQL Queries</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Switching databases? Here are the most common syntax differences you&apos;ll encounter.
      </p>
      <ContentTable headers={["Operation", "SQL Server", "Oracle", "PostgreSQL"]} rows={[
        ["Top N rows", "SELECT TOP 10 *", "SELECT * WHERE ROWNUM &lt;= 10", "SELECT * LIMIT 10"],
        ["String concat", "col1 + col2", "col1 || col2", "col1 || col2"],
        ["Current date", "GETDATE()", "SYSDATE", "NOW()"],
        ["Auto-increment", "IDENTITY(1,1)", "GENERATED ALWAYS AS IDENTITY", "SERIAL / GENERATED ALWAYS"],
        ["Pagination", "OFFSET x ROWS FETCH NEXT y ROWS ONLY", "OFFSET x ROWS FETCH NEXT y ROWS ONLY", "LIMIT y OFFSET x"],
        ["Conditional", "ISNULL(col, val)", "NVL(col, val)", "COALESCE(col, val)"],
        ["String length", "LEN(col)", "LENGTH(col)", "LENGTH(col)"],
        ["Upsert", "MERGE", "MERGE", "INSERT … ON CONFLICT DO UPDATE"],
      ]} />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Pagination example</h3>
      <CodeBlock language="sql">{`-- SQL Server / Oracle
SELECT * FROM Orders
ORDER BY CreatedAt DESC
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

-- PostgreSQL
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 10 OFFSET 20;`}</CodeBlock>
    </div>
  );
}
