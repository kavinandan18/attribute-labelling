from mongoengine import Document, StringField, ReferenceField, FloatField, ListField
from main.db import BaseModel


class Type(BaseModel):
    """
    Model for types.
    """
    name = StringField(required=True, max_length=100, unique=True)
    description = StringField()


class Brand(BaseModel):
    """
    Model for brands.
    """
    name = StringField(required=True, max_length=100)
    description = StringField()


class Attribute(BaseModel):
    """
    Model for attributes.
    """
    name = StringField(required=True, max_length=100)


class AttributeOptions(BaseModel):
    """
    Model for attribute options.
    """
    attribute_id = ReferenceField(Attribute)
    name = StringField()


class Family(BaseModel):
    """
    Model for families.
    """
    type_id = ReferenceField(Type)
    name = StringField(required=True, max_length=100)
    description = StringField()
    brands = ListField(ReferenceField(Brand))
    attributes = ListField(ReferenceField(Attribute))


class Category(BaseModel):
    """
    Model for categories.
    """
    name = StringField(required=True, max_length=100)
    description = StringField()
    family_id = ReferenceField(Family)


class Product(BaseModel):
    """
    Model for products.
    """
    type_id = ReferenceField(Type)
    family_id = ReferenceField(Family)
    category_id = ReferenceField(Category)
    brand_id = ReferenceField(Brand)
    name = StringField(required=True, max_length=100)
    description = StringField()
    prize = FloatField()
    attributes = ListField()
