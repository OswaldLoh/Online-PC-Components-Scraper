import scrapy


class PcimageSpider(scrapy.Spider):
    name = "PCImage"
    allowed_domains = ["www.store.pcimage.com.my"]
    start_urls = ["https://www.store.pcimage.com.my/pc-component"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.store.pcimage.com.my/pc-component",
            meta={
                "playwright":True,
                "playwright_include_page": True,
            }
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page_count = 1
        max_page = 5

        try:
            while page_count <= max_page:
                self.logger.info(f"Scraping page {page_count}")
                html = await page.content()
                selector = scrapy.Selector(text=html)

                for card in selector.css("div.frame"):
                    title = card.css(".product-name a::text").get()
                    price = card.css(".price-new::text").get()
                    if title:
                        clean_title = title.strip()
                        yield {
                            "title": clean_title,
                            "price": price
                        }
                next_button = page.locator("div.links a.beh_pagination").nth(-2)

                if await next_button.count() > 0 and not await next_button.get_attribute("disabled"):
                    await next_button.click(force=True)
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(2000)
                    page_count += 1
                else:
                    self.logger.info("No more pages")
                    break
        finally:
            await page.close()



