# -*- coding: UTF-8 -*-
import datetime
import flask
import flask_restful
import json
import time

app = flask.Flask(__name__)
api = flask_restful.Api(app)

import views.views as views
import models.models as models
import resources.resources as resources 

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
