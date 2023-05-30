from marshmallow import Schema, fields
from main.utils import is_valid_object_id


class TypeSchema(Schema):
    """
    Schema for the Type model.
    """
    name = fields.Str(required=True)


class BrandSchema(Schema):
    """
    Schema for the Type brand.
    """
    name = fields.Str(required=True)
    description = fields.Str(required=False)


class AttributeSchema(Schema):
    """
    Schema for the Type model.
    """
    name = fields.Str(required=True)


class AttributeOptionsSchema(Schema):
    """
    Schema for Attribute Options
    """
    name = fields.Str(required=True)


class FamilySchema(Schema):
    """
    Schema for the Family model.
    """
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    brands = fields.List(fields.Str(validate=is_valid_object_id)) # noqa
    attributes = fields.List(fields.Str(validate=is_valid_object_id)) # noqa


class CategorySchema(Schema):
    """
    Schema for the Category model.
    """
    name = fields.Str(required=True)
    desc = fields.Str()
    family_id = fields.Str(validate=is_valid_object_id, required=True) # noqa


class InputAttributeSchema(Schema):
    attribute_id = fields.Str(validate=is_valid_object_id, required=True) # noqa
    attribute_option_id = fields.Str(validate=is_valid_object_id, required=True) # noqa


class ProductSchema(Schema):
    """
    Schema for the Product model.
    """
    type_id = fields.Str(validate=is_valid_object_id, required=True) # noqa
    family_id = fields.Str(validate=is_valid_object_id, required=True) # noqa
    category_id = fields.Str(validate=is_valid_object_id, required=False) # noqa
    brand_id = fields.Str(validate=is_valid_object_id, required=True) # noqa
    name = fields.Str(required=True)
    description = fields.Str()
    prize = fields.Float()
    attributes = fields.List(fields.Nested(InputAttributeSchema()))
