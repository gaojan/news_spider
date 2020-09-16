# -*- coding: utf-8 -*-
import scrapy
import logging
import datetime
import re
from chongqinggov.settings import MAXDATE
from chongqinggov.items import ChongqinggovItem


class ChongqingSpider(scrapy.Spider):
    name = 'chongqing'
    allowed_domains = ['cq.gov.cn']
    start_urls = ['http://www.cq.gov.cn/zwxx/{nid}_{page}']
    nid_list = ['jrcq', 'zwdt', 'tpxw']

    """
    http://www.cq.gov.cn/zwxx/jrcq_2  今日重庆
    http://www.cq.gov.cn/zwxx/zwdt_2  政务活动
    http://www.cq.gov.cn/zwxx/tpxw_2  图片新闻
    """

    def start_requests(self):
        for page in range(1, 5):
            urls = [''.join(self.start_urls).format(nid=nid, page=page) for nid in self.nid_list]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

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
        """列表页"""
        node_list = response.xpath('//div[@class="border"]/ul/li')
        for node in node_list:
            item = ChongqinggovItem()

            time = node.xpath('./span/text()').extract_first()
            if time:
                item['time'] = time.strip()
                if self.string_toDatetime(item['time']) >= self.scheduler_date():

                    title = node.xpath('./a/text()').extract_first()
                    item['title'] = title.strip().replace('\xa0', '').replace('\u3000', '')

                    url = node.xpath('./a/@href').extract_first()
                    item['url'] = "http://www.cq.gov.cn" + url

                    try:
                        yield scrapy.Request(item['url'], callback=self.parse_content, meta={'meta': item})
                    except Exception as e:
                        logging.warning(e)
                        return None

                else:
                    return None

    def parse_content(self, response):
        """内容页"""
        temp = response.meta['meta']
        content = "".join(response.xpath(' //div[@class="conTxt"]/p/span/text()|'
                                         '//div[@class="conTxt"]/p/span/span/text()'
                                         ).extract()).strip()

        # pattern = re.compile(r'\S')
        # if not pattern.findall(content):
        #     return None

        if content:
            temp['content'] = content.replace('\t', '').replace('\u3000', '').replace('\n', '').replace('\xa0', '')

        item = temp
        print(item, "-----")
        yield item
