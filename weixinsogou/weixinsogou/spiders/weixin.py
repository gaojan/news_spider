# -*- coding: utf-8 -*-
import scrapy
import time
from weixinsogou.items import WeixinsogouItem


class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['weixin.sogou.com', 'mp.weixin.qq.com']
    start_urls = ['http://weixin.sogou.com/pcindex/pc/pc_{}/%s.html']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'pgv_pvid=3122494515; pgv_pvi=9065784320; pt2gguin=o0419914740; RK=BVJonqBgae; ptcz=2f7e75ef987b6510c2643aa7a4b0cc44bf6e22746d0c3f0d1f81fb8cb1c612bb; pac_uid=1_419914740; o_cookie=419914740; rewardsn=; wxtokenkey=777',
        'Host': 'mp.weixin.qq.com',
        'Upgrade-Insecure-Requests': '1'
    }

    def start_requests(self):

        for urls in [''.join(self.start_urls).format(n) for n in range(0, 22)]:
            for url in [urls % m for m in range(1, 16)]:
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """解析url"""
        if response.status == 200:
            node_list = response.xpath('//html/body/li')
            for node in node_list:
                t_url = node.xpath('./div[2]/h3/a/@href').extract_first()
                print(t_url)

                yield scrapy.Request(t_url, callback=self.parse_details, headers=self.headers)
        return None

    def parse_details(self, response):
        """解析详情"""
        item = WeixinsogouItem()

        item['url'] = response.url

        title = response.xpath('//*[@id="activity-name"]/text()').extract_first()
        item['title'] = title.strip()
        print(item['title'])

        t = item['url'].split('&')[1]
        t_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t.split('=')[1])))
        print(t_time)
        item['time'] = t_time

        content = ''.join(response.xpath('//*[@id="js_content"]/p/text()|//*[@id="js_content"]/section[1]/p/span/text()|'
                                         '//*[@id="js_content"]/section/section/section/section/section[3]/section/section[1]/section/section/section/p/text()|'
                                         '//*[@id="js_content"]/p/span/text()|//*[@id="js_content"]/p/span/span/text()|'
                                         '//*[@id="js_content"]/blockquote/p/span/text()|'
                                         '//*[@id="js_content"]/section/section/section/p/span/text()|'
                                         '//*[@id="js_content"]/section[1]/section/section[2]/p/text()').extract())
        item['content'] = content.replace('\t', '').replace('\n', '').replace('\u3000', '').replace('\u200b', '').replace('\xa0', '')

        print(item, "------")
        yield item
