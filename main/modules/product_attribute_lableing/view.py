from flask_restx import Resource, Namespace
from main.modules.product_attribute_lableing.controller import TypeController, AttributeController, \
    AttributeOptionsController, BrandController, FamilyController, ProductController
from flask import request, make_response, jsonify
from main.utils import get_data_from_request_or_raise_validation_error
from main.modules.product_attribute_lableing.schema_validator import TypeSchema, BrandSchema, \
    AttributeSchema, AttributeOptionsSchema, FamilySchema, ProductSchema


class Type(Resource):
    def post(self):
        data = get_data_from_request_or_raise_validation_error(TypeSchema, request.json, many=True)
        inserted_count = TypeController.add_types(data)
        return make_response(jsonify(inserted_count=inserted_count), 201)

    def get(self):
        types = TypeController.get_types()
        return make_response(jsonify(types), 200)


class Brand(Resource):
    def post(self):
        data = get_data_from_request_or_raise_validation_error(BrandSchema, request.json, many=True)
        inserted_count = BrandController.add_brands(data)
        return make_response(jsonify(inserted_count=inserted_count), 201)

    def get(self):
        brands = BrandController.get_brands()
        return make_response(jsonify(brands), 200)


class Attribute(Resource):
    def post(self):
        data = get_data_from_request_or_raise_validation_error(AttributeSchema, request.json, many=True)
        inserted_count = AttributeController.add_attributes(data)
        return make_response(jsonify(inserted_count=inserted_count), 201)

    def get(self):
        attributes = AttributeController.get_attributes()
        return make_response(jsonify(attributes), 200)


class AttributeOptions(Resource):
    def post(self, attribute_id):
        data = get_data_from_request_or_raise_validation_error(AttributeOptionsSchema, request.json, many=True)
        inserted_count = AttributeOptionsController.add_attribute_options(attribute_id, data)
        return make_response(jsonify(inserted_count=inserted_count), 201)

    def get(self, attribute_id):
        attribute_options = AttributeOptionsController.get_attribute_options(attribute_id)
        return make_response(jsonify(attribute_options), 200)


class Family(Resource):
    def post(self, type_id):
        data = get_data_from_request_or_raise_validation_error(FamilySchema, request.json, many=True)
        inserted_count = FamilyController.add_families(type_id, data)
        return make_response(jsonify(inserted_count=inserted_count), 201)

    def get(self, type_id):
        families = FamilyController.get_families(type_id)
        return make_response(jsonify(families), 200)


class Product(Resource):
    def post(self):
        data = get_data_from_request_or_raise_validation_error(ProductSchema, request.json, many=True)
        inserted_count = ProductController.add_products(data)
        return make_response(jsonify(inserted_count=inserted_count), 201)

    def get(self):
        products = ProductController.get_products()
        return make_response(jsonify(products), 200)


product_attribute_labelling_namespace = Namespace("pal", description="Product Attribute Labelling Operations")
product_attribute_labelling_namespace.add_resource(Type, "/types")
product_attribute_labelling_namespace.add_resource(Brand, "/brands")
product_attribute_labelling_namespace.add_resource(Attribute, "/attributes")
product_attribute_labelling_namespace.add_resource(AttributeOptions, "/attribute/<attribute_id>/options")
product_attribute_labelling_namespace.add_resource(Family, "/family/<type_id>")
product_attribute_labelling_namespace.add_resource(Product, "/products")
