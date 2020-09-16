# -*- coding: utf-8 -*-
import scrapy
import logging
import datetime
import re
from zhengfuwang.settings import MAXDATE
from zhengfuwang.items import ZhengfuwangItem


class ZhengfuSpider(scrapy.Spider):
    name = 'zhengfu'
    allowed_domains = ['gov.cn']
    start_urls = ['http://sousuo.gov.cn/column/{nid}/{page}.htm']
    nid_list = ['19423', '31250', '30565', '30611', '31421', '30613', '30902', '30618']

    # http://sousuo.gov.cn/column/19423/0.htm  国务院新闻
    # http://sousuo.gov.cn/column/31250/0.htm 动态
    # http://sousuo.gov.cn/column/30565/0.htm 总理
    # http://sousuo.gov.cn/column/30611/0.htm  新闻-滚动 3298页
    # http://sousuo.gov.cn/column/31421/{}.htm  新闻-要闻 688页
    # http://sousuo.gov.cn/column/30613/{}.htm  政务联播-部门 983页
    # http://sousuo.gov.cn/column/30902/{}.htm  政务联播-地方 1395页
    # http://sousuo.gov.cn/column/30618/{}.htm  新闻发布-部门

    def start_requests(self):

        for page in range(0, 11):
            urls = ["".join(self.start_urls).format(nid=nid, page=page) for nid in self.nid_list]
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

        news_list = response.xpath('//ul[@class="listTxt"]/li/h4')
        for new in news_list:
            item = ZhengfuwangItem()

            p_time = new.xpath('./span/text()|//div[@class="pages-date"]/text()').extract_first()
            if p_time:
                item['time'] = datetime.datetime.strptime(p_time.strip(), '%Y.%m.%d').strftime('%Y-%m-%d')

                if self.string_toDatetime(item['time']) >= self.scheduler_date():

                    title = new.xpath('./a/text()|//div[@class="article oneColumn pub_border"]/h1/text()').extract_first()
                    if title:
                        item['title'] = title.strip().replace("\xa0", "")

                    item['url'] = new.xpath('./a/@href').extract_first()

                    yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'meta': item})
                else:
                    return None

    def parse_detail(self, response):
        temp = response.meta['meta']

        content = "".join(response.xpath('//*[@class="pages_content"]/p/text()|'
                                         '//*[@id="UCAP-CONTENT"]/p/span/text()|'
                                         '//*[@id="UCAP-CONTENT"]/p/text()|'
                                         '//*[@id="UCAP-CONTENT"]/div[2]/p/text()|'
                                         '//*[@id="UCAP-CONTENT"]/div[2]/text()|'
                                         '//*[@id="printContent"]/tbody/tr/td/p/text()').extract())

        # pattern = re.compile(r'\S')
        # if not pattern.findall(content):
        #     return None
        if content:
            temp['content'] = content.replace("\r", "").replace("\n", "").replace("\t", "").replace("\xa0", "").replace('\u3000', '')

        item = temp
        print(item, "******")
        yield item





