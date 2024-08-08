import json
from typing import Iterable

from scrapy import Spider, Request
from scrapy.http import HtmlResponse

from scrFruit.items import ScrFruitItem

BODY = {
    "page": 0,
    "pageSize": "10000"
}

BASE_URL = ("https://lc-events-web-public.ifema.es/api/v1/tenants/3a88c5e5-a6e1-4898-b72b-103e4eed1731/editions"
            "/89eac643-8259-4a90-160a-08dbe9c30491/exhibitors/{}?language=es-ES")


class FruitsSpider(Spider):
    name = 'fruits'
    start_urls = [
        'https://lc-events-web-public.ifema.es/api/v1/tenants/3a88c5e5-a6e1-4898-b72b-103e4eed1731/editions/89eac643'
        '-8259-4a90-160a-08dbe9c30491/exhibitors/search?language=es-ES'
    ]

    def start_requests(self) -> Iterable[Request]:
        yield Request(
            url=self.start_urls[0], method='POST', body=json.dumps(BODY),
            callback=self.parse, dont_filter=True
        )

    def parse(self, response: HtmlResponse, **__) -> None:
        # Items en `data`
        items = response.json()['data']

        # Por cada item extraemos sus datos y los de su parent, si tiene
        for item in items:
            # Datos del item
            _id = item['id']

            yield Request(
                url=BASE_URL.format(_id), callback=self.parse_item, cb_kwargs={'email': item['email']}
            )

    @staticmethod
    def parse_item(response: HtmlResponse, email: str = None) -> None:
        yield ScrFruitItem(**response.json(), email=email)
