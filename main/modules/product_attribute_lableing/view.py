from flask_restx import Resource, Namespace
from main.modules.product_attribute_lableing.controller import ProductController, AttributeConfigController
from flask import request, make_response, jsonify
from main.utils import get_list_of_dict_from_request_or_raise_validation_error, \
    get_data_from_request_or_raise_validation_error
from main.modules.product_attribute_lableing.schema_validator import AttributeConfigSchema


class Product(Resource):
    def post(self):
        data = get_list_of_dict_from_request_or_raise_validation_error(request.json)
        return make_response(jsonify(ProductController.add_products(data)), 201)

    def get(self):
        products = ProductController.get_products(**request.args)
        return make_response(jsonify(products), 200)


class Distinct(Resource):
    def get(self, field: str):
        return make_response(jsonify(ProductController.get_distinct(field)))


class AttributeConfigs(Resource):
    def post(self):
        data = get_data_from_request_or_raise_validation_error(AttributeConfigSchema, request.json, many=True)
        return make_response(jsonify(AttributeConfigController.add_attribute_configs(data)), 201)

    def get(self):
        return make_response(jsonify(AttributeConfigController.get_attribute_configs()), 200)


class FamilyFilters(Resource):
    def get(self, family: str):
        products = ProductController.get_family_products(family, **request.args)
        return make_response(jsonify(products), 200)


class FamilyDistinct(Resource):
    def get(self, family: str, field: str):
        return make_response(jsonify(ProductController.get_family_distinct(family, field)))


product_attribute_labelling_namespace = Namespace("pal", description="Product Attribute Labelling Operations")
product_attribute_labelling_namespace.add_resource(AttributeConfigs, "/configs")

product_attribute_labelling_namespace.add_resource(Product, "/products")
product_attribute_labelling_namespace.add_resource(Distinct, "/products/<field>")

product_attribute_labelling_namespace.add_resource(FamilyFilters, "/products/family/<family>")
product_attribute_labelling_namespace.add_resource(FamilyDistinct, "/products/family/<family>/<field>")


