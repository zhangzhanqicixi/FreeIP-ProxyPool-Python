# -*- coding: utf-8 -*-
# @Time    : 2017/4/11 上午11:08
# @Author  : ZHANGZHANQI
# @File    : proxy_process.py
# @Software: PyCharm

import json
from Util.utils import Util
from DB.mysql import MySql
from Verify.proxy_verify import VerifyProxy

DB_ADDRESS = 'localhost'
DB_USER = 'root'
DB_PASS = 'root'
DB_DATABASE = 'proxy_pool'
DB_CHARSET = 'utf8'


class Process:
    def __init__(self):
        pass

    # 不断循环遍历代理IP
    def infinite_checking(self):
        while True:
            sql = 'SELECT * FROM httpbin'
            fetchall = MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).query(sql)
            if fetchall is not None:
                for each in fetchall:
                    each_id = each[0]
                    proxy = each[1] + ':' + each[2]
                    verify_count = int(each[12]) + 1
                    r = VerifyProxy().validate_proxy(proxy, protocol='http', timeout=3)
                    if isinstance(r, str):
                        # 失效
                        alive = '0'
                        leave_count = int(each[13]) - 1
                        if leave_count == 0:
                            # 尝试20次之后，删除该条代理
                            sql = 'DELETE FROM httpbin WHERE id={0}'.format(each_id)
                            Util.log_error(sql)
                        else:
                            # 更新
                            sql = "UPDATE httpbin SET verify_count={0}, leave_count={1}, alive={2} WHERE id={3}" \
                                .format(verify_count, leave_count, alive, each_id)
                            Util.log_info(sql)
                        MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).execute(sql)
                    elif isinstance(r, dict):
                        if 'exception' not in r.keys():
                            alive = '1'
                            leave_count = 20
                            speed = r['timedelta']
                            # 暂不重复验证是否支持HTTPS
                            # result_https = VerifyProxy().validate_proxy(proxy, 'https', timeout=3)
                            sql = "UPDATE httpbin SET verify_count={0}, speed={1}, alive={2}, leave_count={3} WHERE id={4}" \
                                .format(verify_count, speed, alive, leave_count, each_id)
                            Util.log_info(sql)
                            MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).execute(sql)


if __name__ == '__main__':
    Process().infinite_checking()
