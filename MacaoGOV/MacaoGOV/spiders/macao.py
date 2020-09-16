# -*- coding: utf-8 -*-
import scrapy
import time

from MacaoGOV.items import MacaogovItem


class MacaoSpider(scrapy.Spider):
    name = 'macao'
    allowed_domains = ['gov.mo']
    start_urls = ['http://gov.mo/']
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def start_requests(self):
        url = 'https://www.gov.mo/zh-hant/news/'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        nodes = response.xpath('//div[@class="col-sm-8 col-lg-7 content-block"]/div[@class="row"]')
        next_page = True
        for node in nodes:
            time_str = node.xpath('./div/aside/dl/dd/time[@class="date"]/@datetime').extract_first()
            print(time_str)
            if self.check_time(time_str, self.TIME_FORMAT):
                detail_url = node.xpath('./div/h2/a/@href').extract_first()
                print(detail_url)
                yield scrapy.Request(url=detail_url, callback=self.parse_detail)
            else:
                next_page = False
        if next_page:
            next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_detail(self, response):
        item = MacaogovItem()
        item['time'] = response.xpath('//aside[@class="metadata-list"]/dl/dd/time[@class="date"]/@datetime').extract_first()
        item['title'] = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        item['url'] = response.url
        content_list = response.xpath('//div[@class="container"]/div/div[1]/div[3]/p/text()').extract()
        item['content'] = "".join(content_list)
        yield item

    def check_time(self, time_string, format_string, days_ago=7):
        """
        是否在规定时间内，days_ago
        :param time_string: [2018-08-22]
        :param format_string: [%Y-%m-%d]
        :param days_ago: int
        :return:
        """
        # 算出时间秒数
        # days_ago = datetime.timedelta(days=days_ago)
        # days_sec = days_ago.total_seconds()
        days_sec = 60 * 60 * 24 * days_ago

        old = time.mktime(time.strptime(time_string, format_string))
        now = time.time()
        if now - old > days_sec:
            return False
        return True
