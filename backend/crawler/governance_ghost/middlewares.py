import logging
import random

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
]


class UserAgentRotationMiddleware:
    """Rotate User-Agent header on each request."""

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(USER_AGENTS)


class ProxyRotationMiddleware:
    """Rotate proxies from a configured list.

    Configure PROXY_LIST in settings as a list of proxy URLs.
    Falls back to direct connection if no proxies configured.
    """

    def __init__(self, proxy_list=None):
        self.proxies = proxy_list or []

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.getlist("PROXY_LIST", [])
        return cls(proxy_list=proxy_list)

    def process_request(self, request, spider):
        if self.proxies:
            proxy = random.choice(self.proxies)
            request.meta["proxy"] = proxy
            logger.debug(f"Using proxy: {proxy}")


class RateLimitMiddleware:
    """Add extra delays for government portals to be respectful.

    NOTE: Do NOT use time.sleep() here -- it blocks the Twisted reactor.
    Use Scrapy's built-in AutoThrottle extension instead (configured in
    settings.py with AUTOTHROTTLE_ENABLED = True).  This middleware now
    only logs the intended delay for observability; actual throttling is
    handled by AutoThrottle.
    """

    PORTAL_DELAYS = {
        "philgeps.gov.ph": 5,
        "dbm.gov.ph": 4,
        "coa.gov.ph": 4,
        "foi.gov.ph": 3,
    }

    def process_request(self, request, spider):
        for domain, delay in self.PORTAL_DELAYS.items():
            if domain in request.url:
                # Logging only -- actual throttling is handled by Scrapy's AutoThrottle
                logger.debug(f"Request to rate-limited domain {domain} (target delay: {delay}s)")
                break
