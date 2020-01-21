import bson
import flask
import flask_praetorian

import mainframe 
from models.Users.User_Model import User_Model
from models.Users.User_Schema import User_Schema
from models.Users.Revoked_Token_Model import Revoked_Token_Model
from models.Users.Revoked_Token_Schema import Revoked_Token_Schema

@mainframe.app.route('/auth/user/delete/<user_id>')
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted('admin')
def delete_user(user_id):
    try:
        if not User_Model.id_exists(bson.ObjectId(user_id)):
            return {'msg': 'user does not exists'}, 404
        User_Model.delete_by_id(user_id)
        return '', 204
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500 

@mainframe.app.route('/auth/token/revoke', methods=['POST'])
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted('admin')
def revoke_token():
    try:
        data = flask.request.get_json(force=True)
        token = data['token']
        jti = mainframe.guard.extract_jwt_token(token)['jti']
        if Revoked_Token_Model.is_jti_revoked(jti):
            return {'msg': 'token already revoked (%s)' % (token)}, 400
        new_revocation = Revoked_Token_Schema().load({'jti': jti}).data
        new_revocation.save()
        return {'msg': 'revocation successful (%s)' % (token)}
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500

@mainframe.app.route('/auth/user/disable/<user_id>')
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted('admin')
def disable_user(user_id):
    try:
        if not User_Model.id_exists(bson.ObjectId(user_id)):
            return {'msg': 'user does not exists'}, 404
        user = User_Model.get_by_id(user_id)
        # forbid to deactive root user
        if "root" in user.roles:
            return {'msg': 'deactivation of root user %s is forbidden' % (user.email)}, 403
        
        # user already deactivated or never activated
        if not user.active:
            return {'msg': 'user %s is already deactivated' % (user.email)}, 403

        user.active = False
        user.save()
        return {'msg': 'user %s deactivated' % (user.email)}, 200
    except Exception as e:
        return {'msg': 'Something went wrong', 'detail': str(e)}, 500


@mainframe.app.route('/auth/secret', methods=['GET'])
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted('admin')
def view_secret():
    return {'secret': 299792458.0}

