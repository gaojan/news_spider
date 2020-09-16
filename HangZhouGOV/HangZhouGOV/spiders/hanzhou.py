# -*- coding: utf-8 -*-
import scrapy
import re
import time
from HangZhouGOV.items import HangzhougovItem


class HanzhouSpider(scrapy.Spider):
    name = 'hangzhou'
    allowed_domains = ['hangzhou.gov.cn']
    start_urls = ['http://hangzhou.gov.cn/']

    base_url = "http://www.hangzhou.gov.cn/col/{}/index.html"
    swdt = ["col812258", "col812259"]  # 市委动态 a
    zfdt = ["col812260", "col812261", "col812262"]  # 政府动态 b
    zhdt = ["col812255"]  # 综合动态 b
    bmdt = ["col812266", "col812267", "col812268", "col812269", "col812270"]  # 部门动态 a
    qxzc = ["col812264", "col812265"]   # 区县之窗
    col_numbers = swdt + zfdt + zhdt + bmdt + qxzc

    TIME_FORMAT = "[%Y-%m-%d]"

    def start_requests(self):
        urls = [self.base_url.format(col_number) for col_number in self.col_numbers]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        response_text = response.text
        nodes = re.findall(r'<td height="24"><a href="([^"]*)?" target="_blank" title="(.*)?">(.*)?</a>([^<]*)?</td>',response_text)
        if not nodes:
            nodes = re.findall(r"href='([^']*)?' class='bt_link' title='(.*)?' target=.*?>([^<]*)?</a.*?an class='bt_time'>([^<]*)?</span>",response_text)
        for node in nodes:
            if self.check_time(node[-1], self.TIME_FORMAT):
                item = HangzhougovItem()
                # print(node)  # ('/art/2018/8/23/art_812264_20729342.html','滨江：教育强区','滨江：教育强区','[2018-08-23]')
                url = "http://www.hangzhou.gov.cn" + node[0]
                item["url"] = url
                item["title"] = node[1]
                item["time"] = node[-1][1:-1]  # [2018-08-22] ==> 2018-08-22
                yield scrapy.Request(url=url, callback=self.parse_detail, meta={"meta": item})

    def parse_detail(self, response):
        item = response.meta["meta"]

        content_list = response.xpath('//div[@id="zoom"]/p/text()').extract()
        content = "".join(content_list)
        print(content)
        item["content"] = content.replace("\u3000", "")
        yield item

    def check_time(self, time_string, format_string, days_ago=7):
        # 算出时间秒数
        # days_ago = datetime.timedelta(days=days_ago)
        # days_sec = days_ago.total_seconds()
        days_sec = 60 * 60 * 24 * days_ago

        old = time.mktime(time.strptime(time_string, format_string))
        now = time.time()
        if now - old > days_sec:
            return False
        return True