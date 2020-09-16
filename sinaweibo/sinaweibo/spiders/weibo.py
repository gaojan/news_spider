# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import datetime
import time
import requests
import re
from scrapy import selector
from sinaweibo.items import SinaweiboItem


class MWeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.com', 'm.weibo.cn']
    start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=102803%s&openApp=0&page={}']
    item_id = ['', '_ctg1_4388_-_ctg1_4388', '_ctg1_1988_-_ctg1_1988', '_ctg1_4288_-_ctg1_4288',
               '_ctg1_4188_-_ctg1_4188', 'ctg1_5088_-_ctg1_5088', '_ctg1_1388_-_ctg1_1388',
               '_ctg1_5188_-_ctg1_5188', '_ctg1_3288_-_ctg1_3288', '_ctg1_4888_-_ctg1_4888']

    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0&page={}', 热门 共30页
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4388_-_ctg1_4388&openApp=0&page={}',  # 搞笑
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_1988_-_ctg1_1988&openApp=0&since_id=1',  # 情感
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4288_-_ctg1_4288&openApp=0&since_id=1',  # 明星
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4188_-_ctg1_4188&openApp=0&since_id=1',  # 社会
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_5088_-_ctg1_5088&openApp=0&since_id=1',  # 数码
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_1388_-_ctg1_1388&openApp=0&since_id=1',  # 体育
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_5188_-_ctg1_5188&openApp=0&since_id=2',  # 汽车
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_3288_-_ctg1_3288&openApp=0&since_id=1',  # 电影
    # 'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4888_-_ctg1_4888&openApp=0&since_id=1'   # 游戏
    # https://m.weibo.cn/api/container/getIndex?uid=5044281310&luicode=10000011&lfid=102803&type=uid&value=5044281310&containerid=1076035044281310&page=2  内容页

    def start_requests(self):
        for nid in self.item_id:
            for page in range(1, 101):
                url = (''.join(self.start_urls) % nid).format(page)
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        try:
            res_data = json.loads(response.text).get('data')
        except Exception as e:
            print('----Data is empty----')
            logging.warning(e)
            return None

        cards = res_data.get('cards')
        for card in cards:
            item = SinaweiboItem()
            if 11 == int(card['card_type']):

                for n in card['card_group']:
                    self.parse_weibo_info(n, item)
                    yield scrapy.Request(item['url'], callback=self.parse_pub_time, meta={'meta': item})

            else:
                self.parse_weibo_info(card, item)
                yield scrapy.Request(item['url'], callback=self.parse_pub_time, meta={'meta': item})

    def parse_weibo_info(self, data, item):

        # 用户信息
        try:
            user_info = data.get('mblog')['user']
            item['wb_user_id'] = user_info.get('id')
            item['wb_name'] = user_info.get('screen_name')
            item['wb_gz'] = user_info.get('follow_count')
            item['wb_fs'] = user_info.get('followers_count')
            item['wb_count'] = user_info.get('statuses_count')
            item['wb_level'] = user_info.get('urank')
            item['home_url'] = user_info.get('profile_url')

        except Exception as e:
            print('----No User Info----')
            logging.warning(e)

        # 微博内容信息
        text = data.get('mblog')['text']
        content = ''.join(selector.Selector(text=text).xpath('//text()').extract())
        if content:
            item['content'] = content.strip().replace('\n', '').replace('\r', '').\
                replace('\u200b', '').replace('\xa0', '').replace(' ', '')
        item['url'] = 'https://m.weibo.cn/status/' + data.get('mblog')['id']
        item['wb_user'] = item['wb_user_id']
        item['wb_zf_count'] = data.get('mblog')['reposts_count']
        item['wb_comment_count'] = data.get('mblog')['comments_count']
        item['wb_zan_count'] = data.get('mblog')['attitudes_count']
        item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def parse_pub_time(self, response):

        temp = response.meta['meta']
        res_list = re.findall('render_data\s=\s\[(\{.*?)\]\[0\]', response.text, re.S)
        if len(res_list) > 0:
            created_at = json.loads(res_list[0]).get('status')['created_at']
            # Wed Aug 15 18:19:54 +0800 2018
            # t = created_at.split(' ')
            pub = time.strptime(created_at, '%a %b %d %H:%M:%S +0800 %Y')
            pub_time = time.strftime('%Y-%m-%d %H:%M:%S', pub)
            temp['pub_time'] = pub_time

            item = temp
            print(item, '------')
            yield item


