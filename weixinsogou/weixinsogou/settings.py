# -*- coding: utf-8 -*-

# Scrapy settings for weixinsogou project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weixinsogou'

SPIDER_MODULES = ['weixinsogou.spiders']
NEWSPIDER_MODULE = 'weixinsogou.spiders'

# MYSQL配置
MYSQL_HOST = '192.168.0.138'
MYSQL_PORT = 3306
MYSQL_DB = 'xqzx'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'mysql'

# # 使用scrapy_redis的重复过滤器
# DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# # # 使用scrapy_redis的调度器
# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# # # 是否保持任务队列
# SCHEDULER_PERSIST = True
# REDIS_HOST = '120.78.164.142'
# REDIS_PORT = '6379'
# REDIS_PARAMS = {
#     'password': 'gao1990621'
# }
# REDIS_URL = 'redis://127.0.0.1:6379'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'weixinsogou (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'weixinsogou.middlewares.WeixinsogouSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #    'weixinsogou.middlewares.WeixinsogouDownloaderMiddleware': 543,
    'weixinsogou.middlewares.RandomUserAgent': 544,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'weixinsogou.pipelines.WeixinsogouPipeline': 300,
    'weixinsogou.pipelines.DbPipeline': 301
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 开启log
import datetime
today = datetime.datetime.now()
LOG_ENABLED = True
LOG_LEVEL = 'INFO'
log_file_path = 'log/{}_{}_{}.log'.format(today.year, today.month, today.day)
LOG_FILE = "./" + log_file_path
