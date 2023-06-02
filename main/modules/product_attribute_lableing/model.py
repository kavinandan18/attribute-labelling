from mongoengine import StringField
from main.db import BaseModel


class Product(BaseModel):
    """
    Model for products.
    """
    family = StringField(required=True)


class AttributeConfig(BaseModel):
    """
    Model for Attribute Config
    """
    family = StringField(required=True, unique=True)
