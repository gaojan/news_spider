# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import datetime
from datetime import datetime, timedelta
from xinhuawang.settings import MAXDATE
from xinhuawang.items import XinhuawangItem


class XinhuaSpider(scrapy.Spider):
    name = 'xinhua'
    allowed_domains = ['news.cn', 'xinhuanet.com']

    nid_list = ['113352', '113321', '113322', '113207', '113667', '1198634',
                '1198635', '1198636', '1198637', '1198619', '1198621', '1198623',
                '1198628', '11147664', '115093', '116713', '116714', '116716',
                '116727', '1118296', '11135736', '11135737', '11135739', '11135741',
                '11135742', '11135744', '11135745', '11135746', '11135747', '11135748']

    start_urls = ['http://qc.wa.news.cn/nodeart/list?nid={nid}&pgnum={pg}&cnt=10']

    # 'http://qc.wa.news.cn/nodeart/list?nid=113352&pgnum={}&cnt=10'   # 时政新闻
    # 'http://qc.wa.news.cn/nodeart/list?nid=113321&pgnum={}&cnt=10',  # 地方新闻
    # 'http://qc.wa.news.cn/nodeart/list?nid=113322&pgnum={}&cnt=10',  # 滚动新闻
    # 'http://qc.wa.news.cn/nodeart/list?nid=113207&pgnum={}&cnt=10',  # 法治新闻
    # 'http://qc.wa.news.cn/nodeart/list?nid=113667&pgnum={}&cnt=10',  # 国际新闻
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198634&pgnum={}&cnt=10',  # 亚太政治
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198635&pgnum={}&cnt=10',  # 亚太财经
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198636&pgnum={}&cnt=10',  # 亚太社会
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198637&pgnum={}&cnt=10',  # 亚太文娱
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198619&pgnum={}&cnt=10',  # 亚太要闻
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198621&pgnum={}&cnt=10',  # 亚太观点
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198628&pgnum={}&cnt=10',  # 亚太旅游
    # 'http://qc.wa.news.cn/nodeart/list?nid=1198623&pgnum={}&cnt=10',  # 亚太与中国
    # 'http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum={}&cnt=10',  # 财经新闻
    # 'http://qc.wa.news.cn/nodeart/list?nid=115093&pgnum={}&cnt=10',  # 财经财眼
    # 'http://qc.wa.news.cn/nodeart/list?nid=116713&pgnum={}&cnt=10',  # 娱乐资讯
    # 'http://qc.wa.news.cn/nodeart/list?nid=116716&pgnum={}&cnt=10',  # 娱乐明星
    # 'http://qc.wa.news.cn/nodeart/list?nid=116727&pgnum={}&cnt=10',  # 娱乐电影
    # 'http://qc.wa.news.cn/nodeart/list?nid=116714&pgnum={}&cnt=10',  # 娱乐电视
    # 'http://qc.wa.news.cn/nodeart/list?nid=1118296&pgnum={}&cnt=10',  # 娱乐音乐
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135736&pgnum={}&cnt=10',  # 一带一路 高清大图
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135737&pgnum={}&cnt=10',  # 一带一路 丝路聚焦
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135739&pgnum={}&cnt=10',  # 一带一路 中国议程
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135741&pgnum={}&cnt=10',  # 一带一路 深度透视
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135742&pgnum={}&cnt=10',  # 一带一路 丝路智库
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135744&pgnum={}&cnt=10',  # 一带一路 丝路商机
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135745&pgnum={}&cnt=10',  # 一带一路 丝路国际
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135746&pgnum={}&cnt=10',  # 一带一路 丝路中国
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135747&pgnum={}&cnt=10',  # 一带一路 丝路文化
    # 'http://qc.wa.news.cn/nodeart/list?nid=11135748&pgnum={}&cnt=10']  # 一带一路 丝路旅游

    def start_requests(self):

        for page in range(1, 101):
            urls = ["".join(self.start_urls).format(nid=nid, pg=page) for nid in self.nid_list]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

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
        """列表页"""
        try:
            news_list = json.loads(response.text[1:-1]).get('data').get('list')
        except:
            print('----Data is empty----')
            return None

        for news in news_list:
            item = XinhuawangItem()

            item['time'] = news['PubTime']
            if self.filter_time(item['time']):

                item['title'] = news['Title'].strip()
                item['url'] = news['LinkUrl']

                yield scrapy.Request(item['url'], callback=self.parse_content, meta={'meta': item})
            else:
                return None

    def parse_content(self, response):
        """内容页"""
        temp = response.meta['meta']
        content_list = response.xpath('//*[@id="p-detail"]/p/text()|'
                                      '//*[@id="p-detail"]/p/span/text()|'
                                      '//*[@id="p-detail"]/p/font/text()|'
                                      '//*[@id="p-detail"]/p/font/strong/text()|'
                                      '//*[@id="p-detail"]/p/strong/font/text()|'
                                      '//*[@id="p-detail"]/div[1]/p/text()|'
                                      '//*[@id="p-detail"]/div[2]/p/text()|'
                                      '//*[@id="p-detail"]/div[2]//text()|'
                                      '//*[@id="p-detail"]/div[1]/p/font/text()|'
                                      '//*[@id="p-detail"]/p/span/font/text()|'
                                      '//*[@id="p-detail"]/div[2]/p/strong/font/text()|'
                                      '//*[@id="p-detail"]/div[1]/p/strong/font/text()|'
                                      '//*[@id="p-detail"]/div[1]/p/span/span/text()|'
                                      '//*[@id="p-detail"]/div[1]/p/span/span/span/span/text()|'
                                      '//*[@id="p-detail"]/div[1]/p[position()>2]/text()|'
                                      '//*[@id="p-detail"]//p/text()|'
                                      '//*[@id="p-detail"]//span/text()|'
                                      '//div[@class="bai14"]/text()|'
                                      '//div[@class="bai14"]/span/p/text()|'
                                      '//div[@class="bai14"]/p/text()|'
                                      '//*[@id="content"]/p/text()|'
                                      '//*[@id="content"]/p/span/text()|'
                                      '//*[@id="content"]/span/p/text()|'
                                      '//*[@id="part97"]/p/text()|'
                                      '//*[@id="article"]/div[2]/p/text()|'
                                      '//*[@id="article"]/div[2]/p/span/text()|'
                                      '//*[@id="article"]/div[2]/p/font/text()|'
                                      '//*[@id="article"]/div[2]/p/font/span/text()|'
                                      '//*[@id="article"]/div[2]/font/span/p/font/text()|'
                                      '//*[@id="m3"]/div[2]/p/text()|'
                                      '//*[@id="m1"]/div[2]/p/text()|'
                                      '//*[@id="m4"]/div[2]/p/text()|'
                                      '//div[@class="box txtcont"]/p/text()|'
                                      '//div[@class="box txtcont"]/p/font/text()|'
                                      '//div[@class="box txtcont"]/font/p/text()|'
                                      '//div[@class="box txtcont"]/font/font/font/p/text()|'
                                      '//div[@class="box txtcont"]/ont/font/font/font/p/text()').extract()
        if not content_list:
            temp['content'] = ''
        else:
            content = [content for content in content_list if '原标题' not in content]
            temp['content'] = "||".join(content).replace('\t', '').replace('\u3000', '').replace('\n', '')\
                .replace('\xa0', '').replace('\r', '').replace(' ', '')

        item = temp
        print(item, "*****")
        yield item



