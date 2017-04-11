# -*- coding: utf-8 -*-
# @Time    : 2017/4/10 下午3:47
# @Author  : ZHANGZHANQI
# @File    : mysql.py
# @Software: PyCharm

import pymysql.cursors
from Util.utils import Util


class MySql:
    def __init__(self, host, user, password, db, charset):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
        self.cursor = self.connection.cursor()
        pass

    # 查找全部
    def query(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            Util.log_error(e)
            return None
        finally:
            self.connection.close()

    # 查找一条
    def query_one(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as e:
            Util.log_error(e)
            return None
        finally:
            self.connection.close()

    # 执行sql（自动提交事务）
    def execute(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            Util.log_error(e)
        finally:
            self.connection.close()


if __name__ == '__main__':
    mysql = MySql('localhost', 'root', 'root', 'doubanMovie', 'utf8')
    print(mysql.query('select * from movie limit 10'))
