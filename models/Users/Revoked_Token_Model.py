import mainframe
import bson

db = mainframe.db

class Revoked_Token_Model(db.Document):
    # specify mongodb collection
    meta = {'collection': 'revoked_tokens'}

    _id = db.ObjectIdField()
    jti = db.StringField()

    @classmethod
    def is_jti_revoked(cls, in_jti):
        return cls.objects(jti=in_jti)

    @classmethod
    def get_all(cls):
        return cls.objects

