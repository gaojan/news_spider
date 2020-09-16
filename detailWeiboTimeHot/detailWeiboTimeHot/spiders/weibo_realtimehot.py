# -*- coding: utf-8 -*-
import scrapy
import json
import pymysql
import time
import datetime

from detailWeiboTimeHot import settings
from detailWeiboTimeHot.items import DetailweibotimehotItem


class WeiboRealtimehotSpider(scrapy.Spider):
    name = 'weibo_realtimehot'
    allowed_domains = ['m.weibo.cn']
    # start_urls = ['http://m.sina.cn/']

    def start_requests(self):
        conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DB,
                               user=settings.MYSQL_USER, password=settings.MYSQL_PASSWD)
        with conn.cursor() as cursor:
            cursor.execute("SELECT id,mobile_url FROM t_weibo_realtimehot ORDER BY createdt DESC LIMIT 50")
            urls = cursor.fetchall()
            for res in urls:
                url = res[1].replace('https://m.weibo.cn/search?', 'https://m.weibo.cn/api/container/getIndex?')
                yield scrapy.Request(url, callback=self.parse_list, dont_filter=True, meta={"meta": res[0]})

    def parse_list(self, response):
        res = json.loads(response.text)
        cards = res['data']['cards']
        for card in cards:
            card_group = card.get('card_group')
            if not card_group:
                continue
            for one_card_group in card_group:
                mblog = one_card_group.get('mblog')
                if not mblog:
                    continue
                attitudes_count = mblog['attitudes_count']  # 点赞数
                comments_count = mblog['comments_count']  # 评论数
                reposts_count = mblog['reposts_count']  # 转发数

                edit_at = mblog.get('edit_at')
                if edit_at:
                    pub = time.strptime(edit_at, '%a %b %d %H:%M:%S +0800 %Y')
                    pub_time = time.strftime('%Y-%m-%d %H:%M:%S', pub)  # 创建时间
                else:
                    created_at = mblog.get('created_at')  # '昨天 09:41'
                    if created_at:
                        print(created_at)
                        pub_time = self.get_time(created_at) + ':00'

                if mblog['isLongText']:
                    longTextContent = mblog['longText']['longTextContent']
                else:
                    longTextContent = mblog['text']
                url = 'https://m.weibo.cn/detail/' + mblog['id']

                user = mblog['user']
                user_id = user['id']
                follow_count = user['follow_count']  # 关注数量
                followers_count = user['followers_count']  # 粉丝数量
                screen_name = user['screen_name']  # 微博名称
                statuses_count = user['statuses_count']  # 微博数量
                urank = user['urank']  # 微博等级
                home_url = 'https://m.weibo.cn/profile/' + str(user_id)

                item = DetailweibotimehotItem()
                item['content'] = longTextContent.replace('"', r'\"').replace("'", r"\'")
                item['url'] = url
                item['wb_user'] = user_id
                item['wb_zf_count'] = reposts_count
                item['wb_comment_count'] = comments_count
                item['wb_zan_count'] = attitudes_count
                try:
                    item['pub_time'] = pub_time
                except Exception:
                    item['pub_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                item['wb_user_id'] = user_id
                item['wb_name'] = screen_name
                item['wb_gz'] = follow_count
                item['wb_fs'] = followers_count
                item['wb_count'] = statuses_count
                item['wb_level'] = urank
                item['home_url'] = home_url
                yield item

    @staticmethod
    def get_time(time_str):
        if '昨天' in time_str:
            time_str = time_str.replace("昨天", (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d'))
            return time_str
        elif len(time_str) == 10:
            return time_str + " 00:00"
        elif len(time_str) == 5:  # 01-01
            return datetime.datetime.now().strftime('%Y-{} 00:00'.format(time_str))
        elif "小时前" in time_str:  # 18小时前
            time_day = float(time_str.strip('小时前'))/24
            return (datetime.datetime.now() - datetime.timedelta(days=time_day)).strftime('%Y-%m-%d %H:%M')
