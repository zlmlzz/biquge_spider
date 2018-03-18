#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from download import download
from lxml import etree
from urllib.parse import urljoin
from datewrite import datas_write

def get_links(url):
    html = etree.HTML(download(url))
    #//*[@id="list"]/dl/dd[1]
    urls = html.xpath('//div[@id="list"]/dl/dd/a/@href')
    return urls


def get_datas(stamp_url):
    contents = {}
    html = etree.HTML(download(stamp_url[1]))
    try:
        raw_content = html.xpath('//div[@id="content"]/text()')
        title = html.xpath('//div[@class="bookname"]/h1/text()')[0]
        content = '\n' + title + '\n'
    except:
        print('本章暂无内容')
        return
    for i in raw_content:
        content = content + i
    contents[stamp_url[0]] = content
    return contents
#    return datas_write(contents)


def get_stamp_urls(urls, root_url='http://www.biquge.com.tw/'):
    stamp_urls = []
    for i in range(len(urls)):
        stamp_urls = stamp_urls + [[str(i), urljoin(root_url, urls[i])]]
    return stamp_urls


