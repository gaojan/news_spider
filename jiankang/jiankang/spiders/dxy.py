import scrapy
from jiankang.items import JiankangItem


class DxySpider(scrapy.Spider):
    name = 'dxy'
    allowed_domains = ['dxy.cn']

    def start_requests(self):
        yield scrapy.Request(url='http://www.dxy.cn/', callback=self.parse_href, dont_filter=True)

    def parse_href(self, response):
        href_list = response.xpath('//div[@class="navlst2"]/ul/li/a/@href').extract()
        print(href_list)
        href_list = [href + "tag/news" for href in href_list]

        for href in href_list:
            yield scrapy.Request(url=href, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):
        href_list = response.xpath('//a[@class="b110x75"]/@href').extract()
        for href in href_list:
            yield scrapy.Request(url=href, callback=self.parse_detail)

    def parse_detail(self, response):
        item = JiankangItem()
        item['title'] = response.xpath('//title/text()').extract_first()
        content_list = response.xpath('//div[@id="content"]//p/text()|'
                                      '//div[@id="content"]//p/span/text()').extract()
        item['content'] = "".join(content_list)
        item['url'] = response.url
        time_str = response.xpath('//div[@class="sum"]/span[1]/text()').extract_first().strip('\n').strip(' ').strip('\n')
        item['create_time'] = time_str[:-6]
        yield item