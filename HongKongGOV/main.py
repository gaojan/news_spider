import sys
import os

from scrapy.cmdline import execute


def main():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # print(__file__)
    # print(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "hongkong"])


if __name__ == '__main__':
    main()
