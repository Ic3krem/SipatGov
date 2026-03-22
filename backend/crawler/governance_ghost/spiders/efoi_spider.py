import re
from datetime import datetime, timezone

import scrapy

from governance_ghost.items import FOIRequestItem, GovernmentDocumentItem


class EFOISpider(scrapy.Spider):
    """Spider for crawling the e-FOI (Freedom of Information) Portal.

    Targets the public request tracker, disclosed documents, and agency
    compliance data to assess government transparency.
    """

    name = "efoi"
    allowed_domains = ["foi.gov.ph", "www.foi.gov.ph"]
    start_urls = [
        "https://www.foi.gov.ph/requests",
        "https://www.foi.gov.ph/agencies",
        "https://www.foi.gov.ph/reports",
    ]

    # Known FOI request statuses
    VALID_STATUSES = {
        "successful", "partially successful", "proactively disclosed",
        "denied", "pending", "processing", "closed", "referred",
        "awaiting clarification", "accepted",
    }

    def parse(self, response):
        """Parse the main e-FOI pages (requests tracker, agencies list, reports).

        Routes to specialized parsers based on the page structure.
        """
        self.logger.info(f"Parsing e-FOI page: {response.url}")

        url_lower = response.url.lower()

        if "/requests" in url_lower:
            yield from self._parse_request_tracker(response)
        elif "/agencies" in url_lower:
            yield from self._parse_agencies_list(response)
        elif "/reports" in url_lower:
            yield from self._parse_reports_page(response)
        else:
            # Fallback: try all parsing strategies
            yield from self._parse_request_tracker(response)
            yield from self._parse_agencies_list(response)

        # Follow pagination on all page types
        yield from self._follow_pagination(response)

    def _parse_request_tracker(self, response):
        """Parse the public FOI request tracker page.

        Extracts individual request records with agency, status, processing
        time, and any disclosed document links.
        """
        # Try card/list-based layout
        request_cards = response.css(
            "div.request-card, "
            "div.request-item, "
            "tr.request-row, "
            "div.foi-request, "
            "li.request-entry"
        )

        if request_cards:
            for card in request_cards:
                yield from self._parse_request_card(response, card)
        else:
            # Try table-based layout
            yield from self._parse_request_table(response)

        # Follow links to individual request detail pages
        detail_links = response.css(
            "a[href*='/requests/'], "
            "a[href*='request_id='], "
            "a[href*='request-detail']"
        ).getall()

        seen = set()
        for href in detail_links:
            # Extract just the href attribute if it's an element
            if hasattr(href, "attrib"):
                href = href.attrib.get("href", "")
            full_url = response.urljoin(href)
            if full_url not in seen and "foi.gov.ph" in full_url:
                seen.add(full_url)
                yield response.follow(
                    full_url,
                    callback=self.parse_request_detail,
                )

    def _parse_request_card(self, response, card):
        """Parse a single request card/row element."""
        agency_name = (
            card.css(
                ".agency-name::text, "
                ".agency::text, "
                "[data-field='agency']::text, "
                "td.agency::text"
            ).get("").strip()
        )

        status = (
            card.css(
                ".status::text, "
                ".request-status::text, "
                "[data-field='status']::text, "
                "td.status::text, "
                "span.badge::text"
            ).get("").strip()
        )

        request_type = (
            card.css(
                ".request-type::text, "
                ".type::text, "
                "[data-field='type']::text, "
                "td.type::text"
            ).get("").strip()
        )

        processing_days = self._extract_processing_days(card)

        # Look for disclosed/attached documents
        doc_links = card.css("a[href$='.pdf']::attr(href)").getall()
        doc_links += card.css("a[href*='download']::attr(href)").getall()
        doc_links += card.css("a[href*='document']::attr(href)").getall()
        disclosed_docs = [response.urljoin(link) for link in doc_links]

        if agency_name or status:
            yield FOIRequestItem(
                agency_name=agency_name,
                request_type=request_type or "information_request",
                status=self._normalize_status(status),
                processing_days=processing_days,
                disclosed_documents=disclosed_docs,
                source_url=response.url,
                crawled_at=datetime.now(timezone.utc).isoformat(),
            )

            # If there are disclosed documents, also yield them as GovernmentDocumentItems
            for doc_url in disclosed_docs:
                if self._is_pdf_url(doc_url):
                    yield GovernmentDocumentItem(
                        source_portal="eFOI",
                        source_url=response.url,
                        title=f"FOI Disclosure - {agency_name}",
                        document_type="foi_response",
                        lgu_name=agency_name,
                        pdf_url=doc_url,
                        metadata={
                            "portal": "Freedom of Information Portal",
                            "status": self._normalize_status(status),
                        },
                        crawled_at=datetime.now(timezone.utc).isoformat(),
                    )

    def _parse_request_table(self, response):
        """Parse FOI request data from HTML tables."""
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

            col_map = self._map_foi_columns(headers)
            if col_map.get("agency") is None and col_map.get("status") is None:
                continue

            rows = table.css("tbody tr, tr")[1:]
            for row in rows:
                cells = [c.css("::text").get("").strip() for c in row.css("td")]
                if not cells or all(c == "" for c in cells):
                    continue

                agency = self._safe_get(cells, col_map.get("agency"))
                status = self._safe_get(cells, col_map.get("status"))
                req_type = self._safe_get(cells, col_map.get("type"))
                days_raw = self._safe_get(cells, col_map.get("days"))

                # Extract PDF links within the row
                row_docs = row.css("a[href$='.pdf']::attr(href)").getall()
                row_docs += row.css("a[href*='download']::attr(href)").getall()
                disclosed_docs = [response.urljoin(d) for d in row_docs]

                if agency or status:
                    yield FOIRequestItem(
                        agency_name=agency or "",
                        request_type=req_type or "information_request",
                        status=self._normalize_status(status or ""),
                        processing_days=self._parse_days(days_raw),
                        disclosed_documents=disclosed_docs,
                        source_url=response.url,
                        crawled_at=datetime.now(timezone.utc).isoformat(),
                    )

    def parse_request_detail(self, response):
        """Parse an individual FOI request detail page."""
        self.logger.info(f"Parsing FOI request detail: {response.url}")

        agency_name = (
            response.css(
                "div.agency-name::text, "
                "span.agency::text, "
                "h2.agency::text, "
                "[data-label='Agency']::text, "
                "dt:contains('Agency') + dd::text"
            ).get("").strip()
        )

        status = (
            response.css(
                "span.status::text, "
                "div.request-status::text, "
                "[data-label='Status']::text, "
                "dt:contains('Status') + dd::text"
            ).get("").strip()
        )

        request_type = (
            response.css(
                "span.request-type::text, "
                "[data-label='Type']::text, "
                "dt:contains('Type') + dd::text"
            ).get("").strip()
        )

        processing_days = self._extract_processing_days(response)

        # Disclosed documents / attachments
        doc_links = response.css("a[href$='.pdf']::attr(href)").getall()
        doc_links += response.css(
            "div.attachments a::attr(href), "
            "div.documents a::attr(href), "
            "a[href*='download']::attr(href)"
        ).getall()
        disclosed_docs = list(set(response.urljoin(link) for link in doc_links))

        if agency_name or status:
            yield FOIRequestItem(
                agency_name=agency_name,
                request_type=request_type or "information_request",
                status=self._normalize_status(status),
                processing_days=processing_days,
                disclosed_documents=disclosed_docs,
                source_url=response.url,
                crawled_at=datetime.now(timezone.utc).isoformat(),
            )

        for doc_url in disclosed_docs:
            if self._is_pdf_url(doc_url):
                yield GovernmentDocumentItem(
                    source_portal="eFOI",
                    source_url=response.url,
                    title=f"FOI Disclosure - {agency_name}",
                    document_type="foi_response",
                    lgu_name=agency_name,
                    pdf_url=doc_url,
                    metadata={
                        "portal": "Freedom of Information Portal",
                        "status": self._normalize_status(status),
                        "request_type": request_type,
                    },
                    crawled_at=datetime.now(timezone.utc).isoformat(),
                )

    def _parse_agencies_list(self, response):
        """Parse the agencies listing page.

        Extracts links to individual agency FOI pages for further crawling.
        """
        agency_links = response.css(
            "a[href*='/agencies/'], "
            "a[href*='agency_id='], "
            "div.agency-list a::attr(href), "
            "ul.agency-list a::attr(href)"
        )

        for link in agency_links:
            href = link.attrib.get("href", "") if hasattr(link, "attrib") else link
            full_url = response.urljoin(href)
            if "foi.gov.ph" in full_url:
                yield response.follow(
                    full_url,
                    callback=self.parse_agency_page,
                )

    def parse_agency_page(self, response):
        """Parse an individual agency's FOI page.

        Extracts the agency's FOI compliance data and disclosed documents.
        """
        agency_name = (
            response.css("h1::text").get("")
            or response.css("h2.agency-name::text").get("")
            or response.css("title::text").get("")
        ).strip()

        self.logger.info(f"Parsing agency page: {agency_name} ({response.url})")

        # Look for compliance statistics
        stats = response.css(
            "div.compliance-stats, "
            "div.agency-stats, "
            "div.summary-stats, "
            "section.statistics"
        )

        if stats:
            # Try to extract compliance metrics from the stats section
            total_requests = self._extract_stat(stats, ["total", "requests", "received"])
            successful = self._extract_stat(stats, ["successful", "granted", "approved"])
            pending = self._extract_stat(stats, ["pending", "processing"])
            denied = self._extract_stat(stats, ["denied", "rejected"])

            if any([total_requests, successful, pending, denied]):
                yield FOIRequestItem(
                    agency_name=agency_name,
                    request_type="compliance_summary",
                    status="summary",
                    processing_days="",
                    disclosed_documents=[],
                    source_url=response.url,
                    crawled_at=datetime.now(timezone.utc).isoformat(),
                )

        # Look for disclosed documents on the agency page
        doc_links = response.css(
            "a[href$='.pdf']::attr(href), "
            "a.document-link::attr(href), "
            "div.disclosed-documents a::attr(href)"
        ).getall()

        for doc_link in doc_links:
            doc_url = response.urljoin(doc_link)
            if self._is_pdf_url(doc_url):
                yield GovernmentDocumentItem(
                    source_portal="eFOI",
                    source_url=response.url,
                    title=f"FOI Disclosure - {agency_name}",
                    document_type="foi_response",
                    lgu_name=agency_name,
                    pdf_url=doc_url,
                    metadata={
                        "portal": "Freedom of Information Portal",
                        "agency": agency_name,
                    },
                    crawled_at=datetime.now(timezone.utc).isoformat(),
                )

        # Follow links to the agency's request list
        request_list_link = response.css(
            "a[href*='requests']::attr(href), "
            "a:contains('View Requests')::attr(href)"
        ).get()
        if request_list_link:
            yield response.follow(
                request_list_link,
                callback=self._parse_request_tracker,
            )

    def _parse_reports_page(self, response):
        """Parse the FOI reports/statistics page.

        Extracts compliance rate data and summary statistics by agency.
        """
        self.logger.info(f"Parsing FOI reports page: {response.url}")

        # Look for compliance report tables
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

            col_map = self._map_compliance_columns(headers)
            if col_map.get("agency") is None:
                continue

            rows = table.css("tbody tr, tr")[1:]
            for row in rows:
                cells = [c.css("::text").get("").strip() for c in row.css("td")]
                if not cells or all(c == "" for c in cells):
                    continue

                agency = self._safe_get(cells, col_map.get("agency"))
                if not agency:
                    continue

                yield FOIRequestItem(
                    agency_name=agency,
                    request_type="compliance_report",
                    status="summary",
                    processing_days=self._safe_get(cells, col_map.get("avg_days")) or "",
                    disclosed_documents=[],
                    source_url=response.url,
                    crawled_at=datetime.now(timezone.utc).isoformat(),
                )

        # Look for downloadable report PDFs
        pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()
        for pdf_link in pdf_links:
            pdf_url = response.urljoin(pdf_link)
            link_text = response.css(f"a[href='{pdf_link}']::text").get("").strip()

            yield GovernmentDocumentItem(
                source_portal="eFOI",
                source_url=response.url,
                title=link_text or "FOI Compliance Report",
                document_type="foi_response",
                lgu_name="",
                pdf_url=pdf_url,
                metadata={"portal": "Freedom of Information Portal"},
                crawled_at=datetime.now(timezone.utc).isoformat(),
            )

    def _follow_pagination(self, response):
        """Follow pagination links on e-FOI pages."""
        next_link = response.css(
            "a.next::attr(href), "
            "li.next a::attr(href), "
            "a[rel='next']::attr(href), "
            "ul.pagination li.active + li a::attr(href), "
            "a.pagination-next::attr(href)"
        ).get()
        if next_link:
            self.logger.info(f"Following pagination: {next_link}")
            yield response.follow(next_link, callback=self.parse)

    def _map_foi_columns(self, headers):
        """Map FOI table header keywords to column indices."""
        col_map = {}
        mappings = {
            "agency": ["agency", "office", "department", "entity"],
            "status": ["status", "disposition", "result"],
            "type": ["type", "category", "request type"],
            "days": ["days", "processing", "duration", "turnaround"],
        }

        for key, keywords in mappings.items():
            for idx, header in enumerate(headers):
                if any(kw in header for kw in keywords):
                    col_map[key] = idx
                    break

        return col_map

    def _map_compliance_columns(self, headers):
        """Map compliance report table columns."""
        col_map = {}
        mappings = {
            "agency": ["agency", "office", "department", "entity", "name"],
            "total": ["total", "received", "requests"],
            "successful": ["successful", "granted", "approved", "disclosed"],
            "denied": ["denied", "rejected"],
            "pending": ["pending", "processing"],
            "avg_days": ["average", "days", "turnaround", "processing time"],
            "compliance": ["compliance", "rate", "percentage", "score"],
        }

        for key, keywords in mappings.items():
            for idx, header in enumerate(headers):
                if any(kw in header for kw in keywords):
                    col_map[key] = idx
                    break

        return col_map

    def _extract_processing_days(self, selector):
        """Extract processing days from a page element or response.

        Looks for patterns like '5 days', '3 working days', 'N business days'.
        """
        text = " ".join(selector.css("::text").getall())

        # Match patterns like "5 days", "3 working days", "10 business days"
        match = re.search(r"(\d+)\s*(?:working\s+|business\s+)?days?", text, re.IGNORECASE)
        if match:
            return match.group(1)

        # Match "Processing Time: 5" style
        match = re.search(r"processing\s*(?:time)?[:\s]+(\d+)", text, re.IGNORECASE)
        if match:
            return match.group(1)

        return ""

    def _parse_days(self, raw):
        """Parse a days value from raw text."""
        if not raw:
            return ""
        match = re.search(r"(\d+)", raw)
        return match.group(1) if match else ""

    def _normalize_status(self, status):
        """Normalize a status string to a known value."""
        if not status:
            return ""
        status_lower = status.lower().strip()

        # Direct match
        if status_lower in self.VALID_STATUSES:
            return status_lower

        # Fuzzy match
        for valid in self.VALID_STATUSES:
            if valid in status_lower or status_lower in valid:
                return valid

        return status_lower

    def _extract_stat(self, selector, keywords):
        """Extract a numeric statistic from a stats section matching keywords."""
        text = " ".join(selector.css("::text").getall()).lower()
        for keyword in keywords:
            pattern = rf"{keyword}\s*[:\s]*(\d[\d,]*)"
            match = re.search(pattern, text)
            if match:
                return match.group(1).replace(",", "")
        return ""

    def _is_pdf_url(self, url):
        """Check if a URL points to a PDF."""
        return ".pdf" in url.lower().split("?")[0]

    def _safe_get(self, lst, index):
        """Safely get a list element by index."""
        if index is not None and 0 <= index < len(lst):
            return lst[index].strip()
        return None
