from mongoengine import Document, StringField, ReferenceField, FloatField, ListField

class Type(Document):
    """
    Model for types.
    """
    name = StringField(required=True, max_length=100)
    desc = StringField()


class Category(Document):
    """
    Model for categories.
    """
    name = StringField(required=True, max_length=100)
    desc = StringField()
    family_id = ReferenceField('Family')


class Family(Document):
    """
    Model for families.
    """
    type_id = ReferenceField('Type')
    name = StringField(required=True, max_length=100)
    desc = StringField()
    brands = ListField(ReferenceField('Brand'))
    attributes = ListField(ReferenceField('Attribute'))


class Attribute(Document):
    """
    Model for attributes.
    """
    name = StringField(required=True, max_length=100)


class AttributeOptions(Document):
    """
    Model for attribute options.
    """
    attribute_id = ReferenceField('Attribute')
    family_id = ReferenceField('Family')


class Brand(Document):
    """
    Model for brands.
    """
    name = StringField(required=True, max_length=100)
    desc = StringField()


class AttributeFamilyMapping(Document):
    """
    Model for attribute-family mapping.
    """
    attribute_id = ReferenceField('Attribute')
    family_id = ReferenceField('Family')


class BrandFamilyMapping(Document):
    """
    Model for brand-family mapping.
    """
    brand_id = ReferenceField('Brand')
    family_id = ReferenceField('Family')


class Product(Document):
    """
    Model for products.
    """
    type_id = ReferenceField('Type')
    family_id = ReferenceField('Family')
    category_id = ReferenceField('Category')
    brand_id = ReferenceField('Brand')
    name = StringField(required=True, max_length=100)
    desc = StringField()
    prize = FloatField()
    attributes = ListField(ReferenceField('Attribute'))
