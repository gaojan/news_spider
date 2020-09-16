# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from twisted.enterprise import adbapi
from sinaweibo.settings import (MYSQL_HOST, MYSQL_PORT, MYSQL_DB,
                                MYSQL_USER, MYSQL_PASSWD)

logger = logging.getLogger(__name__)
pymysql.install_as_MySQLdb()


class SinaweiboPipeline(object):
    def __init__(self):
        config = dict(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            db=MYSQL_DB,
            user=MYSQL_USER,
            password=MYSQL_PASSWD,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )

        self.dbpool = adbapi.ConnectionPool('MySQLdb', **config)

    def process_item(self, item, spider):
        db1 = self.dbpool.runInteraction(self.do_insert_one, item)
        db2 = self.dbpool.runInteraction(self.do_insert_two, item)

        db1.addErrback(self.handler_error)
        db2.addErrback(self.handler_error)
        return item

    def do_insert_one(self, conn, item):

        try:
            conn.execute(
                """INSERT INTO t_weibo(content,url,wb_user,wb_zf_count,wb_comment_count,wb_zan_count,pub_time,create_time) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (item['content'],
                 item['url'],
                 item['wb_user'],
                 item['wb_zf_count'],
                 item['wb_comment_count'],
                 item['wb_zan_count'],
                 item['pub_time'],
                 item['create_time']))

        except Exception as e:
            logger.warning(e)
            print("-----Failed to save data-----")

    def do_insert_two(self, conn, item):

        try:
            conn.execute(
                """INSERT INTO t_weibo_user(wb_user_id,wb_name,wb_gz,wb_fs,wb_count,wb_level,home_url) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (item['wb_user_id'],
                 item['wb_name'],
                 item['wb_gz'],
                 item['wb_fs'],
                 item['wb_count'],
                 item['wb_level'],
                 item['home_url']))

        except Exception as e:
            logger.warning(e)
            print("-----Failed to save data-----")

    def handler_error(self, failure, item, spider):
        logger.warning(failure)
