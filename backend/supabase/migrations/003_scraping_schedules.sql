-- Migration 003: Scraping schedules and validation support
-- Adds the scraping_schedules table for managing auto-scraping cron jobs
-- and tracking per-spider health / quality metrics.

CREATE TABLE IF NOT EXISTS scraping_schedules (
    id SERIAL PRIMARY KEY,
    spider_name VARCHAR(50) UNIQUE NOT NULL,
    cron_expression VARCHAR(50) NOT NULL,
    enabled BOOLEAN DEFAULT true,
    last_run_at TIMESTAMPTZ,
    last_status VARCHAR(20),
    items_scraped INTEGER DEFAULT 0,
    avg_quality_score DECIMAL(3,2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Seed default schedules for the four target portals
INSERT INTO scraping_schedules (spider_name, cron_expression) VALUES
    ('philgeps', '0 2 * * *'),
    ('dbm',      '0 3 * * 1'),
    ('coa',      '0 4 1 * *'),
    ('efoi',     '0 5 * * 3')
ON CONFLICT (spider_name) DO NOTHING;

-- Index for quick lookups by spider name (unique constraint already covers this,
-- but being explicit about the intent).
CREATE INDEX IF NOT EXISTS idx_scraping_schedules_spider
    ON scraping_schedules (spider_name);

-- Index on enabled + spider_name for the scheduler's should_run query
CREATE INDEX IF NOT EXISTS idx_scraping_schedules_enabled
    ON scraping_schedules (enabled, spider_name)
    WHERE enabled = true;

-- Add a comment for documentation
COMMENT ON TABLE scraping_schedules IS
    'Manages cron-based auto-scraping schedules and tracks per-spider health metrics.';
