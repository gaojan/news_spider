# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from HangZhouGOV.settings import (MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWD)
from twisted.enterprise import adbapi

logger = logging.getLogger(__name__)
pymysql.install_as_MySQLdb()


class HangzhougovPipeline(object):
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
        db = self.dbpool.runInteraction(self.do_insert, item)
        db.addErrback(self.handle_error)
        return item

    def do_insert(self, conn, item):
        try:
            conn.execute(
                """INSERT INTO t_post(title,url,create_time,content) VALUES (%s,%s,%s,%s)""",
                (item['title'],
                 item['url'],
                 item['time'],
                 item['content']))
        except Exception as e:
            logging.warning(e)
            print("-----Failed to save data-----")

    def handle_error(self, failure, item, spider):
        logging.ERROR(failure)
