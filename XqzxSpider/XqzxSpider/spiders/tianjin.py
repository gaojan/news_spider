# -*- coding: utf-8 -*-

import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class TianjinSpider(BaseSpider):
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

    def parse(self, response):
        urls = response.xpath('//div[@class="left leftlist"]/div[2]/ul/li/a/@href').extract()
        for u in urls:
            url = response.url.split('index')[0] + u.split('./')[1]
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        title = response.xpath('//div[@class="title"]/text()').extract()
        if not title:
            item['title'] = ''
        else:
            item['title'] = "".join(title).strip()

    def parse_time(self, response, item):
        t_time = response.xpath('//div[@class="time xwlc pd"]/span[2]/text()').extract()
        time = t_time[0].split('：')[1].split(' ')
        item['time'] = time[0]+' '+time[-1]

    def parse_content(self, response, item):
        content_list = response.xpath('//*[@id="zoom"]/div/p/text()|'
                                      '//*[@id="zoom"]/div/text()|'
                                      '//*[@id="zoom"]/div/div/text()|'
                                      '//*[@id="zoom"]/div/p/span/text()|'
                                      '//*[@id="zoom"]/div/div/p/text()|'
                                      '//*[@id="zoom"]/div/div/div/p/text()|'
                                      '//*[@id="zoom"]/div/p/font/text()').extract()
        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)

