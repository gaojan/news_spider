# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DongmanItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
