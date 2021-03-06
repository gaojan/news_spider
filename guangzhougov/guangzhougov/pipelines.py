# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from guangzhougov import settings
from twisted.enterprise import adbapi
import pymysql

logger = logging.getLogger(__name__)
pymysql.install_as_MySQLdb()


class DbPipeline(object):
    def __init__(self):
        config = dict(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **config)

    def process_item(self, item, spider):
        db = self.dbpool.runInteraction(self.do_insert, item)
        db.addErrback(self.handle_error)
        return item

    def do_insert(self, conn, item):
        try:
            conn.execute(
                """INSERT INTO t_post(title,url,create_time,content)VALUES (%s,%s,%s,%s)""",
                (item['title'],
                 item['url'],
                 item['time'],
                 item['content']))

        except Exception as e:
            logger.warning(e)
            print('-----Failed to save data-----')

    def handle_error(self, failure, item, spider):
        logger.warning(failure)


class GuangzhougovPipeline(object):
    def process_item(self, item, spider):
        return item
