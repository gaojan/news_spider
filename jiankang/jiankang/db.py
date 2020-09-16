#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Author: Jan Gao
# Date: 2019/1/14
# Description:  to db
# Site: http://www.xrtpay.com/
# Copyright (c) ShenZhen XinRuiTai Payment Service Co.,Ltd. All rights reserved
"""
from jiankang.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWD
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase, declared_attr
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class XqzxDB(Base):
    __tablename__ = 't_post'

    id = Column(Integer, primary_key=True, nullable=False, comment='', autoincrement=True)
    title = Column(String(50), nullable=True, comment='表题')
    create_time = Column(String(20), nullable=True, comment='时间')
    url = Column(String(200), nullable=True, comment='链接')
    content = Column(Text(), nullable=True, comment='内容')


_config = "mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8".\
    format(user=MYSQL_USER, pwd=MYSQL_PASSWD, host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_DB)

sql_engine = create_engine(_config, encoding='utf-8', echo=False, pool_size=100)
Base.metadata.create_all(sql_engine)

Session = sessionmaker(bind=sql_engine)
session_text = Session()
session_text.add_item = XqzxDB
