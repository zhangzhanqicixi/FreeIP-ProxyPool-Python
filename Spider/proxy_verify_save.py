# -*- coding: utf-8 -*-
# @Time    : 2017/4/14 上午11:04
# @Author  : ZHANGZHANQI
# @File    : proxy_verify_save.py
# @Software: PyCharm

import json
import sys

sys.path.append('..')
from Verify.proxy_verify import VerifyProxy
from Util.utils import Util
from DB.mysqlDB import MySql

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


class VerifySave:
    def __init__(self):
        pass

    @staticmethod
    async def verify_and_save(proxy, source):
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

                    # 1. 查找是否已存在该IP和Port
                    sql = "SELECT * FROM httpbin WHERE ip = '{0}' AND port = '{1}'".format(ip, port)
                    fetchone = MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).query_one(sql)
                    if fetchone is None:
                        # 2. 插入数据库中没有的IP
                        sql = "INSERT INTO httpbin(ip, port, https, anonymity, country, speed, source, " \
                              "insert_time) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')" \
                            .format(ip, port, https, anonymity, country, speed, source, Util.get_current_time())
                        Util.log_info('Save Proxy ' + proxy + ' From ' + source)
                        MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).execute(sql)

        except Exception as e:
            pass

if __name__ == '__main__':
    VerifySave.verify_and_save('1.180.239.135:8081', 'mimvp.com')