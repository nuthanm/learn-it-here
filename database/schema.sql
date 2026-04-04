-- ─────────────────────────────────────────────────────────────────────────────
-- Project Requirements Questionnaire — Supabase (PostgreSQL) Schema
-- Run this SQL in the Supabase SQL Editor to create the required table.
-- ─────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS project_requirements (
    id               UUID        DEFAULT gen_random_uuid()   PRIMARY KEY,
    submitted_at     TIMESTAMPTZ DEFAULT NOW()               NOT NULL,
    version_control  TEXT,
    ide              TEXT,
    dotnet_csharp    TEXT,
    ef_core          TEXT,
    architecture     TEXT,
    deployment       TEXT,
    crystal_report   TEXT,
    local_testing    TEXT,
    logging_tools    TEXT,
    project_mgmt     TEXT,
    unit_testing     TEXT,
    code_quality     TEXT,
    additional_notes TEXT
);

-- Enable Row Level Security (RLS)
ALTER TABLE project_requirements ENABLE ROW LEVEL SECURITY;

-- Allow anonymous inserts (used by the Streamlit app with the anon key)
CREATE POLICY "allow_anon_insert"
    ON project_requirements
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- Allow authenticated users to read all rows
CREATE POLICY "allow_auth_select"
    ON project_requirements
    FOR SELECT
    TO authenticated
    USING (true);
