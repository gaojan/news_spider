# -*- coding: utf-8 -*-
import scrapy
import time

from HongKongGOV.items import HongkonggovItem


class HongkongSpider(scrapy.Spider):
    name = 'hongkong'
    allowed_domains = ['info.gov.hk', 'www.news.gov.hk']
    # start_urls = ['http://info.gov.hk/']
    BASE_URL = 'https://www.news.gov.hk'
    TIME_FORMAT = '%Y%m%d'
    lambda_repl = lambda text: text.replace("\r\n", "").replace("\u3000", "").replace("\t", "").replace("\n", "")

    def start_requests(self):
        time1 = int(time.time() * 1000)
        time2 = time1 + 42
        base_url = "https://www.news.gov.hk/jsp/TickerNewsArticle.jsp?language=chi&max=35&presentation=IndexTicker" \
                   ".xsl&time={}&_={}"
        xwsd_url = base_url.format(time1, time2)
        # 新聞速遞
        yield scrapy.Request(url=xwsd_url, callback=self.parse_xwsd, dont_filter=True)
        # 新聞公報
        xwgb_url = "https://www.news.gov.hk/common/feedin/pressreleases/publish_area/pressreleasesHK.xml"
        yield scrapy.Request(url=xwgb_url, callback=self.parse_xwgb, dont_filter=True)

    def parse_xwsd(self, response):
        urls = response.xpath("//ul/li/a[1]/@href").extract()
        for url in urls:
            time_str = url.split('/')[4]
            if self.check_time(time_str, self.TIME_FORMAT):  # 判断时间是否在需要时间之内
                print(url)
                yield scrapy.Request(url=self.BASE_URL + url, callback=self.parse_xwsd_detail)

    def parse_xwsd_detail(self, response):
        """新聞速遞详情内容"""
        item = HongkonggovItem()
        item['title'] = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        time_str = response.xpath('//meta[@name="date"]/@content').extract_first()
        item['time'] = time_str.split("+")[0]
        item['url'] = response.url
        content_list = response.xpath('//div[@class="newsdetail-content mt-3"]/p/text()').extract()
        content = "".join(content_list)
        item['content'] = content.replace('\xa0', '\n').replace('\u3000', '')
        yield item

    def parse_xwgb(self, response):
        urls = response.xpath('//item/link/text()').extract()
        for url in urls:
            time_str = "".join(url.split("/")[5:7])
            if self.check_time(time_str, self.TIME_FORMAT):  # 判断时间是否在限定范围内
                print(url)
                yield scrapy.Request(url=url, callback=self.parse_xwgb_detail)

    def parse_xwgb_detail(self, response):
        """新聞速遞详情内容"""
        item = HongkonggovItem()
        item['title'] = response.xpath('//title/text()').extract_first()
        time_str = response.xpath('//div[@class="mB15 f15"]/text()').extract()
        dtime_str = time_str[1].split('（')[0].replace("年", "-").replace("月", "-").replace("日", "-")
        ttime_str = time_str[-1].split('間')[-1].replace("時", "-").replace("分", "")
        item['time'] = dtime_str + ttime_str
        item['url'] = response.url
        content_list = response.xpath('//span[@id="pressrelease"]//text()').extract()
        content = [content for content in content_list if content or content != "\r\n"]
        content = list(map(lambda text: text.replace("\xa0", "").replace("\r\n", "").replace("\u3000", "").replace("\t", "").replace("\n", ""), content))
        # print(content)
        content = "\n".join(content)
        item['content'] = content.replace("\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n")
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
