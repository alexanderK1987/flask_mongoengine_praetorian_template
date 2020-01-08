from mainframe import db

class User_Model(db.Document):
    # specify mongodb collection
    meta = {'collection': 'users'}

    _id        = db.ObjectIdField()
    email      = db.StringField(required=True)
    password   = db.StringField(required=True)
    origin     = db.DateTimeField(default=None)
    active     = db.BooleanField(default=False)
    last_login = db.DateTimeField(default=None)

