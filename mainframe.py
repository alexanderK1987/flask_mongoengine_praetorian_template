import datetime
import flask
import json
import time
import flask_mongoengine
import flask_praetorian
import flask_mail

app = flask.Flask(__name__)
app.config.from_pyfile('app.config')
db = flask_mongoengine.MongoEngine(app)

from models.Users.User_Model import User_Model
from models.Users.Revoked_Token_Model import Revoked_Token_Model
guard = flask_praetorian.Praetorian()
guard.init_app(app, User_Model, is_blacklisted=Revoked_Token_Model.is_jti_revoked)

mail = flask_mail.Mail(app)

import resources.Hello 
import resources.User
import resources.AdminFunction
import resources.Sitemap
import init_finalize 

