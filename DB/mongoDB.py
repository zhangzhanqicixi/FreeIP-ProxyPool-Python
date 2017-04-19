# -*- coding: utf-8 -*-
# @Time    : 2017/4/7 下午5:33
# @Author  : ZHANGZHANQI
# @File    : mongoDB.py
# @Software: PyCharm

import pymongo


class mongoDB:
    client = pymongo.MongoClient('localhost:27017')
    collection = client.proxydb.total_proxy

    def __init__(self):
        pass

    def mongoDBConnection(self):
        return self.collection.count()

    def save(self, value):
        if isinstance(value, dict):
            self.collection.save(value)

    def is_exist(self, value):
        if isinstance(value, dict):
            db_value = self.collection.find(value)
            print(db_value.count())
            if db_value is not None:
                return True
        return False


if __name__ == '__main__':
    value = {
        'title': '1111',
        'key': '1122'
    }
    mongoDB().save(value)
    print(mongoDB().is_exist(value))

    # mongoDB().mongoDBConnection()
