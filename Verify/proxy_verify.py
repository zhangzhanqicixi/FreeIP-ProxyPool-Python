# -*- coding: utf-8 -*-
# @Time    : 2017/4/7 下午6:10
# @Author  : ZHANGZHANQI
# @File    : proxy_verify.py
# @Software: PyCharm

import re
import requests
import json
from Util.utils import Util


class VerifyProxy:
    mainland = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建',
                '江西', '山东', '广东', '广西', '海南', '河南', '湖北', '湖南', '重庆', '四川', '贵州', '云南', '西藏', '陕西',
                '甘肃', '青海', '宁夏', '新疆', '中国']

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    def __init__(self):
        pass

    # 判断IP是否有效(支持HTTP或HTTPS)
    def validate_proxy(self, ip, protocol, timeout):
        if 'http' != protocol.lower() and 'https' != protocol.lower():
            return '{"exception": "error protocol"}'
        url = protocol + '://httpbin.org/get?show_env=1'
        self.headers['Host'] = 'httpbin.org'
        if ip is not None:
            proxies = {
                protocol: 'http://' + ip,
            }
            pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')
            match = pattern.match(ip)
            if match:
                try:
                    response = requests.get(url, headers=self.headers, proxies=proxies, timeout=timeout)
                    result = json.loads(response.text)
                    result['timedelta'] = str(response.elapsed)[6:]
                    return result

                except Exception as e:
                    Util.log_error(e)
                    return '{"exception": "' + str(e) + '"}'
        return '{"exception": "empty proxy"}'

    # 判断IP所在国家（地区）
    def country_proxy(self, ip):
        if ':' in ip:
            ip = ip.split(':')[0]

        address = '未知'
        try:
            self.headers['Host'] = 'www.ip138.com'
            url = 'http://www.ip138.com/ips138.asp?ip=' + ip
            r = requests.get(url, headers=self.headers, timeout=10)
            r.encoding = 'gbk'
            html = r.text
            pattern = re.compile('本站数据：(.*?) ')
            match = pattern.search(html)
            if match:
                for province in self.mainland:
                    if province in match.group(1):
                        address = '中国大陆'
                        break
                if '未知' == address:
                    address = match.group(1)
        finally:
            return address


if __name__ == '__main__':
    # 124.88.67.39:83
    proxy = '180.119.65.247'
    print(VerifyProxy().country_proxy(proxy))
    # r = VerifyProxy().validate_proxy(proxy, 'http')
    # if isinstance(r, str):
    #     r = json.loads(r)
    # if isinstance(r, dict):
    #     https = '不支持'
    #     speed = ''
    #     ip = proxy.split(':')[0]
    #     port = proxy.split(':')[1]
    #     anonymity = '-1'
    #     country = ''
    #     if 'exception' not in r.keys():
    #         speed = r['timedelta']
    #         origin = r['origin']
    #         if origin == ip:
    #             anonymity = '高匿'
    #         else:
    #             anonymity = '透明'
    #         country = VerifyProxy().country_proxy(ip)
    #         result_https = VerifyProxy().validate_proxy(proxy, 'https')
    #         if not isinstance(result_https, str):
    #             https = '支持'
    #
    #     print(ip + ' ' + port + ' ' + speed + ' ' + https + ' ' + anonymity + ' ' + country)
