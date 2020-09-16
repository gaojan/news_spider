# -*- coding: utf-8 -*-
import scrapy

from FuZhouGOV.items import FuzhougovItem


class FuzhouSpider(scrapy.Spider):
    name = 'fuzhou'
    allowed_domains = ['fuzhou.gov.cn']
    base_url = 'http://fuzhou.gov.cn/'

    # 工作动态=》榕城要闻、部门动态、政府会议、
    gzdt = ['gzdt/rcyw/', 'gzdt/bmdt/', 'gzdt/zfhy/']
    # 政策法规 =》地方性法规
    zcfg = ['zcfg/dfxfg/']
    # 政策解读=》本市政策文字解读、
    zcjd = ['zcjd/bs/bszcwzjd/']
    # 最新文件=》 市政府文件、市府办文件
    zxwj = ['zxwj/szfwj/', 'zxwj/sfbwj/']
    # 规划计划=》规划工作、国民经济和社会发展计划报告、总体规划、专项规划、年度计划、 规划解读
    ghjh = ['ghjh/ghdt/', 'ghjh/gmjjhshfzjhbg/', 'ghjh/ztgh/', 'ghjh/zxgh/', 'ghjh/ndjh/', 'ghjh/ghjd/']
    # 价格与收费=》价费公示、价费资讯
    jgysf = ['jgysf/jfgs/', 'jgysf/jfzx/', 'jgysf/jfjg/']
    # 统计信息=》统计月报、季度统计、年度报告、统计分析
    tjxx = ['tjxx/tjyb/', 'tjxx/jdtj/', 'tjxx/ndbg/', 'tjxx/tjfx/']
    # 城乡建设=》城乡建设动态、城乡建设规划、城乡建设管理、城乡建设进展
    chxjs = ['chxjs/cxjsdt/', 'chxjs/cxjsgh/', 'chxjs/cxjsgl/', 'chxjs/cxjsjz/']
    # 人事信息=》任前公示、人事任免
    rsxx = ['rsxx/rqgs/', 'rsxx/rsrm/']

    def start_requests(self):
        all_end_urls = self.gzdt + self.zcfg + self.zcjd + self.zxwj + self.ghjh + self.jgysf +\
                       self.tjxx + self.chxjs + self.rsxx
        start_urls = [self.base_url + end_url for end_url in all_end_urls]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list, dont_filter=False)
        # yield scrapy.Request('',self.parse_detail)

    def parse_list(self, response):
        urls = response.xpath('//div[@ms-visible="showStatic"]/div/a/@href').extract()
        for url in urls:
            url = response.url + url if "http:" not in url else url
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = FuzhougovItem()
        item['url'] = response.url

        item['title'] = response.xpath('//meta[@name="ArticleTitle"]/@content').extract_first()
        if not item['title']:
            item['title'] = response.xpath('//title/text()').extract_first()

        item['time'] = response.xpath('//meta[@name="PubDate"]/@content').extract_first()
        if not item['time']:  # http://scjg.fuzhou.gov.cn/zzbz/zcjd_10863/bszcjd/201809/t20180903_2565259.htm
            item['time'] = response.xpath('//span[@class="xl_sj_icon"]/text()').extract_first()
            if item['time']:
                item['time'] = item['time'].split("：")[-1]
        if not item['time']:  # http://tzcjj.fuzhou.gov.cn/zz/xxgk/zcjd/201808/t20180831_2564274.htm
            item['time'] = response.xpath('//div[@class="txtleft"]/text()').extract_first()
            if item['time']:
                item['time'] = item['time'].split('\u3000')[0].split("：")[-1]

        if 'http://fuzhou' not in response.url:
            content_list = response.xpath('//div[@class="TRS_Editor"]//p/span/text()|'
                                          '//div[@class="TRS_Editor"]//p/b/text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/p//text()').extract()
        else:
            content_list = response.xpath('//div[@class="Custom_UnionStyle"]/p/text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/div/p//text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/p/span//text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/div[@class="Custom_UnionStyle"]/span/p/text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/p//text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/font//text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/div//text()').extract()
            # if not content_list:
            #     content_list = response.xpath('//p[@class="Custom_UnionStyle"]/div/p//text()').extract()
            if not content_list:
                content_list = response.xpath('//div[@class="TRS_Editor"]/text()').extract()
            # content_list = response.xpath('//div[@id="js_content"]/p/text()').extract()

        content_list = [content.replace('\u3000', '').replace('\xa0', '').replace('\n', '') for content in content_list]
        content_list = [content for content in content_list if content != "\n"]
        content = "".join(content_list)
        item['content'] = content
        if item['content']:
            yield item


