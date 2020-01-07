from mainframe import app
import datetime
import flask 
import json 
import time 

@app.route('/')
@app.route('/hello')
def main():
    resp_json = {'utctime': datetime.datetime.utcfromtimestamp(time.time()).isoformat(), 'message': 'hello'}
    return flask.Response(json.dumps(resp_json), mimetype='application/json')

