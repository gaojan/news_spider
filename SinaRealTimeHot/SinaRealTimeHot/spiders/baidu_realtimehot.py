# -*- coding: utf-8 -*-
from SinaRealTimeHot.items import BaiduRealtimehotItem
import scrapy


class BaiduRealtimehotSpider(scrapy.Spider):
    name = 'baidu_realtimehot'
    allowed_domains = ['top.baidu.com']
    start_urls = ['http://top.baidu.com/buzz?b=1']

    def parse(self, response):
        nodes = response.xpath('//table[@class="list-table"]/tr[not(@class="item-tr")]')[1:]
        for node in nodes:
            item = BaiduRealtimehotItem()
            keyword = node.xpath('./td[@class="keyword"]/a/text()').extract_first()
            url = node.xpath('./td[@class="keyword"]/a/@href').extract_first()
            keyword_heat = node.xpath('./td[@class="last"]/span/text()').extract_first()
            item['keyword'] = keyword
            item['url'] = url
            item['keyword_heat'] = keyword_heat
            yield item
