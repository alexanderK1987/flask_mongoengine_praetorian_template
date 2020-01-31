import bson
import datetime
import flask
import flask_praetorian

import mainframe 
from models.Users.User_Model import User_Model
from models.Users.User_Schema import User_Schema
from models.Users.Revoked_Token_Model import Revoked_Token_Model
from models.Users.Revoked_Token_Schema import Revoked_Token_Schema

@mainframe.app.route('/auth/register', methods=['POST'])
def user_registration():
    schema = User_Schema()
    try:
        data = flask.request.get_json(force=True)
        new_user = schema.load(data).data
        new_user.origin = datetime.datetime.now()
        new_user.email = new_user.email.lower().strip()
        new_user.password = mainframe.guard.hash_password(new_user.password)

        # explicitly fill the roles and active status for security purpose
        new_user.roles = ['guest']
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

@mainframe.app.route('/auth/resend_email', methods=['POST'])
def user_resend_registration_email():
    try:
        data = flask.request.get_json(force=True)
        in_email = data['email'].lower().strip()
        # user does not exist
        if not User_Model.email_exists(in_email):
            return {'msg': 'user %s not found, please register first' % (in_email)}, 404

        user = User_Model.get_by_email(in_email)
        # user already active
        if user.active:
            return {'msg': 'user %s is active already' % (user.email)} , 403
        
        mainframe.guard.send_registration_email(user.email, user=user)
        return {'msg': 'registration mail sent to %s' % (user.email)}

    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/auth/email_confirm')
def user_confirm():
    token = flask.request.args.get('token')
    user = mainframe.guard.get_user_from_registration_token(token)
    # user already active
    if user.active:
        return {'msg': 'user %s is active already' % (user.email)} , 403
        
    user.active = True
    user.save()
    return {
        'msg': 'user %s registered' % (user.email) ,
        'access_token': mainframe.guard.encode_jwt_token(user)}

@mainframe.app.route('/auth/login', methods=['POST'])
def user_login():
    schema = User_Schema()
    try:
        data = flask.request.get_json(force=True)
        input_user = schema.load(data).data
        input_user.email = input_user.email.lower().strip()
        # user does not exist
        if not User_Model.email_exists(input_user.email):
            return {'msg': 'user %s does not exist' % (input_user.email)}, 404

        # praetorian will raise exception and handle wrong credential automatically
        existing_user = mainframe.guard.authenticate(input_user.email, input_user.password)

        # user has not confirm with email
        if not existing_user.active:
            return {'msg': 'user %s has not confirmed by email' % (input_user.email)}, 403

        # log in successful
        __last_login = existing_user.last_login
        existing_user.last_login = datetime.datetime.now()
        existing_user.save()
        str_id = str(existing_user._id)
        return {
            'msg': 'logged in as %s' % (existing_user.email),
            'active': existing_user.active,
            'last_login': str(__last_login),
            'access_token': mainframe.guard.encode_jwt_token(existing_user)}

    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/auth/logout', methods=['POST'])      
@flask_praetorian.auth_required
def user_logout():
    try:
        user = flask_praetorian.current_user()
        header_token = mainframe.guard.read_token_from_header()
        header_jti = mainframe.guard.extract_jwt_token(header_token)['jti']

        disable_token = Revoked_Token_Schema().load({'jti': header_jti}).data
        disable_token.save()
        return {'msg': 'user %s logout' % (user.email)}
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/auth/refresh_token', methods=['GET'])
def refresh():
    try:
        old_token = mainframe.guard.read_token_from_header()
        new_token = mainframe.guard.refresh_jwt_token(old_token)
        return {'token': new_token}
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/user', methods=['GET'])
@flask_praetorian.auth_required
def get_users():
    try:
        return flask.jsonify(User_Schema(many=True).dump(User_Model.get_all()).data)
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/user/<user_id>', methods=['GET'])
@flask_praetorian.auth_required
def get_user(user_id):
    try:
        if not User_Model.id_exists(bson.ObjectId(user_id)):
            return {'msg': 'user does not exists'}, 404
        return User_Schema().dump(User_Model.get_by_id(user_id)) 
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/whoami', methods=['GET'])
@flask_praetorian.auth_required
def who_am_i():
    try:
        return User_Schema().dump(flask_praetorian.current_user())
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 
