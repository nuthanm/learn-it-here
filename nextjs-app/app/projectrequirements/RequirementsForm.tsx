"use client";

import { useState, useCallback } from "react";
import Link from "next/link";
import { STEPS, Step } from "@/lib/steps";
import { RequirementsRecord } from "@/lib/types";

type FormValues = Record<string, string | string[]>;

// ── Section progress tracker ──────────────────────────────────────────────────
function SectionProgress({ completedCount, totalCount }: { completedCount: number; totalCount: number }) {
  const pct = Math.round((completedCount / totalCount) * 100);
  return (
    <div style={{ marginBottom: 20 }}>
      <div className="flex items-center justify-between mb-2">
        <span style={{ fontSize: 12, fontWeight: 600, color: "var(--muted)" }}>
          {completedCount} of {totalCount} answered
        </span>
        <span style={{ fontSize: 12, fontWeight: 700, color: pct === 100 ? "var(--accent-hover)" : "var(--muted)" }}>
          {pct}%
        </span>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

// ── Select widget ─────────────────────────────────────────────────────────────
function SelectWidget({
  step,
  value,
  otherValue,
  onChange,
  onOtherChange,
}: {
  step: Step;
  value: string;
  otherValue: string;
  onChange: (v: string) => void;
  onOtherChange: (v: string) => void;
}) {
  return (
    <div className="mb-5">
      <label className="block mb-1" style={{ fontSize: 13, fontWeight: 600, color: "var(--ink)" }}>
        {step.title}
        {step.help && (
          <span style={{ fontSize: 12, fontWeight: 400, color: "var(--muted)", marginLeft: 6 }}>
            {step.help}
          </span>
        )}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="form-input"
        style={{ color: value ? "var(--ink)" : "var(--muted)" }}>
        <option value="">Choose an option…</option>
        {step.options!.map((opt) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
      {value === "Other" && (
        <input
          type="text"
          placeholder={`Specify ${step.title.toLowerCase()}`}
          value={otherValue}
          onChange={(e) => onOtherChange(e.target.value)}
          className="form-input mt-2"
        />
      )}
    </div>
  );
}

// ── Multi-select widget ───────────────────────────────────────────────────────
function MultiWidget({
  step,
  value,
  otherValue,
  onChange,
  onOtherChange,
}: {
  step: Step;
  value: string[];
  otherValue: string;
  onChange: (v: string[]) => void;
  onOtherChange: (v: string) => void;
}) {
  const toggle = (opt: string) => {
    if (value.includes(opt)) {
      onChange(value.filter((x) => x !== opt));
    } else {
      onChange([...value, opt]);
    }
  };

  return (
    <div className="mb-5">
      <label className="block mb-2" style={{ fontSize: 13, fontWeight: 600, color: "var(--ink)" }}>
        {step.title}
        {step.help && (
          <span style={{ fontSize: 12, fontWeight: 400, color: "var(--muted)", marginLeft: 6 }}>
            {step.help}
          </span>
        )}
      </label>
      <div className="flex flex-wrap gap-2">
        {step.options!.map((opt) => {
          const checked = value.includes(opt);
          return (
            <button
              key={opt}
              type="button"
              onClick={() => toggle(opt)}
              style={{
                padding: "5px 14px",
                borderRadius: 999,
                fontSize: 12,
                fontWeight: 500,
                border: checked ? "1.5px solid var(--accent)" : "1.5px solid var(--border)",
                background: checked ? "var(--accent-soft)" : "var(--card)",
                color: checked ? "var(--accent-hover)" : "var(--muted)",
                cursor: "pointer",
                transition: "all 120ms ease",
              }}>
              {checked && <span style={{ marginRight: 4 }}>✓</span>}
              {opt}
            </button>
          );
        })}
      </div>
      {value.includes("Other") && (
        <input
          type="text"
          placeholder={`Specify other ${step.title.toLowerCase()}`}
          value={otherValue}
          onChange={(e) => onOtherChange(e.target.value)}
          className="form-input mt-2"
        />
      )}
    </div>
  );
}

// ── Text widget ───────────────────────────────────────────────────────────────
function TextWidget({ step, value, onChange }: { step: Step; value: string; onChange: (v: string) => void }) {
  return (
    <div className="mb-5">
      <label className="block mb-1" style={{ fontSize: 13, fontWeight: 600, color: "var(--ink)" }}>
        {step.title}
        {step.help && (
          <span style={{ fontSize: 12, fontWeight: 400, color: "var(--muted)", marginLeft: 6 }}>
            {step.help}
          </span>
        )}
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={step.placeholder ?? ""}
        rows={4}
        className="form-input resize-y"
      />
    </div>
  );
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function resolveSelect(key: string, value: string, others: Record<string, string>): string {
  if (!value) return "";
  if (value === "Other") return (others[`${key}_other`] || "Other").trim();
  return value;
}

function resolveMulti(key: string, value: string[], others: Record<string, string>): string {
  const items = [...(value || [])];
  const other = (others[`${key}_other`] || "").trim();
  if (items.includes("Other") && other) {
    return items.map((x) => (x === "Other" ? other : x)).join(", ");
  }
  return items.join(", ");
}

function buildRecord(values: FormValues, others: Record<string, string>): RequirementsRecord {
  const record: RequirementsRecord = { submitted_at: new Date().toISOString() };
  for (const step of STEPS) {
    const raw = values[step.key];
    if (step.kind === "select") {
      (record as Record<string, string>)[step.key] = resolveSelect(step.key, (raw as string) ?? "", others);
    } else if (step.kind === "multi") {
      (record as Record<string, string>)[step.key] = resolveMulti(step.key, (raw as string[]) ?? [], others);
    } else {
      (record as Record<string, string>)[step.key] = ((raw as string) ?? "").trim();
    }
  }
  return record;
}

function countAnswered(values: FormValues): number {
  return STEPS.filter((s) => {
    const v = values[s.key];
    if (!v) return false;
    if (Array.isArray(v)) return v.length > 0;
    return (v as string).length > 0;
  }).length;
}

// ── Main form ─────────────────────────────────────────────────────────────────
export default function RequirementsForm() {
  const [values, setValues] = useState<FormValues>({});
  const [others, setOthers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [pdfBlob, setPdfBlob] = useState<Blob | null>(null);
  const [pdfError, setPdfError] = useState<string | null>(null);
  const [dbMessage, setDbMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const setValue = useCallback((key: string, val: string | string[]) => {
    setValues((prev) => ({ ...prev, [key]: val }));
  }, []);

  const setOther = useCallback((key: string, val: string) => {
    setOthers((prev) => ({ ...prev, [key]: val }));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const record = buildRecord(values, others);

    // Save to DB
    try {
      const res = await fetch("/api/requirements", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(record),
      });
      const data = await res.json();
      setDbMessage(data.message ?? (data.ok ? "Saved." : "Could not save to database."));
    } catch {
      setDbMessage("Network error — could not reach the database.");
    }

    // Generate PDF
    try {
      const pdfRes = await fetch("/api/pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(record),
      });
      if (pdfRes.ok) {
        setPdfBlob(await pdfRes.blob());
        setPdfError(null);
      } else {
        setPdfError("PDF generation failed.");
      }
    } catch {
      setPdfError("PDF generation failed.");
    }

    setLoading(false);
    setSubmitted(true);
  };

  const downloadPdf = () => {
    if (!pdfBlob) return;
    const url = URL.createObjectURL(pdfBlob);
    const a = document.createElement("a");
    a.href = url;
    const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    a.download = `project_requirements_${ts}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const reset = () => {
    setValues({});
    setOthers({});
    setSubmitted(false);
    setPdfBlob(null);
    setPdfError(null);
    setDbMessage(null);
  };

  // ── Success view ────────────────────────────────────────────────────────────
  if (submitted) {
    return (
      <div style={{ maxWidth: 560 }}>
        {/* Confetti header */}
        <div
          style={{
            background: "var(--hero-grad)",
            border: "1px solid rgba(93,163,52,.2)",
            borderRadius: "var(--r-lg)",
            padding: "32px 28px",
            textAlign: "center",
            marginBottom: 20,
          }}>
          <div style={{ fontSize: 48, marginBottom: 10 }}>🎉</div>
          <h2 style={{ fontSize: 22, fontWeight: 800, color: "var(--ink)", marginBottom: 6 }}>
            All done — great work!
          </h2>
          <p style={{ fontSize: 14, color: "var(--body)", lineHeight: 1.7 }}>
            Your project requirements have been captured.
          </p>
        </div>

        {dbMessage && (
          <div className="info-card mb-4">
            ℹ️ {dbMessage}
          </div>
        )}

        <div className="success-card mb-5">
          <p style={{ fontWeight: 700, color: "var(--ink)", marginBottom: 4 }}>📄 Your PDF is ready</p>
          <p style={{ fontSize: 13, color: "var(--body)", lineHeight: 1.6 }}>
            Download a branded, shareable PDF summary of your project brief — or jump straight into the learning hub.
          </p>
        </div>

        <div className="flex gap-3 flex-wrap mb-4">
          <button
            onClick={downloadPdf}
            disabled={!pdfBlob}
            className="btn-primary">
            📄 Download PDF
          </button>
          <button onClick={reset} className="btn-secondary">
            Submit another response
          </button>
        </div>

        {pdfError && (
          <p style={{ fontSize: 12, color: "var(--muted)", marginBottom: 12 }}>{pdfError}</p>
        )}

        <p style={{ fontSize: 14, marginTop: 16 }}>
          <Link href="/learning-hub" className="no-underline hover:underline" style={{ color: "var(--accent)", fontWeight: 700 }}>
            Browse the learning hub →
          </Link>
        </p>
      </div>
    );
  }

  // ── Form view ───────────────────────────────────────────────────────────────
  const answered = countAnswered(values);
  let lastSection = "";

  return (
    <form onSubmit={handleSubmit}>
      {/* Progress bar */}
      <SectionProgress completedCount={answered} totalCount={STEPS.length} />

      {/* Questions card */}
      <div className="card" style={{ padding: "28px 28px", marginBottom: 20 }}>
        {STEPS.map((step) => {
          const sectionHeader = step.section !== lastSection ? step.section : null;
          if (step.section !== lastSection) lastSection = step.section;

          return (
            <div key={step.key}>
              {sectionHeader && (
                <div
                  style={{
                    fontSize: 10,
                    fontWeight: 800,
                    textTransform: "uppercase" as const,
                    letterSpacing: "0.08em",
                    color: "var(--accent)",
                    marginTop: 20,
                    marginBottom: 12,
                    paddingBottom: 8,
                    borderBottom: "1px solid var(--border)",
                  }}
                  className="first:mt-0">
                  {sectionHeader}
                </div>
              )}
              {step.kind === "select" && (
                <SelectWidget
                  step={step}
                  value={(values[step.key] as string) ?? ""}
                  otherValue={others[`${step.key}_other`] ?? ""}
                  onChange={(v) => setValue(step.key, v)}
                  onOtherChange={(v) => setOther(`${step.key}_other`, v)}
                />
              )}
              {step.kind === "multi" && (
                <MultiWidget
                  step={step}
                  value={(values[step.key] as string[]) ?? []}
                  otherValue={others[`${step.key}_other`] ?? ""}
                  onChange={(v) => setValue(step.key, v)}
                  onOtherChange={(v) => setOther(`${step.key}_other`, v)}
                />
              )}
              {step.kind === "text" && (
                <TextWidget
                  step={step}
                  value={(values[step.key] as string) ?? ""}
                  onChange={(v) => setValue(step.key, v)}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Submit row */}
      <div className="flex justify-between items-center gap-3 flex-wrap">
        <p style={{ fontSize: 12, color: "var(--muted)" }}>
          {answered === STEPS.length
            ? "✅ All questions answered — ready to submit!"
            : `${STEPS.length - answered} question${STEPS.length - answered > 1 ? "s" : ""} remaining`}
        </p>
        <div className="flex gap-3">
          <Link href="/" className="btn-secondary" style={{ fontSize: 13 }}>
            Cancel
          </Link>
          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{ fontSize: 13 }}>
            {loading ? "Submitting…" : "Submit requirements"}
          </button>
        </div>
      </div>
    </form>
  );
}
