import CodeBlock from "@/components/CodeBlock";
import ContentTable from "@/components/ContentTable";

export default function VisualStudio() {
  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>Visual Studio IDE</h2>
      <p className="text-sm mb-4" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Productivity tips and shortcuts for the full Visual Studio IDE (Windows / Mac).
      </p>
      <ContentTable headers={["Shortcut", "Action"]} rows={[
        ["Ctrl + Shift + B", "Build solution"],
        ["F5", "Start debugging"],
        ["Ctrl + F5", "Run without debugger"],
        ["F9", "Toggle breakpoint"],
        ["Ctrl + .", "Quick actions and refactorings"],
        ["Ctrl + K, Ctrl + D", "Format document"],
        ["Ctrl + ,", "Go to All (files, types, members)"],
        ["Alt + Enter", "Apply code fix / suggestion"],
        ["Ctrl + Shift + F", "Find in files"],
        ["Ctrl + T", "Go to type"],
      ]} />
    </div>
  );
}
