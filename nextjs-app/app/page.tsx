import Link from "next/link";
import { LEARN_SECTIONS } from "@/lib/learn-sections";
import { STEPS } from "@/lib/steps";

export const metadata = {
  title: "Learn It Here 🐼 — Know your stack before you build",
  description:
    "A 2-minute requirements questionnaire plus curated, opinionated learning guides for .NET, GIT, Blazor, EF Core and more. Export your answers as a PDF.",
};

const TOPIC_ICONS: Record<string, string> = {
  git: "🌿",
  "visual-studio": "🔷",
  vscode: "🟦",
  "efcore-oracle": "🗄",
  dotnet: "🔵",
  "unit-testing": "✅",
  linq: "🔗",
  blazor: "⚡",
  csharp: "🎯",
  "topic-suggestions": "💡",
  "sql-developer": "🐘",
};

const HOW_IT_WORKS = [
  {
    step: "1",
    icon: "📋",
    title: "Define your stack",
    desc: "Answer 8 targeted questions about your version control, IDE, deployment, architecture, patterns, and ORM.",
  },
  {
    step: "2",
    icon: "📄",
    title: "Export a PDF brief",
    desc: "Instantly download a shareable, branded PDF summary of your project requirements.",
  },
  {
    step: "3",
    icon: "🎓",
    title: "Jump into learning",
    desc: "Browse curated guides matched to your exact tools — GIT, Blazor, C#, EF Core, SQL, and more.",
  },
];

export default function HomePage() {
  const questionCount = STEPS.length;
  const topicCount = LEARN_SECTIONS.length;

  return (
    <div>
      {/* ── Hero ─────────────────────────────────────────────────── */}
      <section className="hero-section">
        <div className="hero-badge fade-up">
          <span>🐼</span>
          <span>Learn It Here</span>
        </div>

        <div
          className="panda-bob select-none fade-up fade-up-delay-1"
          aria-hidden="true"
          style={{ fontSize: 72, lineHeight: 1, marginBottom: 16 }}>
          🐼
        </div>

        <h1 className="hero-title fade-up fade-up-delay-1">
          Know your <span>stack</span>
          <br />before you build.
        </h1>

        <p className="hero-subtitle fade-up fade-up-delay-2">
          A 2-minute questionnaire plus curated, opinionated guides for
          .NET, GIT, Blazor, EF&nbsp;Core and more&nbsp;—&nbsp;export your answers as&nbsp;a&nbsp;PDF.
        </p>

        {/* CTA buttons */}
        <div className="flex justify-center gap-3 flex-wrap mb-8 fade-up fade-up-delay-3">
          <Link href="/projectrequirements" className="btn-primary" style={{ minWidth: 180 }}>
            Start questionnaire →
          </Link>
          <Link href="/learning-hub" className="btn-secondary" style={{ minWidth: 150 }}>
            Browse guides
          </Link>
        </div>

        {/* Stats */}
        <div className="fade-up fade-up-delay-4">
          <div className="stat-strip">
            <div className="stat-item">
              <span className="stat-number">{questionCount}</span>
              <span className="stat-label">Questions</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{topicCount}</span>
              <span className="stat-label">Topics</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">PDF</span>
              <span className="stat-label">Export</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">Free</span>
              <span className="stat-label">Forever</span>
            </div>
          </div>
        </div>
      </section>

      {/* ── How it works ─────────────────────────────────────────── */}
      <section style={{ marginBottom: "var(--section-gap)" }}>
        <div className="text-center mb-8">
          <p className="section-eyebrow">How it works</p>
          <h2 className="section-heading">Three steps to get moving</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {HOW_IT_WORKS.map(({ step, icon, title, desc }) => (
            <div key={step} className="card card-hover" style={{ position: "relative" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
                <div className="step-chip">{step}</div>
                <span style={{ fontSize: 20 }}>{icon}</span>
              </div>
              <h3 style={{ fontSize: 15, fontWeight: 700, color: "var(--ink)", marginBottom: 6 }}>{title}</h3>
              <p style={{ fontSize: 13, color: "var(--muted)", lineHeight: 1.6 }}>{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Topics preview ───────────────────────────────────────── */}
      <section style={{ marginBottom: "var(--section-gap)" }}>
        <div className="flex items-end justify-between mb-6 flex-wrap gap-3">
          <div>
            <p className="section-eyebrow">Learning hub</p>
            <h2 className="section-heading">{topicCount} curated topics</h2>
          </div>
          <Link href="/learning-hub" className="btn-secondary" style={{ fontSize: 13 }}>
            See all topics →
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
          {LEARN_SECTIONS.map((s) => (
            <Link
              key={s.slug}
              href={`/learning-hub?section=${s.slug}`}
              className="topic-card">
              <span className="topic-card-icon">{TOPIC_ICONS[s.slug] ?? "📖"}</span>
              <span className="topic-card-title">{s.title}</span>
              {s.subsections && s.subsections.length > 0 && (
                <span className="topic-card-desc">
                  {s.subsections.length} sub-topic{s.subsections.length > 1 ? "s" : ""}
                </span>
              )}
            </Link>
          ))}
        </div>
      </section>

      {/* ── CTA banner ───────────────────────────────────────────── */}
      <section
        className="text-center"
        style={{
          background: "var(--accent-soft)",
          border: "1px solid rgba(93,163,52,.25)",
          borderRadius: "var(--r-xl)",
          padding: "40px 24px",
          marginBottom: "var(--section-gap)",
        }}>
        <div style={{ fontSize: 36, marginBottom: 12 }}>🐼</div>
        <h2 className="section-heading" style={{ marginBottom: 10 }}>Ready to go?</h2>
        <p style={{ fontSize: 14, color: "var(--body)", maxWidth: 400, margin: "0 auto 22px", lineHeight: 1.7 }}>
          Fill in the questionnaire and you&apos;ll have a PDF brief plus your personal learning roadmap in under two minutes.
        </p>
        <Link href="/projectrequirements" className="btn-primary" style={{ margin: "0 auto" }}>
          Get started — it&apos;s free →
        </Link>
      </section>
    </div>
  );
}
