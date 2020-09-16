# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from WangYi163.items import Wangyi163Item


class War163Spider(CrawlSpider):
    name = 'war163'
    allowed_domains = ['baidu.com', 'war.163.com']
    # pn 为页数*10
    # base_url = 'https://www.baidu.com/s?wd=site:war.163.com&oq=site:war.163.com&ct=2097152&si=war.163.com&pn={}&'
    # start_time_int = 1535385600  # 2018-8-28  -86400 s/day
    base_urls = ['https://www.baidu.com/s?wd=site:war.163.com&oq=site:war.163.com&ct=2097152&si=war.163.com&pn={}&'
                 + 'gpc=stf={},{}|stftype=1'.format(1451577600 - 86400 * (i + 1), 1451577600 - 86400 * i) for i in
                 range(3650)]

    start_urls = []
    for b_url in base_urls:
        for i in range(5):
            start_urls.append(b_url.format(i * 10))

    rules = (
        Rule(LinkExtractor(allow=r'www.baidu.com/link'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'war.news.163.com/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'war.163.com/'), callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        if re.findall(r'http://war.163.com/\d+/\d+/\d+/\w+.html', response.url):
            item = Wangyi163Item()
            item['title'] = response.xpath('//title/text()').extract_first().replace("_网易军事", "")
            item['url'] = response.url
            item['category'] = "军事"
            content_list = response.xpath('//div[@id="endText"]/p/text()').extract()
            content_list = [content for content in content_list if (content and '原标题' not in content)]
            content = "".join(content_list)
            item['content'] = content
            yield item
        elif "special" in response.url:
            item = Wangyi163Item()
            item['url'] = response.url
            item['category'] = "军事"
            item['title'] = response.xpath('//title/text()').extract_first().replace("_网易军事", "")
            # '//td[@class="cDGray"]//text()'
            content_list = response.xpath('//table[@class="bg_white"]//text()').extract()
            content_list = [content for content in content_list if (content and '原标题' not in content)]
            content = "".join(content_list)
            item['content'] = content
            yield item
        elif "photoview" in response.url and "photoview_bbs" not in response.url:
            item = Wangyi163Item()
            item['url'] = response.url
            item['category'] = "军事"
            # '//td[@class="cDGray"]//text()'
            try:
                content_json = response.xpath('//textarea[@name="gallery-data"]/text()').extract_first()
                if content_json:
                    content_dict = json.loads(content_json)
                    item['title'] = content_dict["info"]["setname"].replace("_网易军事", "")
                    content_list = [content["note"].replace('\r', '') for content in content_dict["list"] if
                                    content["note"]]
                    content = "\r".join(content_list)
                    item['content'] = content
                    if content:
                        yield item
                else:
                    item['title'] = response.xpath('//title/text()').extract_first().replace("_网易军事", "")
                    item['content'] = response.xpath('//meta[@name="description"]/@content').extract_first()
                    yield item
            except Exception as e:
                print("错误 ：", response.url)
        else:
            print("无效网址：", response.url)
