# -*- coding: utf-8 -*-
import scrapy
import datetime
from shanghaigov.settings import MAXDATE
from shanghaigov.items import ShanghaigovItem
import requests


class ShanghaiSpider(scrapy.Spider):
    name = 'shanghai'
    allowed_domains = ['shanghai.gov.cn']

    start_urls = ['http://service.shanghai.gov.cn/pagemore/iframePagerIndex_4411_3_30.html?page={}']
    for n in range(1, 15):
        referer = "http://service.shanghai.gov.cn/pagemore/iframePagerIndex_4411_3_30.html?objtype=3&nodeid=4411&page={0}&pagesize=30".format(n)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'service.shanghai.gov.cn',
            'Pragma': 'no-cache',
            'Referer': referer,
            'Upgrade-Insecure-Requests': '1'
        }

    def start_requests(self):
        for i in range(1, 15):
            url = ''.join(self.start_urls).format(i)

            yield scrapy.Request(url, headers=self.headers, callback=self.parse, dont_filter=True)

    @staticmethod
    def string_toDatetime(string):
        """时间字符串转datetime"""
        return datetime.datetime.strptime(string.split(' ')[0] + ' 00:00:00', '%Y-%m-%d %H:%S:%M')

    def scheduler_date(self):
        """设置时间过滤"""
        t = datetime.datetime.now() - datetime.timedelta(days=MAXDATE)
        toStr = t.strftime('%Y-%m-%d')
        return self.string_toDatetime(toStr)


    def parse(self, response):
        # 获取节点列表
        node_list = response.xpath('//ul[@class="uli14 pageList"]/li')
        for node in node_list:
            item = ShanghaigovItem()

            pub_time = node.xpath('./span/text()').extract_first()
            if pub_time:
                item['time'] = datetime.datetime.strptime(pub_time, '%Y.%m.%d').strftime('%Y-%m-%d')
                if self.string_toDatetime(item['time']) >= self.scheduler_date():

                    item['url'] = node.xpath('./a/@href').extract_first()
                    title = node.xpath('./a/text()').extract_first()
                    item['title'] = title.strip().replace('\u3000', '').replace('\xa0', '')

                    yield scrapy.Request(item['url'], callback=self.parse_content, meta={'meta': item})
                else:
                    return None

    def parse_content(self, response):
        temp = response.meta['meta']
        content = "".join(response.xpath('//*[@id="ivs_content"]/p/text()|//*[@id="ivs_content"]/text()').extract())
        if content:
            temp['content'] = content.replace('\t', '').replace('\u3000', '').replace('\n', '').replace('\xa0', '')

            item = temp
            print(item, "------")
            yield item


