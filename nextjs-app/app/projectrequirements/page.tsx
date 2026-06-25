import { Metadata } from "next";
import RequirementsForm from "./RequirementsForm";
import { STEPS } from "@/lib/steps";

export const metadata: Metadata = {
  title: "Project Requirements — Learn It Here",
};

export default function RequirementsPage() {
  return (
    <>
      <nav className="text-xs mb-4" style={{ color: "var(--muted)" }}>
        <a href="/" className="no-underline hover:underline" style={{ color: "var(--muted)" }}>Home</a>
        <span className="mx-2">/</span>
        <span style={{ color: "var(--ink)" }}>Requirements</span>
      </nav>

      <h1 className="font-bold mb-2" style={{ fontSize: "var(--fs-h1)", color: "var(--ink)" }}>
        Project Requirements
      </h1>
      <p className="mb-6" style={{ color: "var(--body)", maxWidth: 640, lineHeight: 1.7 }}>
        Capture your project&apos;s tech-stack details across {STEPS.length} questions,
        then download a shareable PDF.
      </p>

      <RequirementsForm />
    </>
  );
}
