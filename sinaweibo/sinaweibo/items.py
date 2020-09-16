# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaweiboItem(scrapy.Item):

    # t_weibo
    # 微博内容
    content = scrapy.Field()
    # 内容url
    url = scrapy.Field()
    # 微博用户
    wb_user = scrapy.Field()
    # 转发数
    wb_zf_count = scrapy.Field()
    # 评论数
    wb_comment_count = scrapy.Field()
    # 点赞数
    wb_zan_count = scrapy.Field()
    # 发布时间
    pub_time = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()


    # t_weibo_user
    # 微博用户ID
    wb_user_id = scrapy.Field()
    # 微博名称
    wb_name = scrapy.Field()
    # 关注数量
    wb_gz = scrapy.Field()
    # 粉丝数量
    wb_fs = scrapy.Field()
    # 微博数量
    wb_count = scrapy.Field()
    # 微博等级
    wb_level = scrapy.Field()
    # 用户首页
    home_url = scrapy.Field()
