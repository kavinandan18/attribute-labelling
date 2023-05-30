from mongoengine import Document, DateTimeField, connect, StringField, IntField
from datetime import datetime
from bson.objectid import ObjectId
import json
from mongoengine.queryset.visitor import Q
import os
from config import config_by_name

config = config_by_name[os.getenv("FLASK_ENV") or "dev"]

connect(
    db='attribute_labelling',
    host='localhost',
    port=27017
)


class Test(Document):
    email = StringField(max_length=100, unique=True)
    age = IntField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=None, on_update=datetime.now)

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        self._convert_object_ids_to_strings(data)
        return json.loads(json.dumps(data))

    def _convert_object_ids_to_strings(self, data):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = str(datetime)
            elif isinstance(value, dict):
                self._convert_object_ids_to_strings(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._convert_object_ids_to_strings(item)

    @classmethod
    def create(cls, data: dict, to_json=False):
        """
        This function is used to create the record.
        :param data: Data to create the record
        :param to_json: Flag to get response in json
        :return: Created document
        """
        record = cls(**data)
        record.save()
        if to_json:
            return record.to_json()
        return record

    def update(self, data: dict):
        """
        This function is used to update the record.
        :param data: Data to update the record
        """
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.updated_at = datetime.now()
        self.save()

    @classmethod
    def filter(cls, filters_dict, return_all=False, to_json=False):
        pipeline = []
        for operator, conditions in filters_dict.items():
            if operator == "eq":
                for field, value in conditions.items():
                    pipeline.append({"$match": {field: value}})
            elif operator == "op_or":
                or_filters = [{"$match": {field: value}} for field, value in conditions.items()]
                pipeline.append({"$or": or_filters})
            elif operator == "ne":
                for field, value in conditions.items():
                    pipeline.append({"$match": {field: {"$ne": value}}})
            elif operator == "lt":
                for field, value in conditions.items():
                    pipeline.append({"$match": {field: {"$lt": value}}})
            elif operator == "lte":
                for field, value in conditions.items():
                    pipeline.append({"$match": {field: {"$lte": value}}})
            elif operator == "gt":
                for field, value in conditions.items():
                    pipeline.append({"$match": {field: {"$gt": value}}})
            elif operator == "gte":
                for field, value in conditions.items():
                    pipeline.append({"$match": {field: {"$gte": value}}})
            elif operator == "substr":
                for field, value in conditions.items():
                    pipeline.append({"$match": {field: {"$regex": value, "$options": "i"}}})

        return list(cls.objects.aggregate(*pipeline))
        # queryset = cls.objects(*filters)
        # if return_all:
        #     if to_json:
        #         return [result.to_json() for result in queryset]
        # if to_json:
        #     return queryset.first().to_json()
        # return queryset.first()


# data = {
#     "age": 12,
#     "email": "puneet6@gmail.com"
# }
#
# test = Test(**data)
# test.save()

# test = Test.filter(
#     {
#         "eq": {
#             "email": "puneet6@gmail.com",
#         },
#         "gte": {
#             "age": 11
#         }
#     },
# )

test = Test.objects(email="puneet6@gmail.com")
#
# a = Test.filter(filters_dict=)
b = test
