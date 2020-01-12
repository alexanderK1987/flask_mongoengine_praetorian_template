import bson
import datetime
import flask
import flask_praetorian
import sys
import time
import traceback

import mainframe 
from models.Users.User_Model import User_Model
from models.Users.User_Schema import User_Schema

@mainframe.app.route('/registration', methods=['POST'])
def user_registration():
    schema = User_Schema()
    try:
        data = flask.request.get_json(force=True)
        new_user = schema.load(data).data
        new_user.origin = datetime.datetime.now()
        new_user.email = new_user.email.lower().strip()
        new_user.password = mainframe.guard.hash_password(new_user.password)

        # explicitly fill the roles and active status for security purpose
        new_user.role = ['guest']
        new_user.active = False

        # check whether email is already used
        if User_Model.email_exists(new_user.email):
            return {'msg': ('user %s already existed' % new_user.email)}, 400 
        else:
            new_user.save()
            str_id = str(new_user.auto_id_0)
            # for flask-praetorian, must send a user instance with a valid _id field
            new_user._id = bson.ObjectId(str_id)
            mainframe.guard.send_registration_email(new_user.email, user=new_user)
            return {'_id': str_id, 
                    'msg': 'registration mail sent to %s' % (new_user.email)} 

    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/registration/resend/<user_id>', methods=['POST'])
def user_resend_registration_email(user_id):
    if not User_Model.id_exists(user_id):
        return {'msg': 'user not found, please register first'}, 404
    else:
        user = User_Mode.get_by_id(user_id)
        mainframe.guard.send_registration_email(user.email, user=user)
        return {'msg': 'registration mail sent to %s' % (user.email)}

@mainframe.app.route('/registration/confirm')
def user_confirm():
    token = flask.request.args.get('token')
    data = mainframe.guard.extract_jwt_token(token, access_type=flask_praetorian.constants.AccessType.register)
    print (data)
    user = mainframe.guard.get_user_from_registration_token(token)
    user.active = True
    user.save()
    return {'msg': 'user %s registered' % (user.email) ,
            'access_token': mainframe.guard.encode_jwt_token(user)}

@mainframe.app.route('/login', methods=['POST'])
def user_login():
    schema = User_Schema()
    try:
        data = flask.request.get_json(force=True)
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
    return flask.jsonify(User_Schema(many=True).dump(User_Model.get_all()).data)

@mainframe.app.route('/user/<user_id>', methods=['GET', 'DELETE'])
def user(user_id):
    if not User_Model.id_exists(bson.ObjectId(user_id)):
        return {'msg': 'user does not exists'}, 404
    try:
        if flask.request.method == 'GET':
            return User_Schema().dump(User_Model.get_by_id(user_id)) 
        
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

