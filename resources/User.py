from bson import json_util
import flask
import flask_restful
import flask_restful.reqparse
import json 

# parser for parsing tokens requireed for authentication 
parser = flask_restful.reqparse.RequestParser()
parser.add_argument('email', help='This field cannot be blamk', required=True)
parser.add_argument('password', help='This field cannot be blamk', required=True)

from models import UserModel 

class UserRegistration(flask_restful.Resource):
    def post(self):
        data = parser.parse_args()
        new_user = UserModel.UserModel(data['email'], data['password'])

        try:
            if UserModel.UserModel.find_by_email(new_user.email) == None:
                _id = new_user.insert_to_db().inserted_id
                created = json_util.dumps({'_id': _id})
                return flask.Response(created, mimetype='application/json')
            else:
                return {'message': ('user %s already existed' % new_user.email)}, 500 


        except Exception as e:
            return {'message': 'Something went wrong', 'detail': str(e)}, 500 

class UserLogin(flask_restful.Resource):
    def post(self):
        data = parser.parse_args()
        return data 
      
class UserLogoutAccess(flask_restful.Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(flask_restful.Resource):
    def post(self):
        return {'message': 'User logout'}
      
class TokenRefresh(flask_restful.Resource):
    def post(self):
        return {'message': 'Token refresh'}
      
      
class AllUsers(flask_restful.Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}
      
      
class SecretResource(flask_restful.Resource):
    def get(self):
        return {'answer': 42}
