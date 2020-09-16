# -*- coding: utf-8 -*-

import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class ShenzhenSpider(BaseSpider):
    name = 'shenzhen'
    allowed_domains = ['sz.gov.cn']
    start_urls = ['http://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/%s',
                  'http://www.sz.gov.cn/cn/xxgk/zfxxgj/bmdt/%s',
                  'http://www.sz.gov.cn/cn/xxgk/zfxxgj/gqdt/%s',
                  'http://www.sz.gov.cn/cn/xxgk/bmtx/%s']

    def start_requests(self):

        for start_url in self.start_urls:
            links = [start_url % m for m in ['index.htm'] + ['index_%s.htm' % n for n in range(1, 21)]]
            for url in links:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.xpath('//*[@id="top_bg"]/div/div[4]/div[2]/ul/li[position()>1]/span[2]/a/@href').extract()
        for u in urls:
            url = response.url.split('/index')[0] + u.split('.', 1)[1]
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
        content_list = response.xpath('//*[@id="top_bg"]/div[1]/div[4]/div[2]/div[2]/div/p/text()|'
                                      '//div[@class="TRS_Editor"]/div/p/text()|'
                                      '//div[@class="TRS_Editor"]/div/p/span/text()|'
                                      '//div[@class="TRS_Editor"]/div/text()|'
                                      '//div[@class="TRS_Editor"]/div/div/text()|'
                                      '//div[@class="TRS_Editor"]//p/span/text()|'
                                      '//*[@id="jovtecDetail_gbmxxgk"]/p/text()').extract()

        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)


