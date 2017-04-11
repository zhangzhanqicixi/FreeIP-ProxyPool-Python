# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request, Response
from Service.proxy_service import Service

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/get_proxy', methods=['GET'])
def get_task():
    condition = {}
    data = Service().proxy_list(condition)
    for each in data:
        print(each)
        return jsonify(each,)


if __name__ == '__main__':
    app.run()
