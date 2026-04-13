import scrapy


class PcImageSpider(scrapy.Spider):
    name = "PCImage"
    allowed_domains = ["www.store.pcimage.com.my"]
    async def start(self):
        yield scrapy.Request(
            url="https://www.store.pcimage.com.my/pc-component",
            meta={
                "playwright": True,
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
                        yield {
                            "title": title.strip(),
                            "price": price
                        }

                pagination = page.locator("div.links a.beh_pagination")
                btn_count = await pagination.count()

                if btn_count >= 2:
                    next_button = pagination.nth(btn_count - 2)
                    is_disabled = await next_button.evaluate("el => el.classList.contains('disabled')")
                    if is_disabled:
                        self.logger.info("Next button is disabled, no more pages")
                        break
                    async with page.expect_navigation():
                        await next_button.click(force=True)
                    # Ensure the new items are visible before looping back
                    await page.wait_for_selector("div.frame", state="visible")
                    page_count += 1
                else:
                    self.logger.info("No more pages")
                    break
        finally:
            await page.close()