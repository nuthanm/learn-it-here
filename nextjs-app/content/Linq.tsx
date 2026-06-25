import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function Linq() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>LINQ</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Language Integrated Query — query collections, databases, and XML with a unified syntax.
      </p>
      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Common operators</h3>
      <ContentTable headers={["Operator", "Purpose", "SQL equivalent"]} rows={[
        ["Where", "Filter elements", "WHERE"],
        ["Select", "Project / transform", "SELECT"],
        ["OrderBy / OrderByDescending", "Sort", "ORDER BY"],
        ["GroupBy", "Group by key", "GROUP BY"],
        ["First / FirstOrDefault", "First match", "SELECT TOP 1"],
        ["Any / All", "Existence check", "EXISTS / ALL"],
        ["Count / Sum / Average", "Aggregation", "COUNT / SUM / AVG"],
        ["Join / GroupJoin", "Inner / left join", "JOIN / LEFT JOIN"],
        ["Distinct", "Remove duplicates", "DISTINCT"],
        ["Take / Skip", "Pagination", "FETCH / OFFSET"],
      ]} />
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Method vs Query syntax</h3>
      <CodeBlock language="csharp">{`// Method syntax (preferred in most codebases)
var seniors = employees
    .Where(e => e.Age >= 55)
    .OrderBy(e => e.LastName)
    .Select(e => e.FullName);

// Query syntax (SQL-like)
var seniors =
    from e in employees
    where e.Age >= 55
    orderby e.LastName
    select e.FullName;`}</CodeBlock>
    </div>
  );
}
