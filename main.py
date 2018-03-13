#!/usr/bin/env/ python3 
# -*- coding: utf-8 -*-

from search import search, get_pages, choose_novel
from links import get_links, get_stamp_urls, get_datas
from multiprocessing import Pool
from dataswrite import datas_write 

global contents
def main(url):
    contents = {}
    pages = search(url)
    pageall = get_pages(pages)
    book_url = choose_novel(pageall)
    urls = get_links(book_url)
    stamp_urls = get_stamp_urls(urls)
    return stamp_urls



if __name__ == '__main__':
    URL = 'http://www.biquge.com.tw/modules/article/soshu.php'
    p = Pool()
    stamp_urls = main(URL)
    contents = p.map(get_datas, stamp_urls)
    for content in contents:
        datas_write(content)
#    p.map(get_datas, stamp_urls)






