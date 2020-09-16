import os

DEBUG = True

# 定义根路劲
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath('.'), 'SpiderKeeper.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# app线程. 一个通用的设置，使用两个processor -一个处理传入的请求，另一个处理执行后台操作。
THREADS_PER_PAGE = 2

# 启用保护防止*跨站请求伪造(CSRF)*
CSRF_ENABLED = True

# 使用安全、唯一和绝对保密的密钥来签名数据。
CSRF_SESSION_KEY = "secret"

# 签名cookie的密钥
SECRET_KEY = "secret"

# 日志设置
LOG_LEVEL = 'INFO'

# spider 服务器
SERVER_TYPE = 'scrapyd'
SERVERS = ['http://localhost:6800']

# basic 认证
NO_AUTH = False
BASIC_AUTH_USERNAME = 'admin'
BASIC_AUTH_PASSWORD = 'admin'
BASIC_AUTH_FORCE = True
