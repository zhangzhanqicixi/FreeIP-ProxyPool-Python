# -*- coding: utf-8 -*-
# @Time    : 2017/4/11 下午4:33
# @Author  : ZHANGZHANQI
# @File    : proxy_service.py
# @Software: PyCharm

from DB.mysqlDB import MySql
import configparser

cf = configparser.ConfigParser()
cf.read('config.conf')
DATABASE_NAME = 'httpbin'
DB_ADDRESS = cf.get('db_mysql', 'db_host')
DB_USER = cf.get('db_mysql', 'db_user')
DB_PASS = cf.get('db_mysql', 'db_pass')
DB_DATABASE = cf.get('db_mysql', 'db_database')
DB_CHARSET = cf.get('db_mysql', 'db_charset')


class Service:
    def __init__(self):
        pass

    def proxy_list(self, condition):
        data = {}
        if isinstance(condition, dict):
            sql = 'SELECT * FROM ' + DATABASE_NAME + ' WHERE alive=1'

            # https
            if 'https' in condition.keys() and condition.get('https') is not None:
                if condition.get('https') == 1:
                    if 'where' in sql.lower():
                        sql += ' AND https={0}'.format(condition.get('https'))
                    else:
                        sql += ' WHERE https={0}'.format(condition.get('https'))
                else:
                    data['Error'] = 'Invalid "https" Params'
            # 代理类型
            if 'type' in condition.keys() and condition.get('type') is not None:
                if condition.get('type') == 0 or condition.get('type') == 1 or condition.get('type') == 2:
                    if 'where' in sql.lower():
                        sql += ' AND anonymity={0}'.format(condition.get('type'))
                    else:
                        sql += ' WHERE anonymity={0}'.format(condition.get('type'))
                else:
                    data['Error'] = 'Invalid "type" Params'
            # 代理地区
            if 'country' in condition.keys() and condition.get('country') is not None:
                if condition.get('country') == '国内' or condition.get('country') == '国外':
                    if 'where' in sql.lower():
                        sql += ' AND country="中国大陆"' if '国内' == condition.get('country') else ' AND country!="中国大陆"'
                    else:
                        sql += ' WHERE country="中国大陆"' if '国内' == condition.get('country') else ' WHERE country!="中国大陆"'
                else:
                    data['Error'] = 'Invalid "country" Params'
            # 按照连接速度排序
            sql += ' ORDER BY update_time DESC'
            # 取出代理个数, 默认一次取5个
            if 'count' in condition.keys() and condition.get('count') is not None:
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
            https = '支持' if each[3] == 1 else '不支持'
            data = {
                'ip': each[1] + ':' + str(each[2]),
                'https:': https,
                'type': anonymity,
                'country': each[5],
                'lastVerifyTime': last_verify_time
            }
            # str_json = '{"ip": "' + each[1] + ':' + str(each[2]) + \
            #            '", "https":"' + str(each[3]) + \
            #            '", "type": "' + anonymity + \
            #            '", "country": "' + each[5] + \
            #            '", "last_verify_time": "' + last_verify_time + '"}'
            data_list.append(data)

            try:
                # used_count + 1
                used_count = int(each[11]) + 1
                sql_udpate = 'UPDATE httpbin SET used_count={0}, update_time="{1}" WHERE id={2}' \
                    .format(used_count, each[10], each[0])

                MySql(DB_ADDRESS, DB_USER, DB_PASS, DB_DATABASE, DB_CHARSET).execute(sql_udpate)
            except:
                return data_list if len(data_list) > 0 else data

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
