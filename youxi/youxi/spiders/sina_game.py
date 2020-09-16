# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from youxi.items import YouxiItem


class SinaGameSpider(CrawlSpider):
    name = 'sina_game'
    allowed_domains = ['interface.sina.cn', 'sina.cn', 'games.sina.com.cn']
    start_urls = [
        'http://interface.sina.cn/games/gpapi/2016index/2016_interface_game_pc_home.shtml?fid=1_1&page=1&pageSize=25',
        'http://interface.sina.cn/games/gpapi/2016index/2016_interface_game_pc_home.shtml?fid=2_1&page=1&pageSize=25',
        'http://interface.sina.cn/games/gpapi/2016index/2016_interface_game_pc_home.shtml?fid=3_13&page=1&pageSize=25',
        'http://interface.sina.cn/games/gpapi/2016index/2016_interface_game_pc_home.shtml?fid=3_1&page=1&pageSize=25',
        'http://interface.sina.cn/games/gpapi/2016index/2016_interface_game_pc_home.shtml?fid=4_1&page=1&pageSize=25',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'(.*?)shtml'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = YouxiItem()
        title = response.xpath('//title/text()').extract_first()
        if title and '_' in title:
            title = title.split('_')[0]
        time = response.xpath('//meta[@property="article:published_time"]/@content').extract_first()
        if title and time:
            item['url'] = response.url
            item['title'] = title
            content = response.xpath('//div[@id="artibody"]/p//text()|'
                                     '//div[@id="artibody"]/div/p/text()').extract()
            item['content'] = ''.join(content).replace('\u3000', '').replace('\n', '').replace('\xa0', '')
            time = time.replace('T', ' ').split('+')[0]
            item['time'] = time
            return item
