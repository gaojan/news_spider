import time
import datetime


def check_time(time_string, format_string, days_ago=7):
    # 算出时间秒数
    # days_ago = datetime.timedelta(days=days_ago)
    # days_sec = days_ago.total_seconds()
    days_sec = 60*60*24*days_ago

    old = time.mktime(time.strptime(time_string, format_string))
    now = time.time()
    if now - old > days_sec:
        return False
    return True


if __name__ == '__main__':
    rsult = check_time("[2018-08-20]", "[%Y-%m-%d", 1)
    print(rsult)


