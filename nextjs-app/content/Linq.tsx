import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function Linq() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>LINQ</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>
        Language Integrated Query for collections, EF Core queries, XML, and more.
      </p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        LINQ keeps query logic expressive and composable while preserving static type safety.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Method syntax vs query syntax</h3>
      <CodeBlock language="csharp">{`// Method syntax (most common)
var seniors = employees
    .Where(e => e.Age >= 55)
    .OrderBy(e => e.LastName)
    .Select(e => e.FullName);

// Query syntax (SQL-like)
var seniorNames =
    from e in employees
    where e.Age >= 55
    orderby e.LastName
    select e.FullName;`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Core operators</h3>
      <ContentTable
        headers={["Operator", "Use case", "SQL equivalent"]}
        rows={[
          ["Where", "Filter records", "WHERE"],
          ["Select", "Project shape", "SELECT"],
          ["OrderBy / ThenBy", "Sort results", "ORDER BY"],
          ["GroupBy", "Aggregate by key", "GROUP BY"],
          ["Join / GroupJoin", "Combine related sets", "JOIN / LEFT JOIN"],
          ["Any / All", "Existence checks", "EXISTS / ALL"],
          ["Count / Sum / Average", "Aggregations", "COUNT / SUM / AVG"],
          ["Skip / Take", "Pagination", "OFFSET / FETCH"],
          ["Distinct", "Remove duplicates", "DISTINCT"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Deferred vs immediate execution</h3>
      <ContentTable
        headers={["Execution style", "Examples", "Notes"]}
        rows={[
          ["Deferred", "Where, Select, OrderBy", "Runs when enumerated"],
          ["Immediate", "ToList, ToArray, Count", "Executes immediately and materializes"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Practical tips</h3>
      <ul className="text-sm list-disc pl-5" style={{ color: "var(--body)" }}>
        <li className="mb-1">Prefer projection with <code>Select</code> to avoid loading unnecessary columns.</li>
        <li className="mb-1">Avoid calling <code>ToList()</code> too early in EF Core query chains.</li>
        <li className="mb-1">Use <code>AsNoTracking()</code> for read-only queries to improve performance.</li>
        <li className="mb-1">Keep query expressions readable by composing smaller query parts.</li>
      </ul>

      <p className="text-sm mt-4" style={{ color: "var(--muted)" }}>
        Further reading: {" "}
        <a href="https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>LINQ guide</a>
      </p>
    </div>
  );
}
