#!usr/bin/env python  
# -*- coding: utf-8 -*- 
"""
# Author: Jan Gao 
# Date: 2018/5/29
# Description: 
# Site: http://www.xrtpay.com/
# Copyright (c) ShenZhen XinRuiTai Payment Service Co.,Ltd. All rights reserved 
"""

import requests
import random
import json
import re

#
# def huodongxing():
#
#     url = "http://www.huodongxing.com/event/9441998670300?utm_source=%E5%8F%91%E7%8E%B0%E6%B4%BB%E5%8A%A8%E9%A1%B5&utm_medium=&utm_campaign=eventspage"
    # proxies_list = ['http://123.231.236.147:8080', 'http://123.231.228.122:3128', 'http://123.219.105.200:8080',
    #                 'http://123.138.89.133:9999', 'http://123.134.87.136:61234', 'http://122.183.139.107:8080',
    #                 'http://122.147.206.8:53281', 'http://121.206.242.90:53281', 'http://120.26.110.59:8080']
    # http_proxies = random.choice(proxies_list)
    # proxies = {
    #     'http': http_proxies
    # }
#
#
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Host': 'www.huodongxing.com',
#         'Pragma': 'no-cache',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
#     }
#
#       # cookies = {'route': 'd2c7c0352d7addaaa4af66b05a965f69', 'ASP.NET_SessionId': 'kdk45th3h0cq1uxvmonwjhqo',
    #            'HDX_REGION': '%e5%b9%bf%e4%b8%9c%2c%e6%b7%b1%e5%9c%b3', '_gid': 'GA1.2.1784386452.1527765360',
    #            'Hm_lvt_d89d7d47b4b1b8ff993b37eafb0b49bd': '1527765360', '_ga': 'GA1.2.226929382.1527765360',
    #            'Hm_lpvt_d89d7d47b4b1b8ff993b37eafb0b49bd': '1527765378', '_gat': '1'}

#     cookies = {}
#     for i in temp_cookies.split('; '):
#         cookies[i.split('=')[0]] = i.split('=')[1]
#         print(cookies)
#     res = requests.get(url).text
#     print(res)




    # str_res = 'var eventTicketsJson = [{"SN":1,"Status":0,"Price":0,"Currency":"RMB","Title":"免费票","Description":"","Desc":"","Quantity":100,"SoldNumber":84,"BookNumber":0,"BookStart":null,"BookEnd":null,"QuantityUnit":1,"MinOrder":1,"MaxOrder":1,"NeedApply":true,"EffectiveDate":null,"ExpiredDate":null,"Group":null,"CouponId":0,"Enabled":true,"BookPeriodStr":null,"EffectPeriodStr":null,"StatusStr":"报名中","OrderNums":[1],"IsSeriesTicket":false,"PriceStr":"免费","SrcPriceStr":null,"Discount":null,"Token":null},{"SN":1,"Status":0,"Price":0,"Currency":"RMB","Title":"免费票","Description":"","Desc":"","Quantity":100,"SoldNumber":84,"BookNumber":0,"BookStart":null,"BookEnd":null,"QuantityUnit":1,"MinOrder":1,"MaxOrder":1,"NeedApply":true,"EffectiveDate":null,"ExpiredDate":null,"Group":null,"CouponId":0,"Enabled":true,"BookPeriodStr":null,"EffectPeriodStr":null,"StatusStr":"报名中","OrderNums":[1],"IsSeriesTicket":false,"PriceStr":"免费","SrcPriceStr":null,"Discount":null,"Token":null}];'
    # res0 = re.findall('var\seventTicketsJson\s=\s\[(.*?)\];', str_res)
    # print(len(res0), type(res0), res0 )
    # res1 = re.findall('{.*?}', res0[0])
    # print(len(res1), type(res1), res1)
    # for i in res1:
    #     print(type(i), len(i), i)


# if __name__ == '__main__':
