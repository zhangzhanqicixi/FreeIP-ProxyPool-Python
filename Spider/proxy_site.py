# -*- coding: utf-8 -*-
# @Time    : 2017/4/14 上午10:59
# @Author  : ZHANGZHANQI
# @File    : proxy_site.py
# @Software: PyCharm

import aiohttp
import asyncio
import re
import sys
import requests
from pyquery import PyQuery
from PIL import Image
from io import BytesIO

sys.path.append('..')
from Util.utils import Util
from Spider.proxy_verify_save import VerifySave

HEADERS = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           }
DB_ADDRESS = 'localhost'
DB_USER = 'root'
DB_PASS = 'root'
DB_DATABASE = 'proxy_pool'
DB_CHARSET = 'utf8'


class ProxySites:
    def __init__(self):
        pass

    # mimvp -->  http://proxy.mimvp.com/free.php
    @staticmethod
    async def proxy_site_mimvp():
        # 国内普通、高匿，国外普通、高匿
        start_urls = ['in_tp', 'in_hp', 'out_tp', 'out_hp']
        try:
            for url in start_urls:
                url = 'http://proxy.mimvp.com/free.php?proxy=' + url
                header = HEADERS
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url, headers=header) as response:
                        r = await response.text()

                if r is not None and '' != r:
                    r = r.replace('<tbody>', '<tbody><tr>').replace('</tr>', '</tr><tr>')
                    doc = PyQuery(r)
                    for each in doc('tbody')('tr').items():
                        address = each('td').eq(1).text()
                        pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                        match = pattern.match(address)
                        if match:
                            port_img_url = each('td').eq(2)('img').attr.src
                            if 'common' in port_img_url:
                                port_img_url = 'http://proxy.mimvp.com/' + port_img_url
                                r = requests.get(port_img_url, headers=header)
                                image = Image.open(BytesIO(r.content))
                                port = Util.image_to_str(image)
                                try:
                                    port = int(port)
                                    # 非异步，待解决
                                    await VerifySave.verify_and_save(address + ':' + str(port), 'mimvp.com')
                                except:
                                    continue

        except Exception as e:
            Util.log_error('proxy_site_mimvp: ' + str(e))

    # guobanjia 前10页ip --> http://www.goubanjia.com/free/
    @staticmethod
    async def proxy_site_goubanjia():
        try:
            for index in range(1, 6):
                url = 'http://www.goubanjia.com/free/index{0}.shtml'.format(index)
                header = HEADERS
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url, headers=header) as response:
                        r = await response.text()

                if r is not None and '' != r:
                    doc = PyQuery(r)
                    for each in doc('td.ip').items():
                        address = ''
                        for i, tag in enumerate(each('*').items()):
                            if i == 0:
                                continue
                            if (tag.attr.style and 'none;' in tag.attr.style) or '' == tag.text():
                                continue
                            if 'port' in str(tag):
                                address = address + ':' + tag.text()
                            else:
                                address += tag.text()
                        pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')
                        match = pattern.match(address)
                        if match:
                            # 非异步，待解决
                            await VerifySave.verify_and_save(address, 'guobanjia.com')
            pass
        except Exception as e:
            Util.log_error('proxy_site_goubanjia: ' + str(e))

    # xicidaili --> http://www.xicidaili.com/
    @staticmethod
    async def proxy_site_xici():
        try:
            # 高匿、普匿、HTTPS、HTTP
            forms = ['nn', 'nt', 'wn', 'wt']
            for type in forms:
                # 每种类型的前10页
                for page in range(1, 11):
                    url = 'http://www.xicidaili.com/' + type + '/' + str(page)
                    header = HEADERS
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url=url, headers=header) as response:
                            r = await response.text()

                    if r is not None and '' != r:
                        doc = PyQuery(r)
                        for each in doc('tr').items():
                            ip_address = each('td').eq(1).text()
                            pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                            match = pattern.match(ip_address)
                            if match:
                                ip_port = each('td').eq(2).text()
                                # 非异步，待解决
                                await VerifySave.verify_and_save(ip_address + ':' + ip_port, 'xicidaili.com')
        except Exception as e:
            Util.log_error('proxy_site_xici: ' + str(e))

    # ip181 第一页IP --> http://www.ip181.com/
    @staticmethod
    async def proxy_site_ip181():
        try:
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
                        await VerifySave.verify_and_save(ip_address + ':' + ip_port, 'ip181.com')
        except Exception as e:
            Util.log_error('proxy_site_ip181: ' + str(e))

    # 快代理 前5页免费IP --> http://www.kuaidaili.com/proxylist/
    @staticmethod
    async def proxy_site_kuaidaili():
        try:
            header = HEADERS
            header['Cookie'] = 'channelid=0; sid=1492138570160333; _gat=1; _ga=GA1.2.486444152.1491549216'
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
                        await VerifySave.verify_and_save(ip_address + ':' + ip_port, 'kuaidaili.com')
                    pass
        except Exception as e:
            Util.log_error('proxy_site_kuaidaili: ' + str(e))

    # 66代理（API） --> http://m.66ip.cn/mo.php?tqsl=3000
    @staticmethod
    async def proxy_site_66ip_api():
        try:
            url = 'http://m.66ip.cn/mo.php?tqsl=3000'
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=HEADERS) as response:
                    r = await response.text()

            if r is not None and '' != r:
                pattern = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})<br />')
                match = pattern.findall(r)
                if len(match) > 0:
                    for each in match:
                        # 非异步，待解决
                        await VerifySave.verify_and_save(each, 'm.66ip.cn')
        except Exception as e:
            Util.log_error('proxy_site_66ip_api: ' + str(e))

    # 66代理 前5页免费IP --> http://www.66ip.cn/index.html
    @staticmethod
    async def proxy_site_66ip():
        try:
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
                                await VerifySave.verify_and_save(ip_address + ':' + ip_port, '66ip.cn')
        except Exception as e:
            Util.log_error('proxy_site_66ip: ' + str(e))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ProxySites.proxy_site_goubanjia())
    loop.close()
