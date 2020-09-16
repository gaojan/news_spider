# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from datetime import datetime, timedelta
from fenghuangwang.items import FenghuangwangItem
from fenghuangwang.settings import MAXDATE


class FenghuangSportsSpider(scrapy.Spider):
    name = 'fenghuang_sports'
    allowed_domains = ['ifeng.com']
    start_urls = ['http://2018.ifeng.com/listpage/106169/{}/0/59202130/59204540/list.shtml',
                  'http://2018.ifeng.com/listpage/106170/{}/1/58942159/58976484/list.shtml',
                  'http://2018.ifeng.com/listpage/106171/{}/0/58951562/58956120/list.shtml',
                  'http://2018.ifeng.com/listpage/106173/{}/0/58747643/58767425/list.shtml',
                  'http://2018.ifeng.com/listpage/106174/{}/1/58954405/58968428/list.shtml',
                  'http://2018.ifeng.com/listpage/106175/{}/0/59034163/59049314/list.shtml',
                  'http://2018.ifeng.com/listpage/106176/{}/0/59202365/59204549/list.shtml',    # 诸强新闻
                  'http://2018.ifeng.com/listpage/111171/{}/0/59204786/59206989/list.shtml',    # 即时新闻
                  'http://sports.ifeng.com/listpage/31190/{}/1/59316523/59324204/list.shtml',   # 中国足球 中超 10页
                  'http://sports.ifeng.com/listpage/35586/{}/1/57686939/58207911/list.shtml',   # 中国足球 亚冠 10页
                  'http://sports.ifeng.com/listpage/31193/{}/1/59267173/59294342/list.shtml',   # 篮球风云 NBA 10页
                  'http://sports.ifeng.com/listpage/31194/{}/1/59267045/59315062/list.shtml',   # 篮球风云 CBA 10页
                  'http://sports.ifeng.com/listpage/11246/{}/0/59227937/59245917/list.shtml',   # 国际足球 10页
                  'http://sports.ifeng.com/listpage/11247/{}/1/59346016/59346836/list.shtml',   # 综合体育 10页
                  'http://sports.ifeng.com/listpage/101213/{}/1/59321812/59341658/list.shtml',  # 高尔夫 10页
                  'http://sports.ifeng.com/listpage/101214/{}/1/59315662/59337748/list.shtml',  # 高尔夫 美巡赛 10页
                  'http://sports.ifeng.com/listpage/101215/{}/1/59212556/59315081/list.shtml',  # 高尔夫 欧巡赛 10页
                  'http://sports.ifeng.com/listpage/101216/{}/1/58445147/58558073/list.shtml',  # 高尔夫 日巡赛 10页
                  'http://sports.ifeng.com/listpage/101217/{}/1/58610232/58779681/list.shtml',  # 高尔夫 国内新闻 10页
                  'http://sports.ifeng.com/listpage/101218/{}/1/56802891/57191535/list.shtml']  # 高尔夫 实用资讯 10页

    def start_requests(self):
        for url in self.start_urls:
            # 最大10页
            for page in range(1, 7):
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
        """列表页"""
        item = FenghuangwangItem()
        node_list = response.xpath('//div[@class="box650"]/div')
        for node in node_list:

            item['time'] = node.xpath('./div[2]/span/text()').extract_first()
            if item['time']:

                # 如果发布时间大于规定的时间，则继续爬去
                if self.filter_time(item['time']):

                    title = node.xpath('./h2/a/text()').extract_first()
                    if title:
                        item['title'] = title.strip()

                    item['url'] = node.xpath('./h2/a/@href').extract_first()

                    yield scrapy.Request(item['url'], callback=self.parse_content, meta={'meta': item})
                else:
                    return None

    def parse_content(self, response):
        """详情页"""

        temp = response.meta['meta']
        content_list = response.xpath('//*[@id="main_content"]/p/text()|//*[@id="picTxt"]/ul/li/p/text()|'
                                      '//*[@id="photoDesc"]/text()|//*[@id="yc_con_txt"]/p/text()').extract()

        if not content_list:
            temp['content'] = ''
        else:
            content = [content for content in content_list if '原标题' not in content]
            temp['content'] = "||".join(content).replace('\t', '').replace('\n', '').replace('\r', '').\
                replace('\u3000', '').replace('\u200b', '').replace('\xa0', '').replace(' ', '')

        item = temp
        print(item, '++++++')
        yield item

