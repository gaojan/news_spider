# -*- coding: utf-8 -*-
import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class ChongqingSpider(BaseSpider):
    name = 'chongqing'
    allowed_domains = ['cq.gov.cn']
    start_urls = ['http://www.cq.gov.cn/zwxx/{nid}_{page}']
    nid_list = ['jrcq', 'zwdt', 'tpxw']

    """
    http://www.cq.gov.cn/zwxx/jrcq_2  今日重庆
    http://www.cq.gov.cn/zwxx/zwdt_2  政务活动
    http://www.cq.gov.cn/zwxx/tpxw_2  图片新闻
    """

    def start_requests(self):
        for page in range(1, 5):
            urls = [''.join(self.start_urls).format(nid=nid, page=page) for nid in self.nid_list]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """列表页"""
        urls = response.xpath('//div[@class="border"]/ul/li/a/@href').extract()
        for u in urls:
            url = "http://www.cq.gov.cn" + u
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        title = response.xpath('//meta[@name="ArticleTitle"]/@content').extract()
        if not title:
            item['title'] = ''
        else:
            item['title'] = "".join(title).strip()

    def parse_time(self, response, item):
        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first()

    def parse_content(self, response, item):
        content_list = response.xpath('//div[@class="conTxt"]/p/text()|'
                                      '//div[@class="conTxt"]/p/span/text()|'
                                      '//div[@class="conTxt"]/p/span/span/text()').extract()
        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)
