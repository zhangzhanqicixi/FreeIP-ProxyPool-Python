# -*- coding: utf-8 -*-
# @Time    : 2017/4/10 下午3:47
# @Author  : ZHANGZHANQI
# @File    : ProxyPool.py
# @Software: PyCharm

from flask import Flask, jsonify, abort, make_response, request, Response
from flask_restful import reqparse
from Service.proxy_service import Service
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/getProxy', methods=['GET'])
def get_task():
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int)
    parser.add_argument('https', type=int)
    parser.add_argument('type', type=int)
    parser.add_argument('country', type=str)
    args = parser.parse_args()
    data = Service().proxy_list(args)
    """
        出于安全考虑？
        jsonify无法返回content-type指定浏览器编码方式，application/json后必须再加charset=utf-8，否认会出现乱码
        所以只能用Response
    """
    # return jsonify(data)
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json;charset=utf-8')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
