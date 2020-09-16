# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from SinaRealTimeHot import settings
from SinaRealTimeHot.items import SinarealtimehotItem, BaiduRealtimehotItem
logger = logging.getLogger(__name__)
pymysql.install_as_MySQLdb()


class SinarealtimehotPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DB,
                                    user=settings.MYSQL_USER, password=settings.MYSQL_PASSWD)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()

    def process_item(self, item, spider):
        if isinstance(item, SinarealtimehotItem):  # 微博
            table_name_realtimehot = 't_weibo_realtimehot'
            table_name_realtimehot_rank = 't_weibo_realtimehot_rank'
        if isinstance(item, BaiduRealtimehotItem):  # 百度
            table_name_realtimehot = 't_baidu_realtimehot'
            table_name_realtimehot_rank = 't_baidu_realtimehot_rank'

        self.cursor.execute("SELECT `id` FROM {} WHERE keyword='{}'".format(table_name_realtimehot, item['keyword']))
        keyword_id = self.cursor.fetchall()
        if not keyword_id:  # 没存keyword
            if item.get('mobile_url'):
                self.cursor.execute("INSERT INTO {} (keyword,mobile_url) VALUES ('{}','{}')".format(table_name_realtimehot, item['keyword'], item['mobile_url']))
            else:
                self.cursor.execute("INSERT INTO {} (keyword,url) VALUES ('{}','{}')".format(table_name_realtimehot, item['keyword'], item['url']))
            self.conn.commit()
        else:  # 有keyword, 则更新url
            if item.get('mobile_url'):
                print("UPDATE t_weibo_realtimehot SET  `mobile_url` = '{}' WHERE `id`={}".format(item['mobile_url'], keyword_id[0][0]))
                self.cursor.execute("UPDATE t_weibo_realtimehot SET  `mobile_url` = '{}' WHERE `id`={}".format(item['mobile_url'], keyword_id[0][0]))
            else:
                self.cursor.execute("UPDATE t_weibo_realtimehot SET  `url` = '{}' WHERE `id`={}".format(item['url'], keyword_id[0][0]))

        if item['keyword_heat']:  # 有热度指数
            if not keyword_id:  # 是刚刚新增新的
                self.cursor.execute("SELECT `id` FROM {} WHERE keyword='{}'".format(table_name_realtimehot, item['keyword']))
                keyword_id = self.cursor.fetchall()[0][0]
                print(keyword_id)
            else:
                keyword_id = keyword_id[0][0]
            print("INSERT INTO {}(`keyword_id`, `keyword_heat`) VALUES ({}, {})".format(table_name_realtimehot_rank, keyword_id, item['keyword_heat']))
            self.cursor.execute("INSERT INTO {}(`keyword_id`, `keyword_heat`) VALUES ({}, {})".format(table_name_realtimehot_rank, keyword_id, item['keyword_heat']))
            self.conn.commit()

