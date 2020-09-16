# -*- coding: utf-8 -*-
import scrapy
from XqzxSpider.spiders.basespider import BaseSpider


class ShanghaiSpider(BaseSpider):
    name = 'shanghai'
    allowed_domains = ['shanghai.gov.cn']

    # start_urls = ['http://service.shanghai.gov.cn/pagemore/iframePagerIndex_4411_3_30.html?page={}']
    start_urls = ['http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index{}.html']
    # for n in range(1, 15):
    #     referer = "http://service.shanghai.gov.cn/pagemore/iframePagerIndex_4411_3_30.html?objtype=3&nodeid=4411&page={0}&pagesize=30".format(n)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'service.shanghai.gov.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index.html',
        'Upgrade-Insecure-Requests': '1'
    }

    def start_requests(self):
        for i in range(1, 10):
            url = ''.join(self.start_urls).format(i)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.xpath('//*[@id="pageList"]/ul/li/a/@href').extract()
        for u in urls:
            url = 'http://www.shanghai.gov.cn' + u
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        title = response.xpath('//title/text()').extract()
        if not title:
            item['title'] = ''
        else:
            item['title'] = "".join(title).strip()

    def parse_time(self, response, item):
        p_time = response.xpath('//*[@id="ivs_date"]/text()').extract_first()
        time = p_time.replace(' ', '').replace('\n', '')
        item['time'] = time[1:-1].replace('年', '-').replace('月', '-').replace('日', ' ')

    def parse_content(self, response, item):
        content_list = response.xpath('//*[@id="ivs_content"]/p/text()|//*[@id="ivs_content"]/text()').extract()

        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)




