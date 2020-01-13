import marshmallow_mongoengine
import models.Users.Revoked_Token_Model 
# schema
class Revoked_Token_Schema(marshmallow_mongoengine.ModelSchema):
    class Meta:
        model = models.Users.Revoked_Token_Model.Revoked_Token_Model
