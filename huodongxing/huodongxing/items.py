# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuodongxingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()             # 活动标题
    category = scrapy.Field()          # 活动类型
    start_ts = scrapy.Field()          # 活动开始时间
    end_ts = scrapy.Field()            # 活动结束时间
    actoivity_source = scrapy.Field()  # 活动来源 1.来源第三方 2 自己添加
    content = scrapy.Field()           # 活动内容
    price = scrapy.Field()             # 活动价格 0 免费
    publish_id = scrapy.Field()        # 发布者ID 如果来源于第三方，则是第三方的ID
    status = scrapy.Field()            # 活动的状态1报名中 2进行中 3 结束
    limit_persons = scrapy.Field()     # 可参加的人数
    details_url = scrapy.Field()       # 活动详情URL
    address = scrapy.Field()           # 活动地址
    create_ts = scrapy.Field()         # 创建时间
    update_ts = scrapy.Field()         # 更新时间
