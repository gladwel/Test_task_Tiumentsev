from pathlib import Path
import json
import scrapy
import unicodedata


class QuotesSpider(scrapy.Spider):
    name = "sreality"

    def start_requests(self):
        url = 'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response = json.loads(response.body)
        for item in response["_embedded"]["estates"]:
            yield {
                # unicodedata.normalize('NFC', item["name"]) is better but works unstable
                'title': item["name"].replace('\xa0', ' '),
                'image_url': item["_links"]["images"][0]["href"]
            }