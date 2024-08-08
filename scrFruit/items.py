# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import html

import scrapy
from bs4 import BeautifulSoup


def remove_tags(html_text: str):
    if not html_text:
        return None

    # Deserializar caracteres HTML
    text_with_decoded_entities = html.unescape(html_text)

    # Eliminar etiquetas HTML
    soup = BeautifulSoup(text_with_decoded_entities, 'html.parser')
    return soup.get_text()


def empty(data):
    return data or None


class ScrFruitItem(scrapy.Item):
    def __init__(self, location: dict = None, **kwargs):
        if location:
            kwargs.update(location)
        # Filtrar kwargs para eliminar claves no definidas en ScrFruitItem
        valid_keys = set(self.fields.keys())
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}
        super(ScrFruitItem, self).__init__(**filtered_kwargs)

    name = scrapy.Field(serializer=empty)
    parentName = scrapy.Field(serializer=empty)
    description = scrapy.Field(serializer=remove_tags)
    email = scrapy.Field(serializer=empty)
    link = scrapy.Field(serializer=empty)
    countryCode = scrapy.Field(serializer=empty)
    region = scrapy.Field(serializer=empty)
    city = scrapy.Field(serializer=empty)
    address = scrapy.Field(serializer=empty)
    postalCode = scrapy.Field(serializer=empty)
