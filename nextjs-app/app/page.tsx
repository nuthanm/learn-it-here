import Link from "next/link";
import { LEARN_SECTIONS } from "@/lib/learn-sections";
import { STEPS } from "@/lib/steps";

export const metadata = {
  title: "Learn It Here 🐼 — Know your stack before you build",
};

export default function HomePage() {
  const questionCount = STEPS.length;
  const topicCount = LEARN_SECTIONS.length;

  return (
    <>
      {/* Hero */}
      <section className="text-center py-8" style={{ maxWidth: 720, margin: "0 auto" }}>
        <div className="panda-bob text-9xl leading-none my-4 inline-block select-none" aria-hidden="true">
          🐼
        </div>
        <h1 className="font-bold tracking-tight mt-0 mb-3"
          style={{ fontSize: 44, lineHeight: 1.15, letterSpacing: "-0.02em", color: "var(--ink)" }}>
          Know your stack<br />before you build.
        </h1>
        <p className="mx-auto mt-3" style={{ maxWidth: 560, fontSize: 15, color: "var(--body)", lineHeight: 1.7 }}>
          A 2-minute questionnaire plus curated, opinionated guides for
          .NET, GIT, Blazor, EF Core and more — export your answers as a PDF.
        </p>
      </section>

      {/* CTA pair */}
      <div className="flex justify-center gap-3 mt-6 flex-wrap">
        <Link href="/projectrequirements"
          className="inline-flex items-center justify-center px-5 py-2 rounded-lg font-semibold text-white text-sm no-underline"
          style={{ background: "var(--accent)", minHeight: 38 }}>
          Start questionnaire →
        </Link>
        <Link href="/learning-hub"
          className="inline-flex items-center justify-center px-5 py-2 rounded-lg font-semibold text-sm no-underline border"
          style={{ background: "var(--card)", borderColor: "var(--border)", color: "var(--ink)", minHeight: 38 }}>
          Browse guides
        </Link>
      </div>

      {/* Trust strip */}
      <div className="flex gap-9 justify-center mt-7 mb-2 flex-wrap text-sm"
        style={{ color: "var(--muted)" }}>
        <span>⚡ {questionCount} questions</span>
        <span>📄 PDF export</span>
        <span>🗂 {topicCount} topics</span>
      </div>

      {/* Feature row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-10 pt-8 border-t"
        style={{ borderColor: "var(--border)" }}>
        {[
          {
            icon: "📋",
            title: "Capture requirements",
            desc: "Targeted questions that define your project context and tech stack.",
          },
          {
            icon: "🎓",
            title: "Stack-matched guides",
            desc: "Curated learning built around your specific versions and architecture.",
          },
          {
            icon: "⚡",
            title: "Learn & ship fast",
            desc: "Hands-on, zero fluff — only what your project actually needs.",
          },
        ].map(({ icon, title, desc }) => (
          <div key={title} className="flex flex-col gap-2 py-2">
            <span className="text-2xl">{icon}</span>
            <strong className="font-semibold text-sm" style={{ color: "var(--ink)" }}>{title}</strong>
            <span className="text-sm" style={{ color: "var(--muted)", lineHeight: 1.6 }}>{desc}</span>
          </div>
        ))}
      </div>
    </>
  );
}
