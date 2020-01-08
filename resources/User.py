import bson
import flask
import flask_restful 
import datetime
import json 

#from models import User_Model, User_Schema
import models.Users.User_Model
import models.Users.User_Schema
from passlib.hash import pbkdf2_sha256 as SHA256

class UserRegistration(flask_restful.Resource):
    def post(self):
        schema = models.Users.User_Schema.User_Schema()
        try:
            data = flask.request.json
            new_user = schema.load(data).data
            new_user.origin = datetime.datetime.now()
            new_user.email = new_user.email.lower()
            print (new_user.password)
            new_user.password = SHA256.hash(new_user.password)

            # check whether email is already used
            if not models.Users.User_Model.User_Model.objects(email=new_user.email):
                new_user.save()
                return {'_id': str(new_user.auto_id_0)}
            else:
                return {'message': ('user %s already existed' % new_user.email)}, 400 

        except Exception as e:
            return {'message': 'Something went wrong', 'detail': str(e)}, 500 

class UserLogin(flask_restful.Resource):
    def post(self):
        schema = models.Users.User_Schema.User_Schema()
        try:
            data = flask.request.json
            input_user = schema.load(data).data
            input_user.email = input_user.email.lower()
            # user does not exist
            if not models.Users.User_Model.User_Model.objects(email=input_user.email):
                return {'message': ('user %s does not exist' % input_user.email)}, 404

            existing_user = models.Users.User_Model.User_Model.objects.get(email=input_user.email)
            # wrong password
            if not SHA256.verify(input_user.password, existing_user.password):
                return {'message': 'wrong credential'}, 403
            # log in successful
            else:
                __last_login = existing_user.last_login
                existing_user.last_login = datetime.datetime.now()
                existing_user.save()
                response_json = {'message': ('logged in as %s' % existing_user.email),
                                 'active': existing_user.active,
                                 'last_login': str(__last_login)}
                return response_json

        except Exception as e:
            return {'message': 'Something went wrong', 'detail': str(e)}, 500 
      
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
            if not models.Users.User_Model.User_Model.objects(_id=bson.ObjectId(user_id)):
                return {'message': 'user does not exists'}, 404
            result = models.Users.User_Model.User_Model.objects.get(_id=bson.ObjectId(user_id))
            schema = models.Users.User_Schema.User_Schema()
            return schema.dump(result) 

    def delete(self, user_id):
        try:
            if not models.Users.User_Model.User_Model.objects(_id=bson.ObjectId(user_id)):
                return {'message': 'user does not exists'}, 404
            models.Users.User_Model.User_Model.objects(_id=bson.ObjectId(user_id)).delete()
            return '', 204
        except Exception as e:
            return {'message': 'Something went wrong', 'detail': str(e)}, 500 

class SecretResource(flask_restful.Resource):
    def get(self):
        return {'answer': 42}

