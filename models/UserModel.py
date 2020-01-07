import bson
from mainframe import mongo
db = mongo.db

class UserModel:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def insert_to_db(self):
        inserted_id = db.users.insert_one(vars(self))
        return inserted_id

    @classmethod
    def find_by_id(cls, user_id):
        _id = bson.ObjectId(user_id)
        return db.users.find_one_or_404({'_id': _id})

    @classmethod
    def find_by_email(cls, email):
        return db.users.find_one_or_404({'email': email})
