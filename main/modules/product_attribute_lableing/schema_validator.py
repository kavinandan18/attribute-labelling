from marshmallow import Schema, fields, INCLUDE


class AttributeConfigSchema(Schema):
    family = fields.Str(required=True)

    class Meta:
        unknown = INCLUDE
