import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function CSharp() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>C#</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>
        Modern, strongly typed language for building web, desktop, cloud, mobile, and game applications on .NET.
      </p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        C# combines developer productivity, strong tooling, and high runtime performance with a mature enterprise ecosystem.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>What you can build</h3>
      <ContentTable
        headers={["Area", "Frameworks / runtime", "Typical use"]}
        rows={[
          ["Web APIs", "ASP.NET Core", "REST/gRPC backends and microservices"],
          ["Web UI", "Blazor", "Interactive C# web applications"],
          ["Desktop", "WPF / WinForms", "Windows business tools"],
          ["Mobile", ".NET MAUI", "Cross-platform iOS/Android apps"],
          ["Cloud", "Azure + .NET", "Serverless and distributed systems"],
          ["Games", "Unity", "2D/3D mobile and desktop games"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Why teams choose C#</h3>
      <ContentTable
        headers={["Capability", "Why it matters"]}
        rows={[
          ["Async/await", "Readable asynchronous workflows for I/O-heavy services"],
          ["LINQ", "Unified query language for in-memory and data-source operations"],
          ["Nullable reference types", "Compile-time null safety and fewer runtime null bugs"],
          ["Records / pattern matching", "Less boilerplate and expressive domain code"],
          ["NuGet ecosystem", "Large package ecosystem for integrations and infrastructure"],
          ["Tooling", "Excellent debugging, refactoring, and diagnostics"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Version highlights</h3>
      <ContentTable
        headers={["Feature", "Since", "Example"]}
        rows={[
          ["Records", "C# 9", "`public record Point(int X, int Y);`"],
          ["Pattern matching", "C# 8+", "`if (obj is string s && s.Length > 0)`"],
          ["Switch expressions", "C# 8", "`x switch { 1 => \"one\", _ => \"other\" }`"],
          ["Global usings", "C# 10", "`global using System.Linq;`"],
          ["Required members", "C# 11", "`public required string Name { get; init; }`"],
          ["Primary constructors", "C# 12", "`class Service(ILogger logger) { }`"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Async / await sample</h3>
      <CodeBlock language="csharp">{`public async Task<Order> GetOrderAsync(int id, CancellationToken ct)
{
    var order = await _repo.FindAsync(id, ct);
    if (order is null) throw new NotFoundException(id);
    return order;
}`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Learning roadmap</h3>
      <ContentTable
        headers={["Phase", "Focus"]}
        rows={[
          ["Phase 1", "Language basics: variables, conditions, loops, methods"],
          ["Phase 2", "OOP: classes, interfaces, inheritance, encapsulation"],
          ["Phase 3", "Collections, LINQ, error handling, files, async/await"],
          ["Phase 4", "Choose stack path: ASP.NET Core, Blazor, MAUI, or Unity"],
          ["Phase 5", "Ship production projects with testing and CI/CD"],
        ]}
      />

      <p className="text-sm mt-4" style={{ color: "var(--muted)" }}>
        Further reading: {" "}
        <a href="https://learn.microsoft.com/en-us/dotnet/csharp/" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>C# documentation</a>
        {" · "}
        <a href="https://dotnet.microsoft.com/learn" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>Learn .NET</a>
      </p>
    </div>
  );
}
