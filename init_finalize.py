import datetime
import mainframe
from models.Users.User_Model import  User_Model
from models.Users.User_Schema import User_Schema

super_user_profile = mainframe.app.config['SUPER_USER_PROFILE']
super_user = User_Schema().load(super_user_profile).data
super_user.password = mainframe.guard.hash_password(super_user.password)

if not User_Model.email_exists(super_user.email):
    print ('super user does not exist, inserting ...')
    super_user.save()

