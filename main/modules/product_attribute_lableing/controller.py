from main.modules.product_attribute_lableing.model import Type, Attribute, AttributeOptions, \
    Brand, Family, Category, Product
from bson.objectid import ObjectId
from main.exceptions import RecordNotFoundError


class TypeController:

    @classmethod
    def add_types(cls, data: list) -> int:
        """
        To add a list of types.
        :param data:
        :return:
        """
        return Type.bulk_write(data)

    @classmethod
    def get_types(cls) -> list:
        """
        To get all types
        :return:
        """
        return Type.get_all()


class BrandController:

    @classmethod
    def add_brands(cls, data: list) -> int:
        """
        To add brands to the db.
        :param data:
        :return:
        """
        return Brand.bulk_write(data)

    @classmethod
    def get_brands(cls) -> list:
        """
        To get all brands
        :return:
        """
        return Brand.get_all()


class AttributeController:
    @classmethod
    def add_attributes(cls, data: list) -> int:
        """
        To add attributes in db.
        :param data:
        :return:
        """
        return Attribute.bulk_write(data)

    @classmethod
    def get_attributes(cls) -> list:
        """
        To get all types
        :return:
        """
        return Attribute.get_all()


class AttributeOptionsController:

    @classmethod
    def add_attribute_options(cls, attribute_id: str, data: list):
        """
        To add options to attributes
        :param data:
        :param attribute_id:
        :return:
        """
        attribute_id = ObjectId(attribute_id)
        if not Attribute.objects(id=attribute_id).first():
            raise RecordNotFoundError(f"attribute_id '{str(attribute_id)}' not found")

        for i in data:
            i["attribute_id"] = attribute_id
        return AttributeOptions.bulk_write(data)

    @classmethod
    def get_attribute_options(cls, attribute_id) -> list:
        """
        Get available options of an attribute.
        :param attribute_id:
        :return:
        """
        options = AttributeOptions.objects(attribute_id=attribute_id)
        return [option.to_json() for option in options]


class FamilyController:
    @classmethod
    def add_families(cls, type_id: str, data: list) -> int:
        """
        To add family in db.
        :param type_id:
        :param data:
        :return:
        """
        type_id = ObjectId(type_id)
        if not Type.objects(id=type_id).first():
            raise RecordNotFoundError(f"type_id '{str(type_id)}' not found")

        for i in data:
            if not Attribute.check_if_all_exists(i["attributes"]):
                raise RecordNotFoundError(f"Invalid attribute ids present in this list '{i['attributes']}'")

            if not Brand.check_if_all_exists(i["brands"]):
                raise RecordNotFoundError(f"Invalid brands ids present in this list '{i['brands']}'")
            i["attributes"] = [ObjectId(attribute_id) for attribute_id in i["attributes"]]
            i["brands"] = [ObjectId(brand_id) for brand_id in i["brands"]]
            i["type_id"] = type_id
        return Family.bulk_write(data)

    @classmethod
    def get_families(cls, type_id) -> list:
        """
        To get all families of a type.
        :param type_id:
        :return:
        """
        families = Family.objects.select_related(max_depth=2)
        return [family.to_json() for family in families]


class ProductController:

    @classmethod
    def add_products(cls, data: list) -> int:
        for product in data:
            if not Type.objects(id=product["type_id"]).first():
                raise RecordNotFoundError(f"type_id '{product['type_id']}' not found")
            if not Family.objects(id=product["family_id"]).first():
                raise RecordNotFoundError(f"family_id '{product['family_id']}' not found")
            if not Brand.objects(id=product["brand_id"]).first():
                raise RecordNotFoundError(f"brand_id '{product['brand_id']}' not found")
            if product.get("category_id"):
                if not Category.objects(id=product["category_id"]).first():
                    raise RecordNotFoundError(f"category_id '{product['category_id']}' not found")
                product["category_id"] = ObjectId(product["category_id"])

            product["type_id"] = ObjectId(product["type_id"])
            product["brand_id"] = ObjectId(product["brand_id"])
            product["family_id"] = ObjectId(product["family_id"])

            for attribute in product.get("attributes", []):
                if not Attribute.objects(id=attribute["attribute_id"]).first():
                    raise RecordNotFoundError(f"attribute_id '{attribute['attribute_id']}' not found")

                if not AttributeOptions.objects(id=attribute["attribute_option_id"]).first():
                    raise RecordNotFoundError(f"attribute_option_id '{attribute['attribute_option_id']}' not found")

                attribute["attribute_id"] = ObjectId(attribute["attribute_id"])
                attribute["attribute_option_id"] = ObjectId(attribute["attribute_option_id"])

        return Product.bulk_write(data)

    @classmethod
    def get_products(cls) -> list:
        """
        To get all products.
        :return:
        """
        return Product.get_all()
