# -*- coding: utf-8 -*-
import scrapy
import logging
import datetime
import re
from tianjingov.settings import MAXDATE
from tianjingov.items import TianjingovItem


class TianjinSpider(scrapy.Spider):
    name = 'tianjin'
    allowed_domains = ['tj.gov.cn']
    start_urls = ['http://www.tj.gov.cn/xw/bdyw/%s',    # 天津新闻
                  'http://www.tj.gov.cn/xw/bum/%s',     # 部门动态
                  'http://www.tj.gov.cn/xw/qx1/%s']     # 各区动态

    def start_requests(self):
        for url in self.start_urls:
            links = [url % m for m in ['index.html'] + ['index_%s.html' % n for n in range(1, 11)]]
            for link in links:
                yield scrapy.Request(link, callback=self.parse, dont_filter=True)

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

        node_list = response.xpath('//div[@class="left leftlist"]/div[2]/ul/li')
        for node in node_list:
            item = TianjingovItem()

            time = node.xpath('./span/text()').extract_first()
            if time:
                item['time'] = time.strip()
                # 如果发布时间大于规定的时间，则继续爬去
                if self.string_toDatetime(item['time']) >= self.scheduler_date():

                    title = node.xpath('./a/text()').extract_first()
                    item['title'] = title.strip().replace('\xa0', '').replace('\u3000', '')

                    url = node.xpath('./a/@href').extract_first()
                    item['url'] = response.url.split('index')[0] + url.split('./')[1]

                    yield scrapy.Request(item['url'], callback=self.parse_content, meta={'meta': item})
                else:
                    return None

    def parse_content(self, response):

        temp = response.meta['meta']
        content = "".join(response.xpath('//*[@id="zoom"]/div/p/text()|//*[@id="zoom"]/div/div/p/text()').extract())
        # pattern = re.compile(r'\S')
        # if not pattern.findall(content):
        #     return None
        # else:
        if content:
            temp['content'] = content.replace('\t', '').replace('\u3000', '').replace('\n', '').replace('\xa0', '')

        item = temp
        print(item, '-----')
        yield item
