# -*- coding: UTF-8 -*-
import datetime
import flask
import flask_restful
import json
import time
from flask_pymongo import PyMongo

app = flask.Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://memphis_admin:memphis@127.0.0.1:27017/memphis'
mongo = PyMongo(app)
api = flask_restful.Api(app)

import views.views 
import models.UserModel
import resources.User


api.add_resource(resources.User.UserRegistration, '/registration')
api.add_resource(resources.User.UserLogin, '/login')
api.add_resource(resources.User.UserLogoutAccess, '/logout/access')
api.add_resource(resources.User.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.User.TokenRefresh, '/token/refresh')
api.add_resource(resources.User.AllUsers, '/users')
api.add_resource(resources.User.SecretResource, '/secret')
