from mainframe import app
import datetime
import flask 
import json 
import time 
# view only gives few info on RESTful services

@app.route('/', methods=['GET'])
@app.route('/hello', methods=['GET'])
def main():
    resp_json = {'utctime': datetime.datetime.utcfromtimestamp(time.time()).isoformat(), 'message': 'hello'}
    return flask.Response(json.dumps(resp_json), mimetype='application/json')


