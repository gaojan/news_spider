# -*- coding: utf-8 -*-
import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class NanningSpider(BaseSpider):
    name = 'nanning'

    custom_settings = {
        'DOWNLOAD_DELAY': 5
    }

    allowed_domains = ['nanning.gov.cn']
    # 南宁要闻、部门动态、县区动态、图片新闻、视频报道、公共公示、领导活动、政府会议、温馨提示（视频报道spxw 无文字已去掉）
    url_ends = ['jrnn/2018nzwdt', 'bmdt', 'xqdt', 'tpxw', 'gggs', 'ldhd', 'zfhy', 'wxts']
    start_urls = ['http://www.nanning.gov.cn/NNNews/{}/%s'.format(url_end) for url_end in url_ends]

    def start_requests(self):
        for start_url in self.start_urls:
            urls = [start_url % m for m in ['index.html'] + ['index_%s.html' % n for n in range(1, 4)]]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        url_list = response.xpath('//div[@class="list_show"]/ul/li/a/@href').extract()
        for link in url_list:
            url = response.url.split('/index')[0] + link.split('.', 1)[-1]
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        item['title'] = response.xpath('//title/text()').extract_first()

    def parse_time(self, response, item):
        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first().strip()

    def parse_content(self, response, item):
        content_list = response.xpath('//div[@id="content"]/div/p/text()|'
                                      '//div[@class="con_main"]/p/text()|'
                                      '//div[@class="TRS_Editor"]/p/text()').extract()
        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)

