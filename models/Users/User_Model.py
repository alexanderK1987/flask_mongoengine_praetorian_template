from mainframe import db

class User_Model(db.Document):
    meta = {'collection': 'users'}
    _id = db.ObjectIdField()
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    origin = db.DateTimeField()
