import requests

url = 'http://service.shanghai.gov.cn/pagemore/iframePagerIndex_4411_3_30.html?page=1'
link = 'http://service.shanghai.gov.cn/pagemore/iframePagerIndex_4411_3_30.html?page={}'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'ASP.NET_SessionId=wyllng1csp40hkpm5ahdkxzc',
    'Host': 'service.shanghai.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://service.shanghai.gov.cn/pagemore/iframePagerIndex_4411_3_30.html?objtype=3&nodeid=4411&page=16&pagesize=30',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
for i in range(10, 11):
    response = requests.get(link.format(i), headers=headers)
    print('>>Status Code:', response.status_code)
    print(response.text)

