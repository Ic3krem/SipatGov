"""Automatic scraping scheduler for SipatGov crawlers.

Manages cron-based schedules for all spiders, persists state in
``scraping_schedules`` (PostgreSQL), and provides a health-report API.

Uses synchronous psycopg2, same as the Scrapy pipelines, so it can be
called from both the FastAPI process and the Scrapy child processes.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import psycopg2
import psycopg2.extras

from governance_ghost.validation.models import ScrapingSchedule

logger = logging.getLogger(__name__)


def _cron_field_matches(field_expr: str, current_value: int) -> bool:
    """Check whether a single cron field expression matches a value.

    Supports:
      - ``*``        (any)
      - ``5``        (exact)
      - ``1-5``      (range)
      - ``*/15``     (step from 0)
      - ``1,3,5``    (list)
    """
    for part in field_expr.split(","):
        part = part.strip()
        if part == "*":
            return True
        if part.startswith("*/"):
            step = int(part[2:])
            if step > 0 and current_value % step == 0:
                return True
        elif "-" in part:
            lo, hi = part.split("-", 1)
            if int(lo) <= current_value <= int(hi):
                return True
        else:
            if int(part) == current_value:
                return True
    return False


def cron_matches_now(cron_expression: str, now: datetime | None = None) -> bool:
    """Return ``True`` if *cron_expression* matches the current (or given) time.

    Standard 5-field cron: minute hour day-of-month month day-of-week.
    Day-of-week: 0 = Sunday (or 7), 1 = Monday, ..., 6 = Saturday.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    parts = cron_expression.strip().split()
    if len(parts) != 5:
        logger.warning("Invalid cron expression (need 5 fields): %s", cron_expression)
        return False

    minute, hour, dom, month, dow = parts
    # Python weekday: Monday=0, Sunday=6  ->  cron: Sunday=0
    cron_dow = (now.weekday() + 1) % 7  # convert to cron convention

    return (
        _cron_field_matches(minute, now.minute)
        and _cron_field_matches(hour, now.hour)
        and _cron_field_matches(dom, now.day)
        and _cron_field_matches(month, now.month)
        and _cron_field_matches(dow, cron_dow)
    )


class AutoScheduler:
    """Manages automatic scraping schedules for all spiders."""

    DEFAULT_SCHEDULES: dict[str, str] = {
        "philgeps": "0 2 * * *",   # Daily at 2 AM
        "dbm": "0 3 * * 1",        # Weekly Monday 3 AM
        "coa": "0 4 1 * *",        # Monthly 1st at 4 AM
        "efoi": "0 5 * * 3",       # Weekly Wednesday 5 AM
    }

    def __init__(self, db_url: str) -> None:
        """Initialise with a PostgreSQL connection string.

        Accepts both ``postgresql+asyncpg://`` and ``postgresql://`` schemes.
        """
        self._db_url = db_url
        if self._db_url.startswith("postgresql+asyncpg://"):
            self._db_url = self._db_url.replace(
                "postgresql+asyncpg://", "postgresql://", 1
            )

    # ------------------------------------------------------------------
    # Connection helper
    # ------------------------------------------------------------------

    def _connect(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(self._db_url)

    def _ensure_table(self, conn: psycopg2.extensions.connection) -> None:
        """Create the scraping_schedules table if it doesn't already exist."""
        cur = conn.cursor()
        try:
            cur.execute(
                """
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
                )
                """
            )
            conn.commit()
        finally:
            cur.close()

    def _seed_defaults(self, conn: psycopg2.extensions.connection) -> None:
        """Insert default schedule rows if they don't exist."""
        cur = conn.cursor()
        try:
            for spider, cron in self.DEFAULT_SCHEDULES.items():
                cur.execute(
                    """
                    INSERT INTO scraping_schedules (spider_name, cron_expression)
                    VALUES (%s, %s)
                    ON CONFLICT (spider_name) DO NOTHING
                    """,
                    (spider, cron),
                )
            conn.commit()
        finally:
            cur.close()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_schedules(self) -> list[ScrapingSchedule]:
        """Return all schedules from the database, seeding defaults if empty."""
        conn = self._connect()
        try:
            self._ensure_table(conn)
            self._seed_defaults(conn)

            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                cur.execute(
                    """
                    SELECT spider_name, cron_expression, enabled,
                           last_run_at, last_status, items_scraped,
                           avg_quality_score
                    FROM scraping_schedules
                    ORDER BY spider_name
                    """
                )
                rows = cur.fetchall()
            finally:
                cur.close()

            return [
                ScrapingSchedule(
                    spider_name=r["spider_name"],
                    cron_expression=r["cron_expression"],
                    enabled=r["enabled"],
                    last_run=str(r["last_run_at"]) if r["last_run_at"] else None,
                    last_status=r["last_status"],
                    items_scraped=r["items_scraped"] or 0,
                    avg_quality_score=float(r["avg_quality_score"] or 0),
                )
                for r in rows
            ]
        finally:
            conn.close()

    def update_schedule(
        self,
        spider_name: str,
        cron: str | None = None,
        enabled: bool | None = None,
    ) -> bool:
        """Update a spider's cron expression and/or enabled flag.

        Returns ``True`` if a row was updated, ``False`` if the spider
        was not found.
        """
        conn = self._connect()
        try:
            self._ensure_table(conn)

            sets: list[str] = ["updated_at = now()"]
            params: list[object] = []

            if cron is not None:
                sets.append("cron_expression = %s")
                params.append(cron)
            if enabled is not None:
                sets.append("enabled = %s")
                params.append(enabled)

            if len(sets) == 1:
                # Nothing to update besides the timestamp — still proceed so
                # the caller sees the row exists.
                pass

            params.append(spider_name)

            cur = conn.cursor()
            try:
                cur.execute(
                    f"UPDATE scraping_schedules SET {', '.join(sets)} "
                    "WHERE spider_name = %s",
                    params,
                )
                conn.commit()
                return cur.rowcount > 0
            finally:
                cur.close()
        finally:
            conn.close()

    def should_run(self, spider_name: str) -> bool:
        """Return ``True`` if *spider_name* should run right now.

        Checks the schedule's cron expression against the current UTC time
        and ensures the spider is enabled.
        """
        conn = self._connect()
        try:
            self._ensure_table(conn)
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                cur.execute(
                    "SELECT cron_expression, enabled, last_run_at "
                    "FROM scraping_schedules WHERE spider_name = %s",
                    (spider_name,),
                )
                row = cur.fetchone()
            finally:
                cur.close()

            if not row:
                # Unknown spider — use default if available
                cron = self.DEFAULT_SCHEDULES.get(spider_name)
                if not cron:
                    return False
                return cron_matches_now(cron)

            if not row["enabled"]:
                return False

            now = datetime.now(timezone.utc)

            # Don't re-run within the same minute window
            if row["last_run_at"]:
                last_run = row["last_run_at"]
                if hasattr(last_run, "tzinfo") and last_run.tzinfo is None:
                    last_run = last_run.replace(tzinfo=timezone.utc)
                elapsed_seconds = (now - last_run).total_seconds()
                if elapsed_seconds < 60:
                    return False

            return cron_matches_now(row["cron_expression"], now)
        finally:
            conn.close()

    def record_run(
        self,
        spider_name: str,
        status: str,
        items_count: int,
        avg_score: float,
    ) -> None:
        """Record the result of a completed scraping run."""
        conn = self._connect()
        try:
            self._ensure_table(conn)
            cur = conn.cursor()
            try:
                cur.execute(
                    """
                    UPDATE scraping_schedules
                    SET last_run_at = %s,
                        last_status = %s,
                        items_scraped = items_scraped + %s,
                        avg_quality_score = %s,
                        updated_at = now()
                    WHERE spider_name = %s
                    """,
                    (
                        datetime.now(timezone.utc),
                        status[:20],
                        items_count,
                        round(avg_score, 2),
                        spider_name,
                    ),
                )
                conn.commit()
                if cur.rowcount == 0:
                    logger.warning(
                        "record_run: no schedule row for spider '%s'", spider_name
                    )
            finally:
                cur.close()
        finally:
            conn.close()

    def get_health_report(self) -> dict:
        """Return an overall health report for all spiders.

        Includes per-spider stats plus aggregate metrics.
        """
        schedules = self.get_schedules()

        total_items = 0
        total_score = 0.0
        scored_count = 0
        spiders: list[dict] = []

        for s in schedules:
            spider_info = {
                "spider_name": s.spider_name,
                "cron_expression": s.cron_expression,
                "enabled": s.enabled,
                "last_run": s.last_run,
                "last_status": s.last_status,
                "items_scraped": s.items_scraped,
                "avg_quality_score": s.avg_quality_score,
            }
            spiders.append(spider_info)

            total_items += s.items_scraped
            if s.avg_quality_score > 0:
                total_score += s.avg_quality_score
                scored_count += 1

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_spiders": len(schedules),
            "enabled_spiders": sum(1 for s in schedules if s.enabled),
            "total_items_scraped": total_items,
            "overall_avg_quality": (
                round(total_score / scored_count, 3) if scored_count else 0.0
            ),
            "spiders": spiders,
        }
