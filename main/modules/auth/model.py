from main.db import BaseModel
# from main.modules.user.model import User
from mongoengine import StringField


class AuthUser(BaseModel):
    """
    Model for auth_user.
    """

    email = StringField(max_length=100, unique=True)
    username = StringField(max_length=100, unique=True)
    password = StringField(required=True)
    role = StringField(max_length=100)
    mobile_number = StringField(max_length=100)


# @event.listens_for(AuthUser, "after_insert")
# def auth_user_created_listener(mapper, connection, target):
#     connection.execute(User.__table__.insert().values(id=target.id, username=target.username, email=target.email))
