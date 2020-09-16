# -*- coding: utf-8 -*-
import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class NanjingSpider(BaseSpider):
    name = 'nanjing'
    allowed_domains = ['nanjing.gov.cn']
    # 政务要闻、部门动态、各区动态、领导活动、图片新闻、民生资讯、便民提示
    href_ends = ["mjxw", "bmkx", "gqdt", "ldhd", "tpxw", "mszx", "bmts"]
    start_urls = ['http://www.nanjing.gov.cn/xxzx/{}/%s'.format(href_end) for href_end in href_ends]

    def start_requests(self):
        for start_url in self.start_urls:
            urls = [start_url % m for m in ['index.html'] + ['index_%s.html' % n for n in range(1, 10)]]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.xpath('//ul[@class="universal_overview_con"]/li/span[2]/a/@href').extract()
        for u in urls:
            now_url = response.url.split('/index')[0] + u.strip().split('.', 1)[-1]
            yield scrapy.Request(now_url, callback=self.parse_item)

    def parse_title(self, response, item):
        item['title'] = response.xpath('//meta[@name="ArticleTitle"]/@content').extract_first().strip()

    def parse_time(self, response, item):
        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first().strip()

    def parse_content(self, response, item):
        content_list = response.xpath('//div[@class="TRS_Editor"]/p//text()|'
                                      '//div[@class="TRS_Editor"]/div/p//text()|'
                                      '//div[@id="con"]/p/text()').extract()
        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)
