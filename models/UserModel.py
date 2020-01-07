import bson
from mainframe import mongo
db = mongo.db

class UserModel:
    def __init__(self, email, password):
        self.email = email.lower()
        self.password = password

    def insert_to_db(self):
        inserted_id = db.users.insert_one(vars(self))
        return inserted_id

    @classmethod
    def find_all(cls):
        return db.users.find()

    @classmethod
    def find_by_id(cls, user_id, auto404=False):
        query = {'_id': bson.ObjectId(user_id) }
        if auto404:
            return db.users.find_one_or_404(query)
        else:
            return db.users.find_one(query)

    @classmethod
    def find_by_email(cls, email, auto404=False):
        query = {'email': email.lower() }
        if auto404:
            return db.users.find_one_or_404(query)
        else:
            return db.users.find_one(query)
