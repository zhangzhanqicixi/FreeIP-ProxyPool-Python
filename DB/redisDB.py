# -*- coding: utf-8 -*-
# @Time    : 2017/4/7 下午6:11
# @Author  : ZHANGZHANQI
# @File    : redisDB.py
# @Software: PyCharm

import redis

redis_host = '127.0.0.1'
redis_port = 6379

redisConnect = redis.Redis(host=redis_host, port=redis_port, charset='utf-8', decode_responses=True)


class RedisTool:
    @staticmethod
    def hexists(name, key):
        return redisConnect.hexists(name, key)

    @staticmethod
    def hget(name, key):
        return redisConnect.hget(name, key)

    @staticmethod
    def getset(name, value):
        return redisConnect.getset(name, value)

    @staticmethod
    def hdel(name, *keys):
        return redisConnect.hdel(name, *keys)

    @staticmethod
    def hgetall(name):
        return redisConnect.hgetall(name)

    @staticmethod
    def hkeys(name):
        return redisConnect.hkeys(name)

    @staticmethod
    def hlen(name):
        return redisConnect.hlen(name)

    # Set key to value within hash name Returns 1 if HSET created a new field, otherwise 0
    @staticmethod
    def hset(name, key, value):
        return redisConnect.hset(name, key, value)

    @staticmethod
    def setex(name, time, value):
        return redisConnect.setex(name, time, value)

    @staticmethod
    def get(name):
        return redisConnect.get(name)

    @staticmethod
    def exists(name):
        return redisConnect.exists(name)

    @staticmethod
    def set(name, value):
        return redisConnect.set(name, value)

    @staticmethod
    def s_add(name, *value):
        return redisConnect.sadd(name, *value)

    @staticmethod
    def s_members(name):
        return redisConnect.smembers(name)

    @staticmethod
    def s_remove(name, *value):
        return redisConnect.srem(name, *value)

    @staticmethod
    def s_pop(name):
        return redisConnect.spop(name)

    # 返回一个集合的全部成员，该集合是所有给定集合的交集。
    @staticmethod
    def s_sinter(name, *value):
        return redisConnect.sinter(name, *value)

    # 返回一个集合的全部成员，该集合是所有给定集合的并集
    @staticmethod
    def s_sunion(name, *value):
        return redisConnect.sunion(name, *value)

if __name__ == '__main__':
    data = {
        'ip': '127.0.0.2:8080',
        'country': '中国大陆'
    }
    # RedisTool.s_add('proxy_clarity', data)
    # print(RedisTool.s_remove('127.0.0.2:8080'))
    print(RedisTool.s_sinter('proxy_clarity', 'proxy_anonymity'))
