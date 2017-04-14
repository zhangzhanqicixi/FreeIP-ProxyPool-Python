# -*- coding: utf-8 -*-
# @Time    : 2017/4/7 下午3:00
# @Author  : ZHANGZHANQI
# @File    : proxy_spider.py
# @Software: PyCharm


import asyncio
import sys

sys.path.append('..')
from Spider.proxy_site import ProxySites


class SpiderProxy:
    def __init__(self):
        pass

    @staticmethod
    def do_start():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SpiderProxy.proxy_list())
        loop.close()

    @staticmethod
    async def proxy_list():
        while True:
            await asyncio.wait([
                ProxySites.proxy_site_mimvp(),
                ProxySites.proxy_site_kuaidaili(),
                ProxySites.proxy_site_66ip_api(),
                ProxySites.proxy_site_66ip(),
                ProxySites.proxy_site_ip181(),
                ProxySites.proxy_site_xici(),
                ProxySites.proxy_site_goubanjia()
            ])
            await asyncio.sleep(5)


def run():
    while True:
        SpiderProxy.do_start()


if __name__ == '__main__':
    while True:
        SpiderProxy.do_start()
