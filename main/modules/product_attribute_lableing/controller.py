from main.modules.product_attribute_lableing.model import Product, AttributeConfig
from bson.objectid import ObjectId


class AttributeConfigController:
    @classmethod
    def add_attribute_configs(cls, attribute_configs: list):
        inserted_ids = []
        errors = []
        for attribute_config in attribute_configs:
            if AttributeConfig.get_objects_with_filter(family=attribute_config["family"]):
                attribute_config["error"] = "Family already exists"
                errors.append(attribute_config)
                continue
            attribute_config = AttributeConfig.create(attribute_config, to_json=True)
            inserted_ids.append(attribute_config["_id"])
        return {
            "ids": inserted_ids,
            "errors": errors
        }

    @classmethod
    def get_attribute_configs(cls):
        return AttributeConfig.get_all()

    @classmethod
    def get_attribute_mapping_from_config(cls, family: str):
        record = AttributeConfig.get_objects_with_filter(only_first=True, family=family)

        mapping = {}

        if record:
            for key, value in record.items():
                if isinstance(value, dict):
                    mapping[key] = value["name"]
        return mapping


class ProductController:

    @classmethod
    def convert_keys_according_to_db(cls, mapping: dict, product_data: dict):
        converted_data = {}
        mapping = {v: k for k, v in mapping.items()}
        for key, value in product_data.items():
            if key in mapping:
                converted_data[mapping[key]] = value
            else:
                converted_data[key] = value
        return converted_data

    @classmethod
    def convert_data_according_to_response(cls, product_data: dict,  mapping: dict = None):
        converted_data = {}
        if not mapping:
            mapping = AttributeConfigController.get_attribute_mapping_from_config(product_data["family"])
        for key, value in product_data.items():
            if key in mapping:
                converted_data[mapping[key]] = value
            else:
                converted_data[key] = value
        return converted_data

    @classmethod
    def convert_field_name_according_to_db(cls, mapping: dict, filed: str):
        if filed is mapping:
            return filed
        mapping = {v: k for k, v in mapping.items()}
        return mapping.get(filed) or filed

    @classmethod
    def add_products(cls, products: list[dict]):
        inserted_ids = []
        for product in products:
            mapping = AttributeConfigController.get_attribute_mapping_from_config(product["family"])
            product = cls.convert_keys_according_to_db(mapping, product)
            inserted_ids.append(Product.create(product, to_json=True)["_id"])
        return inserted_ids

    @classmethod
    def get_products(cls, **filters):
        products = Product.get_objects_with_filter(**filters)
        return [cls.convert_data_according_to_response(product) for product in products]

    @classmethod
    def get_distinct(cls, field: str):
        distinct = Product.get_distinct_with_filters(field)
        return [str(i) if isinstance(i, ObjectId) else i for i in distinct]

    @classmethod
    def get_family_products(cls, family: str, **filters):
        mapping = AttributeConfigController.get_attribute_mapping_from_config(family)
        filters = cls.convert_keys_according_to_db(mapping, filters)
        filters["family"] = family
        products = Product.get_objects_with_filter(**filters)
        return [cls.convert_data_according_to_response(product, mapping) for product in products]

    @classmethod
    def get_family_distinct(cls, family: str, field: str):
        mapping = AttributeConfigController.get_attribute_mapping_from_config(family)
        field = cls.convert_field_name_according_to_db(mapping, field)
        distinct = Product.get_distinct_with_filters(field, **{"family": family})
        return [str(i) if isinstance(i, ObjectId) else i for i in distinct]

