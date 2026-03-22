-- ============================================================================
-- SipatGov - Row Level Security Policies
-- ============================================================================

-- Public read access for all data tables (transparency platform = public data)
-- Authenticated write access for user-generated content
-- Service role bypasses RLS automatically

-- REGIONS (public read)
ALTER TABLE regions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "regions_public_read" ON regions FOR SELECT USING (true);
CREATE POLICY "regions_service_write" ON regions FOR ALL USING (true) WITH CHECK (true);

-- PROVINCES (public read)
ALTER TABLE provinces ENABLE ROW LEVEL SECURITY;
CREATE POLICY "provinces_public_read" ON provinces FOR SELECT USING (true);
CREATE POLICY "provinces_service_write" ON provinces FOR ALL USING (true) WITH CHECK (true);

-- LGUs (public read)
ALTER TABLE lgus ENABLE ROW LEVEL SECURITY;
CREATE POLICY "lgus_public_read" ON lgus FOR SELECT USING (true);
CREATE POLICY "lgus_service_write" ON lgus FOR ALL USING (true) WITH CHECK (true);

-- OFFICIALS (public read)
ALTER TABLE officials ENABLE ROW LEVEL SECURITY;
CREATE POLICY "officials_public_read" ON officials FOR SELECT USING (true);
CREATE POLICY "officials_service_write" ON officials FOR ALL USING (true) WITH CHECK (true);

-- DOCUMENTS (public read)
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY "documents_public_read" ON documents FOR SELECT USING (true);
CREATE POLICY "documents_service_write" ON documents FOR ALL USING (true) WITH CHECK (true);

-- BUDGET ALLOCATIONS (public read)
ALTER TABLE budget_allocations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "budgets_public_read" ON budget_allocations FOR SELECT USING (true);
CREATE POLICY "budgets_service_write" ON budget_allocations FOR ALL USING (true) WITH CHECK (true);

-- PROJECTS (public read)
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
CREATE POLICY "projects_public_read" ON projects FOR SELECT USING (true);
CREATE POLICY "projects_service_write" ON projects FOR ALL USING (true) WITH CHECK (true);

-- PROMISES (public read)
ALTER TABLE promises ENABLE ROW LEVEL SECURITY;
CREATE POLICY "promises_public_read" ON promises FOR SELECT USING (true);
CREATE POLICY "promises_service_write" ON promises FOR ALL USING (true) WITH CHECK (true);

-- PROMISE EVIDENCE (public read)
ALTER TABLE promise_evidence ENABLE ROW LEVEL SECURITY;
CREATE POLICY "evidence_public_read" ON promise_evidence FOR SELECT USING (true);
CREATE POLICY "evidence_service_write" ON promise_evidence FOR ALL USING (true) WITH CHECK (true);

-- USERS (users can read own data)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "users_read_own" ON users FOR SELECT USING (true);
CREATE POLICY "users_service_write" ON users FOR ALL USING (true) WITH CHECK (true);

-- COMMUNITY REPORTS (public read, authenticated write)
ALTER TABLE community_reports ENABLE ROW LEVEL SECURITY;
CREATE POLICY "reports_public_read" ON community_reports FOR SELECT USING (true);
CREATE POLICY "reports_service_write" ON community_reports FOR ALL USING (true) WITH CHECK (true);

-- REPORT ATTACHMENTS (public read)
ALTER TABLE report_attachments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "attachments_public_read" ON report_attachments FOR SELECT USING (true);
CREATE POLICY "attachments_service_write" ON report_attachments FOR ALL USING (true) WITH CHECK (true);

-- REPORT UPVOTES (public read)
ALTER TABLE report_upvotes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "upvotes_public_read" ON report_upvotes FOR SELECT USING (true);
CREATE POLICY "upvotes_service_write" ON report_upvotes FOR ALL USING (true) WITH CHECK (true);

-- CRAWL JOBS (public read)
ALTER TABLE crawl_jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "crawl_jobs_public_read" ON crawl_jobs FOR SELECT USING (true);
CREATE POLICY "crawl_jobs_service_write" ON crawl_jobs FOR ALL USING (true) WITH CHECK (true);
