# -*- coding: utf-8 -*-
import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class BeijingSpider(BaseSpider):
    name = 'beijing'
    allowed_domains = ['beijing.gov.cn']
    start_urls = ['http://www.beijing.gov.cn/sy/zwyw/%s',
                  'http://zhengwu.beijing.gov.cn/yw/%s',
                  'http://zhengwu.beijing.gov.cn/gzdt/%s',
                  'http://zhengwu.beijing.gov.cn/gqrd/%s',
                  'http://www.beijing.gov.cn/sy/jrbj/%s',
                  'http://www.beijing.gov.cn/sy/rdgz/%s',
                  'http://renwen.beijing.gov.cn/sy/whkb/%s']

    def start_requests(self):
        for url in self.start_urls:
            links = [url % m for m in ['default.htm'] + ['default_%s.htm' % n for n in range(1, 6)]]
            for link in links:
                yield scrapy.Request(link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.xpath("//ul[@class='list']/li/a/@href").extract()
        for u in urls:
            if "http://" not in u:
                url = response.url.split('default')[0] + u.split('./')[1]
                yield scrapy.Request(url, callback=self.parse_item)
            else:
                url = u.strip()
                yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        title = response.xpath('//title/text()').extract_first()
        # '//div[@class="content_text"]/h1/text()|'
        # '//*[@id="title_tex"]/text()|'
        # '//div[@class="main"]/h1/text()|'
        # '//div[@class="right fr"]/h1/text()|'
        # '//*[@id="othermessage"]/h1/text()'

        if not title:
            item['title'] = ''
        else:
            item['title'] = title.strip().split('-', 1)[0]

    def parse_time(self, response, item):
        p_time = response.xpath('//*[@id="othermessage"]/p/span[2]/text()|'
                                '//div[@class="main"]/p/text()|'
                                '//p[@class="time"]/text()|'
                                '//div[@class="zc_jdtit"]/p/span[2]/text()').extract_first()
        if not p_time:
            item['time'] = response.xpath('//meta[@name="publishdate"]/@content').extract_first()
        else:
            if len(p_time.split(' ')) <= 2:
                item['time'] = p_time.split('：')[1]
            if len(p_time.split(' ')) >= 3:
                item['time'] = p_time.split()[0] + ' ' + p_time.split()[1]

    def parse_content(self, response, item):
        content_list = response.xpath('//div[@class="artical"]/p/text()|'
                                      '//*[@id="div_zhengwen"]//text()|'
                                      '//*[@id="tex"]/text/text()').extract()

        if not content_list:
            item['content'] = ''
        else:
            content = [content for content in content_list if '原标题' not in content]
            item['content'] = self.content_to(content)

