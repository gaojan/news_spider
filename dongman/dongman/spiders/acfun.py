# -*- coding: utf-8 -*-
import scrapy
import json
import time
from dongman.items import DongmanItem


class AcfunSpider(scrapy.Spider):
    name = 'acfun'
    allowed_domains = ['acfun.cn']
    start_urls = ['http://acfun.cn/']

    def start_requests(self):
        start_url = "http://webapi.aixifan.com/query/article/list?pageNo=1&size=50&realmIds=13%2C31&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true"
        yield scrapy.Request(url=start_url, callback=self.parse_list, dont_filter=True)
        "contribute_time"  # 发布时间

    def parse_list(self, response):
        detail_li = json.loads(response.text)
        for detail in detail_li['data']['articleList']:
            url = 'http://www.acfun.cn/a/ac' + str(detail['id'])
            item = DongmanItem()
            item['title'] = detail['title']
            item['url'] = url
            time_int = detail['contribute_time']
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_int/1000))
            item['create_time'] = create_time
            yield scrapy.Request(url, callback=self.parse_detail, meta={'meta': item})

    def parse_detail(self, response):
        item = response.meta['meta']
        # title = response.xpath('//div[@id="main"]/section//div[@class="caption"]/text()').extract_first()
        content_list = response.xpath('//section[@id="article-content"]/div[@class="article-content"]/p//text()').extract()
        content = ''.join(content_list)
        item['content'] = content.replace('\xa0', '')
        yield item
