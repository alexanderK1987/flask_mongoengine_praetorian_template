from mainframe import app
import datetime
import flask 
import json 
import time 
# view only gives few info on RESTful services

@app.route('/', methods=['GET'])
def hello():
    resp_json = {'utctime': datetime.datetime.utcfromtimestamp(time.time()).isoformat(), 'msg': 'hello'}
    return flask.Response(json.dumps(resp_json), mimetype='application/json')


