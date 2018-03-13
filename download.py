#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, time, random, datetime, re
from lxml import etree
from multiprocessing import Pool
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPError

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'


#读文件

def get_data(filename, default=''):
    try:
        with open(filename) as f:
            data = [_.strip() for _ in f.readlines()]
    except:
        data = [default]
    return data

#随机读取user_agent
def get_random_user_agent():
    return random.choice(get_data('user_agents.txt',USER_AGENT))

headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'user-agent':get_random_user_agent(),
        }
#获取网页内容
def download(url, headers=headers, params=None, num_retries=2, timeout=20, search=False):
    print('downloading:' + url, end='   ')
    #throttle = Throttle(random.uniform(7, 10))
    #throttle.wait(url)
    time.sleep(random.uniform(0.1, 0.5))
    try:
        res = requests.get(url, headers=headers,params=params, timeout=timeout)
        res.raise_for_status()
    except HTTPError:
        if num_retries > 0:
            if 500 < res.status_code < 600:
                return download(url, num_retries - 1)
    except ConnectionError:
        if num_retries > 0: 
            return download(url, num_retries - 1)
    print(res.status_code)
    if search:
        if re.match(r'http://www.biquge.com.tw/\d*_\d*/', res.url):
            return res.url
    #res.encoding = res.apparent_encoding
    html = res.text

    return html

class Throttle():
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)

        self.domains[domain] = datetime.datetime.now()
