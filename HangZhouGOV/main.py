from scrapy.cmdline import execute

import sys
import os


def main():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # print(__file__)
    # print(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "hanzhou"])


if __name__ == '__main__':
    main()
