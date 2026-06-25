"use client";

import { useState, useCallback } from "react";
import Link from "next/link";
import { STEPS, Step } from "@/lib/steps";
import { RequirementsRecord } from "@/lib/types";

type FormValues = Record<string, string | string[]>;

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
      <label className="block font-semibold mb-1 text-sm" style={{ color: "var(--ink)" }}>
        {step.title}
        {step.help && (
          <span className="ml-2 font-normal" style={{ color: "var(--muted)", fontSize: 12 }}>
            {step.help}
          </span>
        )}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2"
        style={{
          borderColor: "var(--border)",
          background: "var(--card)",
          color: value ? "var(--ink)" : "var(--muted)",
        }}>
        <option value="">Choose an option</option>
        {step.options!.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
      {value === "Other" && (
        <input
          type="text"
          placeholder={`Specify ${step.title.toLowerCase()}`}
          value={otherValue}
          onChange={(e) => onOtherChange(e.target.value)}
          className="mt-2 w-full border rounded-lg px-3 py-2 text-sm focus:outline-none"
          style={{ borderColor: "var(--border)", background: "var(--card)", color: "var(--ink)" }}
        />
      )}
    </div>
  );
}

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
      <label className="block font-semibold mb-1 text-sm" style={{ color: "var(--ink)" }}>
        {step.title}
        {step.help && (
          <span className="ml-2 font-normal" style={{ color: "var(--muted)", fontSize: 12 }}>
            {step.help}
          </span>
        )}
      </label>
      <div className="flex flex-wrap gap-2 mt-1">
        {step.options!.map((opt) => {
          const checked = value.includes(opt);
          return (
            <button
              key={opt}
              type="button"
              onClick={() => toggle(opt)}
              className="px-3 py-1 rounded-full text-xs font-medium border transition-colors duration-100"
              style={{
                borderColor: checked ? "var(--accent)" : "var(--border)",
                background: checked ? "var(--accent-soft)" : "var(--card)",
                color: checked ? "var(--accent-hover)" : "var(--muted)",
              }}>
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
          className="mt-2 w-full border rounded-lg px-3 py-2 text-sm focus:outline-none"
          style={{ borderColor: "var(--border)", background: "var(--card)", color: "var(--ink)" }}
        />
      )}
    </div>
  );
}

function TextWidget({ step, value, onChange }: { step: Step; value: string; onChange: (v: string) => void }) {
  return (
    <div className="mb-5">
      <label className="block font-semibold mb-1 text-sm" style={{ color: "var(--ink)" }}>
        {step.title}
        {step.help && (
          <span className="ml-2 font-normal" style={{ color: "var(--muted)", fontSize: 12 }}>
            {step.help}
          </span>
        )}
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={step.placeholder ?? ""}
        rows={4}
        className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none resize-y"
        style={{ borderColor: "var(--border)", background: "var(--card)", color: "var(--ink)" }}
      />
    </div>
  );
}

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
  const record: RequirementsRecord = {
    submitted_at: new Date().toISOString(),
  };
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
        const blob = await pdfRes.blob();
        setPdfBlob(blob);
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

  if (submitted) {
    return (
      <div style={{ maxWidth: 640 }}>
        <h2 className="font-bold text-2xl mb-2" style={{ color: "var(--ink)" }}>
          All done — great work 🎉
        </h2>
        <p className="mb-4 text-sm" style={{ color: "var(--body)" }}>
          Your project requirements have been captured.
        </p>

        {dbMessage && (
          <div className="p-3 rounded-lg mb-4 text-sm"
            style={{ background: "var(--accent-soft)", color: "var(--ink)", border: "1px solid var(--accent)" }}>
            {dbMessage}
          </div>
        )}

        <div className="success-card mb-6">
          <p className="font-semibold mb-1" style={{ color: "var(--ink)" }}>Submission saved</p>
          <p className="text-sm" style={{ color: "var(--body)" }}>
            Download a shareable PDF of your project brief below, or move on to the learning hub.
          </p>
        </div>

        <div className="flex gap-3 flex-wrap">
          <button
            onClick={downloadPdf}
            disabled={!pdfBlob}
            className="px-5 py-2 rounded-lg text-sm font-semibold text-white disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ background: "var(--accent)" }}>
            📄 Download PDF
          </button>
          <button
            onClick={reset}
            className="px-5 py-2 rounded-lg text-sm font-semibold border"
            style={{ borderColor: "var(--border)", color: "var(--ink)", background: "var(--card)" }}>
            Submit another response
          </button>
        </div>
        {pdfError && (
          <p className="mt-3 text-xs" style={{ color: "var(--muted)" }}>{pdfError}</p>
        )}
        <p className="mt-5 text-sm">
          <Link href="/learning-hub" className="font-semibold no-underline hover:underline"
            style={{ color: "var(--accent)" }}>
            Browse the learning hub →
          </Link>
        </p>
      </div>
    );
  }

  let lastSection = "";

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 640 }}>
      <div className="rounded-xl p-6 mb-6" style={{ background: "var(--card)", boxShadow: "var(--shadow)" }}>
        {STEPS.map((step) => {
          const sectionHeader = step.section !== lastSection ? step.section : null;
          if (step.section !== lastSection) lastSection = step.section;

          return (
            <div key={step.key}>
              {sectionHeader && (
                <div className="text-xs font-semibold uppercase tracking-wider mb-3 mt-5 first:mt-0 pb-1 border-b"
                  style={{ color: "var(--accent)", borderColor: "var(--border)", letterSpacing: "1px" }}>
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

      <div className="flex justify-end gap-3">
        <Link href="/"
          className="inline-flex items-center px-5 py-2 rounded-lg text-sm font-semibold border no-underline"
          style={{ borderColor: "var(--border)", color: "var(--ink)", background: "var(--card)" }}>
          Cancel
        </Link>
        <button
          type="submit"
          disabled={loading}
          className="px-5 py-2 rounded-lg text-sm font-semibold text-white disabled:opacity-60"
          style={{ background: "var(--accent)" }}>
          {loading ? "Submitting…" : "Submit requirements"}
        </button>
      </div>
    </form>
  );
}
