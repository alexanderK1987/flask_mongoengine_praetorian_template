from mainframe import db
from marshmallow_mongoengine import ModelSchema
import models.Users.User_Model as User_Model
# schema
class User_Schema(ModelSchema):
    class Meta:
        model = User_Model.User_Model
