#!usr/bin/env python  
# -*- coding: utf-8 -*- 
"""
# Author: Jan Gao 
# Date: 2018/8/23
# Description: BaseSpider
# Site: http://www.xrtpay.com/
# Copyright (c) ShenZhen XinRuiTai Payment Service Co.,Ltd. All rights reserved 
"""

import logging
from datetime import datetime, timedelta
from scrapy import spiders
from XqzxSpider.items import XqzxspiderItem
from XqzxSpider.settings import MAXDATE


class BaseSpider(spiders.Spider):
    # name = 'BaseSpider'

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
        pass

    def parse_item(self, response):
        item = XqzxspiderItem()
        self.parse_time(response, item)
        if self.filter_time(item['time']):
            self.parse_url(response, item)
            self.parse_title(response, item)
            self.parse_content(response, item)

            print(item, '-----')
            yield item
        else:
            return

    def parse_title(self, response, item):
        pass

    def parse_time(self, response, item):
        pass

    def parse_url(self, response, item):
        if 200 != response.status:
            print('----Page request error----')
            return
        item['url'] = response.url

    def parse_content(self, response, item):
        pass

    def content_to(self, content_list):
        content = list(map(lambda text: text.replace("\xa0", "").replace("\u3000", "").replace("\r", "").
                           replace("\t", "").replace("\n", "").replace(" ", ""), content_list))
        return "||".join(content)
