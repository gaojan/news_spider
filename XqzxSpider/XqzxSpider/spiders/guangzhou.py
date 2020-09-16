# -*- coding: utf-8 -*-

import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class GuangzhouSpider(BaseSpider):
    name = 'guangzhou'
    allowed_domains = ['gz.gov.cn']
    base_url = 'http://www.gz.gov.cn'
    start_urls = ['http://www.gz.gov.cn/gzgov/s2342/xw_list%s',        # 广州要闻
                  'http://www.gz.gov.cn/gzgov/s2344/xw_gqdt_list%s',   # 各区动态
                  'http://www.gz.gov.cn/gzgov/s2345/xw_bmdt_list%s',   # 部门动态
                  'http://www.gz.gov.cn/gzgov/gsgg/xw_list%s',         # 通知公告
                  'http://www.gz.gov.cn/gzgov/jrgz/xw_list%s']         # 今日关注

    def start_requests(self):
        for start_url in self.start_urls:
            urls = [start_url % m for m in ['.shtml'] + ['_%s.shtml' % n for n in range(2, 10)]]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """列表页"""
        urls = response.xpath('//div[@class="news-list"]/ul/li/a/@href|'
                              '//div[@class="news-list gqdt_newslist"]/ul/li/a/@href|'
                              '//div[@class="news-list bmdt_newslist"]/ul/li/a/@href').extract()
        for link in urls:
            if self.base_url not in link:
                url = self.base_url + link.split('..')[-1]
                yield scrapy.Request(url, callback=self.parse_item)
            else:
                yield scrapy.Request(link, callback=self.parse_item)

    def parse_title(self, response, item):
        title = response.xpath('//meta[@name="ArticleTitle"]/@content|'
                               '//div[@class="news-info"]/h1/text()').extract_first()
        if not title:
            title = response.xpath('//title/text()').extract_first()
            item['title'] = "".join(title.split('-')[-1:])
        else:
            item['title'] = title.strip()

    def parse_time(self, response, item):
        item['time'] = response.xpath('//div[@class="news-info"]/div[2]/span[1]/text()|'
                                      '//div[@class="news-info"]/div[1]/span[1]/text()|'
                                      '//span[@class="time"]/text()').extract_first()
        if not item['time']:
            item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first()

    def parse_content(self, response, item):
        content_list = response.xpath('//*[@id="zoomcon"]//text()').extract()

        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)
