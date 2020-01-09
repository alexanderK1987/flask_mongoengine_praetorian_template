import bson
import datetime
import flask
import flask_praetorian

import mainframe 
from models.Users.User_Model import User_Model
from models.Users.User_Schema import User_Schema

@mainframe.app.route('/registration', methods=['POST'])
def user_registration():
    schema = User_Schema()
    try:
        data = flask.request.json
        new_user = schema.load(data).data
        new_user.origin = datetime.datetime.now()
        new_user.email = new_user.email.lower().strip()
        new_user.password = mainframe.guard.hash_password(new_user.password)
        # check whether email is already used
        if not User_Model.email_exists(new_user.email):
            new_user.save()
            str_id = str(new_user.auto_id_0)
            return {'_id': str_id} 
        else:
            return {'msg': ('user %s already existed' % new_user.email)}, 400 

    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/login', methods=['POST'])
def user_login():
    schema = User_Schema()
    try:
        data = flask.request.json
        input_user = schema.load(data).data
        input_user.email = input_user.email.lower().strip()
        # user does not exist
        if not User_Model.email_exists(input_user.email):
            return {'msg': ('user %s does not exist' % input_user.email)}, 404

        # praetorian will raise exception and handle wrong credential automatically
        existing_user = mainframe.guard.authenticate(input_user.email, input_user.password)

        # log in successful
        __last_login = existing_user.last_login
        existing_user.last_login = datetime.datetime.now()
        existing_user.save()
        str_id = str(existing_user._id)
        return {'msg': ('logged in as %s' % existing_user.email),
                'active': existing_user.active,
                'last_login': str(__last_login),
                'access_token': mainframe.guard.encode_jwt_token(existing_user)}

    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/logout/access', methods=['POST'])      
def user_logout_access():
    return {'msg': 'User logout'}

@mainframe.app.route('/logout/refresh', methods=['POST'])      
def user_logout_refresh():
    return {'msg': 'User logout'}

@mainframe.app.route('/token/refresh', methods=['POST'])
def token_refresh():
    return {'msg': 'Token refresh'}

@mainframe.app.route('/user', methods=['GET'])
def users():
    results = User_Model.get_all()
    schema = User_Schema(many=True)
    return flask.jsonify(schema.dump(results).data)

@mainframe.app.route('/user/<user_id>', methods=['GET', 'DELETE'])
def user(user_id):
    if not User_Model.id_exists(bson.ObjectId(user_id)):
        return {'msg': 'user does not exists'}, 404
    try:
        if flask.request.method == 'GET':
            result = User_Model.get_by_id(bson.ObjectId(user_id))
            schema = User_Schema()
            return schema.dump(result) 
        
        elif flask.request.method == 'DELETE':
            User_Model.delete_by_id(user_id)
            return '', 204

    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/secret', methods=['GET'])
@flask_praetorian.roles_accepted('admin')
def secret():
    return {'answer': 42}

mainframe.guard.init_app(mainframe.app, User_Model)

