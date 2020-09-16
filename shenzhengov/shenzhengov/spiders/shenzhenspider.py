# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from shenzhengov.items import ShenzhengovItem
from scrapy.selector import Selector
import re


class ShenzhenSpider(CrawlSpider):
    name = 'shenzhenspider'
    allowed_domains = ['sz.gov.cn']
    start_urls = ['http://sz.gov.cn/']

    rules = (
        # 政务动态
        Rule(LinkExtractor(allow=r'/cn/xxgk/zfxxgj/zwdt/(.*?).htm'), callback='parse_item', follow=True),
        # 部门动态
        Rule(LinkExtractor(allow=r'/cn/xxgk/zfxxgj/bmdt/(.*?).htm'), callback='parse_item', follow=True),
        # 各区动态
        Rule(LinkExtractor(allow=r'/cn/xxgk/zfxxgj/gqdt/(.*?).htm'), callback='parse_item', follow=True),
        # 便民提醒
        Rule(LinkExtractor(allow=r'/cn/xxgk/bmtx/(.*?).htm'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        link_list = ['http://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/',
                     'http://www.sz.gov.cn/cn/xxgk/zfxxgj/bmdt/',
                     'http://www.sz.gov.cn/cn/xxgk/zfxxgj/gqdt/',
                     'http://www.sz.gov.cn/cn/xxgk/bmtx/']

        for url in link_list:
            yield self.make_requests_from_url(url)

    def parse_start_url(self, response):
        """列表页"""
        print('列表页url:%s' % response.url)

        # 下一页
        for i in range(0, 51):
            link_url = 'index_{0}.htm'.format(i)
            if i == 0:
                next_url = response.url
            else:
                next_url = response.urljoin(link_url)
            yield scrapy.Request(next_url, callback=self.parse_item)

    def parse_item(self, response):
        item = ShenzhengovItem()

        title = response.xpath('//div[@class="tit"]/h1/text()').extract_first()
        if title:
            item['title'] = title.strip()

        time = response.xpath('//div[@class="tit"]/h6/span[2]/text()').extract_first()
        if time:
            item['time'] = time.split('：')[1]

        item['url'] = response.url

        content = "".join(response.xpath('//div[@class="news_cont_d_wrap"]/div/p/text()').extract())
        if content:
            item['content'] = content.replace('\t', '').replace('\u3000', '').replace('\n', '').replace('\xa0', '')

        print(item, "----")
        yield item
