# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymysql
from youxi import settings

logger = logging.getLogger(__name__)


class YouxiPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DB,
                                    user=settings.MYSQL_USER, password=settings.MYSQL_PASSWD)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        try:
            self.cursor.execute('INSERT INTO t_post(title,url,create_time,content) VALUES ("{}","{}","{}","{}")'.format(item['title'], item['url'], item['time'], item['content']))
            self.conn.commit()
        except Exception as e:
            logging.warning(e)
            print("-----Failed to save data-----", e)

    def __del__(self):
        self.cursor.close()

