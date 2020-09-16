# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from huodongxing.user_agents import User_Agents
from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
import logging
import random
import requests
import json

logger = logging.getLogger(__name__)


class RandomUserAgent(object):
    """随机用户头"""
    def process_request(self, request, spider):
        ua = random.choice(User_Agents)
        print("User_Agents >>> %s" % ua)
        request.headers['User_Agent'] = ua


class RandomProxy(object):
    """添加代理IP"""
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError,
                         ConnectError, ResponseNeverReceived, ValueError)

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        print('this is request ip>>>> %s' % proxy)
        logger.warning(msg='this is request ip:%s' % proxy)
        request.meta['proxy'] = proxy['ip_port']

    def process_response(self, request, response, spider):
        """对返回的response处理"""
        # 如果请求失败，重新请求
        if 200 != response.status:
            proxy = self.get_random_proxy()
            print('this is response ip>>>> %s' % proxy)
            logger.warning(msg='this is response ip:%s' % proxy)
            request.meta['proxy'] = proxy['ip_port']
            return request
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.DONT_RETRY_ERRORS):
            proxy = self.get_random_proxy()
            print('this is exception ip>>>> %s' % proxy)
            logger.warning(msg='this is exception ip:%s' % proxy)
            request.meta['proxy'] = proxy['ip_port']
            return request

    def get_random_proxy(self):
        """随机获取proxy"""
        url = "http://127.0.0.1:8080/?types=0&count=25&country=%E5%9B%BD%E5%86%85"
        res = requests.get(url)
        ip_ports = json.loads(res.text)

        proxy_list = []
        for proxy in ip_ports:
            ip = proxy[0]
            port = proxy[1]
            score = proxy[2]

            max_score = {}
            if int(score) > 9:
                max_score['ip_port'] = "http://" + ip + ":" + port
                proxy_list.append(max_score)

        proxy = random.choice(proxy_list)
        return proxy


class HuodongxingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HuodongxingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
