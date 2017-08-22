# -*- coding: utf-8 -*-
# @Time    : 2017/4/11 上午11:08
# @Author  : ZHANGZHANQI
# @File    : proxy_process.py
# @Software: PyCharm

import sys
import threading
import time
import configparser

sys.path.append('..')

from Util.utils import Util
from DB.mysqlDB import MySql
from Verify.proxy_verify import VerifyProxy

cf = configparser.ConfigParser()
cf.read('config.conf')

DB_ADDRESS = cf.get('db_mysql', 'db_host')
DB_USER = cf.get('db_mysql', 'db_user')
DB_PASS = cf.get('db_mysql', 'db_pass')
DB_DATABASE = cf.get('db_mysql', 'db_database')
DB_CHARSET = cf.get('db_mysql', 'db_charset')
thread_count = cf.get('process_threads', 'threads')
threadLock = threading.Lock()
threads = []


class Process(threading.Thread):
    def checking(self, sql):
        try:
            fetchall = MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).query(sql)
            if fetchall is None:
                # 如果查出来没有数据，则优先重复验证最新验证的IP（保证IP高度可用）
                sql = 'SELECT * FROM httpbin WHERE anonymity=2 AND alive=1 ORDER BY update_time DESC'
                fetchall = MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).query(sql)
            if fetchall is None:
                # 休息5秒后退出
                time.sleep(5)
                return
            for each in fetchall:
                each_id = each[0]
                proxy = each[1] + ':' + each[2]
                verify_count = int(each[12]) + 1
                r = VerifyProxy().validate_proxy(proxy, protocol='http', timeout=3)
                threadLock.acquire()
                if isinstance(r, str):
                    # 失效
                    sql = 'SELECT leave_count FROM httpbin WHERE id={0}'.format(each_id)
                    fetchone = MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).query_one(sql)
                    alive = '0'
                    leave_count = int(fetchone[0]) - 1
                    if leave_count <= 0:
                        # 尝试20次之后，删除该条代理
                        sql = 'DELETE FROM httpbin WHERE id={0}'.format(each_id)
                        Util.log_error(sql)
                    else:
                        # 更新
                        sql = "UPDATE httpbin SET verify_count={0}, leave_count={1}, alive={2} WHERE id={3}" \
                            .format(verify_count, leave_count, alive, each_id)
                        # Util.log_info(sql)
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
                        # Util.log_info(sql)
                        MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).execute(sql)
                threadLock.release()

        except Exception as e:
            Util.log_error(e)

    # 不断循环遍历代理IP
    def run(self):
        while True:
            if self.getName() == 'Thread-1':
                # 线程1 验证前20个IP已验证时间较长的IP
                sql = 'SELECT * FROM httpbin ORDER BY update_time LIMIT 20'
            elif self.getName() == 'Thread-2':
                # 线程2 验证所有未验证的IP
                sql = 'SELECT * FROM httpbin WHERE update_time IS NULL'
            else:
                # 线程N(N>2) 验证高匿且可用的最新的IP
                sql = 'SELECT * FROM httpbin WHERE anonymity=2 AND alive=1 ORDER BY update_time DESC'
            self.checking(sql)


def run():
    for i in range(int(thread_count)):
        thread = Process()
        thread.start()
        threads.append(thread)

    for i in threads:
        i.join()


if __name__ == '__main__':
    for i in range(int(thread_count)):
        thread = Process()
        thread.start()
        threads.append(thread)

    for i in threads:
        i.join()
