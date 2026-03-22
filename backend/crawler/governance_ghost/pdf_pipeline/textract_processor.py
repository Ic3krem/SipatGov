import logging
import os
import time

import boto3

from app.config import settings

logger = logging.getLogger(__name__)


def _mock_ocr_enabled() -> bool:
    """Check if MOCK_OCR is enabled via environment variable."""
    return os.environ.get("MOCK_OCR", "").lower() == "true"


class TextractProcessor:
    """Process PDFs using AWS Textract for OCR."""

    def __init__(self):
        if _mock_ocr_enabled():
            logger.info("MOCK_OCR is enabled; skipping Textract client initialisation")
            self.client = None
        else:
            self.client = boto3.client(
                "textract",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )

    def process_pdf_from_s3(self, bucket: str, key: str) -> str:
        """Process a PDF stored in S3 using Textract async API.

        Returns the extracted raw text.
        """
        if _mock_ocr_enabled():
            from governance_ghost.pdf_pipeline.mock_data import MOCK_OCR_BID_NOTICE_TEXT

            logger.info("MOCK_OCR: returning canned OCR text instead of calling Textract")
            return MOCK_OCR_BID_NOTICE_TEXT

        # Start async text detection job
        response = self.client.start_document_text_detection(
            DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
        )
        job_id = response["JobId"]
        logger.info(f"Started Textract job: {job_id} for s3://{bucket}/{key}")

        # Poll for completion
        text_blocks = []
        while True:
            result = self.client.get_document_text_detection(JobId=job_id)
            status = result["JobStatus"]

            if status == "SUCCEEDED":
                for block in result.get("Blocks", []):
                    if block["BlockType"] == "LINE":
                        text_blocks.append(block["Text"])

                # Handle pagination for multi-page results
                next_token = result.get("NextToken")
                while next_token:
                    result = self.client.get_document_text_detection(
                        JobId=job_id, NextToken=next_token
                    )
                    for block in result.get("Blocks", []):
                        if block["BlockType"] == "LINE":
                            text_blocks.append(block["Text"])
                    next_token = result.get("NextToken")

                break
            elif status == "FAILED":
                error = result.get("StatusMessage", "Unknown error")
                logger.error(f"Textract job failed: {error}")
                raise RuntimeError(f"Textract processing failed: {error}")
            else:
                logger.debug(f"Textract job {job_id} status: {status}, waiting...")
                time.sleep(5)

        raw_text = "\n".join(text_blocks)
        logger.info(f"Textract extracted {len(text_blocks)} lines, {len(raw_text)} chars")
        return raw_text

    def process_pdf_bytes(self, pdf_bytes: bytes) -> str:
        """Process a PDF from bytes (synchronous, for documents < 5MB / 1 page).

        For multi-page documents, use process_pdf_from_s3 instead.
        """
        if _mock_ocr_enabled():
            from governance_ghost.pdf_pipeline.mock_data import MOCK_OCR_BID_NOTICE_TEXT

            logger.info("MOCK_OCR: returning canned OCR text instead of calling Textract")
            return MOCK_OCR_BID_NOTICE_TEXT

        response = self.client.detect_document_text(
            Document={"Bytes": pdf_bytes}
        )
        text_blocks = [
            block["Text"]
            for block in response.get("Blocks", [])
            if block["BlockType"] == "LINE"
        ]
        return "\n".join(text_blocks)
