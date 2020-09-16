# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from datetime import datetime, timedelta
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from WangYi.items import WangyiItem
from WangYi.settings import MAXDATE



class WangyiMoneySpider(CrawlSpider):
    name = 'wangyi'
    allowed_domains = ['163.com']
    start_urls = ['http://{}.163.com/']
    category = ['news', 'money', 'sports', 'ent', 'auto', 'tech', 'mobile',
                'digi', 'lady', 'travel', 'home', 'edu', 'jiankang', 'art',
                'gongyi', 'gov', 'media', 'war', 'data', 'biz', 'fashion',
                'baby', 'daxue', 'sz.house']

    """
    新闻：https://news.163.com/
    财经： http://money.163.com/
    体育：http://sports.163.com/
    娱乐：http://ent.163.com/
    汽车：http://auto.163.com/
    科技：http://tech.163.com/
    手机: http://mobile.163.com/
    数码：http://digi.163.com/
    女人：http://lady.163.com/
    旅游：http://travel.163.com/
    房产：http://sz.house.163.com/  
    家居：http://home.163.com/
    教育：http://edu.163.com/
    健康：http://jiankang.163.com/
    艺术：http://art.163.com
    公益：http://gongyi.163.com/
    政务：http://gov.163.com/
    媒体：http://media.163.com/
    军事：http://war.163.com/
    数独：http://data.163.com/
    商业：http://biz.163.com/
    时尚：http://fashion.163.com/
    亲子：http://baby.163.com/
    校园：http://daxue.163.com/
    """
    rules = (
        Rule(LinkExtractor(allow=r'[\w]+.163.com/[\d]+/[\d]+/[\d]+/[\w]+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'[\w]+house.163.com/[\d]+/[\d]+/[\d]+/[\w]+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'[\w]+.163.com/v2/article/detail/[\w]+.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'[\w]+.163.com/[\w]+'), follow=True),
        # Rule(LinkExtractor(allow=r'[\w]+.163.com/special/.*'), follow=True),
        # Rule(LinkExtractor(allow=r'[\w]+.163.com/[\w]+/[\w]+/[\w]+.html'), follow=True),
        Rule(LinkExtractor(allow=r'[\w]+.163.com/.*'), follow=True),
        Rule(LinkExtractor(allow=r'[\w]+.[\w+].163.com/.*'), follow=True),
    )

    def start_requests(self):
        urls = [''.join(self.start_urls).format(c) for c in self.category]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        item = WangyiItem()

        # self.parse_time(response, item)
        # if self.filter_time(item['time']):
        self.parse_title(response, item)
        self.parse_url(response, item)
        self.parse_content(response, item)
        self.parse_category(response, item)
        print(item, '------')
        yield item

    def parse_title(self, response, item):
        title = response.xpath('//*[@id="epContentLeft"]/h1/text()|'
                               '//div[@class="col_l"]/h1/text()|'
                               '//*[@id="h1title"]/text()|'
                               '//div[@class="left"]/h1/text()|'
                               '//div[@class="brief"]/h1/text()|'
                               '//div[@class="article_title"]/h2/text()|'
                               '//div[@class="articles"]/h1/text()').extract()
        if not title:
            print('----title failed to get----')
            item['title'] = ''
        else:
            item['title'] = title[0].strip().replace('\u3000', '').replace('\xa0', '')

    # def parse_time(self, response, item):
    #
    #     match_time1 = r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}'
    #     match_time2 = r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}'
    #     match_time3 = r'\d{4}-\d{1,2}-\d{1,2}'
    #
    #     p_time = response.xpath('//div[@class="post_time_source"]/text()|'
    #                             '//*[@id="ptime"]/text()|'
    #                             '//div[@class="pub_time"]/text()|'
    #                             '//div[@class="articles"]/span/text()').extract()
    #     if not p_time:
    #         if not re.findall(match_time1, response.text):
    #             if not re.findall(match_time2, response.text):
    #                 if not re.findall(match_time3, response.text):
    #                     print('----page error----')
    #                     return None
    #                 item['time'] = re.findall(match_time3, response.text)[0]   # 2018-08-29
    #             item['time'] = re.findall(match_time2, response.text)[0]       # 2018-08-29 00:00
    #         item['time'] = re.findall(match_time1, response.text)[0]           # 2018-08-29 00:00:00
    #     else:
    #         if not re.findall(match_time1, "".join(p_time)):
    #             if not re.findall(match_time2, "".join(p_time)):
    #                 if not re.findall(match_time3, "".join(p_time)):
    #                     print('----Fetch time error----')
    #                     return None
    #                 item['time'] = re.findall(match_time3, "".join(p_time))[0]  # 2018-08-29
    #             item['time'] = re.findall(match_time2, "".join(p_time))[0]      # 2018-08-29 00:00
    #         item['time'] = re.findall(match_time1, "".join(p_time))[0]          # 2018-08-29 00:00:00

    def parse_category(self, response, item):
        res_url = response.url
        if ('money.163' in res_url) or ('biz.163' in res_url):
            item['category'] = '财经'
        elif 'travel.163' in res_url:
            item['category'] = '旅游'
        elif 'jiankang.163' in res_url:
            item['category'] = '健康'
        elif ('tech.163' in res_url) or ('mobile.163' in res_url) or ('digi.163' in res_url):
            item['category'] = '科技'
        elif 'auto.163' in res_url:
            item['category'] = '汽车'
        else:
            return

    def parse_url(self, response, item):
        if 200 != response.status:
            return None
        else:
            item['url'] = response.url

    def parse_content(self, response, item):
        content_list = response.xpath('//*[@id="endText"]/p/text()|'
                                      '//*[@id="endText"]/p/span/text()|'
                                      '//*[@id="endText"]/p/font/text()|'
                                      '//*[@id="endText"]/p/strong/text()|'
                                      '//*[@id="endText"]/p/font/b/text()|'
                                      '//*[@id="endText"]/div/span/text()|'
                                      '//*[@id="endText"]/div/text()|'
                                      '//*[@id="endText"]/span/text()|'
                                      '//*[@id="endText"]/text()|'
                                      '//*[@id="endText"]/p/span/font/text()|'
                                      '//*[@id="endText"]//p/text()|'
                                      '//*[@id="endText"]//p/span/text()|'   
                                      '//*[@id="endText"]/section/section/section/p/text()|'
                                      '//*[@id="endText"]/section/section/section/p/b/text()|'
                                      '//*[@id="content"]/p/text()|'
                                      '//*[@id="bs_content"]/p/strong/text()|'
                                      '//div[@class="w_text"]/p/text()|'
                                      '//div[@class="w_text"]/p/font/text()|'
                                      '//*[@id="mp-editor"]/p/text()|'
                                      '//div[@class="overview"]/p/text()|'
                                      '//div[@class="art_content"]/p/text()'
                                      ).extract()

        if not content_list:
            item['content'] = ''
        else:
            content = [content for content in content_list if not
            ('原标题' in content or '版权声明' in content or '本文来源' in content or '责任编辑' in content or '来源：网易' in content)]
            item['content'] = "".join(content).replace('\t', '').replace('\n', '').replace('\r', '').\
                replace('\xa0', '').replace('\u3000', '').replace(' ', '')

    # def filter_time(self, string, day=MAXDATE):
    #     """时间过滤"""
    #     pre_time = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d %H:%S:%M')
    #     to_pre_time = datetime.strptime(pre_time, '%Y-%m-%d %H:%S:%M')
    #
    #     t = string.split(' ')
    #     if len(t) == 1:
    #         if to_pre_time > datetime.strptime(string + ' 00:00:00', '%Y-%m-%d %H:%S:%M'):
    #             return False
    #         return True
    #
    #     if len(t) >= 2:
    #         t2 = t[1].split(':')
    #         if len(t2) == 1:
    #             if to_pre_time > datetime.strptime(string + ':00:00', '%Y-%m-%d %H:%S:%M'):
    #                 return False
    #             return True
    #
    #         elif len(t2) == 2:
    #             if to_pre_time > datetime.strptime(string + ':00', '%Y-%m-%d %H:%S:%M'):
    #                 return False
    #             return True
    #
    #         elif len(t2) == 3:
    #             if to_pre_time > datetime.strptime(string, '%Y-%m-%d %H:%S:%M'):
    #                 return False
    #             return True
