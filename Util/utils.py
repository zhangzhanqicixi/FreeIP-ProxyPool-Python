# -*- coding: utf-8 -*-
# @Time    : 2017/4/10 下午5:09
# @Author  : ZHANGZHANQI
# @File    : utils.py
# @Software: PyCharm
# 工具方法集合

import time


class Util:
    def __init__(self):
        pass

    # 获得当前系统时间
    @staticmethod
    def get_current_time():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 处理特殊字符
    @staticmethod
    def format_str(str):
        if str is None:
            return str
        str.strip()
        str.replace('\n', '')
        str.replace('\r', '')
        str.replace('\t', '')
        str.replace('&nbsp', '')
        str.strip()
        return str
