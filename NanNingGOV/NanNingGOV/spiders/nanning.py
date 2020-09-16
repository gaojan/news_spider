# -*- coding: utf-8 -*-
import scrapy
import time

from NanNingGOV.items import NanninggovItem


class NanningSpider(scrapy.Spider):
    name = 'nanning'
    allowed_domains = ['nanning.gov.cn']
    # 南宁要闻、部门动态、县区动态、图片新闻、视频报道、公共公示、领导活动、政府会议、（视频报道spxw 无文字已去掉）
    url_ends = ['jrnn/2018nzwdt/', 'bmdt', 'xqdt', 'tpxw', 'gggs', 'ldhd', 'zfhy']
    base_url = 'http://www.nanning.gov.cn/NNNews/'
    TIME_FORMAT = '[%Y-%m-%d]'

    def start_requests(self):
        # 信息公开
        start_urls = [self.base_url + url_end for url_end in self.url_ends]
        start_urls = ['http://www.nanning.gov.cn/NNNews/jrnn/2018nzwdt/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        nodes = response.xpath('//div[@class="list_show"]/ul/li')
        # 此时所在目录。用来构造detail页和下一页
        now_url = "/".join(response.url.split("/")[0:-1])+"/" if "index_" in response.url else response.url
        next_page = True  # 标记是否爬取下一页
        for node in nodes:
            time_str = node.xpath('./span/text()').extract_first()
            if self.check_time(time_str, self.TIME_FORMAT):
                url = node.xpath('./a/@href').extract_first()
                yield scrapy.Request(url=now_url+url, callback=self.parse_detail)
            else:
                next_page = False
        if next_page:
            if "index_" not in response.url:
                next_page_end = "index_1.html"
            else:
                now_page_index = response.url.split("/")[-1]
                page_index = now_page_index.split(".")[0].split("_")[-1]
                next_page_end = "index_{}.html".format(str(int(page_index) + 1))
            yield scrapy.Request(url=now_url + next_page_end, callback=self.parse_list, dont_filter=True)

    def parse_detail(self, response):
        item = NanninggovItem()
        item['title'] = response.xpath('//title/text()').extract_first()
        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first()
        item['url'] = response.url
        content_list = response.xpath('//div[@id="content"]/div/p/text()|'
                                      '//div[@class="con_main"]/p/text()|'
                                      '//div[@class="TRS_Editor"]/p/text()').extract()
        content_list = [content.replace("\n", "").replace("\r", "").replace("\r\n", "") for content in content_list]
        item['content'] = "\r".join(content_list).replace("\u3000", "").replace("\xa0", "")
        yield item

    def check_time(self, time_string, format_string, days_ago=8):
        """
        是否在规定时间内，days_ago
        :param time_string: [2018-08-22]
        :param format_string: [%Y-%m-%d]
        :param days_ago: int
        :return:
        """
        # 算出时间秒数
        # days_ago = datetime.timedelta(days=days_ago)
        # days_sec = days_ago.total_seconds()
        days_sec = 60 * 60 * 24 * days_ago

        old = time.mktime(time.strptime(time_string, format_string))
        now = time.time()
        if now - old > days_sec:
            return False
        return True
