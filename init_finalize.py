import datetime
import mainframe
from models.Users.User_Model import  User_Model
from models.Users.User_Schema import User_Schema

super_user_profile = {'email': 'admin@memphis.gov',
                      'password': mainframe.guard.hash_password('memphis'),
                      'roles': ['admin'],
                      'active': True,
                      'last_login': str(datetime.datetime.now()),
                      'origin': str(datetime.datetime.now())}

super_user = User_Schema().load(super_user_profile).data

if not User_Model.email_exists(super_user.email):
    print ('super user does not exist, inserting ...')
    super_user.save()

