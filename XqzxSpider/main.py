from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'tianjin'])
# execute(['scrapy', 'crawl', 'beijing'])
# execute(['scrapy', 'crawl', 'guangzhou'])
# execute(['scrapy', 'crawl', 'chengdu'])
# execute(['scrapy', 'crawl', 'chongqing'])
# execute(['scrapy', 'crawl', 'shanghai'])
# execute(['scrapy', 'crawl', 'shenzhen'])
# execute(['scrapy', 'crawl', 'zhengfu'])
# execute(['scrapy', 'crawl', 'nanjing'])
execute(['scrapy', 'crawl', 'nanning'])
# execute(['scrapy', 'crawl', 'hangzhou'])
