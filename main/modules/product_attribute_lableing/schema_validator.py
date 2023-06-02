from marshmallow import INCLUDE, Schema, fields


class AttributeConfigSchema(Schema):
    family = fields.Str(required=True)

    class Meta:
        unknown = INCLUDE


class ProductSchema(Schema):
    family = fields.Str(required=True)
    article_id = fields.Str(required=True)

    class Meta:
        unknown = INCLUDE
