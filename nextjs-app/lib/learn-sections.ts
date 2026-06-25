/**
 * Canonical learning-hub menu definition.
 * Mirrors LEARN_SECTIONS in the Streamlit config.py.
 *
 * Rule: slugs are URL-stable and must never change once published.
 *       Titles are display-only and can be edited freely.
 */
import { LearnSection } from "./types";

export const LEARN_SECTIONS: LearnSection[] = [
  {
    slug: "git",
    title: "GIT",
    subsections: [
      { slug: "basics", title: "Basics" },
      { slug: "branching", title: "Branching" },
    ],
  },
  { slug: "visual-studio", title: "Visual Studio IDE" },
  { slug: "vscode", title: "VS Code" },
  { slug: "efcore-oracle", title: "EF Core + Oracle" },
  { slug: "dotnet", title: ".NET" },
  {
    slug: "unit-testing",
    title: "Unit Testing",
    subsections: [
      { slug: "tdd", title: "TDD" },
      { slug: "unit-test", title: "Unit Test" },
      { slug: "integration-test", title: "Integration Test" },
    ],
  },
  { slug: "linq", title: "LINQ" },
  {
    slug: "blazor",
    title: "Blazor",
    subsections: [
      { slug: "webforms-comparison", title: "Web Forms vs Blazor" },
      { slug: "fluent-ui", title: "Fluent UI Blazor" },
      {
        slug: "oracle-efcore-dapper",
        title: "Oracle Data Access with EF Core and Dapper",
      },
      { slug: "cqrs", title: "CQRS Pattern with Blazor Auto" },
    ],
  },
  { slug: "csharp", title: "C#" },
  { slug: "topic-suggestions", title: "Topic Suggestions" },
  {
    slug: "sql-developer",
    title: "SQL Developer",
    subsections: [
      {
        slug: "query-comparison",
        title: "SQL Server vs Oracle vs PostgreSQL Queries",
      },
    ],
  },
];

export const LATEST_NEW_TOPIC =
  "SQL Server vs Oracle vs PostgreSQL Queries";

export function findSection(identifier: string | null | undefined) {
  if (!identifier) return null;
  return (
    LEARN_SECTIONS.find(
      (s) => s.slug === identifier || s.title === identifier
    ) ?? null
  );
}

export function findSubsection(
  section: LearnSection | null | undefined,
  identifier: string | null | undefined
) {
  if (!section || !identifier) return null;
  return (
    section.subsections?.find(
      (s) => s.slug === identifier || s.title === identifier
    ) ?? null
  );
}

export function defaultSectionSlug() {
  return LEARN_SECTIONS[0]?.slug ?? null;
}
