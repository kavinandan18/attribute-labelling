from mongoengine import IntField, StringField

from main.db import BaseModel


class Product(BaseModel):
    """
    Model for products.
    """

    family = StringField(required=True)
    article_id = IntField(required=True, unique=True)


class AttributeConfig(BaseModel):
    """
    Model for Attribute Config
    """

    family = StringField(required=True, unique=True)
