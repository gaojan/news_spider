# -*- coding: utf-8 -*-
import scrapy
import json
from SinaRealTimeHot.items import SinarealtimehotItem


class MweiborealtimehotSpider(scrapy.Spider):
    name = 'mWeiboRealtimehot'
    allowed_domains = ['m.sina.cn']
    # start_urls = ['http://m.sina.cn/']

    def start_requests(self):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        res_dict = json.loads(response.text)
        card_group = res_dict['data']['cards'][0]['card_group']
        for card in card_group:
            item = SinarealtimehotItem()
            item['mobile_url'] = card['scheme']
            item['keyword'] = card['desc']
            item['keyword_heat'] = card.get('desc_extr')
            yield item
