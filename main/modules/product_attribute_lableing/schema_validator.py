from marshmallow import Schema, fields, validate
from main.db import BaseModel, db


class TypeSchema(Schema):
    """
    Schema for the Type model.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    desc = fields.Str()


class CategorySchema(Schema):
    """
    Schema for the Category model.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    desc = fields.Str()
    family_id = fields.Int()


class FamilySchema(Schema):
    """
    Schema for the Family model.
    """
    id = fields.Int(dump_only=True)
    type_id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(max=100))
    desc = fields.Str()
    brands = fields.List(fields.Nested('BrandSchema', exclude=('families',)))
    attributes = fields.List(fields.Nested('AttributeSchema', exclude=('families',)))


class AttributeSchema(Schema):
    """
    Schema for the Attribute model.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))


class AttributeOptionsSchema(Schema):
    """
    Schema for the AttributeOptions model.
    """
    id = fields.Int(dump_only=True)
    attribute_id = fields.Int()
    family_id = fields.Int()


class BrandSchema(Schema):
    """
    Schema for the Brand model.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    desc = fields.Str()


class AttributeFamilyMappingSchema(Schema):
    """
    Schema for the AttributeFamilyMapping model.
    """
    id = fields.Int(dump_only=True)
    attribute_id = fields.Int()
    family_id = fields.Int()


class BrandFamilyMappingSchema(Schema):
    """
    Schema for the BrandFamilyMapping model.
    """
    id = fields.Int(dump_only=True)
    brand_id = fields.Int()
    family_id = fields.Int()


class ProductSchema(Schema):
    """
    Schema for the Product model.
    """
    id = fields.Int(dump_only=True)
    type_id = fields.Int()
    family_id = fields.Int()
    category_id = fields.Int()
    brand_id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(max=100))
    desc = fields.Str()
    prize = fields.Float()
    attributes = fields.List(fields.Nested('AttributeSchema', exclude=('products',)))


# Usage example:
type_schema = TypeSchema()
category_schema = CategorySchema()
family_schema = FamilySchema()
attribute_schema = AttributeSchema()
attribute_options_schema = AttributeOptionsSchema()
brand_schema = BrandSchema()
attribute_family_mapping_schema = AttributeFamilyMappingSchema()
brand_family_mapping_schema = BrandFamilyMappingSchema()
product_schema = ProductSchema()
