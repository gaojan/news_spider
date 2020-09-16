# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinarealtimehotItem(scrapy.Item):
    """sina热度"""
    keyword = scrapy.Field()
    url = scrapy.Field()
    mobile_url = scrapy.Field()
    keyword_heat = scrapy.Field()


class BaiduRealtimehotItem(scrapy.Item):
    """baidu热度"""
    keyword = scrapy.Field()
    url = scrapy.Field()
    keyword_heat = scrapy.Field()
