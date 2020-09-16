# -*- coding: utf-8 -*-

import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class ZhengfuSpider(BaseSpider):
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

    def parse(self, response):

        url_list = response.xpath('//ul[@class="listTxt"]/li/h4/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        title = response.xpath('//title/text()').extract_first()
        if not title:
            item['title'] = ''
        else:
            item['title'] = title.strip().split('_')[0]

    def parse_time(self, response, item):
        p_time = response.xpath('//div[@class="pages-date"]/text()').extract_first()
        item['time'] = p_time.strip()

    def parse_content(self, response, item):
        content_list = response.xpath('//*[@class="pages_content"]/p/text()|'
                                      '//*[@id="UCAP-CONTENT"]/p/span/text()|'
                                      '//*[@id="UCAP-CONTENT"]/p/text()|'
                                      '//*[@id="UCAP-CONTENT"]/div[2]/p/text()|'
                                      '//*[@id="UCAP-CONTENT"]/div[2]/text()|'
                                      '//*[@id="UCAP-CONTENT"]//p/text()|'
                                      '//*[@id="printContent"]/tbody/tr/td/p/text()').extract()
        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)
