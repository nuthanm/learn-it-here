import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function VSCode() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>VS Code</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>
        Lightweight, extensible editor for quick edits and full-stack development.
      </p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        VS Code starts fast and scales well with extensions for C#, Python, JavaScript, Docker,
        remote development, and live collaboration.
      </p>

      <h3 className="font-semibold text-sm mb-2" style={{ color: "var(--ink)" }}>High-impact daily features</h3>
      <ContentTable
        headers={["Feature", "Shortcut / Usage", "Benefit"]}
        rows={[
          ["Multi-cursor editing", "Alt+Click / Ctrl+D / Ctrl+Shift+L", "Edit many matches at once"],
          ["Command Palette", "Ctrl+Shift+P", "Access every command quickly"],
          ["Integrated terminal", "Ctrl+`", "Run build/test/git without leaving editor"],
          ["Live Share", "Install Live Share extension", "Real-time pair programming"],
          ["Remote development", "Remote-SSH / Dev Containers", "Edit server/container code locally"],
          ["IntelliSense", "Built-in with language servers", "Completions, hovers, signature help"],
          ["Zen mode", "Ctrl+K Z", "Distraction-free coding"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Recommended extensions</h3>
      <ContentTable
        headers={["Extension", "What it adds", "Best for"]}
        rows={[
          ["C# Dev Kit", "Rich .NET support, tests, debugging", "C#/.NET teams"],
          ["GitHub Copilot", "AI-assisted code suggestions", "General productivity"],
          ["GitLens", "Advanced commit/blame/history insights", "Git-heavy workflows"],
          ["REST Client / Thunder Client", "API request testing", "Backend/API work"],
          ["Prettier", "Consistent formatting", "Frontend/full-stack"],
          ["ESLint / Pylint", "Inline linting diagnostics", "JS/TS/Python"],
          ["Docker", "Container explorer and commands", "Containerized apps"],
        ]}
      />

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Suggested settings.json</h3>
      <CodeBlock language="json">{`{
  "editor.fontSize": 14,
  "editor.fontLigatures": true,
  "editor.formatOnSave": true,
  "editor.wordWrap": "on",
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "files.autoSave": "afterDelay",
  "git.autofetch": true,
  "[csharp]": {
    "editor.defaultFormatter": "ms-dotnettools.csharp"
  }
}`}</CodeBlock>

      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Essential shortcuts</h3>
      <ContentTable
        headers={["Shortcut", "Action"]}
        rows={[
          ["Ctrl + P", "Quick open file"],
          ["Ctrl + Shift + P", "Command palette"],
          ["Ctrl + `", "Toggle terminal"],
          ["Ctrl + /", "Toggle line comment"],
          ["Alt + Shift + F", "Format document"],
          ["F2", "Rename symbol"],
          ["F12 / Shift + F12", "Definition / references"],
          ["Ctrl + B", "Toggle sidebar"],
          ["Ctrl + K Z", "Zen mode"],
        ]}
      />

      <p className="text-sm mt-4" style={{ color: "var(--muted)" }}>
        Further reading: {" "}
        <a href="https://code.visualstudio.com/docs" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>VS Code docs</a>
        {" · "}
        <a href="https://code.visualstudio.com/docs/getstarted/keybindings" target="_blank" rel="noopener noreferrer" className="font-semibold no-underline hover:underline" style={{ color: "var(--accent)" }}>Keyboard shortcuts</a>
      </p>
    </div>
  );
}
