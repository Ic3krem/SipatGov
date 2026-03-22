import re
from datetime import datetime, timezone
from urllib.parse import urljoin

import scrapy

from governance_ghost.items import BudgetItem, GovernmentDocumentItem


class DBMSpider(scrapy.Spider):
    """Spider for crawling the Department of Budget and Management (DBM) website.

    Targets the National Expenditure Program (NEP), General Appropriations Act
    (GAA), and LGU budget data to track government budget allocations.
    """

    name = "dbm"
    allowed_domains = ["dbm.gov.ph", "www.dbm.gov.ph"]
    start_urls = [
        "https://www.dbm.gov.ph/index.php/budget-documents",
        "https://www.dbm.gov.ph/index.php/budget-documents/national-expenditure-program",
        "https://www.dbm.gov.ph/index.php/budget-documents/general-appropriations-act",
        "https://www.dbm.gov.ph/index.php/programs-activities/lgu-budget",
    ]

    # Maps human-friendly names to URL path fragments for classification
    DOCUMENT_CATEGORIES = {
        "national-expenditure-program": "NEP",
        "general-appropriations-act": "GAA",
        "lgu-budget": "LGU Budget",
        "budget-documents": "Budget Document",
        "data-and-budget-management": "Data & Budget Management",
    }

    def parse(self, response):
        """Parse the main budget documents listing pages.

        Dispatches to specialized parsers based on the URL path.
        """
        self.logger.info(f"Parsing DBM page: {response.url}")

        # Detect the page category from the URL
        category = self._classify_url(response.url)

        # --- Extract links to individual budget document pages ---
        content_links = response.css(
            "div.item-page a::attr(href), "
            "div.category a::attr(href), "
            "div.blog a::attr(href), "
            "div#content a::attr(href), "
            "article a::attr(href)"
        ).getall()

        for link in content_links:
            full_url = response.urljoin(link)
            # Only follow internal links
            if "dbm.gov.ph" in full_url:
                if self._is_pdf_url(full_url):
                    yield self._build_document_item(
                        title=self._title_from_url(full_url),
                        pdf_url=full_url,
                        source_url=response.url,
                        document_type=category,
                    )
                elif self._is_budget_page(full_url):
                    yield response.follow(
                        full_url,
                        callback=self.parse_budget_page,
                        meta={"category": category},
                    )

        # --- Try to extract budget tables directly on the page ---
        yield from self._parse_budget_tables(response, category)

        # --- Follow pagination ---
        yield from self._follow_pagination(response)

    def parse_budget_page(self, response):
        """Parse an individual budget document or data page."""
        category = response.meta.get("category", "Budget Document")
        page_title = (
            response.css("h1::text").get("")
            or response.css("h2.article-title::text").get("")
            or response.css("title::text").get("")
        ).strip()

        self.logger.info(f"Parsing budget page: {page_title} ({response.url})")

        # --- Extract all PDF links ---
        pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()
        pdf_links += response.css("a[href*='.pdf?']::attr(href)").getall()

        for pdf_link in pdf_links:
            pdf_url = response.urljoin(pdf_link)
            # Try to get a meaningful title from the link text
            link_text = response.css(
                f"a[href='{pdf_link}']::text"
            ).get("").strip()
            doc_title = link_text or page_title or self._title_from_url(pdf_url)

            yield self._build_document_item(
                title=doc_title,
                pdf_url=pdf_url,
                source_url=response.url,
                document_type=category,
            )

        # --- Parse any budget data tables on the page ---
        yield from self._parse_budget_tables(response, category)

        # --- Follow sub-links on the page ---
        sub_links = response.css("div.item-page a::attr(href)").getall()
        for link in sub_links:
            full_url = response.urljoin(link)
            if "dbm.gov.ph" in full_url and self._is_pdf_url(full_url):
                yield self._build_document_item(
                    title=self._title_from_url(full_url),
                    pdf_url=full_url,
                    source_url=response.url,
                    document_type=category,
                )

    def _parse_budget_tables(self, response, category):
        """Extract structured budget data from HTML tables on the page.

        Looks for tables with columns like fiscal year, LGU/agency, category,
        and amount. Yields BudgetItem for each parseable row.
        """
        tables = response.css("table")

        for table in tables:
            headers = [
                h.css("::text").get("").strip().lower()
                for h in table.css("thead th, thead td, tr:first-child th, tr:first-child td")
            ]

            if not headers:
                continue

            # Identify column indices by keywords
            col_map = self._map_table_columns(headers)

            # Need at least a name/agency column and an amount column to be useful
            if col_map.get("name") is None and col_map.get("amount") is None:
                continue

            rows = table.css("tbody tr, tr")[1:]  # Skip header row
            for row in rows:
                cells = [
                    c.css("::text").get("").strip()
                    for c in row.css("td")
                ]
                if not cells or all(c == "" for c in cells):
                    continue

                lgu_name = self._safe_get(cells, col_map.get("name"))
                fiscal_year = self._safe_get(cells, col_map.get("year"))
                budget_category = self._safe_get(cells, col_map.get("category"))
                subcategory = self._safe_get(cells, col_map.get("subcategory"))
                amount_raw = self._safe_get(cells, col_map.get("amount"))

                # Skip rows with no meaningful data
                if not lgu_name and not amount_raw:
                    continue

                yield BudgetItem(
                    lgu_name=lgu_name or "",
                    fiscal_year=fiscal_year or self._extract_fiscal_year(response.url),
                    category=budget_category or category,
                    subcategory=subcategory or "",
                    allocated_amount=self._clean_amount(amount_raw),
                    source_url=response.url,
                    source_document_url="",
                    crawled_at=datetime.now(timezone.utc).isoformat(),
                )

    def _map_table_columns(self, headers):
        """Map header keywords to column indices.

        Returns a dict with keys: name, year, category, subcategory, amount.
        """
        col_map = {}
        name_keywords = ["lgu", "agency", "entity", "name", "office", "department"]
        year_keywords = ["year", "fiscal", "fy"]
        category_keywords = ["category", "sector", "program", "function"]
        subcategory_keywords = ["sub-category", "subcategory", "sub category", "object"]
        amount_keywords = ["amount", "budget", "allocation", "total", "appropriation"]

        for idx, header in enumerate(headers):
            header_lower = header.lower()
            if not col_map.get("name") and any(k in header_lower for k in name_keywords):
                col_map["name"] = idx
            elif not col_map.get("year") and any(k in header_lower for k in year_keywords):
                col_map["year"] = idx
            elif not col_map.get("subcategory") and any(k in header_lower for k in subcategory_keywords):
                col_map["subcategory"] = idx
            elif not col_map.get("category") and any(k in header_lower for k in category_keywords):
                col_map["category"] = idx
            elif not col_map.get("amount") and any(k in header_lower for k in amount_keywords):
                col_map["amount"] = idx

        return col_map

    def _follow_pagination(self, response):
        """Follow pagination links on DBM pages."""
        # Joomla-style pagination (DBM uses Joomla)
        next_link = response.css(
            "a.pagenav[title='Next']::attr(href), "
            "li.pagination-next a::attr(href), "
            "a.next::attr(href), "
            "ul.pagination li.active + li a::attr(href)"
        ).get()
        if next_link:
            self.logger.info(f"Following pagination: {next_link}")
            yield response.follow(next_link, callback=self.parse)

    def _classify_url(self, url):
        """Classify a URL into a budget document category."""
        url_lower = url.lower()
        for fragment, label in self.DOCUMENT_CATEGORIES.items():
            if fragment in url_lower:
                return label
        return "Budget Document"

    def _is_pdf_url(self, url):
        """Check if a URL points to a PDF file."""
        return ".pdf" in url.lower().split("?")[0]

    def _is_budget_page(self, url):
        """Check if a URL looks like a budget-related page."""
        budget_keywords = [
            "budget", "nep", "gaa", "appropriation", "expenditure",
            "lgu", "allocation", "fiscal", "ira", "national-tax",
        ]
        url_lower = url.lower()
        return any(kw in url_lower for kw in budget_keywords)

    def _title_from_url(self, url):
        """Extract a human-readable title from a PDF URL."""
        filename = url.split("/")[-1].split("?")[0]
        # Remove extension and replace separators with spaces
        name = filename.rsplit(".", 1)[0]
        name = re.sub(r"[_\-]+", " ", name)
        return name.strip().title() if name else "Untitled Document"

    def _extract_fiscal_year(self, url):
        """Try to extract a fiscal year from the URL or page context."""
        match = re.search(r"(20\d{2})", url)
        return match.group(1) if match else ""

    def _clean_amount(self, raw):
        """Clean a raw amount string, removing currency symbols and commas."""
        if not raw:
            return ""
        cleaned = re.sub(r"[^\d.\-]", "", raw)
        return cleaned

    def _safe_get(self, lst, index):
        """Safely get a list element by index."""
        if index is not None and 0 <= index < len(lst):
            return lst[index].strip()
        return None

    def _build_document_item(self, title, pdf_url, source_url, document_type):
        """Create a GovernmentDocumentItem for a PDF document."""
        return GovernmentDocumentItem(
            source_portal="DBM",
            source_url=source_url,
            title=title,
            document_type=document_type,
            lgu_name="",
            pdf_url=pdf_url,
            metadata={"portal": "Department of Budget and Management"},
            crawled_at=datetime.now(timezone.utc).isoformat(),
        )
