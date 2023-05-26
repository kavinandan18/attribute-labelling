from mongoengine import StringField, IntField
from main.db import BaseModel


class TokenBlocklist(BaseModel):
    """
    This model is used to store revoked tokens.
    """

    jti = StringField(required=True, max_length=36)
    type = StringField(required=True, max_length=16)
    user_id = StringField(required=True)
