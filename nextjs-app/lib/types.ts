/**
 * Shared TypeScript types used across the Next.js app.
 * Mirrors the Python models.py in the Streamlit source.
 */

export interface RequirementsRecord {
  submitted_at?: string;
  version_control?: string;
  ide?: string;
  code_push?: string;
  deployment?: string;
  architecture?: string;
  design_patterns?: string;
  orm?: string;
  additional_requirements?: string;
}

export interface SaveResult {
  ok: boolean;
  message: string;
}

export interface TopicRow {
  topic: string;
}

/** A single section in the learning hub menu. */
export interface LearnSection {
  slug: string;
  title: string;
  subsections?: LearnSubsection[];
}

export interface LearnSubsection {
  slug: string;
  title: string;
}
