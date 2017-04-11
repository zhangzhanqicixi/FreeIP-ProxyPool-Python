# -*- coding: utf-8 -*-
# @Time    : 2017/4/11 下午4:33
# @Author  : ZHANGZHANQI
# @File    : proxy_service.py
# @Software: PyCharm

from DB.mysql import MySql
import json

DATABASE_NAME = 'httpbin'
DB_ADDRESS = 'localhost'
DB_USER = 'root'
DB_PASS = 'root'
DB_DATABASE = 'proxy_pool'
DB_CHARSET = 'utf8'


class Service:
    def __init__(self):
        pass

    def proxy_list(self, condition):
        data = {}
        if isinstance(condition, dict):
            sql = 'SELECT * FROM ' + DATABASE_NAME + ' WHERE alive=1'

            # https
            if 'https' in condition.keys():
                if condition.get('https') == 0 or condition.get('https') == 1:
                    if 'where' in sql.lower():
                        sql += ' AND https={0}'.format(condition.get('https'))
                    else:
                        sql += ' WHERE https={0}'.format(condition.get('https'))
                else:
                    data['Error'] = 'Invalid "https" Params'
            # 代理类型
            if 'type' in condition.keys():
                if condition.get('type') == 0 or condition.get('type') == 1 or condition.get('type') == 2:
                    if 'where' in sql.lower():
                        sql += ' AND anonymity={0}'.format(condition.get('type'))
                    else:
                        sql += ' WHERE anonymity={0}'.format(condition.get('type'))
                else:
                    data['Error'] = 'Invalid "type" Params'
            # 代理地区
            if 'country' in condition.keys():
                if condition.get('country') == '国内' or condition.get('country') == '国外':
                    if 'where' in sql.lower():
                        sql += ' AND country="中国大陆"' if '国内' == condition.get('country') else ' AND country!="中国大陆"'
                    else:
                        sql += ' WHERE country="中国大陆"' if '国内' == condition.get('country') else ' WHERE country!="中国大陆"'
                else:
                    data['Error'] = 'Invalid "country" Params'
            # 按照连接速度排序
            sql += ' ORDER BY speed'
            # 取出代理个数, 默认一次取5个
            if 'count' in condition.keys():
                # 一次最多取出20个代理
                if isinstance(condition.get('count'), int):
                    if condition.get('count') > 20:
                        data['Error'] = 'The maximum "count" is 20'
                    else:
                        sql += ' LIMIT {0}'.format(condition.get('count'))
                else:
                    data['Error'] = 'Invalid "count" Params'
            else:
                sql += ' LIMIT {0}'.format('5')

            # 返回错误内容
            if 'Error' in data.keys():
                return data

        else:
            sql = 'SELECT * FROM ' + DATABASE_NAME + ' WHERE alive=1 ORDER BY speed LIMIT 5'

        # 执行SQL
        fetchall = MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).query(sql)
        data_list = []
        for each in fetchall:
            anonymity = '高匿' if each[4] == 2 else '透明'
            last_verify_time = str(each[10] if each[10] is not None else each[9])
            data = {
                'ip': each[1] + ':' + str(each[2]),
                'https:': each[3],
                'type': anonymity,
                'country': each[5],
                'last_verify_time': last_verify_time
            }
            # str_json = '{"ip": "' + each[1] + ':' + str(each[2]) + \
            #            '", "https":"' + str(each[3]) + \
            #            '", "type": "' + anonymity + \
            #            '", "country": "' + each[5] + \
            #            '", "last_verify_time": "' + last_verify_time + '"}'
            data_list.append(data)

        return data_list if len(data_list) > 0 else data


if __name__ == '__main__':
    condition = {
        'count': 5,
        'type': 2
    }
    data_local = Service().proxy_list(condition)
    if isinstance(data_local, list):
        for each_local in data_local:
            print(each_local)
