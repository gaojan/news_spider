# -*- coding: utf-8 -*-
import scrapy
import time
from ChengDuGOV.items import ChengdugovItem


class ChengduSpider(scrapy.Spider):
    name = 'chengdu'
    allowed_domains = ['chengdu.gov.cn']
    start_urls = ['http://www.chengdu.gov.cn/es-search/search/17b0921ed7834c66aa970471b5f6315f?_isAgg=0&_pageSize'
                  '=1000&_template=chengdu_list&_channelName=%E6%96%B0%E9%97%BB&_allNum=0&page=1']
    TIME_FORMAT = '%Y-%m-%d'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        nodes = response.xpath('//ul[@class="list"]/li')
        for node in nodes:
            time_str = node.xpath('./span/text()').extract_first()
            if self.check_time(time_str, self.TIME_FORMAT):  # 如果在需要爬取时间内爬取
                detail_url = node.xpath('./a/@href').extract_first()
                yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = ChengdugovItem()
        item['title'] = response.xpath('//title/text()').extract_first()
        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first()
        item['url'] = response.url
        content_list = response.xpath('//div[@class="text_content"]//text()').extract()
        content = "".join(content_list)
        content = content.replace("\r\n", "").replace("\n", "").replace("\t", "").replace("\xa0", "")
        item['content'] = content
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
    
    
