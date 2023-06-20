from flask_restx import Api

from main.modules.product_attribute_lableing.view import (
    product_attribute_labelling_namespace,
)

api = Api()
api.add_namespace(product_attribute_labelling_namespace)
