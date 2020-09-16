# -*- coding: utf-8 -*-
import re
import json
import scrapy
import logging
from huodongxing.activity_category import category_list
from huodongxing.utlis import str_to_datetime, now_time
from huodongxing.items import HuodongxingItem


class HuodongSpider(scrapy.Spider):
    name = 'huodong'
    allowed_domains = ['huodongxing.com']

    def start_requests(self):
        for i in range(1, 1118):
            start_link = 'http://www.huodongxing.com/events?orderby=o&city=%E5%85%A8%E9%83%A8&page={0}'.format(i)
            yield scrapy.Request(start_link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """列表页"""
        nodelist = response.xpath('//section[@class="Nav-search"]/div[2]/div[2]/div')

        item = HuodongxingItem()
        for node in nodelist:
            title = node.xpath('./a/img/@alt').extract_first()
            if title:
                item['title'] = title.strip()

            details_url = node.xpath('./a/@href').extract_first()
            if details_url:
                item['details_url'] = "http://www.huodongxing.com" + details_url

            address = node.xpath('./a/div[1]/div[2]/p/text()').extract_first()
            if address:
                item['address'] = address.strip()

        yield scrapy.Request(item['details_url'], callback=self.parse_detail, meta={'meta': item})

    def parse_detail(self, response):
        """详情页"""
        temp = response.meta['meta']

        # 活动类型
        category = response.xpath('//*[@id="container-lg"]/div[4]/div[7]/a/text()').extract_first()
        if category_list.get(category) is not None:
            temp['category'] = category_list.get(category.strip())
        else:
            temp['category'] = 39  # 其他

        # 开始时间 结束时间
        time_str = response.xpath('//*[@id="container-lg"]/div[1]/div/div[1]/text()[2]').extract_first()
        if time_str:
            start_ts = time_str.split('～')[0].strip()
            end_ts = time_str.split('～')[1].strip()
            try:
                temp['start_ts'] = str_to_datetime(start_ts)
                temp['end_ts'] = str_to_datetime(end_ts)
            except:
                temp['start_ts'] = None
                temp['end_ts'] = None


        # 活动内容
        content = "".join(response.xpath('//*[@id="event_desc_page"]/p/span/text()|'
                                         '//*[@id="event_desc_page"]/p/text()|'
                                         '//*[@id="event_desc_page"]/section/section/section/section/p/text()|'
                                         '//*[@id="event_desc_page"]/div/section/section/section/section/p/text()').extract())

        con = content.replace('\u200b', '').replace('\t', '').replace('\u3000', '').replace('\n', '').replace('\xa0', '')
        if 0 != len(re.findall('\S', con)):
            temp['content'] = con

        else:
            content = "".join(re.findall(u"[\u4e00-\u9fa5]+", "".join(response.xpath('//*[@id="event_desc_page"]/*').extract())))
            temp['content'] = content.strip()

        # 活动价格 0免费
        res0 = re.findall('var\seventTicketsJson\s=\s\[(.*?)\];', response.text)
        res1 = re.findall('{.*?}', res0[0])
        price = json.loads(res1[0], encoding='utf-8')

        if price['PriceStr'] == r'免费':
            temp['price'] = 0
        else:
            PriceStr = price['PriceStr']
            try:
                temp['price'] = int(float(PriceStr.replace('¥', ''))/0.01)   # 金额转整型 单位/分
            except:
                temp['price'] = None

        # 活动状态 1 报名中 2 进行中 3 结束
        status = response.xpath('//*[@id="btn_register_main"]/text()').extract_first()
        if status:
            if status == '我要报名':
                temp['status'] = 1
            if status == '活动已结束':
                temp['status'] = 3
        else:
            temp['status'] = None

        # 可参加的人数
        limit_persons = response.xpath('//*[@id="container-lg"]/div[1]/div/div[3]/text()[2]').extract_first()
        if limit_persons:
            try:
                temp['limit_persons'] = int("".join(re.findall('\d+', limit_persons)))
            except:
                temp['limit_persons'] = None

        # 创建时间 和更新时间
        temp['create_ts'] = now_time()
        temp['update_ts'] = now_time()

        # 发布者ID  1 活动行
        temp['publish_id'] = 1
        # 活动来源 1 来源第三方
        temp['actoivity_source'] = 1

        item = temp
        print(item, "-----")
        return item
