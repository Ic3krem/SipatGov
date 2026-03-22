"""Crawler management endpoints.

Allows triggering Scrapy spiders and checking job status.
"""

import logging
import multiprocessing
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import CrawlJob

logger = logging.getLogger(__name__)

router = APIRouter()

ALLOWED_SPIDERS = {"philgeps"}


# ---- request / response schemas -------------------------------------------

class TriggerRequest(BaseModel):
    spider: str


class TriggerResponse(BaseModel):
    job_id: int
    spider: str
    status: str


class JobStatusResponse(BaseModel):
    id: int
    spider_name: str
    status: str
    items_scraped: int
    items_failed: int
    started_at: str | None
    finished_at: str | None
    error_log: str | None


# ---- subprocess runner -----------------------------------------------------

def _run_spider(spider_name: str, job_id: int) -> None:
    """Run a Scrapy spider in a separate process.

    This function is the target of multiprocessing.Process so it must be
    importable at module level and must not reference any async objects.
    """
    import os
    import sys

    # Ensure the crawler package is importable
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )))
    crawler_dir = os.path.join(backend_dir, "crawler")
    if crawler_dir not in sys.path:
        sys.path.insert(0, crawler_dir)

    # Late imports so the Twisted reactor is only installed in the child process
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    os.chdir(crawler_dir)

    try:
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(spider_name)
        process.start()  # blocks until the spider finishes

        # Update job status after completion (sync psycopg2, same as pipeline)
        _update_job_status(job_id, "completed")
    except Exception as exc:
        logger.exception(f"Spider {spider_name} failed")
        _update_job_status(job_id, "failed", error_log=str(exc))


def _update_job_status(
    job_id: int, status: str, *, error_log: str | None = None
) -> None:
    """Update a CrawlJob record using synchronous psycopg2 (runs in child process)."""
    import os

    import psycopg2

    database_url = os.environ.get("DATABASE_URL", "")
    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    if not database_url:
        logger.error("DATABASE_URL not set; cannot update job status")
        return

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute(
            "UPDATE crawl_jobs SET status = %s, finished_at = %s, error_log = %s WHERE id = %s",
            (status, datetime.now(timezone.utc), error_log, job_id),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        logger.exception(f"Failed to update crawl_job {job_id}")


# ---- endpoints --------------------------------------------------------------

@router.post("/trigger", response_model=TriggerResponse)
async def trigger_crawler(
    body: TriggerRequest,
    db: AsyncSession = Depends(get_db),
):
    """Trigger a Scrapy spider run.

    Spawns the spider in a separate process so the async event loop is not
    blocked by Scrapy's Twisted reactor.
    """
    if body.spider not in ALLOWED_SPIDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown spider '{body.spider}'. Allowed: {sorted(ALLOWED_SPIDERS)}",
        )

    # Create CrawlJob record
    job = CrawlJob(
        spider_name=body.spider,
        status="running",
        items_scraped=0,
        items_failed=0,
        started_at=datetime.now(timezone.utc),
    )
    db.add(job)
    await db.flush()  # populate job.id
    job_id = job.id

    # Spawn spider in a child process
    proc = multiprocessing.Process(
        target=_run_spider,
        args=(body.spider, job_id),
        daemon=True,
    )
    proc.start()
    logger.info(f"Started spider '{body.spider}' in process {proc.pid}, job_id={job_id}")

    return TriggerResponse(job_id=job_id, spider=body.spider, status="running")


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get the status of a crawl job."""
    result = await db.execute(select(CrawlJob).where(CrawlJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Crawl job not found")
    return JobStatusResponse(
        id=job.id,
        spider_name=job.spider_name,
        status=job.status,
        items_scraped=job.items_scraped,
        items_failed=job.items_failed,
        started_at=str(job.started_at) if job.started_at else None,
        finished_at=str(job.finished_at) if job.finished_at else None,
        error_log=job.error_log,
    )
