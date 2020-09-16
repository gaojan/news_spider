# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from datetime import datetime, timedelta
from fenghuangwang.items import FenghuangwangItem
from fenghuangwang.settings import MAXDATE


class FenghuangEntSpider(scrapy.Spider):
    name = 'fenghuang_ent'
    allowed_domains = ['ent.ifeng.com']
    start_urls = ['http://ent.ifeng.com/listpage/3/{}/list.shtml',
                  'http://ent.ifeng.com/listpage/6/{}/list.shtml',
                  'http://ent.ifeng.com/listpage/1370/{}/list.shtml',
                  'http://ent.ifeng.com/listpage/30741/{}/list.shtml']

    def start_requests(self):
        for url in self.start_urls:
            for page in range(1, 6):
                link = url.format(page)
                yield scrapy.Request(link, callback=self.parse, dont_filter=True)

    def filter_time(self, string, day=MAXDATE):
        """时间过滤"""
        pre_time = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d %H:%S:%M')
        to_pre_time = datetime.strptime(pre_time, '%Y-%m-%d %H:%S:%M')

        t = string.split(' ')
        if len(t) == 1:
            if to_pre_time > datetime.strptime(string + ' 00:00:00', '%Y-%m-%d %H:%S:%M'):
                return False
            return True

        if len(t) >= 2:
            t2 = t[1].split(':')
            if len(t2) == 1:
                if to_pre_time > datetime.strptime(string + ':00:00', '%Y-%m-%d %H:%S:%M'):
                    return False
                return True

            elif len(t2) == 2:
                if to_pre_time > datetime.strptime(string + ':00', '%Y-%m-%d %H:%S:%M'):
                    return False
                return True

            elif len(t2) == 3:
                if to_pre_time > datetime.strptime(string, '%Y-%m-%d %H:%S:%M'):
                    return False
                return True

    def parse(self, response):

        item = FenghuangwangItem()
        node_list = response.xpath('//div[@class="box650"]/div')
        for node in node_list:

            item['time'] = node.xpath('./div[2]/span/text()').extract_first()
            if self.filter_time(item['time']):

                title = node.xpath('./h2/a/text()').extract_first()
                if title:
                    item['title'] = title.strip().replace('\u3000', '').replace('\xa0', '')

                item['url'] = node.xpath('./h2/a/@href').extract_first()

                yield scrapy.Request(item['url'], callback=self.parse_content, meta={'meta': item})
            else:
                return None

    def parse_content(self, response):

        temp = response.meta['meta']
        content_list = response.xpath('//*[@id="main_content"]/p/text()|'
                                      '//*[@id="main_content"]/p/strong/text()|'
                                      '//*[@id="picTxt"]/ul/li/p/text()|'
                                      '//*[@id="imgBox"]/div[3]/ul/li/p/text()|'
                                      '//*[@id="photoDesc"]/text()|'
                                      '//*[@id="yc_con_txt"]/p/text()').extract()

        if not content_list:
            temp['content'] = ''
        else:
            content = [content for content in content_list if '原标题' not in content]
            temp['content'] = "||".join(content).replace('\t', '').replace('\n', '').replace('\r', '').\
                replace('\u3000', '').replace('\u200b', '').replace('\xa0', '').replace(' ', '')

        item = temp
        print(item, "------")
        yield item
