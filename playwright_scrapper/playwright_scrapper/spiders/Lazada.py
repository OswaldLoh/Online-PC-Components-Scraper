import scrapy
from scrapy_playwright.page import PageMethod

class LazadaSpider(scrapy.Spider):
    name = "Lazada"
    allowed_domains = ["www.lazada.com.my"]
    start_urls = ["https://www.lazada.com.my/"]

    def start_requests(self):
        url = "https://www.lazada.com.my/"

        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".card-jfy-item-desc")
                ],
            }
        )

    def parse(self, response):
        products = response.css(".card-jfy-item-desc")

        for product in products:
            name = product.css("::text").get()

            if name:
                yield {"title": name.strip()}