import sys
import os
from scrapy.cmdline import execute


def main():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "weibo_realtimehot"])


if __name__ == '__main__':
    main()
