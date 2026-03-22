BOT_NAME = "governance_ghost"

SPIDER_MODULES = ["governance_ghost.spiders"]
NEWSPIDER_MODULE = "governance_ghost.spiders"

# Crawl responsibly - respect robots.txt and rate limits
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True

# Retry configuration
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [429, 500, 502, 503, 504]

# User-Agent rotation
USER_AGENT = "SipatGov Research Bot (+https://sipatgov.ph/bot)"

DOWNLOADER_MIDDLEWARES = {
    "governance_ghost.middlewares.ProxyRotationMiddleware": 610,
    "governance_ghost.middlewares.UserAgentRotationMiddleware": 400,
    "governance_ghost.middlewares.RateLimitMiddleware": 500,
}

ITEM_PIPELINES = {
    "governance_ghost.pipelines.DuplicateFilterPipeline": 100,
    "governance_ghost.pipelines.ValidationPipeline": 150,
    "governance_ghost.pipelines.PDFDownloadPipeline": 200,
    "governance_ghost.pipelines.DatabasePipeline": 300,
    "governance_ghost.pipelines.ProcessingQueuePipeline": 400,
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
