import { Suspense } from "react";
import { Metadata } from "next";
import LearningHubClient from "./LearningHubClient";

export const metadata: Metadata = {
  title: "Learning Hub — Learn It Here",
};

export default function LearningHubPage() {
  return (
    <Suspense fallback={<div style={{ color: "var(--muted)" }}>Loading…</div>}>
      <LearningHubClient />
    </Suspense>
  );
}
