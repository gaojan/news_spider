# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from twisted.enterprise import adbapi
from detailWeiboTimeHot import settings

logger = logging.getLogger(__name__)
pymysql.install_as_MySQLdb()


class DetailweibotimehotPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DB,
                                    user=settings.MYSQL_USER, password=settings.MYSQL_PASSWD)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()

    def process_item(self, item, spider):
        try:
            sql0 = "SELECT url FROM t_weibo WHERE url='{}'".format(item['url'])
            self.cursor.execute(sql0)
            url = self.cursor.fetchall()
            if not url:
                sql1 = 'INSERT INTO t_weibo(content,url,wb_user,wb_zf_count,wb_comment_count,wb_zan_count,pub_time,create_time,wb_user_name) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(item['content'], item['url'], item['wb_user'], item['wb_zf_count'], item['wb_comment_count'], item['wb_zan_count'], item['pub_time'], item['create_time'], item['wb_name'])
                print("sql1", sql1)
                self.cursor.execute(sql1)
                self.conn.commit()
            sql3 = "SELECT wb_user_id FROM t_weibo_user WHERE wb_user_id='{}'".format(item['wb_user_id'])
            self.cursor.execute(sql3)
            wb_user_id = self.cursor.fetchall()
            if not wb_user_id:
                sql2 = "INSERT INTO t_weibo_user(wb_user_id,wb_name,wb_gz,wb_fs,wb_count,wb_level,home_url) VALUES ('{}','{}',{},{},{},{},'{}')".format(item['wb_user_id'], item['wb_name'], item['wb_gz'], item['wb_fs'], item['wb_count'], item['wb_level'], item['home_url'])
                print("sql2", sql2)
                self.cursor.execute(sql2)
                self.conn.commit()


        except Exception as e:
            logging.warning(e)
            print("-----Failed to save data-----", e)
