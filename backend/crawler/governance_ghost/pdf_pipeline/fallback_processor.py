import logging

logger = logging.getLogger(__name__)


def extract_text_pymupdf(file_path: str) -> str:
    """Extract text from a PDF using PyMuPDF (fitz).

    Best for: text-native PDFs (not scanned).
    Fast and accurate for well-formatted documents.
    """
    import fitz  # PyMuPDF

    text_parts = []
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(text)
        doc.close()
    except Exception as e:
        logger.error(f"PyMuPDF extraction failed for {file_path}: {e}")
        return ""

    result = "\n\n".join(text_parts)
    logger.info(f"PyMuPDF extracted {len(result)} chars from {file_path}")
    return result


def extract_text_pdfplumber(file_path: str) -> str:
    """Extract text from a PDF using pdfplumber.

    Best for: PDFs with tables and structured layouts.
    Slower than PyMuPDF but better at preserving table structure.
    """
    import pdfplumber

    text_parts = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Try table extraction first
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        for row in table:
                            cells = [str(cell or "") for cell in row]
                            text_parts.append(" | ".join(cells))
                        text_parts.append("")  # Blank line between tables

                # Also extract regular text
                text = page.extract_text()
                if text:
                    text_parts.append(text)
    except Exception as e:
        logger.error(f"pdfplumber extraction failed for {file_path}: {e}")
        return ""

    result = "\n".join(text_parts)
    logger.info(f"pdfplumber extracted {len(result)} chars from {file_path}")
    return result


def is_text_native(file_path: str, threshold: int = 100) -> bool:
    """Check if a PDF contains extractable text (not just scanned images).

    If PyMuPDF can extract more than `threshold` characters, the PDF is
    likely text-native and doesn't need OCR via Textract.
    """
    text = extract_text_pymupdf(file_path)
    return len(text.strip()) > threshold


def extract_text_with_fallback(file_path: str) -> tuple[str, str]:
    """Try multiple extraction methods and return the best result.

    Returns:
        Tuple of (extracted_text, method_used)
    """
    # Try PyMuPDF first (fastest)
    text = extract_text_pymupdf(file_path)
    if len(text.strip()) > 100:
        return text, "pymupdf"

    # Try pdfplumber for table-heavy docs
    text = extract_text_pdfplumber(file_path)
    if len(text.strip()) > 100:
        return text, "pdfplumber"

    # Both failed - needs OCR (Textract)
    logger.info(f"Local extraction failed for {file_path}, needs OCR")
    return "", "needs_ocr"
