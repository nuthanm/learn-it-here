"use client";

import { useState, useEffect } from "react";

const TAG_COLORS = [
  "#8B1A6B", "#C41E7A", "#4B1040", "#6B2D5E", "#A0256E",
  "#3D0F35", "#B5127A", "#7A1E5A", "#501048", "#D42085",
];

interface TopicCount {
  topic: string;
  count: number;
}

function buildCounts(rows: { topic: string }[]): TopicCount[] {
  const buckets: Record<string, TopicCount> = {};
  for (const row of rows) {
    const t = (row.topic ?? "").trim();
    if (!t) continue;
    const key = t.toLowerCase();
    if (!buckets[key]) {
      buckets[key] = { topic: t, count: 0 };
    }
    buckets[key].count++;
  }
  return Object.values(buckets).sort((a, b) => b.count - a.count);
}

export default function TopicSuggestions() {
  const [topics, setTopics] = useState<TopicCount[]>([]);
  const [loading, setLoading] = useState(true);
  const [topicInput, setTopicInput] = useState("");
  const [whyInput, setWhyInput] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [feedbackOk, setFeedbackOk] = useState(true);

  useEffect(() => {
    fetch("/api/topics")
      .then((r) => r.json())
      .then((rows) => {
        setTopics(buildCounts(rows));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topicInput.trim()) return;
    setSubmitting(true);
    try {
      const res = await fetch("/api/topics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topicInput.trim() }),
      });
      const data = await res.json();
      if (data.ok) {
        setFeedback("Thank you! Your suggestion has been noted. 🐼");
        setFeedbackOk(true);
        setTopicInput("");
        setWhyInput("");
        // Optimistically add to tag cloud
        setTopics((prev) => {
          const key = topicInput.trim().toLowerCase();
          const existing = prev.find((t) => t.topic.toLowerCase() === key);
          if (existing) {
            return prev.map((t) =>
              t.topic.toLowerCase() === key ? { ...t, count: t.count + 1 } : t
            );
          }
          return [{ topic: topicInput.trim(), count: 1 }, ...prev];
        });
      } else {
        setFeedback(data.message ?? "Could not save suggestion.");
        setFeedbackOk(false);
      }
    } catch {
      setFeedback("Network error — could not save suggestion.");
      setFeedbackOk(false);
    }
    setSubmitting(false);
  };

  const maxCount = topics.reduce((m, t) => Math.max(m, t.count), 1);
  const minCount = topics.reduce((m, t) => Math.min(m, t.count), maxCount);
  const range = Math.max(maxCount - minCount, 1);

  return (
    <div>
      <h2 className="font-bold text-xl mb-1" style={{ color: "var(--ink)" }}>What others want to learn</h2>
      <p className="text-sm mb-1" style={{ color: "var(--muted)" }}>Community-requested topics.</p>
      <p className="text-sm mb-5" style={{ color: "var(--body)", lineHeight: 1.7 }}>
        Tag size reflects how many people have requested it.
        The most-requested topics get added to the learning hub first.
      </p>

      {/* Tag cloud */}
      {loading ? (
        <p className="text-sm" style={{ color: "var(--muted)" }}>Loading…</p>
      ) : topics.length === 0 ? (
        <p className="text-sm" style={{ color: "var(--muted)" }}>No suggestions yet. Be the first!</p>
      ) : (
        <div className="flex flex-wrap gap-1 mb-6">
          {topics.map((t, i) => {
            const size = 0.85 + ((t.count - minCount) / range) * (3.0 - 0.85);
            const color = TAG_COLORS[i % TAG_COLORS.length];
            const delay = (i * 0.08).toFixed(2);
            return (
              <span
                key={t.topic}
                className="tc-tag"
                title={`${t.count} ${t.count === 1 ? "request" : "requests"}`}
                style={{ fontSize: `${size.toFixed(2)}em`, color, animationDelay: `${delay}s` }}>
                {t.topic}
                <sup className="tc-count">{t.count}</sup>
              </span>
            );
          })}
        </div>
      )}

      {/* Inline suggestion form */}
      <div className="rounded-xl p-5 mt-4" style={{ background: "var(--card)", boxShadow: "var(--shadow)", maxWidth: 480 }}>
        <h3 className="font-semibold text-sm mb-3" style={{ color: "var(--ink)" }}>Suggest your own</h3>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            type="text"
            value={topicInput}
            onChange={(e) => setTopicInput(e.target.value)}
            placeholder="Topic name (e.g. Docker for .NET devs)"
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none"
            style={{ borderColor: "var(--border)", background: "var(--surface)", color: "var(--ink)" }}
          />
          <textarea
            value={whyInput}
            onChange={(e) => setWhyInput(e.target.value)}
            placeholder="Why it matters (optional)"
            rows={3}
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none resize-y"
            style={{ borderColor: "var(--border)", background: "var(--surface)", color: "var(--ink)" }}
          />
          <p className="text-xs" style={{ color: "var(--muted)" }}>Suggestions are public. Be kind. 🐼</p>
          {feedback && (
            <p className="text-xs" style={{ color: feedbackOk ? "var(--accent-hover)" : "var(--warn)" }}>
              {feedback}
            </p>
          )}
          <button
            type="submit"
            disabled={!topicInput.trim() || submitting}
            className="px-5 py-2 rounded-lg text-sm font-semibold text-white disabled:opacity-50"
            style={{ background: "var(--accent)" }}>
            {submitting ? "Submitting…" : "Submit suggestion"}
          </button>
        </form>
      </div>
    </div>
  );
}
