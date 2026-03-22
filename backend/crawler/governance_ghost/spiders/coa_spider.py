import re
from datetime import datetime, timezone

import scrapy

from governance_ghost.items import AuditReportItem, GovernmentDocumentItem


class COASpider(scrapy.Spider):
    """Spider for crawling the Commission on Audit (COA) website.

    Targets Annual Audit Reports (AARs) for LGUs, extracting audit findings,
    disallowances, and related PDF documents.
    """

    name = "coa"
    allowed_domains = ["coa.gov.ph", "www.coa.gov.ph"]
    start_urls = [
        "https://www.coa.gov.ph/reports/annual-audit-reports/",
        "https://www.coa.gov.ph/reports/annual-financial-report/",
        "https://www.coa.gov.ph/reports/",
    ]

    # Known patterns for LGU audit report sections
    REPORT_SECTION_PATTERNS = [
        "local-government",
        "lgu",
        "cities",
        "municipalities",
        "provinces",
        "barangay",
    ]

    def parse(self, response):
        """Parse the main reports index page.

        Follows links to specific report sections (LGU audit reports,
        annual financial reports, etc.).
        """
        self.logger.info(f"Parsing COA page: {response.url}")

        # --- Follow links to report category pages ---
        report_links = response.css(
            "div.entry-content a::attr(href), "
            "article a::attr(href), "
            "div.page-content a::attr(href), "
            "main a::attr(href), "
            "div#content a::attr(href)"
        ).getall()

        seen_urls = set()
        for link in report_links:
            full_url = response.urljoin(link)
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            if not self._is_coa_domain(full_url):
                continue

            if self._is_pdf_url(full_url):
                yield from self._handle_pdf_link(
                    response=response,
                    pdf_url=full_url,
                    context_text=self._get_link_text(response, link),
                )
            elif self._is_report_page(full_url):
                yield response.follow(
                    full_url,
                    callback=self.parse_report_listing,
                    meta={"parent_url": response.url},
                )

        # --- Parse tables on this page directly ---
        yield from self._parse_audit_tables(response)

        # --- Follow pagination ---
        yield from self._follow_pagination(response)

    def parse_report_listing(self, response):
        """Parse a report listing page (e.g., LGU annual audit reports for a year).

        These pages typically list audit reports by LGU with links to PDFs.
        """
        page_title = (
            response.css("h1.entry-title::text").get("")
            or response.css("h1::text").get("")
            or response.css("title::text").get("")
        ).strip()

        self.logger.info(f"Parsing report listing: {page_title} ({response.url})")

        # --- Extract PDF links with context ---
        pdf_links = response.css("a[href$='.pdf']")
        pdf_links += response.css("a[href*='.pdf?']")

        for pdf_anchor in pdf_links:
            pdf_href = pdf_anchor.attrib.get("href", "")
            if not pdf_href:
                continue
            pdf_url = response.urljoin(pdf_href)
            link_text = pdf_anchor.css("::text").get("").strip()

            yield from self._handle_pdf_link(
                response=response,
                pdf_url=pdf_url,
                context_text=link_text or page_title,
            )

        # --- Parse audit summary tables ---
        yield from self._parse_audit_tables(response)

        # --- Follow sub-page links (e.g., per-region or per-year breakdowns) ---
        sub_links = response.css(
            "div.entry-content a::attr(href), "
            "ul.report-list a::attr(href), "
            "table a::attr(href)"
        ).getall()

        for link in sub_links:
            full_url = response.urljoin(link)
            if (
                self._is_coa_domain(full_url)
                and not self._is_pdf_url(full_url)
                and self._is_report_page(full_url)
                and full_url != response.url
            ):
                yield response.follow(
                    full_url,
                    callback=self.parse_report_listing,
                    meta={"parent_url": response.url},
                )

        # --- Follow pagination ---
        yield from self._follow_pagination(response)

    def _parse_audit_tables(self, response):
        """Extract structured audit data from HTML tables.

        Looks for tables containing audit findings, disallowances, and LGU names.
        Yields AuditReportItem for each row with meaningful data.
        """
        tables = response.css("table")

        for table in tables:
            headers = [
                h.css("::text").get("").strip().lower()
                for h in table.css(
                    "thead th, thead td, tr:first-child th, tr:first-child td"
                )
            ]

            if not headers:
                continue

            col_map = self._map_audit_columns(headers)

            # Need at least a name column to be useful
            if col_map.get("lgu_name") is None:
                continue

            rows = table.css("tbody tr, tr")[1:]
            for row in rows:
                cells = [c.css("::text").get("").strip() for c in row.css("td")]
                if not cells or all(c == "" for c in cells):
                    continue

                lgu_name = self._safe_get(cells, col_map.get("lgu_name"))
                if not lgu_name:
                    continue

                # Extract PDF links within this row
                row_pdfs = row.css("a[href$='.pdf']::attr(href)").getall()
                row_pdf_urls = [response.urljoin(p) for p in row_pdfs]

                findings = self._safe_get(cells, col_map.get("findings"))
                disallowances_raw = self._safe_get(cells, col_map.get("disallowances"))
                audit_year = (
                    self._safe_get(cells, col_map.get("year"))
                    or self._extract_year(response.url)
                )

                yield AuditReportItem(
                    lgu_name=lgu_name,
                    audit_year=audit_year or "",
                    title=f"Audit Report - {lgu_name} ({audit_year})" if audit_year else f"Audit Report - {lgu_name}",
                    findings_summary=findings or "",
                    total_disallowances=self._clean_amount(disallowances_raw),
                    pdf_urls=row_pdf_urls,
                    source_url=response.url,
                    crawled_at=datetime.now(timezone.utc).isoformat(),
                )

    def _map_audit_columns(self, headers):
        """Map audit table header keywords to column indices."""
        col_map = {}
        mappings = {
            "lgu_name": ["lgu", "agency", "entity", "name", "office", "city", "municipality", "province"],
            "year": ["year", "period", "fiscal"],
            "findings": ["finding", "observation", "summary", "remark"],
            "disallowances": ["disallowance", "suspension", "charge", "amount"],
        }

        for key, keywords in mappings.items():
            for idx, header in enumerate(headers):
                if any(kw in header for kw in keywords):
                    col_map[key] = idx
                    break

        return col_map

    def _handle_pdf_link(self, response, pdf_url, context_text):
        """Process a PDF link found on a COA page.

        Yields a GovernmentDocumentItem and, if LGU info can be extracted,
        also yields an AuditReportItem.
        """
        lgu_name = self._extract_lgu_name(context_text, pdf_url)
        audit_year = self._extract_year(pdf_url) or self._extract_year(context_text)
        doc_title = context_text if context_text else self._title_from_url(pdf_url)

        yield GovernmentDocumentItem(
            source_portal="COA",
            source_url=response.url,
            title=doc_title,
            document_type="audit_report",
            lgu_name=lgu_name,
            pdf_url=pdf_url,
            metadata={
                "portal": "Commission on Audit",
                "audit_year": audit_year or "",
            },
            crawled_at=datetime.now(timezone.utc).isoformat(),
        )

        # If we can identify the LGU, also yield a structured AuditReportItem
        if lgu_name:
            yield AuditReportItem(
                lgu_name=lgu_name,
                audit_year=audit_year or "",
                title=doc_title,
                findings_summary="",
                total_disallowances="",
                pdf_urls=[pdf_url],
                source_url=response.url,
                crawled_at=datetime.now(timezone.utc).isoformat(),
            )

    def _follow_pagination(self, response):
        """Follow pagination links on COA pages."""
        # WordPress-style pagination (COA uses WordPress)
        next_link = response.css(
            "a.next.page-numbers::attr(href), "
            "li.next a::attr(href), "
            "a.page-numbers[aria-label='Next']::attr(href), "
            "nav.pagination a.next::attr(href)"
        ).get()
        if next_link:
            self.logger.info(f"Following pagination: {next_link}")
            yield response.follow(next_link, callback=self.parse)

    def _extract_lgu_name(self, text, url=""):
        """Try to extract an LGU name from link text or URL.

        Uses heuristics: looks for patterns like 'City of X', 'Municipality of X',
        'Province of X', or capitalized proper nouns after known prefixes.
        """
        combined = f"{text} {url}"

        # Common patterns in COA reports
        patterns = [
            r"(?:City|Municipality|Province)\s+of\s+([A-Z][a-zA-Z\s]+)",
            r"(?:city|municipality|province)\s+of\s+([A-Z][a-zA-Z\s]+)",
            r"(?:Brgy\.?|Barangay)\s+([A-Z][a-zA-Z\s]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, combined)
            if match:
                return match.group(0).strip()

        return ""

    def _extract_year(self, text):
        """Extract a four-digit year from text."""
        if not text:
            return ""
        match = re.search(r"(20\d{2})", str(text))
        return match.group(1) if match else ""

    def _is_pdf_url(self, url):
        """Check if a URL points to a PDF."""
        return ".pdf" in url.lower().split("?")[0]

    def _is_coa_domain(self, url):
        """Check if a URL belongs to the COA domain."""
        return "coa.gov.ph" in url.lower()

    def _is_report_page(self, url):
        """Check if a URL looks like a report-related page."""
        report_keywords = [
            "report", "audit", "annual", "aar", "financial",
            "lgu", "local-government", "cities", "municipalities",
            "provinces", "findings", "disallowance",
        ]
        url_lower = url.lower()
        return any(kw in url_lower for kw in report_keywords)

    def _get_link_text(self, response, href):
        """Get the text content of a link by its href."""
        text = response.css(f"a[href='{href}']::text").get("")
        return text.strip()

    def _title_from_url(self, url):
        """Extract a human-readable title from a URL."""
        filename = url.split("/")[-1].split("?")[0]
        name = filename.rsplit(".", 1)[0]
        name = re.sub(r"[_\-]+", " ", name)
        return name.strip().title() if name else "Untitled Document"

    def _clean_amount(self, raw):
        """Clean a raw amount string."""
        if not raw:
            return ""
        cleaned = re.sub(r"[^\d.\-]", "", raw)
        return cleaned

    def _safe_get(self, lst, index):
        """Safely get a list element by index."""
        if index is not None and 0 <= index < len(lst):
            return lst[index].strip()
        return None
