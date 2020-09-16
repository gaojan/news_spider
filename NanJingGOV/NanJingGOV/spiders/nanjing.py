# -*- coding: utf-8 -*-
import scrapy
import time
from NanJingGOV.items import NanjinggovItem


class NanjingSpider(scrapy.Spider):
    name = 'nanjing'
    allowed_domains = ['nanjing.gov.cn']
    # 政务要闻、部门动态、各区动态、领导活动、图片新闻、民生资讯、便民提示
    href_ends = ["mjxw", "bmkx", "gqdt", "ldhd", "tpxw", "mszx", "bmts"]
    start_urls = ['http://www.nanjing.gov.cn/xxzx/{}'.format(href_end) for href_end in href_ends]

    # start_urls = ['http://www.nanjing.gov.cn/xxzx/gqdt/']
    TIME_FORMAT = '%Y-%m-%d'

    # BASE_URL =

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        nodes = response.xpath('//ul[@class="universal_overview_con"]/li')[:-1]
        is_next_page = True  # 记录最后一篇时间是否在时间之内，如果不在则不访问下一页
        now_url = "/".join(response.url.split("/")[0:-1])+"/" if "index_" in response.url else response.url

        for node in nodes:
            detail_href = now_url + node.xpath('./span[2]/a/@href').extract_first()
            print(detail_href)
            time_str = node.xpath('./span[@class="time"]/text()').extract_first()
            check_time = self.check_time(time_str, self.TIME_FORMAT)
            is_next_page = check_time
            if check_time:  # 规定时间范围内才爬取
                yield scrapy.Request(url=detail_href, callback=self.parse_detail)
        if is_next_page:
            # 获取下一页
            if "index_" not in response.url:
                next_page = "index_1.html"
            else:
                now_page_index = response.url.split("/")[-1]
                page_index = now_page_index.split(".")[0].split("_")[-1]
                next_page = "index_{}.html".format(str(int(page_index) + 1))
            yield scrapy.Request(url=now_url + next_page, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        item = NanjinggovItem()
        item['title'] = response.xpath('//meta[@name="ArticleTitle"]/@content').extract_first()
        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first()
        item['url'] = response.url
        content_list = response.xpath('//div[@class="TRS_Editor"]/p//text()|//div[@id="con"]/p/text()').extract()
        if not content_list:
            content_list = response.xpath('//div[@class="TRS_Editor"]/div/p/text()').extract()

        content = "".join(content_list)
        item['content'] = content
        yield item

    def check_time(self, time_string, format_string, days_ago=7):
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
