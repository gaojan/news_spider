# -*- coding: utf-8 -*-
import scrapy
import time
from youxi.items import YouxiItem


class Game97973Spider(scrapy.Spider):
    name = 'game97973'
    allowed_domains = ['97973.com']
    start_urls = ['http://97973.com/']

    def start_requests(self):
        urls = ['http://top.sina.com.cn/news/show/news/iphone/0',
                'http://top.sina.com.cn/news/show/industry/iphone/0',
                'http://top.sina.com.cn/news/show/news/android/0',
                'http://top.sina.com.cn/news/show/industry/android/0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        nodes = response.xpath('//div[@class="pictxtlist clear"]/ul/li')
        ask_next_page = True
        for node in nodes:
            time_str = node.xpath('./span[@class="fr time"]/text()').extract_first().strip()
            if self.check_time(time_str, '%Y-%m-%d'):
                href = node.xpath('./a[1]/@href').extract_first()
                yield scrapy.Request(url=href, callback=self.parse_detail, meta={'time_str': time_str})
            else:
                ask_next_page = False
        if ask_next_page:
            current_url = response.url
            # 每次加12条
            current_url_split_list = current_url.split('/')
            number = int(current_url_split_list.pop()) + 12
            current_url_split_list.append(str(number))
            next_url = '/'.join(current_url_split_list)
            yield scrapy.Request(url=next_url, callback=self.parse_list, dont_filter=True)

    def parse_detail(self, response):
        item = YouxiItem()
        item['url'] = response.url
        item['time'] = response.meta['time_str']
        title = response.xpath('//title/text()').extract_first()
        if '_' in title:
            title = title.split('_')[0]
        item['title'] = title
        content_list = response.xpath('//div[@id="fonttext"]/p/text()').extract()
        content = '\n'.join(content_list).replace('\u3000', '').replace('\xa0', '')
        item['content'] = content
        yield item

    def check_time(self, time_string, format_string, days_ago=10):
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
