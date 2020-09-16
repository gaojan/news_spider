# -*- coding: utf-8 -*-
import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class ChengduSpider(BaseSpider):
    name = 'chengdu'
    allowed_domains = ['chengdu.gov.cn']
    start_urls = ['http://www.chengdu.gov.cn/es-search/search/17b0921ed7834c66aa970471b5f6315f?_isAgg=0&_pageSize'
                  '=1000&_template=chengdu_list&_channelName=%E6%96%B0%E9%97%BB&_allNum=0&page={}']

    def start_requests(self):
        for page in range(1, 2):
            url = "".join(self.start_urls).format(page)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.xpath('//ul[@class="list"]/li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        title = response.xpath('//title/text()').extract()
        if not title:
            item['title'] = ''
        else:
            item['title'] = "".join(title)

    def parse_time(self, response, item):
        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first().strip()

    def parse_content(self, response, item):
        content_list = response.xpath('//div[@class="text_content"]//text()').extract()
        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)
