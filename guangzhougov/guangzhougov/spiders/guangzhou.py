# -*- coding: utf-8 -*-

import logging
import re
import datetime
import scrapy
from guangzhougov.settings import MAXDATE
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from guangzhougov.items import GuangzhougovItem


class GuangzhouSpider(scrapy.Spider):
    name = 'guangzhou'
    allowed_domains = ['gz.gov.cn']
    base_url = 'http://www.gz.gov.cn'
    start_urls = ['http://www.gz.gov.cn/gzgov/s2342/xw_list%s',        # 广州要闻
                  'http://www.gz.gov.cn/gzgov/s2344/xw_gqdt_list%s',   # 各区动态
                  'http://www.gz.gov.cn/gzgov/s2345/xw_bmdt_list%s',   # 部门动态
                  'http://www.gz.gov.cn/gzgov/gsgg/xw_list%s',         # 通知公告
                  'http://www.gz.gov.cn/gzgov/jrgz/xw_list%s']         # 今日关注

    def start_requests(self):
        for start_url in self.start_urls:
            urls = [start_url % m for m in ['.shtml'] + ['_%s.shtml' % n for n in range(2, 10)]]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    @staticmethod
    def string_toDatetime(string):
        """时间字符串转datetime"""
        return datetime.datetime.strptime(string.split(' ')[0] + ' 00:00:00', '%Y-%m-%d %H:%S:%M')

    def scheduler_date(self):
        """设置时间过滤"""
        t = datetime.datetime.now() - datetime.timedelta(days=MAXDATE)
        toStr = t.strftime('%Y-%m-%d')
        return self.string_toDatetime(toStr)

    def parse(self, response):
        """列表页"""
        item = GuangzhougovItem()

        node_list = response.xpath('//div[@class="news-list"]/ul/li|'
                                   '//div[@class="news-list gqdt_newslist"]/ul/li|'
                                   '//div[@class="news-list bmdt_newslist"]/ul/li')
        for node in node_list:

            item['time'] = node.xpath('./span/text()').extract_first()
            if item['time']:
                if self.string_toDatetime(item['time']) >= self.scheduler_date():

                    title = node.xpath('./a/text()').extract_first()
                    item['title'] = title.strip().replace('\r', '')

                    url = node.xpath('./a/@href').extract_first()
                    if self.base_url not in url:
                        link = url.split('..')[-1]
                        item['url'] = self.base_url + link
                    else:
                        item['url'] = url

                    yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'meta': item})
                else:
                    return None
            else:
                return None

    def parse_detail(self, response):
        """详情页"""
        temp = response.meta['meta']

        content = "".join(response.xpath('//*[@id="zoomcon"]//text()').extract()).strip()

        # pattern = re.compile(r'\S')
        # if not pattern.findall(content):
        #     return None
        # else:
        if content:
            temp['content'] = content.replace('\t', '').replace('\u3000', '').replace('\n', '').replace('\xa0', '').replace('\r', '')

        item = temp
        print(item, "-----")
        yield item
