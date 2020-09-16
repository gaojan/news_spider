# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from SinaRealTimeHot.items import SinarealtimehotItem


class RealtimehotSpider(scrapy.Spider):
    name = 'realtimehot'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/top/summary?cate=realtimehot']

    def parse(self, response):
        nodes = response.xpath('//div[@id="pl_top_realtimehot"]/table/tbody/tr')
        for node in nodes:
            item = SinarealtimehotItem()
            url = node.xpath('//td[@class="td-02"]/a/@href').extract_first()
            keyword = node.xpath('./td[@class="td-02"]/a/text()').extract_first()
            keyword_heat = node.xpath('./td[@class="td-02"]/span/text()').extract_first()

            item['url'] = urljoin(response.url, url)
            item['keyword'] = keyword.strip()
            item['keyword_heat'] = keyword_heat
            yield item

