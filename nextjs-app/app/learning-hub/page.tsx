import { Suspense } from "react";
import { Metadata } from "next";
import LearningHubClient from "./LearningHubClient";

export const metadata: Metadata = {
  title: "Learning Hub — Learn It Here",
  description:
    "Curated guides for .NET, GIT, Blazor, EF Core, C#, LINQ, Unit Testing, SQL Developer and more. Community-requested topics.",
};

export default function LearningHubPage() {
  return (
    <Suspense fallback={
      <div style={{ padding: "40px 0", textAlign: "center", color: "var(--muted)", fontSize: 14 }}>
        Loading learning hub…
      </div>
    }>
      <LearningHubClient />
    </Suspense>
  );
}
