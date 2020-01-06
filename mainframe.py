# -*- coding: UTF-8 -*-
from flask import Flask, Response
import datetime
import json
import time

app = Flask(__name__)

@app.route('/hello')
def main():
    resp_json = {'utctime': datetime.datetime.utcfromtimestamp(time.time()).isoformat(), 'message': 'hello'}
    return Response(json.dumps(resp_json), mimetype='application/json')

if __name__ == '__main__':
    app.run()
