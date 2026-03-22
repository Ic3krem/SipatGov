import scrapy


class GovernmentDocumentItem(scrapy.Item):
    """Item representing a crawled government document."""
    source_portal = scrapy.Field()
    source_url = scrapy.Field()
    title = scrapy.Field()
    document_type = scrapy.Field()
    lgu_name = scrapy.Field()
    pdf_url = scrapy.Field()
    metadata = scrapy.Field()
    crawled_at = scrapy.Field()


class BidNoticeItem(scrapy.Item):
    """PhilGEPS bid notice."""
    reference_number = scrapy.Field()
    title = scrapy.Field()
    procuring_entity = scrapy.Field()
    approved_budget = scrapy.Field()
    bid_submission_deadline = scrapy.Field()
    pdf_urls = scrapy.Field()
    source_url = scrapy.Field()
    crawled_at = scrapy.Field()


class AwardNoticeItem(scrapy.Item):
    """PhilGEPS award notice."""
    reference_number = scrapy.Field()
    title = scrapy.Field()
    procuring_entity = scrapy.Field()
    winning_bidder = scrapy.Field()
    contract_amount = scrapy.Field()
    award_date = scrapy.Field()
    pdf_urls = scrapy.Field()
    source_url = scrapy.Field()
    crawled_at = scrapy.Field()


class BudgetItem(scrapy.Item):
    """DBM budget allocation."""
    lgu_name = scrapy.Field()
    fiscal_year = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    allocated_amount = scrapy.Field()
    source_url = scrapy.Field()
    source_document_url = scrapy.Field()
    crawled_at = scrapy.Field()
