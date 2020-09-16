# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin

from jiankang.items import JiankangItem


class ChunyuyishengSpider(scrapy.Spider):
    name = 'chunyuyisheng'
    allowed_domains = ['chunyuyisheng.com']
    start_urls = ['https://www.chunyuyisheng.com/pc/health_news/?page={}#channel'.format(i) for i in range(1, 4)]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        urls = response.xpath('//ul[@class="health-news-list"]/li/div/a/@href').extract()
        urls = [urljoin(response.url, url) for url in urls]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = JiankangItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').extract_first().strip()[:-5]
        time_str = response.xpath('//p[@class="time"]/text()').extract_first()
        if "小时" in time_str:
            item['create_time'] = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
        else:
            item['create_time'] = (datetime.now() + timedelta(days=-1)).strftime('%Y-')\
                           + time_str.replace("月", "-").replace("日", "")

        content_list = response.xpath('//div[@class="main-wrap"]/div//p/text()').extract()
        item['content'] = "".join(content_list)
        yield item

    def check_time(self, time_string, format_string, days_ago=7):
        """
        是否在规定时间内，days_ago
        :param time_string: [2018-08-22]
        :param format_string: [%Y-%m-%d]
        :param days_ago: int
        :return:
        """
        # 算出时间秒数
        # days_ago = datetime.timedelta(days=days_ago)
        # days_sec = days_ago.total_seconds()
        days_sec = 60 * 60 * 24 * days_ago

        old = time.mktime(time.strptime(time_string, format_string))
        now = time.time()
        if now - old > days_sec:
            return False
        return True
