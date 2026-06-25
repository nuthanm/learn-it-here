"use client";

import { useState } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { LEARN_SECTIONS, LATEST_NEW_TOPIC, defaultSectionSlug } from "@/lib/learn-sections";
import { LearnSection } from "@/lib/types";

// ── Lazy-load content components ─────────────────────────────────────────────
import { GitOverview, GitBasics, GitBranching } from "@/content/git";
import UnitTestingOverview, { TDD, UnitTestContent, IntegrationTest } from "@/content/unit-testing";
import { BlazorOverview, WebFormsVsBlazor, FluentUIBlazor, BlazorCQRS, BlazorOracleEfCoreDapper } from "@/content/blazor";
import { SqlDeveloperOverview, SqlQueryComparison } from "@/content/sql-developer";
import VisualStudio from "@/content/VisualStudio";
import VSCode from "@/content/VSCode";
import EFCoreOracle from "@/content/EFCoreOracle";
import DotNet from "@/content/DotNet";
import Linq from "@/content/Linq";
import CSharp from "@/content/CSharp";
import TopicSuggestions from "@/components/TopicSuggestions";

// ── Section icons & descriptions ──────────────────────────────────────────────
const SECTION_META: Record<string, { icon: string; desc: string }> = {
  git:              { icon: "🌿", desc: "Daily workflow, branching strategies and team collaboration" },
  "visual-studio":  { icon: "🔷", desc: "Shortcuts, extensions and debugging tips for Visual Studio" },
  vscode:           { icon: "🟦", desc: "Settings, extensions and keyboard shortcuts for VS Code" },
  "efcore-oracle":  { icon: "🗄", desc: "Fluent API, Oracle configuration and migrations with EF Core" },
  dotnet:           { icon: "🔵", desc: ".NET platform overview, LTS versions and tooling" },
  "unit-testing":   { icon: "✅", desc: "xUnit, NUnit, MSTest, TDD, integration tests and mocking" },
  linq:             { icon: "🔗", desc: "Deferred execution, common operators and query syntax" },
  blazor:           { icon: "⚡", desc: "Blazor Server, WebAssembly, component model and patterns" },
  csharp:           { icon: "🎯", desc: "Language versions, async/await, generics and pattern matching" },
  "topic-suggestions": { icon: "💡", desc: "Community-requested topics — vote and suggest your own" },
  "sql-developer":  { icon: "🐘", desc: "SQL workflow tips, cross-database query comparison" },
};

// ── Content resolver ──────────────────────────────────────────────────────────
function resolveContent(section: string | null, sub: string | null) {
  if (section === "git") {
    if (sub === "basics")    return <GitBasics />;
    if (sub === "branching") return <GitBranching />;
    return <GitOverview />;
  }
  if (section === "visual-studio")  return <VisualStudio />;
  if (section === "vscode")         return <VSCode />;
  if (section === "efcore-oracle")  return <EFCoreOracle />;
  if (section === "dotnet")         return <DotNet />;
  if (section === "unit-testing") {
    if (sub === "tdd")              return <TDD />;
    if (sub === "unit-test")        return <UnitTestContent />;
    if (sub === "integration-test") return <IntegrationTest />;
    return <UnitTestingOverview />;
  }
  if (section === "linq")    return <Linq />;
  if (section === "blazor") {
    if (sub === "webforms-comparison")  return <WebFormsVsBlazor />;
    if (sub === "fluent-ui")            return <FluentUIBlazor />;
    if (sub === "oracle-efcore-dapper") return <BlazorOracleEfCoreDapper />;
    if (sub === "cqrs")                 return <BlazorCQRS />;
    return <BlazorOverview />;
  }
  if (section === "csharp")            return <CSharp />;
  if (section === "topic-suggestions") return <TopicSuggestions />;
  if (section === "sql-developer") {
    if (sub === "query-comparison") return <SqlQueryComparison />;
    return <SqlDeveloperOverview />;
  }
  return (
    <p style={{ fontSize: 14, color: "var(--muted)" }}>Select a topic from the sidebar.</p>
  );
}

// ── Sidebar item ──────────────────────────────────────────────────────────────
function SidebarItem({
  section,
  activeSection,
  activeSub,
  onNavigate,
}: {
  section: LearnSection;
  activeSection: string;
  activeSub: string | null;
  onNavigate: (section: string, sub?: string) => void;
}) {
  const isActive = section.slug === activeSection;
  const meta = SECTION_META[section.slug];

  return (
    <li>
      <button
        onClick={() => onNavigate(section.slug)}
        className={`sidebar-item${isActive && !activeSub ? " active" : ""}`}>
        <span style={{ fontSize: 15, flexShrink: 0 }}>{meta?.icon ?? "📖"}</span>
        <span>{section.title}</span>
      </button>

      {isActive && section.subsections && section.subsections.length > 0 && (
        <ul style={{ marginLeft: 4, marginTop: 2, display: "flex", flexDirection: "column", gap: 1 }}>
          {section.subsections.map((sub) => {
            const subActive = activeSub === sub.slug;
            return (
              <li key={sub.slug}>
                <button
                  onClick={() => onNavigate(section.slug, sub.slug)}
                  className={`sidebar-sub-item${subActive ? " active" : ""}`}>
                  {sub.title}
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </li>
  );
}

// ── Mobile topic drawer ───────────────────────────────────────────────────────
function MobileTopicPicker({
  activeSection,
  activeSub,
  onNavigate,
}: {
  activeSection: string;
  activeSub: string | null;
  onNavigate: (section: string, sub?: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const current = LEARN_SECTIONS.find((s) => s.slug === activeSection);
  const meta = SECTION_META[activeSection];

  return (
    <div className="md:hidden mb-5">
      <button
        onClick={() => setOpen((v) => !v)}
        style={{
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 8,
          padding: "10px 14px",
          background: "var(--card)",
          border: "1px solid var(--border)",
          borderRadius: "var(--r-md)",
          fontSize: 13,
          fontWeight: 600,
          color: "var(--ink)",
          cursor: "pointer",
        }}>
        <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span>{meta?.icon ?? "📖"}</span>
          <span>{current?.title ?? "Select topic"}</span>
        </span>
        <span style={{ fontSize: 10 }}>{open ? "▲" : "▼"}</span>
      </button>

      {open && (
        <div
          style={{
            marginTop: 4,
            background: "var(--card)",
            border: "1px solid var(--border)",
            borderRadius: "var(--r-md)",
            padding: 8,
            boxShadow: "var(--shadow)",
          }}>
          {LEARN_SECTIONS.map((s) => {
            const m = SECTION_META[s.slug];
            const isActive = s.slug === activeSection;
            return (
              <div key={s.slug}>
                <button
                  onClick={() => { onNavigate(s.slug); setOpen(false); }}
                  className={`sidebar-item${isActive && !activeSub ? " active" : ""}`}>
                  <span style={{ fontSize: 14 }}>{m?.icon ?? "📖"}</span>
                  <span>{s.title}</span>
                </button>
                {isActive && s.subsections && s.subsections.length > 0 && (
                  s.subsections.map((sub) => {
                    const subActive = activeSub === sub.slug;
                    return (
                      <button
                        key={sub.slug}
                        onClick={() => { onNavigate(s.slug, sub.slug); setOpen(false); }}
                        className={`sidebar-sub-item${subActive ? " active" : ""}`}
                        style={{ display: "block", width: "100%" }}>
                        {sub.title}
                      </button>
                    );
                  })
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ── Main client component ─────────────────────────────────────────────────────
export default function LearningHubClient() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const rawSection = searchParams.get("section");
  const rawSub     = searchParams.get("sub");

  const activeSection =
    LEARN_SECTIONS.find((s) => s.slug === rawSection || s.title === rawSection)
      ?.slug ?? defaultSectionSlug() ?? "git";

  const sectionDef = LEARN_SECTIONS.find((s) => s.slug === activeSection);
  const activeSub  =
    sectionDef?.subsections?.find((s) => s.slug === rawSub || s.title === rawSub)
      ?.slug ?? null;

  const navigate = (section: string, sub?: string) => {
    const params = new URLSearchParams();
    params.set("section", section);
    if (sub) params.set("sub", sub);
    router.push(`${pathname}?${params.toString()}`);
  };

  const meta = SECTION_META[activeSection];
  const activeSubTitle = sectionDef?.subsections?.find((s) => s.slug === activeSub)?.title;

  return (
    <div>
      {/* New topic banner */}
      {LATEST_NEW_TOPIC && (
        <div
          style={{
            background: "var(--accent-soft)",
            border: "1px solid rgba(93,163,52,.25)",
            borderRadius: "var(--r-md)",
            padding: "10px 16px",
            marginBottom: 20,
            fontSize: 13,
            color: "var(--accent-hover)",
            fontWeight: 500,
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}>
          <span>🆕</span>
          <span>New topic: <strong>{LATEST_NEW_TOPIC}</strong></span>
        </div>
      )}

      <div className="flex gap-8">
        {/* ── Sidebar (desktop) ─────────────────────────────────────────── */}
        <aside
          className="hidden md:block flex-none"
          style={{ width: 220, flexShrink: 0 }}>
          {/* Search hint */}
          <div
            style={{
              fontSize: 10,
              fontWeight: 700,
              textTransform: "uppercase" as const,
              letterSpacing: "0.07em",
              color: "var(--muted)",
              padding: "0 12px",
              marginBottom: 8,
            }}>
            {LEARN_SECTIONS.length} Topics
          </div>
          <nav aria-label="Learning hub topics">
            <ul style={{ display: "flex", flexDirection: "column", gap: 1, listStyle: "none", padding: 0, margin: 0 }}>
              {LEARN_SECTIONS.map((section) => (
                <SidebarItem
                  key={section.slug}
                  section={section}
                  activeSection={activeSection}
                  activeSub={activeSub}
                  onNavigate={navigate}
                />
              ))}
            </ul>
          </nav>
        </aside>

        {/* ── Content area ──────────────────────────────────────────────── */}
        <div style={{ flex: 1, minWidth: 0 }}>
          {/* Mobile picker */}
          <MobileTopicPicker
            activeSection={activeSection}
            activeSub={activeSub}
            onNavigate={navigate}
          />

          {/* Content header */}
          <div className="content-page-header">
            {/* Breadcrumb */}
            <div className="breadcrumb" style={{ marginBottom: 10 }}>
              <a href="/">Home</a>
              <span className="breadcrumb-sep">›</span>
              <button
                onClick={() => navigate(activeSection)}
                style={{ background: "none", border: "none", cursor: "pointer", padding: 0, fontSize: 12, color: activeSub ? "var(--muted)" : "var(--ink)", fontWeight: activeSub ? 400 : 600 }}>
                {sectionDef?.title}
              </button>
              {activeSub && (
                <>
                  <span className="breadcrumb-sep">›</span>
                  <span style={{ color: "var(--ink)", fontWeight: 600 }}>{activeSubTitle}</span>
                </>
              )}
            </div>

            <div style={{ display: "flex", alignItems: "flex-start", gap: 12 }}>
              <span style={{ fontSize: 28, lineHeight: 1, marginTop: 2 }}>{meta?.icon ?? "📖"}</span>
              <div>
                <h2 style={{ margin: 0, marginBottom: 4 }}>
                  {activeSub ? activeSubTitle : sectionDef?.title}
                </h2>
                {meta?.desc && (
                  <p style={{ fontSize: 13, color: "var(--muted)", margin: 0, lineHeight: 1.5 }}>
                    {meta.desc}
                  </p>
                )}
              </div>
            </div>

            {/* Sub-topic tabs */}
            {sectionDef?.subsections && sectionDef.subsections.length > 0 && (
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 16 }}>
                <button
                  onClick={() => navigate(activeSection)}
                  style={{
                    padding: "4px 14px",
                    borderRadius: 999,
                    fontSize: 12,
                    fontWeight: 600,
                    border: !activeSub ? "1.5px solid var(--accent)" : "1.5px solid var(--border)",
                    background: !activeSub ? "var(--accent-soft)" : "var(--card)",
                    color: !activeSub ? "var(--accent-hover)" : "var(--muted)",
                    cursor: "pointer",
                    transition: "all 120ms ease",
                  }}>
                  Overview
                </button>
                {sectionDef.subsections.map((sub) => {
                  const isActive = activeSub === sub.slug;
                  return (
                    <button
                      key={sub.slug}
                      onClick={() => navigate(activeSection, sub.slug)}
                      style={{
                        padding: "4px 14px",
                        borderRadius: 999,
                        fontSize: 12,
                        fontWeight: 600,
                        border: isActive ? "1.5px solid var(--accent)" : "1.5px solid var(--border)",
                        background: isActive ? "var(--accent-soft)" : "var(--card)",
                        color: isActive ? "var(--accent-hover)" : "var(--muted)",
                        cursor: "pointer",
                        transition: "all 120ms ease",
                      }}>
                      {sub.title}
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Actual content */}
          {resolveContent(activeSection, activeSub)}
        </div>
      </div>
    </div>
  );
}
