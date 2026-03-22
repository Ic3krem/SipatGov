-- ============================================================================
-- SipatGov - Initial Schema Migration
-- Translated from SQLAlchemy models in backend/app/models/
-- ============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- REGIONS
-- ============================================================================
CREATE TABLE regions (
    id              SERIAL PRIMARY KEY,
    psgc_code       VARCHAR(10) NOT NULL,
    name            VARCHAR(100) NOT NULL,
    region_code     VARCHAR(20) NOT NULL
);

CREATE UNIQUE INDEX idx_regions_psgc ON regions (psgc_code);

-- ============================================================================
-- PROVINCES
-- ============================================================================
CREATE TABLE provinces (
    id              SERIAL PRIMARY KEY,
    psgc_code       VARCHAR(10) NOT NULL,
    name            VARCHAR(100) NOT NULL,
    region_id       INTEGER NOT NULL REFERENCES regions(id)
);

CREATE UNIQUE INDEX idx_provinces_psgc ON provinces (psgc_code);
CREATE INDEX idx_provinces_region ON provinces (region_id);

-- ============================================================================
-- LGUs (Local Government Units)
-- ============================================================================
CREATE TABLE lgus (
    id                  SERIAL PRIMARY KEY,
    psgc_code           VARCHAR(10) NOT NULL,
    name                VARCHAR(150) NOT NULL,
    lgu_type            VARCHAR(20) NOT NULL,
    province_id         INTEGER REFERENCES provinces(id),
    region_id           INTEGER NOT NULL REFERENCES regions(id),
    latitude            NUMERIC(10,7),
    longitude           NUMERIC(10,7),
    population          INTEGER,
    income_class        VARCHAR(10),
    transparency_score  NUMERIC(5,2) NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_lgus_type CHECK (
        lgu_type IN ('municipality', 'city', 'province', 'barangay')
    )
);

CREATE UNIQUE INDEX idx_lgus_psgc ON lgus (psgc_code);
CREATE INDEX idx_lgus_type ON lgus (lgu_type);
CREATE INDEX idx_lgus_province ON lgus (province_id);
CREATE INDEX idx_lgus_region ON lgus (region_id);
CREATE INDEX idx_lgus_coords ON lgus (latitude, longitude);

-- ============================================================================
-- OFFICIALS
-- ============================================================================
CREATE TABLE officials (
    id              SERIAL PRIMARY KEY,
    lgu_id          INTEGER NOT NULL REFERENCES lgus(id),
    full_name       VARCHAR(200) NOT NULL,
    position        VARCHAR(100) NOT NULL,
    party           VARCHAR(100),
    term_start      DATE,
    term_end        DATE,
    is_current      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_officials_lgu ON officials (lgu_id);
CREATE INDEX idx_officials_current ON officials (is_current) WHERE is_current = true;

-- ============================================================================
-- DOCUMENTS
-- ============================================================================
CREATE TABLE documents (
    id                  SERIAL PRIMARY KEY,
    source_portal       VARCHAR(50) NOT NULL,
    source_url          TEXT NOT NULL,
    title               VARCHAR(500),
    document_type       VARCHAR(50),
    lgu_id              INTEGER REFERENCES lgus(id),
    file_path           TEXT,
    file_hash           VARCHAR(64),
    raw_text            TEXT,
    structured_data     JSONB,
    processing_status   VARCHAR(20) NOT NULL DEFAULT 'pending',
    processing_error    TEXT,
    crawled_at          TIMESTAMPTZ,
    processed_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_docs_source_portal CHECK (
        source_portal IN ('philgeps', 'dbm', 'coa', 'efoi', 'manual')
    ),
    CONSTRAINT ck_docs_processing_status CHECK (
        processing_status IN ('pending', 'downloading', 'ocr_processing', 'nlp_processing', 'completed', 'failed')
    )
);

CREATE INDEX idx_docs_source_portal ON documents (source_portal);
CREATE INDEX idx_docs_lgu ON documents (lgu_id);
CREATE INDEX idx_docs_processing_status ON documents (processing_status);
CREATE UNIQUE INDEX idx_docs_hash ON documents (file_hash) WHERE file_hash IS NOT NULL;
CREATE INDEX idx_docs_structured ON documents USING GIN (structured_data);

-- ============================================================================
-- BUDGET ALLOCATIONS
-- ============================================================================
CREATE TABLE budget_allocations (
    id                      SERIAL PRIMARY KEY,
    lgu_id                  INTEGER NOT NULL REFERENCES lgus(id),
    fiscal_year             INTEGER NOT NULL,
    category                VARCHAR(100) NOT NULL,
    subcategory             VARCHAR(150),
    allocated_amount        NUMERIC(18,2) NOT NULL,
    released_amount         NUMERIC(18,2) NOT NULL DEFAULT 0,
    utilized_amount         NUMERIC(18,2) NOT NULL DEFAULT 0,
    source_document_id      INTEGER REFERENCES documents(id),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_budget UNIQUE (lgu_id, fiscal_year, category, subcategory)
);

CREATE INDEX idx_budget_category ON budget_allocations (category);
CREATE INDEX idx_budget_lgu_year ON budget_allocations (lgu_id, fiscal_year);

-- ============================================================================
-- PROJECTS
-- ============================================================================
CREATE TABLE projects (
    id                  SERIAL PRIMARY KEY,
    lgu_id              INTEGER NOT NULL REFERENCES lgus(id),
    title               VARCHAR(500) NOT NULL,
    description         TEXT,
    category            VARCHAR(100),
    status              VARCHAR(30) NOT NULL DEFAULT 'planned',
    contractor          VARCHAR(300),
    approved_budget     NUMERIC(18,2),
    contract_amount     NUMERIC(18,2),
    actual_cost         NUMERIC(18,2),
    start_date          DATE,
    target_end_date     DATE,
    actual_end_date     DATE,
    latitude            NUMERIC(10,7),
    longitude           NUMERIC(10,7),
    address             TEXT,
    philgeps_ref        VARCHAR(50),
    source_document_id  INTEGER REFERENCES documents(id),
    fiscal_year         INTEGER,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_projects_status CHECK (
        status IN ('planned', 'bidding', 'awarded', 'ongoing', 'completed', 'delayed', 'cancelled', 'suspended')
    )
);

CREATE INDEX idx_projects_lgu ON projects (lgu_id);
CREATE INDEX idx_projects_status ON projects (status);
CREATE INDEX idx_projects_philgeps ON projects (philgeps_ref);
CREATE INDEX idx_projects_fiscal_year ON projects (fiscal_year);
CREATE INDEX idx_projects_coords ON projects (latitude, longitude);

-- ============================================================================
-- PROMISES
-- ============================================================================
CREATE TABLE promises (
    id                  SERIAL PRIMARY KEY,
    official_id         INTEGER REFERENCES officials(id),
    lgu_id              INTEGER NOT NULL REFERENCES lgus(id),
    title               VARCHAR(500) NOT NULL,
    description         TEXT,
    category            VARCHAR(100),
    status              VARCHAR(20) NOT NULL DEFAULT 'pending',
    evidence_summary    TEXT,
    date_promised       DATE,
    deadline            DATE,
    verified_at         TIMESTAMPTZ,
    verified_by         VARCHAR(100),
    confidence_score    NUMERIC(3,2),
    source_document_id  INTEGER REFERENCES documents(id),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_promises_status CHECK (
        status IN ('kept', 'broken', 'in_progress', 'pending', 'partially_kept', 'unverifiable')
    )
);

CREATE INDEX idx_promises_official ON promises (official_id);
CREATE INDEX idx_promises_lgu ON promises (lgu_id);
CREATE INDEX idx_promises_status ON promises (status);

-- ============================================================================
-- PROMISE EVIDENCE
-- ============================================================================
CREATE TABLE promise_evidence (
    id              SERIAL PRIMARY KEY,
    promise_id      INTEGER NOT NULL REFERENCES promises(id) ON DELETE CASCADE,
    evidence_type   VARCHAR(30) NOT NULL,
    project_id      INTEGER REFERENCES projects(id),
    document_id     INTEGER REFERENCES documents(id),
    budget_id       INTEGER REFERENCES budget_allocations(id),
    report_id       INTEGER,  -- FK added after community_reports table is created
    external_url    TEXT,
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_evidence_type CHECK (
        evidence_type IN ('project', 'document', 'budget', 'report', 'external_link')
    )
);

CREATE INDEX idx_evidence_promise ON promise_evidence (promise_id);

-- ============================================================================
-- USERS
-- ============================================================================
CREATE TABLE users (
    id                      SERIAL PRIMARY KEY,
    email                   VARCHAR(255),
    phone                   VARCHAR(20),
    display_name            VARCHAR(100),
    password_hash           VARCHAR(255),
    avatar_url              TEXT,
    home_lgu_id             INTEGER REFERENCES lgus(id),
    home_region_id          INTEGER REFERENCES regions(id),
    role                    VARCHAR(20) NOT NULL DEFAULT 'citizen',
    is_verified             BOOLEAN NOT NULL DEFAULT FALSE,
    onboarding_completed    BOOLEAN NOT NULL DEFAULT FALSE,
    supabase_uid            VARCHAR(36),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_users_role CHECK (role IN ('citizen', 'moderator', 'admin'))
);

CREATE UNIQUE INDEX idx_users_email ON users (email) WHERE email IS NOT NULL;
CREATE UNIQUE INDEX idx_users_phone ON users (phone) WHERE phone IS NOT NULL;
CREATE UNIQUE INDEX idx_users_supabase_uid ON users (supabase_uid) WHERE supabase_uid IS NOT NULL;
CREATE INDEX idx_users_home_lgu ON users (home_lgu_id);

-- ============================================================================
-- COMMUNITY REPORTS
-- ============================================================================
CREATE TABLE community_reports (
    id                  SERIAL PRIMARY KEY,
    user_id             INTEGER NOT NULL REFERENCES users(id),
    lgu_id              INTEGER NOT NULL REFERENCES lgus(id),
    project_id          INTEGER REFERENCES projects(id),
    title               VARCHAR(300) NOT NULL,
    description         TEXT NOT NULL,
    report_type         VARCHAR(30) NOT NULL,
    status              VARCHAR(20) NOT NULL DEFAULT 'submitted',
    latitude            NUMERIC(10,7),
    longitude           NUMERIC(10,7),
    address             TEXT,
    upvote_count        INTEGER NOT NULL DEFAULT 0,
    is_anonymous        BOOLEAN NOT NULL DEFAULT FALSE,
    moderation_notes    TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_reports_type CHECK (
        report_type IN ('concern', 'feedback', 'corruption_tip', 'progress_update', 'delay_report')
    ),
    CONSTRAINT ck_reports_status CHECK (
        status IN ('submitted', 'under_review', 'verified', 'resolved', 'dismissed')
    )
);

CREATE INDEX idx_reports_user ON community_reports (user_id);
CREATE INDEX idx_reports_lgu ON community_reports (lgu_id);
CREATE INDEX idx_reports_project ON community_reports (project_id);
CREATE INDEX idx_reports_type ON community_reports (report_type);
CREATE INDEX idx_reports_status ON community_reports (status);

-- Deferred FK: promise_evidence.report_id -> community_reports.id
ALTER TABLE promise_evidence
    ADD CONSTRAINT fk_evidence_report
    FOREIGN KEY (report_id) REFERENCES community_reports(id);

-- ============================================================================
-- REPORT ATTACHMENTS
-- ============================================================================
CREATE TABLE report_attachments (
    id              SERIAL PRIMARY KEY,
    report_id       INTEGER NOT NULL REFERENCES community_reports(id) ON DELETE CASCADE,
    file_url        TEXT NOT NULL,
    file_type       VARCHAR(20),
    thumbnail_url   TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_attachments_report ON report_attachments (report_id);

-- ============================================================================
-- REPORT UPVOTES (composite PK)
-- ============================================================================
CREATE TABLE report_upvotes (
    user_id     INTEGER NOT NULL REFERENCES users(id),
    report_id   INTEGER NOT NULL REFERENCES community_reports(id) ON DELETE CASCADE,

    PRIMARY KEY (user_id, report_id)
);

-- ============================================================================
-- CRAWL JOBS
-- ============================================================================
CREATE TABLE crawl_jobs (
    id              SERIAL PRIMARY KEY,
    spider_name     VARCHAR(50) NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'running',
    items_scraped   INTEGER NOT NULL DEFAULT 0,
    items_failed    INTEGER NOT NULL DEFAULT 0,
    started_at      TIMESTAMPTZ,
    finished_at     TIMESTAMPTZ,
    error_log       TEXT,

    CONSTRAINT ck_crawl_status CHECK (
        status IN ('running', 'completed', 'failed')
    )
);

-- ============================================================================
-- AUTO-UPDATE updated_at TRIGGER
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to all tables with that column
DO $$
DECLARE
    tbl TEXT;
BEGIN
    FOR tbl IN
        SELECT table_name FROM information_schema.columns
        WHERE column_name = 'updated_at'
          AND table_schema = 'public'
    LOOP
        EXECUTE format(
            'CREATE TRIGGER trg_%s_updated_at
             BEFORE UPDATE ON %I
             FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();',
            tbl, tbl
        );
    END LOOP;
END;
$$;
