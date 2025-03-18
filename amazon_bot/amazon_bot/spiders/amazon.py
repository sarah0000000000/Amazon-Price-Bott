import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.fr"]
    start_urls = ["https://amazon.fr"]

    def parse(self, response):
        pass
