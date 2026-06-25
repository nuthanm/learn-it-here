import { Metadata } from "next";
import RequirementsForm from "./RequirementsForm";
import { STEPS } from "@/lib/steps";

export const metadata: Metadata = {
  title: "Project Requirements — Learn It Here",
  description:
    "Capture your project's tech-stack details across 8 questions, then download a shareable PDF brief.",
};

export default function RequirementsPage() {
  const sections = STEPS.map((s) => s.section).filter(
    (sec, idx, arr) => arr.indexOf(sec) === idx
  );

  return (
    <div style={{ maxWidth: 720, margin: "0 auto" }}>
      {/* Breadcrumb */}
      <nav className="breadcrumb">
        <a href="/">Home</a>
        <span className="breadcrumb-sep">›</span>
        <span style={{ color: "var(--ink)" }}>Project Requirements</span>
      </nav>

      {/* Page header */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
          <span style={{ fontSize: 28 }}>📋</span>
          <h1 style={{ fontSize: 28, fontWeight: 800, color: "var(--ink)", letterSpacing: "-0.02em", margin: 0 }}>
            Project Requirements
          </h1>
        </div>
        <p style={{ color: "var(--body)", lineHeight: 1.7, maxWidth: 560, marginBottom: 16 }}>
          Answer {STEPS.length} questions about your stack. We&apos;ll save your answers and generate
          a shareable PDF brief you can download instantly.
        </p>

        {/* Section pills */}
        <div className="flex flex-wrap gap-2">
          {sections.map((sec) => (
            <span
              key={sec}
              style={{
                display: "inline-block",
                background: "var(--accent-soft)",
                color: "var(--accent-hover)",
                borderRadius: 999,
                fontSize: 11,
                fontWeight: 600,
                padding: "3px 12px",
                border: "1px solid rgba(93,163,52,.2)",
              }}>
              {sec}
            </span>
          ))}
        </div>
      </div>

      <RequirementsForm />
    </div>
  );
}
