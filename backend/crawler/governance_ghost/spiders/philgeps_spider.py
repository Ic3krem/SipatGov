from datetime import datetime, timezone

import scrapy

from governance_ghost.items import AwardNoticeItem, BidNoticeItem


class PhilGEPSSpider(scrapy.Spider):
    """Spider for crawling PhilGEPS (Philippine Government Electronic Procurement System).

    Targets bid notices and award notices to track public procurement.
    """

    name = "philgeps"
    allowed_domains = ["philgeps.gov.ph"]
    start_urls = [
        "https://www.philgeps.gov.ph/GEPSNONPILOT/Opportunity/SplashOpportunity.aspx",
    ]

    def parse(self, response):
        """Parse the main opportunity listing page."""
        # Extract bid notice links
        bid_links = response.css("a[href*='Opportunity']::attr(href)").getall()
        for link in bid_links:
            yield response.follow(link, callback=self.parse_bid_notice)

        # Follow pagination
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_bid_notice(self, response):
        """Parse individual bid notice page."""
        title = response.css("h2.opportunity-title::text").get("").strip()
        if not title:
            title = response.css("#ContentPlaceHolder1_lblTitle::text").get("").strip()

        # Extract PDF links from the page
        pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()
        pdf_links += response.css("a[href*='download']::attr(href)").getall()

        yield BidNoticeItem(
            reference_number=response.css("#ContentPlaceHolder1_lblRefNo::text").get("").strip(),
            title=title,
            procuring_entity=response.css("#ContentPlaceHolder1_lblProcEntity::text").get("").strip(),
            approved_budget=response.css("#ContentPlaceHolder1_lblABC::text").get("").strip(),
            bid_submission_deadline=response.css("#ContentPlaceHolder1_lblDeadline::text").get("").strip(),
            pdf_urls=[response.urljoin(url) for url in pdf_links],
            source_url=response.url,
            crawled_at=datetime.now(timezone.utc).isoformat(),
        )

        # Check for award notice link on the same page
        award_link = response.css("a[href*='Award']::attr(href)").get()
        if award_link:
            yield response.follow(award_link, callback=self.parse_award_notice)

    def parse_award_notice(self, response):
        """Parse award notice page."""
        pdf_links = response.css("a[href$='.pdf']::attr(href)").getall()

        yield AwardNoticeItem(
            reference_number=response.css("#ContentPlaceHolder1_lblRefNo::text").get("").strip(),
            title=response.css("#ContentPlaceHolder1_lblTitle::text").get("").strip(),
            procuring_entity=response.css("#ContentPlaceHolder1_lblProcEntity::text").get("").strip(),
            winning_bidder=response.css("#ContentPlaceHolder1_lblWinner::text").get("").strip(),
            contract_amount=response.css("#ContentPlaceHolder1_lblAmount::text").get("").strip(),
            award_date=response.css("#ContentPlaceHolder1_lblAwardDate::text").get("").strip(),
            pdf_urls=[response.urljoin(url) for url in pdf_links],
            source_url=response.url,
            crawled_at=datetime.now(timezone.utc).isoformat(),
        )
