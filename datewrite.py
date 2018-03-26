#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from search import BOOK_NAME

def datas_write(datas, bookname=BOOK_NAME):
    if datas is None:
        return
    print('即将完成!')
    with open('{}.txt'.format(bookname), 'a') as f:
        for num, content in datas.items():
            f.write(content)
