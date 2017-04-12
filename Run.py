# -*- coding: utf-8 -*-
# @Time    : 2017/4/12 下午2:13
# @Author  : ZHANGZHANQI
# @File    : Run.py
# @Software: PyCharm

from multiprocessing import Process

from ProxyPool import run as WebService
from Spider.proxy_spider import run as Spider
from Process.proxy_process import run as Verify

if __name__ == '__main__':
    # clean up the log file
    f = open('proxy_spider.log', 'w')
    f.truncate()
    f.close()

    # 1. crawler
    p1 = Process(target=Spider)
    # 2. verify
    p2 = Process(target=Verify)
    # 3. web api
    p3 = Process(target=WebService)

    p1.start()
    p2.start()
    p3.start()
