import bson
import flask
import flask_restful
import flask_restful.reqparse
from flask_restful import request
import datetime
import json 

#from models import User_Model, User_Schema
import models.Users.User_Model
import models.Users.User_Schema
class UserRegistration(flask_restful.Resource):
    def post(self):
        data = request.json
        # MARSHMALLOW HAS PROBLEM CONVERTING DATETIME
        data['origin'] = str(datetime.datetime.now())
        schema = models.Users.User_Schema.User_Schema()
        new_user = schema.load(data).data
        try:
            if not models.Users.User_Model.User_Model.objects(email=new_user.email):
                new_user.save()
                return {'_id': str(new_user.auto_id_0)}
            else:
                return {'message': ('user %s already existed' % new_user.email)}, 400 

        except Exception as e:
            return {'message': 'Something went wrong', 'detail': str(e)}, 500 

class UserLogin(flask_restful.Resource):
    def post(self):
        data = request.json
        user = User_Model.objects(email=data['email'])
        if data['password'] == user.password:
            return {'message': ('logged in as %s.' % user['email'])}
        else:
            return {'message': 'wrong credential'}, 500
      
class UserLogoutAccess(flask_restful.Resource):
    def post(self):
        return {'message': 'User logout'}
      
class UserLogoutRefresh(flask_restful.Resource):
    def post(self):
        return {'message': 'User logout'}
      
class TokenRefresh(flask_restful.Resource):
    def post(self):
        return {'message': 'Token refresh'}
     
class User(flask_restful.Resource):
    def get(self, user_id=None):
        if None == user_id:
            results = models.Users.User_Model.User_Model.objects.all()
            schema = models.Users.User_Schema.User_Schema(many=True)
            return schema.dump(results) 
        else:
            result = models.Users.User_Model.User_Model.objects.get(_id=bson.ObjectId(user_id))
            schema = models.Users.User_Schema.User_Schema()
            return schema.dump(result) 

class SecretResource(flask_restful.Resource):
    def get(self):
        return {'answer': 42}

