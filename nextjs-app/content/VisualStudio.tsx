import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function VisualStudio() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Visual Studio IDE</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>
        Microsoft&apos;s flagship IDE for .NET, C#, ASP.NET, Azure, and enterprise applications.
      </p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Visual Studio is a full development workbench with debugging, profiling, testing, refactoring,
        package management, and source control integration in one place.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>Real-world workflow example</h3>
      <p className="text-sm mb-2" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        A common flow: generate C# models from incoming JSON, apply quick fixes with the lightbulb,
        debug with breakpoints, then validate with Test Explorer before pushing.
      </p>
      <CodeBlock language="json">{`{
  "patientId": "P-1042",
  "fullName": "Jane Smith",
  "dateOfBirth": "1985-04-15",
  "testResults": [
    { "testName": "Blood Sugar", "value": 5.4, "unit": "mmol/L" }
  ]
}`}</CodeBlock>
      <p className="text-sm my-2" style={{ color: "var(--body)" }}>
        Use <strong>Edit → Paste Special → Paste JSON as Classes</strong> to generate model classes instantly.
      </p>
      <CodeBlock language="csharp">{`public class PatientResult
{
    public string PatientId { get; set; }
    public string FullName { get; set; }
    public string DateOfBirth { get; set; }
    public TestResult[] TestResults { get; set; }
}`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Key productivity features</h3>
      <ContentTable
        headers={["Feature", "How to access", "What it does"]}
        rows={[
          ["Paste JSON as Classes", "Edit → Paste Special", "Generate matching C# model classes from JSON"],
          ["Quick Actions", "Ctrl + .", "Generate methods, implement interfaces, apply refactors"],
          ["Generate from usage", "Ctrl + . on missing symbol", "Create method/type stubs automatically"],
          ["Live code analysis", "Built-in Roslyn analyzers", "Flags issues and suggests fixes as you type"],
          ["Test Explorer", "View → Test Explorer", "Run and debug xUnit/NUnit/MSTest from the IDE"],
          ["NuGet Package Manager", "Tools → NuGet Package Manager", "Install/update dependencies across projects"],
          ["Performance Profiler", "Debug → Performance Profiler", "Inspect CPU, memory, and performance hotspots"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Settings worth configuring</h3>
      <ContentTable
        headers={["Setting", "Where", "Recommended setup"]}
        rows={[
          ["Editor font", "Tools → Options → Fonts and Colors", "Use Cascadia Code/JetBrains Mono at readable size"],
          ["IntelliSense", "Text Editor → C# → IntelliSense", "Enable matching highlights and smart completion"],
          ["Code style", "Text Editor → C# → Code Style", "Set naming rules and formatting preferences"],
          ["Format on save", ".editorconfig", "Enforce consistent team formatting automatically"],
          ["Word wrap", "Edit → Advanced → Word Wrap", "Reduce horizontal scrolling on long lines"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Essential shortcuts</h3>
      <ContentTable
        headers={["Shortcut", "Action"]}
        rows={[
          ["Ctrl + .", "Quick Actions"],
          ["Ctrl + R, R", "Rename symbol everywhere"],
          ["F12", "Go to definition"],
          ["Shift + F12", "Find all references"],
          ["Ctrl + K, Ctrl + D", "Format document"],
          ["Ctrl + Shift + B", "Build solution"],
          ["F5 / Ctrl + F5", "Debug / run without debugger"],
          ["Ctrl + T", "Search files/types/members"],
        ]}
      />

      <p className="text-sm mt-4" style={{ color: "var(--muted)" }}>
        Further reading: {" "}
        <a href="https://learn.microsoft.com/en-us/visualstudio/" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>Visual Studio docs</a>
        {" · "}
        <a href="https://visualstudio.microsoft.com/downloads/" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>Download Visual Studio</a>
      </p>
    </div>
  );
}
