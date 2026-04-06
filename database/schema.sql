-- ─────────────────────────────────────────────────────────────────────────────
-- Project Requirements Questionnaire — Supabase (PostgreSQL) Schema
-- Run this SQL in the Supabase SQL Editor to create the required table.
-- ─────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS project_requirements (
    id                 UUID        DEFAULT gen_random_uuid()   PRIMARY KEY,
    submitted_at       TIMESTAMPTZ DEFAULT NOW()               NOT NULL,
    version_control    TEXT,
    ide                TEXT,
    code_push          TEXT,
    deployment         TEXT,
    architecture       TEXT,
    design_patterns    TEXT,
    orm                TEXT,
    query_interaction  TEXT,
    databases          TEXT,
    analytical_tools   TEXT
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


-- ─────────────────────────────────────────────────────────────────────────────
-- Topic Suggestions — stores learning-hub topic requests from users
-- ─────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS topic_suggestions (
    id           UUID        DEFAULT gen_random_uuid()   PRIMARY KEY,
    topic        TEXT        NOT NULL,
    created_at   TIMESTAMPTZ DEFAULT NOW()               NOT NULL
);

-- Enable Row Level Security (RLS)
ALTER TABLE topic_suggestions ENABLE ROW LEVEL SECURITY;

-- Allow anonymous inserts (used by the Streamlit app with the anon key)
CREATE POLICY "allow_anon_insert"
    ON topic_suggestions
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- Allow anonymous users to read all rows (used by the app to display community topic suggestions)
CREATE POLICY "allow_anon_select"
    ON topic_suggestions
    FOR SELECT
    TO anon
    USING (true);

-- Allow authenticated users to read all rows
CREATE POLICY "allow_auth_select"
    ON topic_suggestions
    FOR SELECT
    TO authenticated
    USING (true);
