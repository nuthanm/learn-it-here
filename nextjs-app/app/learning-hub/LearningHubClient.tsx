"use client";

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

// ── Content resolver ─────────────────────────────────────────────────────────
function resolveContent(section: string | null, sub: string | null) {
  if (section === "git") {
    if (sub === "basics") return <GitBasics />;
    if (sub === "branching") return <GitBranching />;
    return <GitOverview />;
  }
  if (section === "visual-studio") return <VisualStudio />;
  if (section === "vscode") return <VSCode />;
  if (section === "efcore-oracle") return <EFCoreOracle />;
  if (section === "dotnet") return <DotNet />;
  if (section === "unit-testing") {
    if (sub === "tdd") return <TDD />;
    if (sub === "unit-test") return <UnitTestContent />;
    if (sub === "integration-test") return <IntegrationTest />;
    return <UnitTestingOverview />;
  }
  if (section === "linq") return <Linq />;
  if (section === "blazor") {
    if (sub === "webforms-comparison") return <WebFormsVsBlazor />;
    if (sub === "fluent-ui") return <FluentUIBlazor />;
    if (sub === "oracle-efcore-dapper") return <BlazorOracleEfCoreDapper />;
    if (sub === "cqrs") return <BlazorCQRS />;
    return <BlazorOverview />;
  }
  if (section === "csharp") return <CSharp />;
  if (section === "topic-suggestions") return <TopicSuggestions />;
  if (section === "sql-developer") {
    if (sub === "query-comparison") return <SqlQueryComparison />;
    return <SqlDeveloperOverview />;
  }
  // Fallback
  return (
    <p className="text-sm" style={{ color: "var(--muted)" }}>
      Select a topic from the sidebar.
    </p>
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

  return (
    <li>
      <button
        onClick={() => onNavigate(section.slug)}
        className="w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-100"
        style={{
          background: isActive && !activeSub ? "var(--accent-soft)" : "transparent",
          color: isActive ? "var(--accent-hover)" : "var(--body)",
          fontWeight: isActive ? 600 : 400,
        }}>
        {section.title}
      </button>
      {isActive && section.subsections && section.subsections.length > 0 && (
        <ul className="ml-3 mt-1 flex flex-col gap-0.5">
          {section.subsections.map((sub) => {
            const subActive = activeSub === sub.slug;
            return (
              <li key={sub.slug}>
                <button
                  onClick={() => onNavigate(section.slug, sub.slug)}
                  className="w-full text-left px-3 py-1.5 rounded-lg text-xs transition-colors duration-100"
                  style={{
                    background: subActive ? "var(--accent-soft)" : "transparent",
                    color: subActive ? "var(--accent-hover)" : "var(--muted)",
                    fontWeight: subActive ? 600 : 400,
                  }}>
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

// ── Main client component ─────────────────────────────────────────────────────
export default function LearningHubClient() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const rawSection = searchParams.get("section");
  const rawSub = searchParams.get("sub");

  // Resolve to a valid section slug
  const activeSection =
    LEARN_SECTIONS.find((s) => s.slug === rawSection || s.title === rawSection)
      ?.slug ?? defaultSectionSlug() ?? "git";

  // Resolve sub only if it belongs to the active section
  const sectionDef = LEARN_SECTIONS.find((s) => s.slug === activeSection);
  const activeSub =
    sectionDef?.subsections?.find((s) => s.slug === rawSub || s.title === rawSub)
      ?.slug ?? null;

  const navigate = (section: string, sub?: string) => {
    const params = new URLSearchParams();
    params.set("section", section);
    if (sub) params.set("sub", sub);
    router.push(`${pathname}?${params.toString()}`);
  };

  return (
    <div className="flex gap-8">
      {/* Sidebar */}
      <aside className="flex-none" style={{ width: 220 }}>
        <nav aria-label="Learning hub topics">
          <ul className="flex flex-col gap-0.5">
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

      {/* Content area */}
      <div className="flex-1 min-w-0">
        {/* New topic banner */}
        {LATEST_NEW_TOPIC && (
          <div className="mb-5 px-4 py-3 rounded-lg text-xs font-medium"
            style={{ background: "var(--accent-soft)", color: "var(--accent-hover)", border: "1px solid var(--accent)" }}>
            🆕 New topic: <strong>{LATEST_NEW_TOPIC}</strong>
          </div>
        )}

        {resolveContent(activeSection, activeSub)}
      </div>
    </div>
  );
}
