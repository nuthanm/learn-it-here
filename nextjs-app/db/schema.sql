-- ─────────────────────────────────────────────────────────────────────────────
-- Learn It Here — Neon DB Schema
-- Compatible with the original Supabase schema in database/schema.sql
-- Run this in the Neon SQL Editor (or via psql) to provision the tables.
-- ─────────────────────────────────────────────────────────────────────────────

-- Project Requirements Questionnaire
CREATE TABLE IF NOT EXISTS project_requirements (
    id                     UUID        DEFAULT gen_random_uuid()   PRIMARY KEY,
    submitted_at           TIMESTAMPTZ DEFAULT NOW()               NOT NULL,
    version_control        TEXT,
    ide                    TEXT,
    code_push              TEXT,
    deployment             TEXT,
    architecture           TEXT,
    design_patterns        TEXT,
    orm                    TEXT,
    additional_requirements TEXT,
    -- legacy columns kept for data-migration compatibility
    query_interaction      TEXT,
    databases              TEXT,
    analytical_tools       TEXT
);

-- Topic Suggestions
CREATE TABLE IF NOT EXISTS topic_suggestions (
    id          UUID        DEFAULT gen_random_uuid()   PRIMARY KEY,
    topic       TEXT        NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()               NOT NULL
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_topic_suggestions_created_at
    ON topic_suggestions (created_at DESC);
