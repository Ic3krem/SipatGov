import hashlib
import json
import logging
import os
from datetime import datetime, timezone

import psycopg2
import psycopg2.extras
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class DuplicateFilterPipeline:
    """Filter duplicate documents by URL hash."""

    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        url = item.get("source_url", "")
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        if url_hash in self.seen_urls:
            raise DropItem(f"Duplicate document: {url}")
        self.seen_urls.add(url_hash)
        return item


class PDFDownloadPipeline:
    """Download PDFs and store them.

    TODO: Implement S3 upload or local storage.
    """

    def process_item(self, item, spider):
        pdf_urls = item.get("pdf_urls", []) or item.get("pdf_url", [])
        if pdf_urls:
            if isinstance(pdf_urls, str):
                pdf_urls = [pdf_urls]
            logger.info(f"Found {len(pdf_urls)} PDF(s) for: {item.get('title', 'unknown')}")
            # TODO: Download PDFs and compute file_hash
        return item


class DatabasePipeline:
    """Insert crawled items into PostgreSQL using synchronous psycopg2.

    Scrapy pipelines run in a synchronous context, so we use psycopg2
    directly instead of the async SQLAlchemy engine used by the FastAPI app.
    """

    def open_spider(self, spider):
        database_url = os.environ.get("DATABASE_URL", "")
        # psycopg2 needs a postgresql:// scheme (not postgresql+asyncpg://)
        if database_url.startswith("postgresql+asyncpg://"):
            database_url = database_url.replace("postgresql+asyncpg://", "postgresql://", 1)
        if not database_url:
            logger.error("DATABASE_URL environment variable is not set")
            raise RuntimeError("DATABASE_URL is required for DatabasePipeline")
        self.conn = psycopg2.connect(database_url)
        self.conn.autocommit = False
        logger.info("DatabasePipeline: connected to PostgreSQL")

    def close_spider(self, spider):
        if hasattr(self, "conn") and self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("DatabasePipeline: closed PostgreSQL connection")

    def _resolve_lgu_id(self, procuring_entity: str) -> int | None:
        """Fuzzy-match procuring_entity to an LGU id via SQL LIKE."""
        if not procuring_entity:
            return None
        cur = self.conn.cursor()
        try:
            # Try exact-ish match first (case-insensitive LIKE with the entity name)
            pattern = f"%{procuring_entity}%"
            cur.execute(
                "SELECT id FROM lgus WHERE name ILIKE %s LIMIT 1",
                (pattern,),
            )
            row = cur.fetchone()
            return row[0] if row else None
        finally:
            cur.close()

    def process_item(self, item, spider):
        source_url = item.get("source_url", "")
        url_hash = hashlib.sha256(source_url.encode()).hexdigest()

        cur = self.conn.cursor()
        try:
            # Deduplicate by SHA-256 hash of source_url stored in file_hash column
            cur.execute(
                "SELECT id FROM documents WHERE file_hash = %s",
                (url_hash,),
            )
            if cur.fetchone():
                logger.debug(f"Document already in DB (hash={url_hash[:12]}...): {source_url}")
                return item

            # Determine document type from item class name
            item_class = type(item).__name__
            doc_type_map = {
                "BidNoticeItem": "bid_notice",
                "AwardNoticeItem": "award_notice",
                "BudgetItem": "budget_document",
                "GovernmentDocumentItem": "general",
            }
            document_type = doc_type_map.get(item_class, "general")

            # Determine source portal from spider name
            source_portal = getattr(spider, "name", "manual")

            # Resolve LGU
            procuring_entity = item.get("procuring_entity", "") or item.get("lgu_name", "")
            lgu_id = self._resolve_lgu_id(procuring_entity)

            # Build structured metadata from item fields
            structured_data = {k: v for k, v in dict(item).items() if k != "source_url"}

            cur.execute(
                """
                INSERT INTO documents
                    (source_portal, source_url, title, document_type,
                     lgu_id, file_hash, structured_data, processing_status,
                     crawled_at, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """,
                (
                    source_portal,
                    source_url,
                    item.get("title", ""),
                    document_type,
                    lgu_id,
                    url_hash,
                    json.dumps(structured_data),
                    "pending",
                    datetime.now(timezone.utc),
                ),
            )
            self.conn.commit()
            logger.info(f"Saved to DB: {item.get('title', 'unknown')} (lgu_id={lgu_id})")

        except Exception:
            self.conn.rollback()
            logger.exception(f"Failed to insert document: {source_url}")
        finally:
            cur.close()

        return item


class ProcessingQueuePipeline:
    """Queue downloaded PDFs for OCR/NLP processing via Celery.

    TODO: Implement Celery task dispatch.
    """

    def process_item(self, item, spider):
        if item.get("pdf_urls") or item.get("pdf_url"):
            logger.info(f"Queuing for processing: {item.get('title', 'unknown')}")
            # TODO: Dispatch Celery task for Textract + Claude processing
        return item
