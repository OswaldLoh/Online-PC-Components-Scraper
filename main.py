import datetime
from scrapy.crawler import CrawlerProcess
from playwright_scrapper.playwright_scrapper.spiders.PCImage import PcImageSpider


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

        "CONCURRENT_REQUESTS": 32,
        "PLAYWRIGHT_MAX_CONTEXTS": 5,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 5,

        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },

        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
        }
    }

    process = CrawlerProcess(settings=custom_settings)
    process.crawl(PcImageSpider)
    process.start()

if __name__ == "__main__":
    run_scraper()