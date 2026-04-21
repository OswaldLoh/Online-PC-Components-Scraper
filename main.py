import datetime
from scrapy.crawler import CrawlerProcess
from playwright_scrapper.playwright_scrapper.spiders.PCImage import PcImageSpider


def should_abort_request(request):
    # 1. Block heavy visual and media resource types
    if request.resource_type in ("image", "media", "font", "stylesheet", "other"):
        return True

    blocked_domains = [
        "zoho", "zohocdn", "zohopublic", "salesiq",
        "google-analytics", "googletagmanager",
        "facebook", "pixel", "clarity"
    ]

    # If any of the blocked domains are in the request URL, kill the request
    if any(domain in request.url.lower() for domain in blocked_domains):
        return True

    return False


def run_scraper():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


    output_file = f"pcimage.{timestamp}.csv"

    custom_settings = {
        "FEEDS": {
            output_file: {
                "format": "csv",
                "encoding": "utf8",
                "store_empty": False,
            },
        },
        "ROBOTSTXT_OBEY": True,

        "CONCURRENT_REQUESTS": 64,
        "PLAYWRIGHT_MAX_CONTEXTS": 4,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 2,

        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },

        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

        "PLAYWRIGHT_ABORT_REQUESTS": should_abort_request,
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
        }
    }

    process = CrawlerProcess(settings=custom_settings)
    process.crawl(PcImageSpider)
    process.start(stop_after_crawl=True)

if __name__ == "__main__":
    run_scraper()