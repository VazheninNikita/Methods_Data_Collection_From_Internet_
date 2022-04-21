# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import Compose, MapCompose, TakeFirst


def convert_price(value):
    value = value.replace('\xa0', '')
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        return value
    return value


def parse_value(data):
    for num, elem in enumerate(data):
        elem = elem.strip()
        data[num] = elem
    return data


def parse_category_name(category_name):
    name = re.search(r"(?<=([']\b))(?:(?=(\\?))\2.)*?(?=\1)", category_name.get())
    if name is None:
        return category_name.get()
    else:
        name = name.group()
        return name


class CastoramaItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(input_processor=MapCompose(parse_category_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    attribute_label = scrapy.Field(input_processor=Compose(parse_value))
    attribute_value = scrapy.Field(input_processor=Compose(parse_value))
    photos = scrapy.Field()
    _id = scrapy.Field()
    specifications = scrapy.Field()
