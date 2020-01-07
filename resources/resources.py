import flask_restful

class UserRegistration(flask_restful.Resource):
    def post(self):
        return {'message': 'User registration'}


class UserLogin(flask_restful.Resource):
    def post(self):
        return {'message': 'User login'}
      
      
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
        return {
            'answer': 42
        }
