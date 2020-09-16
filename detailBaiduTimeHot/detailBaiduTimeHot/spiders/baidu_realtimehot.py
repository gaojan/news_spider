# -*- coding: utf-8 -*-
import scrapy
import pymysql
from detailBaiduTimeHot import settings
from detailBaiduTimeHot.items import DetailbaidutimehotItem


class BaiduRealtimehotSpider(scrapy.Spider):
    name = 'baidu_realtimehot'
    allowed_domains = ['baidu.com']
    # start_urls = ['http://baidu.com/']

    def start_requests(self):
        conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DB,
                               user=settings.MYSQL_USER, password=settings.MYSQL_PASSWD)
        with conn.cursor() as cursor:
            cursor.execute("SELECT id,url FROM t_baidu_realtimehot ORDER BY createdt DESC LIMIT 50")
            urls = cursor.fetchall()
            # urls = [url[0] for url in urls]
            for url in urls:
                yield scrapy.Request(url[1], callback=self.parse_list, dont_filter=True, meta={"meta": url[0]})

    def parse_list(self, response):
        realtimehot_keyword_id = response.meta['meta']
        nodes = response.xpath('//div[@id="content_left"]/div[@class="result-op c-container xpath-log"][1]/div/div')
        for node in nodes:
            href = node.xpath('./a/@href').extract_first()
            yield scrapy.Request(href, callback=self.parse_detail, meta={"meta": realtimehot_keyword_id})

    def parse_detail(self, response):
        realtimehot_keyword_id = response.meta['meta']
        item = DetailbaidutimehotItem()
        title = response.xpath('//title/text()').extract_first()
        time_str = response.xpath('//meta[@itemprop="dateUpdate"]/@content').extract_first()
        content_list = response.xpath('//div[@class="article-content"]/p/span/text()|'
                                      '//div[@class="article-content"]/p/text()').extract()
        content = "".join(content_list)
        item['content'] = content.encode().decode('utf-8')
        item['title'] = title
        item['time'] = time_str
        item['url'] = response.url
        item['realtimehot_keyword_id'] = realtimehot_keyword_id
        yield item
