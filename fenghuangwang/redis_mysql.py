#!usr/bin/env python  
# -*- coding: utf-8 -*- 
"""
# Author: Jan Gao 
# Date: 2018/3/30
# Description: 使用redis去重，并将数据持久化到mysql
# Site: http://www.xrtpay.com/
# Copyright (c) ShenZhen XinRuiTai Payment Service Co.,Ltd. All rights reserved 
"""

import redis
import json
from pymysql import *

if __name__ == '__main__':
    # redis数据库连接
    redis_cli = redis.Redis(host='192.168.1.114', port=6379)

    # mysql数据库连接
    mysql_cli = connect(
        # host='112.124.65.234',
        host='192.168.1.114',
        port=3306,
        database='xqzx',
        user='root',
        # user='xqzx',
        # password='xqzx@2018',
        password='mysql',
        charset='utf8'
    )
    cur = mysql_cli.cursor()

    while True:
        # 读取redis数据，先进先出sports_ifeng:items
        source, data = redis_cli.blpop(['sports_ifeng:items'])
        print(source, data)
        # 将数据转换成字典
        str_data = data.decode()
        dict_data = json.loads(str_data)
        # 保存到mysql数据
        cur.execute("INSERT INTO t_post (title,url,create_time,content) VALUES (%s,%s,%s,%s)",
                    (dict_data['title'],
                     dict_data['url'],
                     dict_data['time'],
                     dict_data['content']))

        mysql_cli.commit()

