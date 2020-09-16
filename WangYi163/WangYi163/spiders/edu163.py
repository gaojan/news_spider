# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from WangYi163.items import Wangyi163Item


class Edu163Spider(CrawlSpider):
    name = 'edu163'
    allowed_domains = ['baidu.com', 'edu.163.com']
    # pn 为页数*10
    # base_url = 'https://www.baidu.com/s?wd=site:edu.163.com&oq=site:edu.163.com&ct=2097152&si=edu.163.com&pn={}&'
    # start_time_int = 1535385600  # 2018-8-28  -86400 s/day
    base_urls = ['https://www.baidu.com/s?wd=site:edu.163.com&oq=site:edu.163.com&ct=2097152&si=edu.163.com&pn={}&'
                 + 'gpc=stf={},{}|stftype=1'.format(1535558400-86400*(i+1), 1535558400-86400*i) for i in range(3650)]

    start_urls = []
    for b_url in base_urls:
        for i in range(5):
            start_urls.append(b_url.format(i*10))

    rules = (
        Rule(LinkExtractor(allow=r'www.baidu.com/link'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'edu.news.163.com'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'edu.163.com'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if re.findall(r'http://edu.163.com/\d+/\d+/\d+/\w+.html', response.url):
            item = Wangyi163Item()
            item['title'] = response.xpath('//title/text()').extract_first().split("_")[0]
            item['url'] = response.url
            item['category'] = "教育"
            content_list = response.xpath('//div[@id="endText"]/p/text()|'
                                          '//div[@class="articon"]//text()').extract()
            content_list = [content for content in content_list if (content and '原标题'not in content)]
            content_list = set(content_list)
            content = "".join(content_list)
            item['content'] = content
            yield item
        elif "special" in response.url:  #
            item = Wangyi163Item()
            item['url'] = response.url
            item['category'] = "教育"
            item['title'] = response.xpath('//title/text()').extract_first().split("_")[0]
            # http://edu.163.com/special/en_xx08/
            content_list = response.xpath('//div[@class="main_artc"]/p/text()|'
                                          '//table[@class="bg_white"]//p/text()|'
                                          '//table[@width="960"]//span/text()|'  # http://edu.163.com/special/njd33/
                                          '//div[@class="slidemain"]/a/@title|'
                                          '//p[@class="paragraph"]/text()|'
                                          '//div[@class="post_desc"]/text()|'
                                          '//div[@id="endText"]//text()|'
                                          '//div[@class="post_text"]//p/text()|'
                                          '//body/div/div/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/text()').extract()  # http://edu.163.com/special/overseas16/
            # if not content_list:  # http://edu.163.com/special/njd33/
            #     content_list = response.xpath('//table[@width="960"]//span/text()').extract()
            # if not content_list:  # http://edu.163.com/special/overseas16/
            #     content_list = response.xpath('//div[@class="slidemain"]/a/@title').extract()

            content_list = [content for content in content_list if (content and '原标题' not in content)]
            content_list = set(content_list)
            content = "".join(content_list)
            item['content'] = content
            yield item
        elif "photoview" in response.url and "photoview_bbs" not in response.url:
            item = Wangyi163Item()
            item['url'] = response.url
            item['category'] = "教育"
            # '//td[@class="cDGray"]//text()'
            try:
                content_json = response.xpath('//textarea[@name="gallery-data"]/text()').extract_first()
                if content_json:
                    content_dict = json.loads(content_json)
                    item['title'] = content_dict["info"]["setname"].split("_")[0]  # 去掉 '_网易**'
                    if content_dict['list'][0]['title']:
                        content_list = [content["title"].replace('\r', '') for content in content_dict["list"] if content["title"]]
                    content_list = [content["note"].replace('\r', '') for content in content_dict["list"] if content["note"]]
                    content_list = set(content_list)
                    content = "\r".join(content_list)
                    item['content'] = content
                    if content:
                        yield item
                else:
                    item['title'] = response.xpath('//title/text()').extract_first().split("_")[0]
                    item['content'] = response.xpath('//meta[@name="description"]/@content').extract_first()
                    yield item
            except Exception as e:
                print("错误 ：", e)
                print("错误 ：", response.url)
        else:
            print("无效网址：", response.url)
