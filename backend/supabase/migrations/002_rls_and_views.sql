-- ============================================================================
-- SipatGov - Row-Level Security (RLS) Policies & Materialized Views
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE regions ENABLE ROW LEVEL SECURITY;
ALTER TABLE provinces ENABLE ROW LEVEL SECURITY;
ALTER TABLE lgus ENABLE ROW LEVEL SECURITY;
ALTER TABLE officials ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_allocations ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE promises ENABLE ROW LEVEL SECURITY;
ALTER TABLE promise_evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE report_attachments ENABLE ROW LEVEL SECURITY;
ALTER TABLE report_upvotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE crawl_jobs ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- PUBLIC READ POLICIES (geographic & government data is public)
-- ============================================================================

-- Regions: public read
CREATE POLICY regions_public_read ON regions
    FOR SELECT USING (true);

-- Provinces: public read
CREATE POLICY provinces_public_read ON provinces
    FOR SELECT USING (true);

-- LGUs: public read
CREATE POLICY lgus_public_read ON lgus
    FOR SELECT USING (true);

-- Officials: public read
CREATE POLICY officials_public_read ON officials
    FOR SELECT USING (true);

-- Promises: public read
CREATE POLICY promises_public_read ON promises
    FOR SELECT USING (true);

-- Promise evidence: public read
CREATE POLICY promise_evidence_public_read ON promise_evidence
    FOR SELECT USING (true);

-- Projects: public read
CREATE POLICY projects_public_read ON projects
    FOR SELECT USING (true);

-- Budget allocations: public read
CREATE POLICY budget_allocations_public_read ON budget_allocations
    FOR SELECT USING (true);

-- Documents: public read (metadata only, raw_text access controlled by app)
CREATE POLICY documents_public_read ON documents
    FOR SELECT USING (true);

-- Community reports: public read (non-anonymous shows user, anonymous hides)
CREATE POLICY community_reports_public_read ON community_reports
    FOR SELECT USING (true);

-- Report attachments: public read
CREATE POLICY report_attachments_public_read ON report_attachments
    FOR SELECT USING (true);

-- Report upvotes: public read
CREATE POLICY report_upvotes_public_read ON report_upvotes
    FOR SELECT USING (true);

-- ============================================================================
-- USER-SPECIFIC WRITE POLICIES
-- ============================================================================

-- Helper function: get app user id from Supabase auth.uid()
CREATE OR REPLACE FUNCTION get_app_user_id()
RETURNS INTEGER AS $$
    SELECT id FROM users WHERE supabase_uid = auth.uid()::TEXT LIMIT 1;
$$ LANGUAGE sql SECURITY DEFINER STABLE;

-- Users: can update own profile
CREATE POLICY users_self_read ON users
    FOR SELECT USING (true);

CREATE POLICY users_self_update ON users
    FOR UPDATE USING (supabase_uid = auth.uid()::TEXT)
    WITH CHECK (supabase_uid = auth.uid()::TEXT);

CREATE POLICY users_self_insert ON users
    FOR INSERT WITH CHECK (supabase_uid = auth.uid()::TEXT);

-- Community reports: authenticated users can create
CREATE POLICY community_reports_insert ON community_reports
    FOR INSERT WITH CHECK (user_id = get_app_user_id());

-- Community reports: authors can update their own (status stays submitted)
CREATE POLICY community_reports_update_own ON community_reports
    FOR UPDATE USING (user_id = get_app_user_id())
    WITH CHECK (user_id = get_app_user_id());

-- Report attachments: authors of the parent report can insert
CREATE POLICY report_attachments_insert ON report_attachments
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM community_reports cr
            WHERE cr.id = report_id AND cr.user_id = get_app_user_id()
        )
    );

-- Report upvotes: authenticated users can manage their own votes
CREATE POLICY report_upvotes_insert ON report_upvotes
    FOR INSERT WITH CHECK (user_id = get_app_user_id());

CREATE POLICY report_upvotes_delete ON report_upvotes
    FOR DELETE USING (user_id = get_app_user_id());

-- ============================================================================
-- ADMIN/MODERATOR POLICIES
-- ============================================================================

-- Helper function: check if current user is admin or moderator
CREATE OR REPLACE FUNCTION is_admin_or_moderator()
RETURNS BOOLEAN AS $$
    SELECT EXISTS (
        SELECT 1 FROM users
        WHERE supabase_uid = auth.uid()::TEXT
          AND role IN ('admin', 'moderator')
    );
$$ LANGUAGE sql SECURITY DEFINER STABLE;

-- Admins can manage all government data tables
CREATE POLICY officials_admin_all ON officials
    FOR ALL USING (is_admin_or_moderator());

CREATE POLICY promises_admin_all ON promises
    FOR ALL USING (is_admin_or_moderator());

CREATE POLICY promise_evidence_admin_all ON promise_evidence
    FOR ALL USING (is_admin_or_moderator());

CREATE POLICY projects_admin_all ON projects
    FOR ALL USING (is_admin_or_moderator());

CREATE POLICY budget_admin_all ON budget_allocations
    FOR ALL USING (is_admin_or_moderator());

CREATE POLICY documents_admin_all ON documents
    FOR ALL USING (is_admin_or_moderator());

CREATE POLICY lgus_admin_all ON lgus
    FOR ALL USING (is_admin_or_moderator());

-- Moderators can update community report status
CREATE POLICY community_reports_moderate ON community_reports
    FOR UPDATE USING (is_admin_or_moderator());

-- Crawl jobs: admin only
CREATE POLICY crawl_jobs_admin_read ON crawl_jobs
    FOR SELECT USING (is_admin_or_moderator());

CREATE POLICY crawl_jobs_admin_all ON crawl_jobs
    FOR ALL USING (is_admin_or_moderator());

-- ============================================================================
-- SERVICE ROLE BYPASS (for backend API / cron jobs)
-- These policies use the Supabase service_role which bypasses RLS by default.
-- No explicit policies needed; the service_role key skips RLS.
-- ============================================================================

-- ============================================================================
-- MATERIALIZED VIEW: Promise Statistics per LGU
-- ============================================================================
CREATE MATERIALIZED VIEW mv_promise_stats AS
SELECT
    l.id                                        AS lgu_id,
    l.name                                      AS lgu_name,
    l.lgu_type,
    r.name                                      AS region_name,
    r.region_code,
    COUNT(p.id)                                 AS total_promises,
    COUNT(p.id) FILTER (WHERE p.status = 'kept')           AS kept_count,
    COUNT(p.id) FILTER (WHERE p.status = 'broken')         AS broken_count,
    COUNT(p.id) FILTER (WHERE p.status = 'in_progress')    AS in_progress_count,
    COUNT(p.id) FILTER (WHERE p.status = 'pending')        AS pending_count,
    COUNT(p.id) FILTER (WHERE p.status = 'partially_kept') AS partially_kept_count,
    COUNT(p.id) FILTER (WHERE p.status = 'unverifiable')   AS unverifiable_count,
    CASE
        WHEN COUNT(p.id) > 0 THEN
            ROUND(
                (COUNT(p.id) FILTER (WHERE p.status = 'kept')::NUMERIC
                 + 0.5 * COUNT(p.id) FILTER (WHERE p.status = 'partially_kept')::NUMERIC)
                / COUNT(p.id)::NUMERIC * 100,
            1)
        ELSE 0
    END                                         AS fulfillment_rate,
    l.latitude,
    l.longitude
FROM lgus l
JOIN regions r ON r.id = l.region_id
LEFT JOIN promises p ON p.lgu_id = l.id
GROUP BY l.id, l.name, l.lgu_type, r.name, r.region_code, l.latitude, l.longitude
WITH DATA;

-- Unique index required for REFRESH MATERIALIZED VIEW CONCURRENTLY
CREATE UNIQUE INDEX idx_mv_promise_stats_lgu ON mv_promise_stats (lgu_id);
CREATE INDEX idx_mv_promise_stats_region ON mv_promise_stats (region_code);

-- ============================================================================
-- VIEW: Budget Summary per LGU per Year
-- ============================================================================
CREATE OR REPLACE VIEW vw_budget_summary AS
SELECT
    ba.lgu_id,
    l.name                                      AS lgu_name,
    ba.fiscal_year,
    ba.category,
    SUM(ba.allocated_amount)                    AS total_allocated,
    SUM(ba.released_amount)                     AS total_released,
    SUM(ba.utilized_amount)                     AS total_utilized,
    CASE
        WHEN SUM(ba.allocated_amount) > 0 THEN
            ROUND(SUM(ba.utilized_amount) / SUM(ba.allocated_amount) * 100, 1)
        ELSE 0
    END                                         AS utilization_rate
FROM budget_allocations ba
JOIN lgus l ON l.id = ba.lgu_id
GROUP BY ba.lgu_id, l.name, ba.fiscal_year, ba.category;

-- ============================================================================
-- VIEW: Official Scorecard
-- ============================================================================
CREATE OR REPLACE VIEW vw_official_scorecard AS
SELECT
    o.id                                        AS official_id,
    o.full_name,
    o.position,
    o.party,
    l.id                                        AS lgu_id,
    l.name                                      AS lgu_name,
    COUNT(p.id)                                 AS total_promises,
    COUNT(p.id) FILTER (WHERE p.status = 'kept')           AS kept,
    COUNT(p.id) FILTER (WHERE p.status = 'broken')         AS broken,
    COUNT(p.id) FILTER (WHERE p.status = 'in_progress')    AS in_progress,
    COUNT(p.id) FILTER (WHERE p.status = 'pending')        AS pending,
    COUNT(p.id) FILTER (WHERE p.status = 'partially_kept') AS partially_kept,
    CASE
        WHEN COUNT(p.id) > 0 THEN
            ROUND(
                (COUNT(p.id) FILTER (WHERE p.status = 'kept')::NUMERIC
                 + 0.5 * COUNT(p.id) FILTER (WHERE p.status = 'partially_kept')::NUMERIC)
                / COUNT(p.id)::NUMERIC * 100,
            1)
        ELSE 0
    END                                         AS fulfillment_rate
FROM officials o
JOIN lgus l ON l.id = o.lgu_id
LEFT JOIN promises p ON p.official_id = o.id
WHERE o.is_current = true
GROUP BY o.id, o.full_name, o.position, o.party, l.id, l.name;

-- ============================================================================
-- FUNCTION: Refresh promise stats (call from cron or after bulk updates)
-- ============================================================================
CREATE OR REPLACE FUNCTION refresh_promise_stats()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_promise_stats;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
