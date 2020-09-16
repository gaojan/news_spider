#!usr/bin/env python  
# -*- coding: utf-8 -*- 
"""
# Author: Jan Gao 
# Date: 2018/5/7
# Description: 
# Site: http://www.xrtpay.com/
# Copyright (c) ShenZhen XinRuiTai Payment Service Co.,Ltd. All rights reserved 
"""

# import requests
#
# url = 'http://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/201805/t20180507_11813409.htm'
#
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie':  'PHPStat_Cookie_Group_10000003=%7C%3A%7CPHPStat_First_Time_10000003%3D1525684416066%7C%3A%7CPHPStat_Cookie_Global_User_Id%3D_ck18050717133610716392711412492%7C%3A%7CPHPStat_Return_Time_10000003%3D1525684416066%7C%3A%7CPHPStat_Visit_Time_Str_10000003%3D1525684416066%7C%3A%7CPHPStat_Visit_Time_10000003%3D1525684752374%7C%3A%7CPHPStat_Main_Website_10000003%3D_ck18050717133610716392711412492%7C10000003%7C%7C%7C',
#     'Host': 'www.sz.gov.cn',
#     'Referer': 'http://www.sz.gov.cn/cn/xxgk/index_sl_23448.htm',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
# }
# response = requests.get(url)
# print(response.status_code)
# print(response.content.decode('gb2312'))




import requests
import json
import random


def get_proxy():
    """
    ip代理池获取ip
    :return: ip  type(list)
    """
    url = "http://127.0.0.1:8000/?types=0&count=20&country=%E5%9B%BD%E5%86%85"
    res = requests.get(url)
    ip_ports = json.loads(res.text)

    PROXY_LIST = []
    for proxy in ip_ports:
        ip = proxy[0]
        port = proxy[1]
        score = proxy[2]

        max_score = {}
        if int(score) >= 9:
            max_score['ip_port'] = "http://" + ip + ":" + port
            PROXY_LIST.append(max_score)
    proxy = random.choice(PROXY_LIST)

    return proxy


ip = get_proxy()
print(ip)
