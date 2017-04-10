# -*- coding: utf-8 -*-
# @Time    : 2017/4/7 下午3:00
# @Author  : ZHANGZHANQI
# @File    : spider_proxy.py
# @Software: PyCharm


import asyncio
import aiohttp
import re
import json
from pyquery import PyQuery
from Verify.verifyProxy import VerifyProxy
from Util.utils import Util
from DB.mysql import MySql

HEADERS = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           }


class SpiderProxy:
    def __init__(self):
        pass

    @staticmethod
    async def verify_and_save(proxy, source):
        print(proxy + ' from ' + source)
        try:
            r = VerifyProxy().validate_proxy(proxy, protocol='http', timeout=3)
            if isinstance(r, str):
                r = json.loads(r)
            if isinstance(r, dict):
                if 'exception' not in r.keys():
                    https = '0'
                    ip = proxy.split(':')[0]
                    port = proxy.split(':')[1]

                    speed = r['timedelta']
                    origin = r['origin']
                    if origin == ip:
                        # 高匿
                        anonymity = '2'
                    else:
                        # 透明
                        anonymity = '0'
                    country = VerifyProxy().country_proxy(ip)
                    result_https = VerifyProxy().validate_proxy(proxy, 'https', timeout=3)
                    if not isinstance(result_https, str):
                        https = '1'

                    sql = "INSERT INTO httpbin(ip, port, https, anonymity, country, speed, source, " \
                          "insert_time) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')" \
                        .format(ip, port, https, anonymity, country, speed, source, Util.get_current_time())
                    print(sql)
                    MySql('localhost', 'root', 'root', 'proxy_pool', 'utf8').save(sql)


                    # print(
                    #     'ip:' + ip + ' port:' + port + ' speed:' + speed + ' https:' + https + ' anonymity:' + anonymity +
                    #     ' country:' + country + ' source:' + source)

        except Exception as e:
            print(e)

    @staticmethod
    def do_start():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SpiderProxy.proxy_list())
        loop.close()

    @staticmethod
    async def proxy_list():
        await asyncio.wait([
            # SpiderProxy.proxy_site_kuaidaili(),
            # SpiderProxy.proxy_site_66ip(),
            SpiderProxy.proxy_site_ip181(),
        ])

    # ip181 第一页IP --> http://www.ip181.com/
    @staticmethod
    async def proxy_site_ip181():
        url = 'http://www.ip181.com'
        header = HEADERS
        header['Host'] = 'www.ip181.com'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=header) as response:
                r = await response.text()

        if r is not None and '' != r:
            doc = PyQuery(r)
            for each in doc('tr').items():
                ip_address = each('td').eq(0).text()
                pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                match = pattern.match(ip_address)
                if match:
                    ip_port = each('td').eq(1).text()
                    # 非异步，待解决
                    await SpiderProxy.verify_and_save(ip_address + ':' + ip_port, 'ip181')

    # 快代理 前5页免费IP --> http://www.kuaidaili.com/proxylist/
    @staticmethod
    async def proxy_site_kuaidaili():
        header = HEADERS
        header['Cookie'] = '_ydclearance=314dc9a3db689e222ea71a06-c0c5-457f-8639-80480d86f402-1491822539'
        for i in range(1, 6):
            url = 'http://www.kuaidaili.com/proxylist/{page}/'.format(page=i)
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=header) as response:
                    r = await response.text()

            if r is not None and '' != r:
                doc = PyQuery(r)
                for each in doc('#index_free_list > table > tbody')('tr').items():
                    ip_address = each('td[data-title=IP]').eq(0).text()
                    ip_port = each('td[data-title=PORT]').eq(0).text()
                    # 非异步，待解决
                    await SpiderProxy.verify_and_save(ip_address + ':' + ip_port, 'kuaidaili.com')
                pass

    # 66代理 前5页免费IP --> http://www.66ip.cn/index.html
    @staticmethod
    async def proxy_site_66ip():
        # 遍历全国的代理
        for i in range(0, 35):
            if i == 0:
                url = 'http://www.66ip.cn/'
            else:
                url = 'http://www.66ip.cn/areaindex_{area}/'.format(area=i)
            # 获得前5页IP
            for j in range(1, 6):
                url_page = url + '{page}.html'.format(page=j)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url_page, headers=HEADERS) as response:
                        r = await response.text()

                if r is not None and '' != r:
                    doc = PyQuery(r)
                    for each in doc('tr').items():
                        ip_address = each('td').eq(0).text()
                        pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                        match = pattern.match(ip_address)
                        if match:
                            ip_port = each('td').eq(1).text()
                            # 非异步，待解决
                            await SpiderProxy.verify_and_save(ip_address + ':' + ip_port, '66ip')


if __name__ == '__main__':
    SpiderProxy.do_start()
