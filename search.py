#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from download import download
from lxml import etree



BOOK_NAME = input('Enter your novel name:')
URL = 'http://www.biquge.com.tw/modules/article/soshu.php'


def __get_name(name=BOOK_NAME):
    name = BOOK_NAME
    return name.encode('gbk')


payload = {
    'searchkey':__get_name(),
}


def get_pages(num, url=URL):
    if num == '0' or num == 0:
        return 0
    if len(str(num)) > 30 and type(num) == type(str()):
        print('.', end='')
        return num
    total = []
    for i in range(1, int(num) + 1):
        payload['page'] = str(i)
        raw_html = etree.HTML(download(url, params=payload))
        infos = raw_html.xpath('//tr[@id="nr"]/td[@class="odd"][1]/a/@href | //tr[@id="nr"]/td[@class="odd"][1]/a/text() | //tr[@id="nr"]/td[@class="odd"][2]/text()')
        total = total + infos
    return total



def search(url):
    raw_html = download(url, params=payload, is_search=True)
    if re.match(r'http://www.biquge.com.tw/\d*_\d*/', raw_html):
        print('prepare download.', end='')
        return raw_html

    html = etree.HTML(raw_html)
    try:
        td = html.xpath('//tr[@id="nr"]/td/')
        pages = html.xpath('//*[@id="pagelink"]/a/text()')[-1]
    except IndexError as e:
        return 0
    except etree.XPathEvalError as e:
        return raw_html 
    return pages

def choose_novel(total):
    if type(total) == type(str()):
        print('.')
        return total
    urls = []
    titles = []
    authors = []
    for i in range(0, len(total), 3):
        urls = urls + [total[i]]
        titles = titles + [total[i + 1]]
        authors = authors + [total[i + 2]]
    for i in range(len(urls)):
        print('作者:%-40s\t书名:\t%-40s\t序号:\t%-20s' %(authors[i], titles[i], str(i)))
    num = -1 if total == 0 else int(input('choose one:'))
    if 0 <= num <= len(urls):
        return urls[num]
    else:
        print('sorry')
        return

#pages = search('http://www.biquge.com.tw/modules/article/soshu.php')
#url = choose_novel(get_pages(pages))
#print(url)

