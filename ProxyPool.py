# -*- coding: utf-8 -*-
# @Time    : 2017/4/10 下午3:47
# @Author  : ZHANGZHANQI
# @File    : ProxyPool.py
# @Software: PyCharm

from flask import Flask, jsonify, abort, make_response, request, Response
from Service.proxy_service import Service
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/get_proxy', methods=['GET'])
def get_task():
    condition = {}
    data = Service().proxy_list(condition)
    for each in data:
        print(each)
    """
        出于安全考虑？
        jsonify无法返回content-type指定浏览器编码方式，application/json后必须再加charset=utf-8，否认会出现乱码
        所以只能用Response
    """
    # return jsonify(data)
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json;charset=utf-8')


if __name__ == '__main__':
    app.run()
