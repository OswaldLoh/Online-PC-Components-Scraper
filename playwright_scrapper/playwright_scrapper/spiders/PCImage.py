import scrapy


class PcimageSpider(scrapy.Spider):
    name = "PCImage"
    allowed_domains = ["www.store.pcimage.com.my"]
    start_urls = ["https://www.store.pcimage.com.my/pc-component"]

    def parse(self, response):
        products = response.css("div.frame")
        for product in products:
            title = product.css(".product-name a::text").get()
            price = product.css(".price-new::text").get()
            if title:
                clean_title = title.strip()
                yield {
                    "title": clean_title,
                    "price": price
                }



