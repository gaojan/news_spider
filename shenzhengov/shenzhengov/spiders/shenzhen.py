# -*- coding: utf-8 -*-
import datetime
import scrapy
import logging
import re
from shenzhengov.settings import MAXDATE
from shenzhengov.items import ShenzhengovItem
# from scrapy_redis.spiders import RedisSpider


class ShenzhenSpider(scrapy.Spider):
    name = 'shenzhen'
    allowed_domains = ['sz.gov.cn']
    start_urls = ['http://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/%s',
                  'http://www.sz.gov.cn/cn/xxgk/zfxxgj/bmdt/%s',
                  'http://www.sz.gov.cn/cn/xxgk/zfxxgj/gqdt/%s',
                  'http://www.sz.gov.cn/cn/xxgk/bmtx/%s']

    def start_requests(self):

        for start_url in self.start_urls:
            links = [start_url % m for m in ['index.htm'] + ['index_%s.htm' % n for n in range(1, 21)]]
            for url in links:
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

        nodelist = response.xpath('//*[@id="top_bg"]/div/div[4]/div[2]/ul/li[position()>1]')
        res_url = response.url.split('/index')[0]

        for node in nodelist:
            item = ShenzhengovItem()

            str_time = node.xpath('./span[3]/text()').extract_first()
            if str_time:
                item['time'] = datetime.datetime.strptime(str_time, '%Y年%m月%d日').strftime('%Y-%m-%d')
                # 如果发布时间大于规定的时间，则继续爬去
                if self.string_toDatetime(item['time']) >= self.scheduler_date():

                    title = node.xpath('./span[2]/a/text()').extract_first()
                    item['title'] = title.strip().replace('\u3000', '').replace('\xa0', '')

                    url = node.xpath('./span[2]/a/@href').extract_first()
                    item['url'] = res_url + url.split('.', 1)[1]

                    yield scrapy.Request(item['url'], callback=self.get_content, meta={'meta': item})
                else:
                    return None

    def get_content(self, response):
        """详情页"""
        temp = response.meta['meta']
        content = "".join(response.xpath('//*[@id="top_bg"]/div[1]/div[4]/div[2]/div[2]/div/p/text()').extract()).strip()
        # pattern = re.compile(r'\S')
        # if not pattern.findall(content):
        #     return None
        # else:
        if content:
            temp['content'] = content.replace('\t', '').replace('\u3000', '').replace('\n', '').replace('\xa0', '')

        item = temp
        print(item, "------")
        yield item
