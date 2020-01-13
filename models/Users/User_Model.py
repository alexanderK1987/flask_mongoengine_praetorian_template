import mainframe
import bson

db = mainframe.db

class User_Model(db.Document):
    # specify mongodb collection
    meta = {'collection': 'users'}

    _id        = db.ObjectIdField()
    email      = db.StringField(required=True)
    password   = db.StringField(required=True)
    origin     = db.DateTimeField(default=None)
    active     = db.BooleanField(default=False)
    last_login = db.DateTimeField(default=None)
    roles      = db.ListField(db.StringField())

    # used by praetorian
    @property
    def rolenames(self):
        try:
            return [] if (self.roles == None) else self.roles
        except Exception:
            return []

    # used by praetorian
    @classmethod
    def get_all(cls):
        return cls.objects

    # used by praetorian
    @classmethod
    def identify(cls, in_id):
        if cls.id_exists(in_id):
            return cls.get_by_id(in_id)
        return None

    # used by praetorian
    @classmethod
    def lookup(cls, in_email):
        if cls.email_exists(in_email):
            return cls.get_by_email(in_email)
        return None

    # used by praetorian
    @property
    def identity(self):
        return str(self._id)

    # used by praetorian
    def is_valid(self):
        return self.active

    @classmethod
    def get_by_id(cls, in_id):
        if type(in_id) is str:
            in_id = bson.ObjectId(in_id)
        return cls.objects.get(_id=in_id)

    @classmethod
    def delete_by_id(cls, in_id):
        if type(in_id) is str:
            in_id = bson.ObjectId(in_id)
        return cls.objects(_id=in_id).delete()

    @classmethod
    def get_by_email(cls, in_email):
        in_email = str(in_email)
        return cls.objects.get(email=in_email)

    @classmethod
    def email_exists(cls, in_email):
        in_email = str(in_email)
        return cls.objects(email=in_email)

    @classmethod
    def id_exists(cls, in_id):
        if type(in_id) is str:
            in_id = bson.ObjectId(in_id)
        return cls.objects(_id=in_id)

