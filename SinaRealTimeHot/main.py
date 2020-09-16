import sys
import os
from scrapy.cmdline import execute


def main():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # execute(["scrapy", "crawl", "realtimehot"])
    # execute(["scrapy", "crawl", "baidu_realtimehot"])
    execute(["scrapy", "crawl", "mWeiboRealtimehot"])


if __name__ == '__main__':
    main()
