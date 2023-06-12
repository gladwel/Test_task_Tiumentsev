import json
import scrapy
# from pathlib import Path - used for saving request to flats.json


class QuotesSpider(scrapy.Spider):
    name = "sreality"

    def start_requests(self):
        url = 'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response = json.loads(response.body)
        for item in response["_embedded"]["estates"]:
            yield {
                'title': item["name"].encode('latin1').decode('utf8'),
                'image_url': item["_links"]["images"][0]["href"]
            }