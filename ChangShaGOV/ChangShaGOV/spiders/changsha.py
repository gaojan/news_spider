# -*- coding: utf-8 -*-
import scrapy
import time

from ChangShaGOV.items import ChangshagovItem
from urllib.parse import urljoin


class ChangshaSpider(scrapy.Spider):
    name = 'changsha'
    allowed_domains = ['changsha.gov.cn']
    TIME_FORMAT = '%Y-%m-%d'
    start_urls = ['http://www.changsha.gov.cn/xxgk/szfxxgkml/gzdt/bmdt/index.html',  # 部门动态
                  'http://www.changsha.gov.cn/xxgk/szfxxgkml/gzdt/zwdt/index.html',  # 政务动态
                  'http://www.changsha.gov.cn/xxgk/szfxxgkml/gzdt/qsxdt/index.html',  # 区市县动态
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        nodes = response.xpath('//div[@class="news_box"]/div[1]/ul/li/h4')
        is_next_page = True
        for node in nodes:
            time_str = node.xpath('./span/text()').extract_first()
            if self.check_time(time_str, self.TIME_FORMAT):
                url = node.xpath('./a/@href').extract_first()
                url = urljoin(response.url, url)
                yield scrapy.Request(url=url, callback=self.parse_detail)
            else:
                is_next_page = False
        if is_next_page:
            next_page_url = self.get_next_page_url(response.url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_list)

    def parse_detail(self, response):
        item = ChangshagovItem()
        item['url'] = response.url
        node = response.xpath('//div[@class="article oneColumn pub_border"]')
        item['title'] = node.xpath('./h1/text()').extract_first().strip("\n").strip(" ").strip("\n")
        item['time'] = node.xpath('./div[@class="pages-date"]//text()').extract_first()
        content_list = response.xpath('//div[@class="TRS_PreAppend"]/span/p//text()|'
                                      '//div[@class="pages_content"]/span//text()').extract()
        if not content_list:
            content_list = node.xpath('./div[@class="pages_content"]//p//text()').extract()
        # if not content_list:
        #     content_list = node.xpath('//div[@id="UCAP-CONTENT"]/text()').extract()
        if not content_list:
            content_list = node.xpath('//div[@id="UCAP-CONTENT"]/div/text()|'
                                      '//div[@id="UCAP-CONTENT"]/text()').extract()
        if not content_list:
            content_list = node.xpath('//div[@id="UCAP-CONTENT"]/span//text()').extract()

        content_list = [content.replace('\u3000', '').replace('\xa0', '') for content in content_list]
        content = ''.join(content_list)
        item['content'] = content
        yield item

    def get_next_page_url(self, old_url):
        if "index.html" in old_url:
            # url = '/'.join(old_url.split('/')[:-1].append('index_1.html'))
            url = old_url[:-10] + 'index_1.html'
        else:
            start, end = old_url.split('_')
            end = int(end.split('.')[0])+1
            url = start + '_' + str(end) + '.html'
        return url

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
