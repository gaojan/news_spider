#!usr/bin/env python  
# -*- coding: utf-8 -*- 
"""
# Author: Jan Gao 
# Date: 2018/8/21
# Description:  去重过滤器，传入需过滤的字段
# Site: http://www.xrtpay.com/
# Copyright (c) ShenZhen XinRuiTai Payment Service Co.,Ltd. All rights reserved 
"""

import redis
from hashlib import md5
from sinaweibo.settings import (REDIS_HOST, REDIS_PORT,
                                REDIS_DB, REDIS_KEY)


class SimpleHash(object):
    """哈希算法"""
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    """Bloom过滤"""
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, blockNum=1, key=REDIS_KEY):

        self.server = redis.Redis(host=host, port=port, db=db)
        self.bit_size = 1 << 31  # <<向左移动31，没有就补0  1+31个0  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input.encode('utf-8'))
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str_input.encode('utf-8'))
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


if __name__ == '__main__':
    """ 第一次运行时会显示 not exists!，之后再运行会显示 exists! """
    bf = BloomFilter()
    if bf.isContains('http://www.baidu.com'):   # 判断字符串是否存在
        print('exists!')
    else:
        print('not exists!')
        bf.insert('http://www.baidu.com')