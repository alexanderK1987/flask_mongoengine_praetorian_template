import datetime
import flask
import json
import time
import flask_mongoengine
import flask_praetorian

app = flask.Flask(__name__)
app.config.from_pyfile('app.config')
db = flask_mongoengine.MongoEngine(app)
guard = flask_praetorian.Praetorian()
# note: guard init is in the User_Model class

import views.views 
import resources.User

