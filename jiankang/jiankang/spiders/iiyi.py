# -*- coding: utf-8 -*-
import scrapy
from jiankang.items import JiankangItem


class IiyiSpider(scrapy.Spider):
    name = 'iiyi'
    allowed_domains = ['iiyi.com']
    start_urls = ['https://article.iiyi.com/hot/{}.html'.format(i) for i in range(1, 6)]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        url_list = response.xpath('//div[@class="article_lists"]/div[@class="li"]/div/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = JiankangItem()
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="top"]/h1/text()').extract_first()
        time_str = response.xpath('//div[@class="top"]/span/var/text()').extract_first()
        item['create_time'] = time_str.split('　')[0]
        content_list = response.xpath('//div[@class="cont"]//span/text()|'
                                      '//div[@class="cont"]//p/text()').extract()
        item['content'] = "".join(content_list)
        yield item
