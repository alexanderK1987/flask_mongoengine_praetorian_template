from bson import json_util
import flask
import flask_restful
import flask_restful.reqparse
from flask_restful import request
import json 

# parser for parsing tokens requireed for authentication 
parser = flask_restful.reqparse.RequestParser()
parser.add_argument('email', help='This field cannot be blamk', required=True)
parser.add_argument('password', help='This field cannot be blamk', required=True)

from models import UserModel 
from mainframe import api 

class UserRegistration(flask_restful.Resource):
    def post(self):
        data = parser.parse_args()
        new_user = UserModel.UserModel(data['email'], data['password'])
        try:
            if UserModel.UserModel.find_by_email(new_user.email) == None:
                _id = new_user.insert_to_db().inserted_id
                return json.loads(json_util.dumps({'_id': _id}))
            else:
                return {'message': ('user %s already existed' % new_user.email)}, 500 

        except Exception as e:
            return {'message': 'Something went wrong', 'detail': str(e)}, 500 

class UserLogin(flask_restful.Resource):
    def post(self):
        data = parser.parse_args()
        user = UserModel.UserModel.find_by_email(data['email'])
        if data['password'] == user['password']:
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
            return json.loads(json_util.dumps(UserModel.UserModel.find_all()))
        else:
            return json.loads(json_util.dumps(UserModel.UserModel.find_by_id(user_id)))

class SecretResource(flask_restful.Resource):
    def get(self):
        return {'answer': 42}

