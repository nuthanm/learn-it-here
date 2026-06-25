import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function CSharp() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>C#</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Modern C# features and patterns used in production .NET applications.
      </p>
      <ContentTable headers={["Feature", "Since", "Example"]} rows={[
        ["Records", "C# 9", "`public record Point(int X, int Y);`"],
        ["Pattern matching", "C# 8", "`if (obj is string s && s.Length > 0)`"],
        ["Nullable reference types", "C# 8", "`string? name = null;`"],
        ["Switch expressions", "C# 8", "`var result = x switch { 1 => \"one\", _ => \"other\" };`"],
        ["Top-level statements", "C# 9", "No `Main` class needed in `Program.cs`"],
        ["Global usings", "C# 10", "`global using System.Linq;` in any file"],
        ["Required members", "C# 11", "`public required string Name { get; init; }`"],
        ["Primary constructors", "C# 12", "`class Service(ILogger logger) { … }`"],
      ]} />
      <h3 className="font-semibold text-sm mb-2 mt-4" style={{ color: "var(--ink)" }}>Async / await basics</h3>
      <CodeBlock language="csharp">{`public async Task<Order> GetOrderAsync(int id, CancellationToken ct)
{
    var order = await _repo.FindAsync(id, ct);
    if (order is null) throw new NotFoundException(id);
    return order;
}`}</CodeBlock>
    </div>
  );
}
