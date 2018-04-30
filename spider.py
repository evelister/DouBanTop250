import json
import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<li>.*?em c.*?>(\d+)</em>.*?title">(.*?)</span>.*?class="">.*?(\d+).*?average">'
                         '(.*?)</span>.*?inq">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排名': item[0],
            '名称': item[1],
            '时间': item[2],
            '评分': item[3],
            '名言': item[4],
        }

def write_to_file(content):
    with open('result.text', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def mian(start):
    url = 'https://movie.douban.com/top250?start=' +str(start)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(25):
        mian(i*10)