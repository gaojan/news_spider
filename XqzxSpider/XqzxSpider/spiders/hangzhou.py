# -*- coding: utf-8 -*-
import scrapy
import re
import time
from XqzxSpider.spiders.basespider import BaseSpider


class HangzhouSpider(BaseSpider):
    name = 'hangzhou'
    allowed_domains = ['hangzhou.gov.cn']
    base_url = "http://www.hangzhou.gov.cn/col/"
    col_dict = {'col812259': '4037001', 'col812258': '4037001', 'col812260': '4037001',
                'col812261': '4037001', 'col812262': '4037001', 'col812255': '4037001',
                'col812266': '4037020', 'col812267': '4037020', 'col812268': '4037020',
                'col812269': '4037020', 'col812270': '4037020', 'col812264': '4037020',
                'col812265': '4037020', 'col812254': '4038209'}

    # http://www.hangzhou.gov.cn/col/col812259/index.html?uid=4037001&pageNum=1  市委动态 活动  135页
    # http://www.hangzhou.gov.cn/col/col812258/index.html?uid=4037001&pageNum=3  市委动态 会议  139页
    # http://www.hangzhou.gov.cn/col/col812260/index.html?uid=4037001&pageNum=2  政府动态 会议   214页
    # http://www.hangzhou.gov.cn/col/col812261/index.html?uid=4037001&pageNum=2  政府动态 活动   237页
    # http://www.hangzhou.gov.cn/col/col812262/index.html?uid=4037001&pageNum=2  政府动态 服务   757页
    # http://www.hangzhou.gov.cn/col/col812255/index.html?uid=4037001&pageNum=2  党政动态 综合   356页
    # http://www.hangzhou.gov.cn/col/col812266/index.html?uid=4037020&pageNum=4  部门动态 工经   256页
    # http://www.hangzhou.gov.cn/col/col812267/index.html?uid=4037020&pageNum=2  部门动态 农业   116页
    # http://www.hangzhou.gov.cn/col/col812268/index.html?uid=4037020&pageNum=2  部门动态 旅贸   188页
    # http://www.hangzhou.gov.cn/col/col812269/index.html?uid=4037020&pageNum=2  部门动态 城建   324页
    # http://www.hangzhou.gov.cn/col/col812270/index.html?uid=4037020&pageNum=2  部门动态 文卫   544页
    # http://www.hangzhou.gov.cn/col/col812264/index.html?uid=4037020&pageNum=2  区县之窗 城区   706页
    # http://www.hangzhou.gov.cn/col/col812265/index.html?uid=4037020&pageNum=2  区县之窗 县市   297页
    # http://www.hangzhou.gov.cn/col/col812254/index.html?uid=4038209&pageNum=2  图片信息  62页

    def start_requests(self):
        for k, v in self.col_dict.items():
            start_url = [self.base_url+k+'/index.html?uid='+v+'&pageNum={}'.format(page) for page in range(1, 3)]
            for url in start_url:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        nodes = re.findall(r'<td height="24"><a href="([^"]*)?" target="_blank" title="(.*)?">(.*)?</a>([^<]*)?</td>', response.text)
        if not nodes:
            nodes = re.findall(r"href='([^']*)?' class='bt_link' title='(.*)?' target=.*?>([^<]*)?</a.*?an class='bt_time'>([^<]*)?</span>", response.text)

        for node in nodes:
            url = "http://www.hangzhou.gov.cn" + node[0]
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_title(self, response, item):
        item['title'] = response.xpath('//meta[@name="title"]/@content').extract_first().strip()

    def parse_time(self, response, item):
        item['time'] = response.xpath('//meta[@name="pubDate"]/@content').extract_first().strip()

    def parse_content(self, response, item):
        content_list = response.xpath('//div[@id="zoom"]/p/text()').extract()
        if not content_list:
            item['content'] = ''
        else:
            item['content'] = self.content_to(content_list)
