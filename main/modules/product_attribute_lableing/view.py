import json

import pandas as pd
from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource

from main.decorators.check_permissions import verify_permissions
from main.decorators.verify_user import verify_user
from main.modules.product_attribute_lableing.controller import (
    AttributeConfigController,
    ProductController,
)
from main.modules.product_attribute_lableing.schema_validator import (
    AttributeConfigSchema,
    ProductSchema,
)
from main.utils import get_data_from_request_or_raise_validation_error


class TestServer(Resource):
    @staticmethod
    def get():
        return make_response(jsonify(status="ok", msg="Server is running..."))


class AttributeConfigs(Resource):
    @staticmethod
    @verify_user()
    def post():
        data = get_data_from_request_or_raise_validation_error(AttributeConfigSchema, request.json, many=True)
        return make_response(jsonify(AttributeConfigController.add_attribute_configs(data)), 201)

    @staticmethod
    def get():
        return make_response(jsonify(AttributeConfigController.get_attribute_configs()), 200)


class AttributeConfig(Resource):
    method_decorators = [verify_user()]

    @staticmethod
    def put(attribute_config_id: str):
        return make_response(
            jsonify(AttributeConfigController.update_attribute_config(attribute_config_id, request.json))
        )


class Products(Resource):
    method_decorators = [verify_user()]

    @staticmethod
    @verify_permissions({"Product": ["create"]})
    def post():
        data = get_data_from_request_or_raise_validation_error(ProductSchema, request.json, many=True)
        return make_response(jsonify(ProductController.add_products(data)), 201)

    @staticmethod
    @verify_permissions({"Product": ["read"]})
    def get():
        products = ProductController.get_products(**request.args)
        return make_response(jsonify(products), 200)


class Distinct(Resource):
    @staticmethod
    def get(field: str):
        return make_response(jsonify(ProductController.get_distinct(field=field, **request.args)))


class FamilyFilters(Resource):
    @staticmethod
    def get(family: str):
        products = ProductController.get_family_products(family, **request.args)
        return make_response(jsonify(products), 200)


class FamilyDistinct(Resource):
    @staticmethod
    def get(family: str, field: str):
        return make_response(jsonify(ProductController.get_family_distinct(family, field)))


class Product(Resource):
    method_decorators = [verify_permissions({"Product": ["update"]}), verify_user()]

    @staticmethod
    def put(product_id: str):
        return make_response(jsonify(ProductController.update_product(product_id, request.json)))


class FileUpload(Resource):
    @staticmethod
    def post(file_type: str):
        file = request.files["file"]

        if (
            not file.filename.endswith(".json")
            and not file.filename.endswith(".xlsx")
            and not file.filename.endswith(".csv")
        ):
            return make_response(jsonify({"error": "Invalid file extension."}), 400)
        if file.filename.endswith(".json"):
            data = json.load(file)  # noqa
        elif file.filename.endswith(".csv"):
            df = pd.read_csv(file)  # noqa
            data = df.to_json(orient="records")
            data = json.loads(data)
        else:
            df = pd.read_excel(file)
            data = df.to_json(orient="records")
            data = json.loads(data)

        if file_type == "product":
            data = get_data_from_request_or_raise_validation_error(ProductSchema, data, many=True)
            ids, errors = ProductController.add_products(data)
            return make_response(jsonify(ids=ids, errors=errors), 201 if ids else 409)

        elif file_type == "config":
            data = get_data_from_request_or_raise_validation_error(AttributeConfigSchema, data, many=True)
            ids, errors = AttributeConfigController.add_attribute_configs(data)
            return make_response(jsonify(ids=ids, errors=errors), 201 if ids else 409)

        return make_response(jsonify(error=f"Invalid type '{file}'"))


product_attribute_labelling_namespace = Namespace("pal-api", description="Product Attribute Labelling Operations")

product_attribute_labelling_namespace.add_resource(TestServer, "/")

product_attribute_labelling_namespace.add_resource(AttributeConfigs, "/configs")
product_attribute_labelling_namespace.add_resource(AttributeConfig, "/config/<attribute_config_id>")

product_attribute_labelling_namespace.add_resource(Products, "/products")
product_attribute_labelling_namespace.add_resource(Distinct, "/products/<field>")
product_attribute_labelling_namespace.add_resource(FileUpload, "/upload/<file_type>")
product_attribute_labelling_namespace.add_resource(Product, "/product/<product_id>")

product_attribute_labelling_namespace.add_resource(FamilyFilters, "/products/family/<family>")
product_attribute_labelling_namespace.add_resource(FamilyDistinct, "/products/family/<family>/<field>")
