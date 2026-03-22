"""Scheduler management endpoints.

Allows viewing/updating auto-scraping schedules, triggering immediate runs,
and inspecting overall scraping health and validation statistics.
"""

from __future__ import annotations

import logging
import multiprocessing
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import CrawlJob
from app.models.scraping_schedule import ScrapingScheduleModel

logger = logging.getLogger(__name__)

router = APIRouter()

ALLOWED_SPIDERS = {"philgeps", "dbm", "coa", "efoi"}

DEFAULT_SCHEDULES: dict[str, str] = {
    "philgeps": "0 2 * * *",
    "dbm": "0 3 * * 1",
    "coa": "0 4 1 * *",
    "efoi": "0 5 * * 3",
}


# ---- Pydantic schemas -------------------------------------------------------


class ScheduleResponse(BaseModel):
    spider_name: str
    cron_expression: str
    enabled: bool
    last_run_at: str | None = None
    last_status: str | None = None
    items_scraped: int = 0
    avg_quality_score: float = 0.0


class ScheduleUpdateRequest(BaseModel):
    cron_expression: str | None = Field(
        None, description="5-field cron expression, e.g. '0 2 * * *'"
    )
    enabled: bool | None = Field(None, description="Enable or disable the schedule")


class TriggerRunResponse(BaseModel):
    job_id: int
    spider_name: str
    status: str


class HealthReportResponse(BaseModel):
    generated_at: str
    total_spiders: int
    enabled_spiders: int
    total_items_scraped: int
    overall_avg_quality: float
    spiders: list[ScheduleResponse]


class ValidationStatsResponse(BaseModel):
    total_items: int
    auto_approved: int
    flagged_for_review: int
    rejected: int
    avg_quality_score: float


# ---- Helpers -----------------------------------------------------------------


def _validate_cron(expr: str) -> None:
    """Basic validation that a cron expression has 5 fields."""
    parts = expr.strip().split()
    if len(parts) != 5:
        raise HTTPException(
            status_code=400,
            detail=f"Cron expression must have 5 fields, got {len(parts)}: '{expr}'",
        )


async def _ensure_schedules_seeded(db: AsyncSession) -> None:
    """Seed default schedules if the table is empty."""
    result = await db.execute(
        select(ScrapingScheduleModel).limit(1)
    )
    if result.scalar_one_or_none() is not None:
        return

    for spider_name, cron in DEFAULT_SCHEDULES.items():
        schedule = ScrapingScheduleModel(
            spider_name=spider_name,
            cron_expression=cron,
        )
        db.add(schedule)


def _run_spider_process(spider_name: str, job_id: int) -> None:
    """Run a Scrapy spider in a separate process (same pattern as crawler.py)."""
    import psycopg2

    backend_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
        )
    )
    crawler_dir = os.path.join(backend_dir, "crawler")
    if crawler_dir not in sys.path:
        sys.path.insert(0, crawler_dir)

    os.chdir(crawler_dir)

    try:
        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings

        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(spider_name)
        process.start()

        _update_job_sync(job_id, "completed")
    except Exception as exc:
        logger.exception("Spider %s failed", spider_name)
        _update_job_sync(job_id, "failed", error_log=str(exc))


def _update_job_sync(
    job_id: int, status: str, *, error_log: str | None = None
) -> None:
    """Update a CrawlJob row using synchronous psycopg2 (child process)."""
    import psycopg2 as pg2

    db_url = os.environ.get("DATABASE_URL", "")
    if db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    if not db_url:
        return
    try:
        conn = pg2.connect(db_url)
        cur = conn.cursor()
        cur.execute(
            "UPDATE crawl_jobs SET status = %s, finished_at = %s, error_log = %s "
            "WHERE id = %s",
            (status, datetime.now(timezone.utc), error_log, job_id),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        logger.exception("Failed to update crawl_job %s", job_id)


# ---- Endpoints ---------------------------------------------------------------


@router.get("/schedules", response_model=list[ScheduleResponse])
async def get_schedules(db: AsyncSession = Depends(get_db)):
    """Get all spider schedules."""
    await _ensure_schedules_seeded(db)
    await db.flush()

    result = await db.execute(
        select(ScrapingScheduleModel).order_by(ScrapingScheduleModel.spider_name)
    )
    rows = result.scalars().all()

    return [
        ScheduleResponse(
            spider_name=r.spider_name,
            cron_expression=r.cron_expression,
            enabled=r.enabled,
            last_run_at=str(r.last_run_at) if r.last_run_at else None,
            last_status=r.last_status,
            items_scraped=r.items_scraped or 0,
            avg_quality_score=float(r.avg_quality_score or 0),
        )
        for r in rows
    ]


@router.put("/schedules/{spider_name}", response_model=ScheduleResponse)
async def update_schedule(
    spider_name: str,
    body: ScheduleUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Update a spider's schedule (cron expression and/or enabled flag)."""
    if spider_name not in ALLOWED_SPIDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown spider '{spider_name}'. Allowed: {sorted(ALLOWED_SPIDERS)}",
        )

    await _ensure_schedules_seeded(db)
    await db.flush()

    result = await db.execute(
        select(ScrapingScheduleModel).where(
            ScrapingScheduleModel.spider_name == spider_name
        )
    )
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if body.cron_expression is not None:
        _validate_cron(body.cron_expression)
        schedule.cron_expression = body.cron_expression

    if body.enabled is not None:
        schedule.enabled = body.enabled

    schedule.updated_at = datetime.now(timezone.utc)
    await db.flush()

    return ScheduleResponse(
        spider_name=schedule.spider_name,
        cron_expression=schedule.cron_expression,
        enabled=schedule.enabled,
        last_run_at=str(schedule.last_run_at) if schedule.last_run_at else None,
        last_status=schedule.last_status,
        items_scraped=schedule.items_scraped or 0,
        avg_quality_score=float(schedule.avg_quality_score or 0),
    )


@router.post("/schedules/{spider_name}/run", response_model=TriggerRunResponse)
async def trigger_run(
    spider_name: str,
    db: AsyncSession = Depends(get_db),
):
    """Trigger an immediate spider run, bypassing the cron schedule."""
    if spider_name not in ALLOWED_SPIDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown spider '{spider_name}'. Allowed: {sorted(ALLOWED_SPIDERS)}",
        )

    # Create a CrawlJob record
    job = CrawlJob(
        spider_name=spider_name,
        status="running",
        items_scraped=0,
        items_failed=0,
        started_at=datetime.now(timezone.utc),
    )
    db.add(job)
    await db.flush()
    job_id = job.id

    # Spawn spider in a child process
    proc = multiprocessing.Process(
        target=_run_spider_process,
        args=(spider_name, job_id),
        daemon=True,
    )
    proc.start()
    logger.info(
        "Scheduler: started spider '%s' in process %s, job_id=%s",
        spider_name,
        proc.pid,
        job_id,
    )

    return TriggerRunResponse(
        job_id=job_id,
        spider_name=spider_name,
        status="running",
    )


@router.get("/health", response_model=HealthReportResponse)
async def get_health_report(db: AsyncSession = Depends(get_db)):
    """Overall scraping health report: last runs, success rates, quality scores."""
    await _ensure_schedules_seeded(db)
    await db.flush()

    result = await db.execute(
        select(ScrapingScheduleModel).order_by(ScrapingScheduleModel.spider_name)
    )
    rows = result.scalars().all()

    total_items = 0
    total_score = 0.0
    scored_count = 0
    spiders: list[ScheduleResponse] = []

    for r in rows:
        score_val = float(r.avg_quality_score or 0)
        items_val = r.items_scraped or 0

        spiders.append(
            ScheduleResponse(
                spider_name=r.spider_name,
                cron_expression=r.cron_expression,
                enabled=r.enabled,
                last_run_at=str(r.last_run_at) if r.last_run_at else None,
                last_status=r.last_status,
                items_scraped=items_val,
                avg_quality_score=score_val,
            )
        )
        total_items += items_val
        if score_val > 0:
            total_score += score_val
            scored_count += 1

    return HealthReportResponse(
        generated_at=datetime.now(timezone.utc).isoformat(),
        total_spiders=len(rows),
        enabled_spiders=sum(1 for r in rows if r.enabled),
        total_items_scraped=total_items,
        overall_avg_quality=round(total_score / scored_count, 3) if scored_count else 0.0,
        spiders=spiders,
    )


@router.get("/validation-stats", response_model=ValidationStatsResponse)
async def get_validation_stats(db: AsyncSession = Depends(get_db)):
    """Aggregate validation statistics computed from recent crawl data.

    Reads ``structured_data`` from the ``documents`` table where the
    validation pipeline has attached ``_validation_score`` metadata.
    """
    from sqlalchemy import text

    # Query documents that have validation metadata in their structured_data
    query = text(
        """
        SELECT
            COUNT(*) AS total,
            COUNT(*) FILTER (
                WHERE (structured_data->>'_auto_approved')::boolean = true
            ) AS approved,
            COUNT(*) FILTER (
                WHERE (structured_data->>'_needs_review')::boolean = true
            ) AS flagged,
            COALESCE(
                AVG((structured_data->>'_validation_score')::numeric), 0
            ) AS avg_score
        FROM documents
        WHERE structured_data ? '_validation_score'
        """
    )

    try:
        result = await db.execute(query)
        row = result.one()

        total = int(row.total)
        approved = int(row.approved)
        flagged = int(row.flagged)

        return ValidationStatsResponse(
            total_items=total,
            auto_approved=approved,
            flagged_for_review=flagged,
            rejected=0,  # rejected items are dropped and never reach the DB
            avg_quality_score=round(float(row.avg_score), 3),
        )
    except Exception as exc:
        logger.warning("validation-stats query failed (table may not exist yet): %s", exc)
        return ValidationStatsResponse(
            total_items=0,
            auto_approved=0,
            flagged_for_review=0,
            rejected=0,
            avg_quality_score=0.0,
        )
