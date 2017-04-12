# -*- coding: utf-8 -*-
# @Time    : 2017/4/10 下午5:09
# @Author  : ZHANGZHANQI
# @File    : utils.py
# @Software: PyCharm
# 工具方法集合

import time
import logging

# 创建一个logger
logger = logging.getLogger('proxy_spider')
logger.setLevel(logging.DEBUG)
# 创建一个handler，写入日志文件
fh = logging.FileHandler('proxy_spider.log')
fh.setLevel(logging.DEBUG)

# 创建一个handler，输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)


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

    @staticmethod
    def log_info(message):
        logger.info(message)

    @staticmethod
    def log_error(message):
        logger.error(message)


if __name__ == '__main__':
    message = 'test logger'
    # Util.log_error(message)
    Util.log_info(message)
    Util.log_error(message)
