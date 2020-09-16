# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from huodongxing import settings
from twisted.enterprise import adbapi

logger = logging.getLogger(__name__)
pymysql.install_as_MySQLdb()


class HuodongxingPipeline(object):
    def __init__(self):
        config = dict(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWD,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )

        self.dbpool = adbapi.ConnectionPool('MySQLdb', **config)

    def process_item(self, item, spider):
        db = self.dbpool.runInteraction(self.do_insert, item)
        db.addErrback(self.handle_error)
        return item

    def handle_error(self, failure, item, spider):
        logger.warning(failure)

    def do_insert(self, conn, item):
        insert_sql = """INSERT INTO t_activity(title,category,start_ts,end_ts,actoivity_source,content,price,publish_id,status,limit_persons,details_url,address,create_ts,update_ts) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params = (item['title'],
                  item['category'],
                  item['start_ts'],
                  item['end_ts'],
                  item['actoivity_source'],
                  item['content'],
                  item['price'],
                  item['publish_id'],
                  item['status'],
                  item['limit_persons'],
                  item['details_url'],
                  item['address'],
                  item['create_ts'],
                  item['update_ts'])
        try:
            conn.execute(insert_sql, params)

        except Exception as e:
            logger.warning(e)
            print("-----Failed to save data-----")
