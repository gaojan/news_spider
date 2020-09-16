#!usr/bin/env python  
# -*- coding: utf-8 -*- 

import datetime


def str_to_datetime(str):
    return datetime.datetime.strptime(str, "%Y年%m月%d日 %H:%M")


def now_time():
    return datetime.datetime.now()

