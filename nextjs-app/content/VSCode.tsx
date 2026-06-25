import ContentTable from "@/components/ContentTable";

export default function VSCode() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>VS Code</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Essential shortcuts and extensions for Visual Studio Code.
      </p>
      <ContentTable headers={["Shortcut", "Action"]} rows={[
        ["Ctrl + Shift + P", "Command palette"],
        ["Ctrl + P", "Quick open file"],
        ["Ctrl + `", "Toggle terminal"],
        ["Ctrl + Shift + E", "Explorer sidebar"],
        ["Ctrl + Shift + G", "Source control sidebar"],
        ["Ctrl + B", "Toggle sidebar"],
        ["Alt + Shift + F", "Format document"],
        ["F2", "Rename symbol"],
        ["Ctrl + .", "Quick fix"],
        ["Ctrl + Shift + K", "Delete line"],
        ["Alt + ↑ / ↓", "Move line up / down"],
      ]} />
      <h3 className="font-semibold text-sm mb-2 mt-5" style={{ color: "var(--ink)" }}>Recommended extensions</h3>
      <ul className="text-sm list-disc pl-5" style={{ color: "var(--body)" }}>
        <li className="mb-1"><strong>C# Dev Kit</strong> — full .NET support including IntelliSense and debugging</li>
        <li className="mb-1"><strong>GitLens</strong> — enhanced Git annotations and history</li>
        <li className="mb-1"><strong>Prettier</strong> — opinionated code formatter for JS/TS</li>
        <li className="mb-1"><strong>REST Client</strong> — send HTTP requests from `.http` files</li>
        <li className="mb-1"><strong>Thunder Client</strong> — lightweight Postman alternative</li>
      </ul>
    </div>
  );
}
