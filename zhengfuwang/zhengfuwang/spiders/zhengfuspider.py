# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zhengfuwang.items import ZhengfuwangItem
from datetime import datetime


class ZhengfuspiderSpider(CrawlSpider):
    name = 'zhengfuspider'
    allowed_domains = ['gov.cn']
    # start_urls = ['http://gov.cn/']
    start_urls = ['http://sousuo.gov.cn/column/31421/0.htm']

    rules = [
        Rule(LinkExtractor(allow=r'column/(\d+)/(\d+)\.htm'), follow=True),
        Rule(LinkExtractor(allow=r'xinwen/(\d+)-(\d+)/(\d+)/content_(\d+)\.htm'), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        print(response.url, "-----")
        item = ZhengfuwangItem()
        self.get_title(response, item)
        self.get_url(response, item)
        self.get_content(response, item)
        self.get_time(response, item)
        print(item, "------")
        yield item

    @staticmethod
    def get_title(response, item):
        title = response.xpath(
            '//div[@class="article oneColumn pub_border"]/h1/text()|//div[@class="article-colum"]/div[1]/text()'
        ).extract_first()
        if title:
            item['title'] = title.strip()

    @staticmethod
    def get_url(response, item):
        new_url = response.url
        if response.url:
            item['url'] = new_url

    @staticmethod
    def get_content(response, item):
        content = "".join(response.xpath(
            '//*[@class="pages_content"]/p/text()|//*[@id="UCAP-CONTENT"]/p/span/text()|'
            '//*[@class="pages_content"]/table/tr/td/p/text()|//*[@id="printContent"]/tr/td/p/text()'
        ).extract())
        item['content'] = content.strip()

    @staticmethod
    def get_time(response, item):
        pub_date = response.xpath(
            '//div[@class="pages-date"]/text()'
        ).extract_first()
        if pub_date:
            item['time'] = pub_date.strip()
        else:
            item['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
