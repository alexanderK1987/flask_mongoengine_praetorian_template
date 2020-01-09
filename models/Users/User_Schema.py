import marshmallow_mongoengine
import models.Users.User_Model 
# schema
class User_Schema(marshmallow_mongoengine.ModelSchema):
    class Meta:
        model = models.Users.User_Model.User_Model
