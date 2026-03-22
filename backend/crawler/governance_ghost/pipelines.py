import hashlib
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
import psycopg2.extras
import requests
from scrapy.exceptions import DropItem

from governance_ghost.validation.data_validator import DataValidator

logger = logging.getLogger(__name__)

# Maximum PDF file size to download (50 MB)
MAX_PDF_SIZE_BYTES = 50 * 1024 * 1024


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


class ValidationPipeline:
    """Validate scraped items for data quality. Priority 150.

    Items scoring below 0.3 are dropped.  Items between 0.3 and 0.8 are
    flagged for manual review.  Items above 0.8 are auto-approved.
    Validation metadata is attached to the item for downstream use.
    """

    def __init__(self) -> None:
        self.validator = DataValidator()
        self.stats: dict[str, int] = {
            "total": 0,
            "approved": 0,
            "flagged": 0,
            "rejected": 0,
        }

    def open_spider(self, spider) -> None:
        logger.info("ValidationPipeline: initialised for spider '%s'", spider.name)

    def close_spider(self, spider) -> None:
        logger.info(
            "ValidationPipeline stats for '%s': %s",
            spider.name,
            self.stats,
        )

    def process_item(self, item, spider):
        self.stats["total"] += 1

        item_type = type(item).__name__
        result = self.validator.validate_item(item, item_type)

        if result.score < 0.3:
            self.stats["rejected"] += 1
            raise DropItem(
                f"Low quality score ({result.score:.2f}): {result.issues}"
            )

        # Attach validation metadata to the item
        item["_validation_score"] = result.score
        item["_validation_issues"] = result.issues
        item["_auto_approved"] = result.auto_approve
        item["_needs_review"] = result.needs_review
        item["_claude_verified"] = result.claude_verified

        if result.auto_approve:
            self.stats["approved"] += 1
        else:
            self.stats["flagged"] += 1

        if result.issues:
            logger.info(
                "Validation issues for %s (score=%.2f): %s",
                item.get("title", "unknown")[:60],
                result.score,
                result.issues,
            )

        return item


class PDFDownloadPipeline:
    """Download PDFs to local storage with deduplication by content hash.

    PDFs are saved to ``data/pdfs/`` relative to the Scrapy project root.
    Each file is named ``{spider_name}_{hash[:8]}_{timestamp}.pdf`` where
    *hash* is the SHA-256 of the file content.  Files that already exist
    (same content hash) are skipped automatically.
    """

    def __init__(self):
        self._base_dir: Path | None = None
        # Set of SHA-256 content hashes already on disk (populated in open_spider)
        self._seen_hashes: set[str] = set()

    def open_spider(self, spider):
        self._base_dir = Path(
            getattr(spider, "settings", {}).get("PDF_STORE_DIR", "data/pdfs")
        )
        self._base_dir.mkdir(parents=True, exist_ok=True)
        # Pre-populate seen hashes from existing files so we never re-download
        for pdf_file in self._base_dir.glob("*.pdf"):
            # Hash is embedded between the first and second underscore in the filename
            parts = pdf_file.stem.split("_")
            if len(parts) >= 2:
                self._seen_hashes.add(parts[1])
        logger.info(
            f"PDFDownloadPipeline: storage dir={self._base_dir}, "
            f"existing files={len(self._seen_hashes)}"
        )

    def process_item(self, item, spider):
        pdf_urls = item.get("pdf_urls", []) or item.get("pdf_url", [])
        if not pdf_urls:
            return item

        if isinstance(pdf_urls, str):
            pdf_urls = [pdf_urls]

        logger.info(f"Found {len(pdf_urls)} PDF(s) for: {item.get('title', 'unknown')}")

        local_paths: list[str] = []
        for url in pdf_urls:
            local_path = self._download_pdf(url, spider)
            if local_path:
                local_paths.append(local_path)

        if local_paths:
            # Store the first (or only) local path on the item for downstream use
            item["local_pdf_path"] = local_paths[0] if len(local_paths) == 1 else local_paths

        return item

    # ------------------------------------------------------------------
    def _download_pdf(self, url: str, spider) -> str | None:
        """Download a single PDF, returning the local file path or None."""
        spider_name = getattr(spider, "name", "unknown")

        try:
            # Stream the response so we can check Content-Length before reading
            resp = requests.get(url, stream=True, timeout=60)
            resp.raise_for_status()

            # Check declared content-length first (avoids downloading huge files)
            content_length = resp.headers.get("Content-Length")
            if content_length and int(content_length) > MAX_PDF_SIZE_BYTES:
                logger.warning(
                    f"Skipping PDF (declared size {int(content_length)} bytes > "
                    f"{MAX_PDF_SIZE_BYTES} limit): {url}"
                )
                return None

            # Read the content in full
            content = resp.content

            # Enforce size limit on actual content
            if len(content) > MAX_PDF_SIZE_BYTES:
                logger.warning(
                    f"Skipping PDF (actual size {len(content)} bytes > "
                    f"{MAX_PDF_SIZE_BYTES} limit): {url}"
                )
                return None

            # Compute SHA-256 of file content
            content_hash = hashlib.sha256(content).hexdigest()
            short_hash = content_hash[:8]

            # Dedup: skip if we already have a file with the same content hash
            if short_hash in self._seen_hashes:
                logger.info(f"PDF already on disk (hash={short_hash}): {url}")
                # Find the existing file to return its path
                existing = list(self._base_dir.glob(f"*_{short_hash}_*.pdf"))
                return str(existing[0]) if existing else None

            # Build filename: {spider_name}_{hash[:8]}_{timestamp}.pdf
            timestamp = int(time.time())
            filename = f"{spider_name}_{short_hash}_{timestamp}.pdf"
            dest_path = self._base_dir / filename

            dest_path.write_bytes(content)
            self._seen_hashes.add(short_hash)
            logger.info(f"Downloaded PDF ({len(content)} bytes) → {dest_path}")
            return str(dest_path)

        except requests.RequestException as exc:
            logger.error(f"Failed to download PDF from {url}: {exc}")
            return None


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

    def _resolve_lgu_id(self, item: dict) -> int | None:
        """Resolve an LGU id from the item, trying multiple name fields.

        Checks ``procuring_entity`` first (bid/award notices), then falls
        back to ``lgu_name`` (budget items, audit reports), and finally
        ``agency_name`` (FOI requests).  Uses case-insensitive SQL LIKE.
        """
        candidates = [
            item.get("procuring_entity", ""),
            item.get("lgu_name", ""),
            item.get("agency_name", ""),
        ]
        cur = self.conn.cursor()
        try:
            for name in candidates:
                if not name:
                    continue
                pattern = f"%{name}%"
                cur.execute(
                    "SELECT id FROM lgus WHERE name ILIKE %s LIMIT 1",
                    (pattern,),
                )
                row = cur.fetchone()
                if row:
                    return row[0]
            return None
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
                "AuditReportItem": "audit_report",
                "FOIRequestItem": "foi_response",
                "GovernmentDocumentItem": "general",
            }
            document_type = doc_type_map.get(item_class, "general")

            # Determine source portal from spider name
            source_portal = getattr(spider, "name", "manual")

            # Resolve LGU (tries procuring_entity, lgu_name, agency_name)
            lgu_id = self._resolve_lgu_id(dict(item))

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

            # For BudgetItems, also insert directly into budget_allocations
            if item_class == "BudgetItem" and lgu_id:
                self._process_budget_item(cur, item, lgu_id)

            self.conn.commit()
            logger.info(f"Saved to DB: {item.get('title', 'unknown')} (lgu_id={lgu_id})")

        except Exception:
            self.conn.rollback()
            logger.exception(f"Failed to insert document: {source_url}")
        finally:
            cur.close()

        return item

    def _process_budget_item(self, cur, item, lgu_id: int) -> None:
        """Insert a BudgetItem directly into the budget_allocations table.

        Uses an upsert so re-crawled data overwrites stale amounts.
        """
        fiscal_year = item.get("fiscal_year")
        category = item.get("category", "")
        subcategory = item.get("subcategory", "")
        allocated_amount = item.get("allocated_amount", 0)
        source_document_url = item.get("source_document_url", "") or item.get("source_url", "")

        if not fiscal_year or not category:
            logger.warning("BudgetItem missing fiscal_year or category — skipping budget_allocations insert")
            return

        cur.execute(
            """
            INSERT INTO budget_allocations
                (lgu_id, fiscal_year, category, subcategory, allocated_amount, source_document_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (lgu_id, fiscal_year, category, subcategory)
            DO UPDATE SET allocated_amount = EXCLUDED.allocated_amount
            """,
            (
                lgu_id,
                fiscal_year,
                category,
                subcategory,
                allocated_amount,
                source_document_url,
            ),
        )
        logger.info(
            f"Upserted budget_allocation: lgu_id={lgu_id}, "
            f"FY{fiscal_year} {category}/{subcategory} = {allocated_amount}"
        )


class ProcessingQueuePipeline:
    """Queue downloaded PDFs for OCR/NLP processing via Celery.

    TODO: Implement Celery task dispatch.
    """

    def process_item(self, item, spider):
        if item.get("pdf_urls") or item.get("pdf_url"):
            logger.info(f"Queuing for processing: {item.get('title', 'unknown')}")
            # TODO: Dispatch Celery task for Textract + Claude processing
        return item
